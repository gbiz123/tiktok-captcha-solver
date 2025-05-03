# TikTok Captcha Solver API
This project is the [SadCaptcha TikTok Captcha Solver](https://www.sadcaptcha.com?ref=ghclientrepo) API client.
The purpose is to make integrating SadCaptcha into your Selenium, Playwright, or Async Playwright app as simple as one line of code.
Instructions for integrating with Selenium, Playwright, and Async Playwright are described below in their respective sections. 
This API also works on mobile devices (Appium, etc.). 

This tool works on both TikTok and Douyin and can solve any of the four captcha challenges pictured below:

<div align="center">
    <img src="https://sadcaptcha.b-cdn.net/tiktok3d.webp" width="100" alt="TikTok Captcha Solver">
    <img src="https://sadcaptcha.b-cdn.net/tiktokrotate.webp" width="100" alt="TikTok Captcha Solver">
    <img src="https://sadcaptcha.b-cdn.net/tiktokpuzzle.webp" width="100" alt="TikTok Captcha Solver">
    <img src="https://sadcaptcha.b-cdn.net/tiktokicon.webp" width="100" alt="TikTok Captcha Solver">
    <br/>
</div>

## Requirements
- Python >= 3.10
- **If using Selenium** - Selenium properly installed and in `PATH`
- **If using Playwright** - Playwright must be properly installed with `playwright install`
- **If using mobile** - Appium and opencv must be properly installed
- **Stealth plugin** - You must use the appropriate `stealth` plugin for whichever browser automation framework you are using.
    - For Selenium, you can use [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
    - For Playwright, you can use [playwright-stealth](https://pypi.org/project/playwright-stealth/)

## Installation
This project can be installed with `pip`. Just run the following command:
```
pip install tiktok-captcha-solver
```

## Note for NodeJS users
For users automating in NodeJS or another programming language, the recommended method is to download the chrome extension from the 
chrome web store, unzip the file, patch the script.js file with your API key, and load it into your browser.
This will save you a lot of time implementing the API on your own.

## Note on running headless
To run in headless mode, you need to use the launch arg `headless=new` or `headless=chrome` as a launch arg.
Instructions to do this are in their own respective sections.
Another option is to use [Xvfb](https://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml) with `headless=True` to spoof a graphical environment.

## Selenium Client 
Import the function `make_undetected_chromedriver_solver`
This function will create an undetected chromedriver instance patched with the tiktok Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
from tiktok_captcha_solver import make_undetected_chromedriver_solver
from selenium_stealth import stealth
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc

chrome_options = ChromeOptions()
# chrome_options.add_argument("--headless=chrome") # If running headless, use this option

api_key = "YOUR_API_KEY_HERE"
driver = make_undetected_chromedriver_solver(api_key, options=options) # Returns uc.Chrome instance
stealth(driver) # Add stealth if needed
# ... [The rest of your code that accesses tiktok goes here]

# Now tiktok captchas will be automatically solved!
```
You may also pass `ChromeOptions` to `make_undetected_chromedriver_solver()`, as well as keyword arguments for `uc.Chrome()`.

## Playwright Client
Import the function `make_playwright_solver_context`
This function will create a playwright BrowserContext instance patched with the tiktok Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
from tiktok_captcha_solver import make_playwright_solver_context
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync, StealthConfig

launch_args = ["--headless=chrome"] # or --headless=new if that doesn't work

api_key = "YOUR_API_KEY_HERE"
with sync_playwright() as p:
    # Keyword arguments are passed to p.chromium.launch_persistent_context()
    # Returns playwright BrowserContext instance
    context = make_playwright_solver_context(p, api_key, args=launch_args)

    # If using playwright_stealth, you need to use this StealthConfig to avoid the white screen:
    page = context.new_page()
    stealth_config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
    stealth_sync(page, stealth_config)

    # ... [The rest of your code that accesses tiktok goes here]

# Now tiktok captchas will be automatically solved!
```
You may also pass keyword args to this function, which will be passed directly to playwright's call to `playwright.chromium.launch_persistent_context()`.
By default, the user data directory is a tempory directory that is deleted at the end of runtime.

## Async Playwright Client
Import the function `make_async_playwright_solver_context`
This function will create an async playwright BrowserContext instance patched with the tiktok Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
import asyncio
from playwright.async_api import async_playwright
from tiktok_captcha_solver import make_async_playwright_solver_context
from playwright_stealth import stealth_ssync, StealthConfig

# Need this arg if running headless
launch_args = ["--headless=chrome"] # or --headless=new if that doesn't work

async def main():
    api_key = "YOUR_API_KEY_HERE"
    async with async_playwright() as p:
        # Keyword arguments are passed to p.chromium.launch_persistent_context()
        # Returns playwright BrowserContext instance
        context = await make_async_playwright_solver_context(p, api_key, args=launch_args)

        # If using playwright_stealth, you need to use this StealthConfig to avoid the white screen:
        page = await context.new_page()
        stealth_config = StealthConfig(navigator_languages=False, navigator_vendor=False, navigator_user_agent=False)
        stealth_async(page, stealth_config)

        # ... [The rest of your code that accesses tiktok goes here]

asyncio.run(main())

# Now tiktok captchas will be automatically solved!
```
You may also pass keyword args to this function, which will be passed directly to playwright's call to `playwright.chromium.launch_persistent_context()`.
By default, the user data directory is a tempory directory that is deleted at the end of runtime.

## Mobile (Appium)
Currently there is no premade solver for Mobile/appium, but you can implement the API with relative ease.
The idea is that you take a screenshot using the mobile driver, crop the images, and then send the images to the API.
Once you've done that, you can consume the response.
Here is a working example for Puzzle and Rotate captcha. 
keep in mind, you will need to adjust the `captcha_box` and `offset_x` varaibles according to your particular mobile device.

### Puzzle slide
```py
from PIL import Image, ImageDraw
import base64
import requests

# SOLVING PUZZLE CAPTCHA
BASE_URL = 'https://www.sadcaptcha.com/api/v1'
LICENSE_KEY = ''
puzzle_url = f'{BASE_URL}/puzzle?licenseKey={LICENSE_KEY}'

def solve_puzzle():
    # Screenshot of page
    driver.save_screenshot('puzzle.png')
    full_image = Image.open('puzzle.png')

    # Full puzzle image - adjust box to your device
    captcha_box1 = (165, 1175, 303, 1330)
    captcha_image1 = full_image.crop(captcha_box1)

    # Draw circle over left side to occlude the puzzle piece in the main image
    draw = ImageDraw.Draw(captcha_image1)
    draw.ellipse([(0, 0), (captcha_image1.width / 4, captcha_image1.height)], fill="blue", outline="blue")
    captcha_image1.save('puzzle_screenshot.png')

    # Puzzle piece image - adjust box to your device
    captcha_box2 = (300, 945, 1016, 1475)
    captcha_image2 = full_image.crop(captcha_box2)
    captcha_image2.save('puzzle_screenshot1.png')


    with open('puzzle_screenshot.png', 'rb') as f:
        puzzle = base64.b64encode(f.read()).decode()
    with open('puzzle_screenshot1.png', 'rb') as f:
        piece = base64.b64encode(f.read()).decode()

    data = {
        'puzzleImageB64': puzzle,
        'pieceImageB64': piece
    }

    r = requests.post(puzzle_url, json=data)

    slide_x_proportion = r.json().get('slideXProportion')

    offset_x = 46 + (46 * float(slide_x_proportion))

    driver.swipe(start_x=55, start_y=530, end_x=55 + int(offset_x), end_y=530, duration=1000)
    time.sleep(3)
```
The number `46` in my equation comes from the distance between the captcha image and the side of the screen, which is why you add it to the value `offset_x`. `start_x` is supposed to be the center of the puzzle piece. Similarly, `530` is supposed to be the center of the puzzle piece as well.

### Rotate
```py
# SOLVING ROTATE CAPTCHA
BASE_URL = 'https://www.sadcaptcha.com/api/v1'
LICENSE_KEY = ''
rotate_url = f'{BASE_URL}/rotate?licenseKey={LICENSE_KEY}'

def solve_rotate():
    driver.save_screenshot('full_screenshot.png')

    full_image = Image.open('full_screenshot.png')

    captcha_box1 = (415, 1055, 755, 1395)
    captcha_image1 = full_image.crop(captcha_box1)

    mask = Image.new('L', captcha_image1.size, 0)
    draw = ImageDraw.Draw(mask)
    circle_bbox = (0, 0, captcha_image1.size[0], captcha_image1.size[1])
    draw.ellipse(circle_bbox, fill=255)

    captcha_image1.putalpha(mask)
    captcha_image1.save('captcha_image_circular.png')

    captcha_box2 = (318, 958, 852, 1492)
    captcha_image2 = full_image.crop(captcha_box2)

    mask2 = Image.new('L', captcha_image2.size, 0)
    draw = ImageDraw.Draw(mask2)
    draw.ellipse((captcha_box1[0] - captcha_box2[0], captcha_box1[1] - captcha_box2[1],
                  captcha_box1[2] - captcha_box2[0], captcha_box1[3] - captcha_box2[1]), fill=255)

    captcha_image_with_hole = captcha_image2.copy()
    captcha_image_with_hole.paste((0, 0, 0, 0), (0, 0), mask2)
    captcha_image_with_hole.save('captcha_image_with_hole.png')

    # inner and outer images should be cropped to the edges of the circle, without whitespace on the edges
    with open('captcha_image_with_hole.png', 'rb') as f:
        outer = base64.b64encode(f.read()).decode('utf-8')
    with open('captcha_image_circular.png', 'rb') as f:
        inner = base64.b64encode(f.read()).decode('utf-8')

    data = {
        'outerImageB64': outer,
        'innerImageB64': inner
    }

    r = requests.post(rotate_url, json=data)
    r.raise_for_status()
    response = r.json()
    angle = response.get('angle', 0)

    # calculate where the button needs to be dragged to
    # 55 is the width of the slide button
    # 286 in the example is the width of the entire bar.
    # These values may vary based on your device!
    slide_button_width = 55
    slide_bar_width = 286
    result = ((slide_bar_width - slide_button_width) * angle) / 360
    start_x = 55
    start_y = 530
    offset_x = result

    driver.swipe(start_x, start_y, start_x + int(offset_x), start_y, duration=1000)
```


## API Client
If you are not using Selenium or Playwright, you can still import and use the API client to help you make calls to SadCaptcha
```py
from tiktok_captcha_solver import ApiClient

api_key = "YOUR_API_KEY_HERE"
client = ApiClient(api_key)

# Rotate
res = client.rotate("base64 encoded outer", "base64 encoded inner")

# Puzzle
res = client.puzzle("base64 encoded puzzle", "base64 encoded piece")

# Shapes
res = client.shapes("base64 encoded shapes image")

# Icon (Video upload)
res = client.icon("Which of these objects... ?", base64 encoded icon image")
```

## Troubleshooting
### Captcha solved but still says Verification failed?
This common problem is due to your browser settings. 
If using Selenium, you must use `undetected_chromedriver` with the **default** settings.
If you are using Playwright, you must use the `playwright_stealth` package with the **default** settings.
Do not change the user agent, or modify any other browser characteristics as this is easily detected and flagged as suspicious behavior.

## Contact
To contact us, make an accout and reach out through the contact form or message us on Telegram.
- Homepage: https://www.sadcaptcha.com/
- Telegram @toughdata

## The SadCaptcha Team
- [Michael P](https://github.com/michaelzeboth) - Python Client and Chrome Extension Maintainer
- [Greg B](https://github.com/gbiz123) - Full Stack and Algorithm Developer
