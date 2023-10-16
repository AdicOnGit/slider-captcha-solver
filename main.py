import cv2
import time
import json
from PIL import Image
import io
import os
import tempfile
import numpy as np

class PuzzleSolver:
    def __init__(self, background_path):
        self.background_path = background_path
        
    def find_gap_position(self, threshold=100):
        edges = self.__sobel_operator(self.background_path)
        _, binary_mask = cv2.threshold(edges, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        
        if M["m00"] == 0:
            raise ValueError("Unable to find gap position in the image")
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)

    def __sobel_operator(self, img_path):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

class CaptchaSolver:
    def __init__(self):
        self.captured_data = None
    
    # Can make the response specific to your needs
    def _handle_response(self, response):
        try:
            response_text = response.text()
            json_data = json.loads(response_text)
            self.captured_data = json_data
        except Exception as e:
            print(f"Error while handling response: {str(e)}")
            self.captured_data = None

    def solve_captcha(self, page, iframe, background_selector, puzzle_piece_selector, captcha_close_button_selector,captcha_open_button_selector, success_item_selector, jitter=5, max_tries=5):
        for _ in range(max_tries):
            print(f"Trying solving captcha attempt: {_+1}")
            temp_image_path = self._capture_background_image(iframe, background_selector)
            iframe.wait_for_selector(puzzle_piece_selector)
            time.sleep(2)
            puzzle_piece = iframe.query_selector(puzzle_piece_selector)
            
            puzzle_solver = PuzzleSolver(temp_image_path)

            # Can use gap_y if needed to move in y axis
            gap_x, gap_y = puzzle_solver.find_gap_position()
            time.sleep(3)
            slider_box = puzzle_piece.bounding_box()
            page.on("response", self._handle_response)
            page.mouse.move(slider_box["x"] + slider_box["width"] / 2, slider_box["y"] + slider_box["height"] / 2)
            page.mouse.down()
            target_x = (slider_box["x"]-20) + gap_x + (jitter * (1 if _ % 2 == 0 else -1))
            target_y = slider_box["y"] + slider_box["height"] / 2 + (jitter * (1 if _ % 2 == 0 else -1))
            page.mouse.move(target_x, target_y)
            page.mouse.up()
            os.remove(temp_image_path)
            
            # Here waiting for indication for successful captcha solving.
            try:
                success = iframe.wait_for_selector(success_item_selector, timeout=3000)
                if success:
                    print("captcha solved")
                    return True
            except Exception:
                print("Couldn't solve captcha, retrying...")
                iframe.click(captcha_close_button_selector)
                page.wait_for_selector(captcha_open_button_selector)
                page.click(captcha_open_button_selector)
        return False

    def _capture_background_image(self, iframe, background_selector):
        print("waiting for images to load for screenshot...")
        image_element = iframe.wait_for_selector(background_selector)
        time.sleep(3)
        image_url = image_element.get_attribute("style").split('url("')[1].split('")')[0]
        screenshot_page = iframe.context.new_page()
        screenshot_page.set_content(f'<img src="{image_url}" />')
        screenshot_bytes = screenshot_page.screenshot(type="png", full_page=True)
        image = Image.open(io.BytesIO(screenshot_bytes))
        cropped_image = self._crop_image_background(image)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        cropped_image.save(temp_file.name)
        screenshot_page.context.close()
        return temp_file.name

    def _crop_image_background(self, img):
        grayscale_img = img.convert("L")
        img_data = np.array(grayscale_img)
        non_white_pixels = np.where(img_data != 255)
        bbox = [np.min(non_white_pixels[1]), np.min(non_white_pixels[0]), np.max(non_white_pixels[1]), np.max(non_white_pixels[0])]
        return img.crop(bbox)
