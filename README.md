# Project Name: Captcha Solver

![Project Image](assests/profile.jpg)

## Project Description

This Python project provides a captcha-solving solution using headless browsing and image processing techniques. It can be used to automate the process of solving captchas on websites that use slider-based captcha challenges. Note: Only tested with playwright python but should work with other frameworks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Demo Video](#demo-video)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this captcha solver clone this repository:

```bash
git clone https://github.com/AdicOnGit/slider-captcha-solver.git
```

Change directory to slider-captcha-solver:

```bash
cd slider-captcha-solver
```

You need to install the following Python libraries:

- [cv2](https://pypi.org/project/opencv-python/)
- [time](https://docs.python.org/3/library/time.html)
- [json](https://docs.python.org/3/library/json.html)
- [PIL](https://pillow.readthedocs.io/en/stable/)
- [numpy](https://numpy.org/)

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Import the necessary libraries and create an instance of `CaptchaSolver`.

2. Use the `solve_captcha` method to solve the captcha challenge on a webpage.

Example usage:

```python
from captcha_solver import CaptchaSolver

# Create an instance of CaptchaSolver
captcha_solver = CaptchaSolver()

# Define the selectors and other parameters
page = # Your page object (e.g., from Playwright)
iframe = # Your iframe object (e.g., from Playwright)
background_selector = # Selector for the captcha background image
puzzle_piece_selector = # Selector for the puzzle piece element
captcha_close_button_selector = # Selector for the close button of the captcha
captcha_open_button_selector = # Selector for the open button of the captcha
success_item_selector = # Selector for the success indicator element

# Attempt to solve the captcha
solved = captcha_solver.solve_captcha(
    page,
    iframe,
    background_selector,
    puzzle_piece_selector,
    captcha_close_button_selector,
    captcha_open_button_selector,
    success_item_selector,
    jitter=5
)

if solved:
    print("Captcha solved successfully!")
else:
    print("Failed to solve the captcha.")
```

## How It Works

The Captcha Solver uses a combination of image processing and automation techniques to solve slider-based captchas. Here's a brief overview of how it works:

1. **Capture Background Image**: It captures the background image of the captcha challenge by waiting for the image to load on the webpage.

2. **Detect Gap Position**: It uses the Sobel operator to detect edges in the background image and finds the position of the gap in the puzzle piece.

3. **Slider Movement**: The script simulates mouse movement to drag the puzzle piece to the correct gap position.

4. **Success Indicator**: It waits for a success indicator on the webpage to confirm whether the captcha was solved successfully.

5. **Retry Mechanism**: If the captcha is not solved on the first attempt, it retries up to five times with slight jitter in mouse movements.

## Demo Video

[Watch the demo video](assests/captcha_solver_demo.mp4) to see the Captcha Solver in action.

## Contributing

Contributions to this project are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
