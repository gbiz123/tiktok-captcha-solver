# TikTok Captcha Solver API
This project is the [SadCaptcha TikTok Captcha Solver](https://www.sadcaptcha.com?ref=ghclientrepo) API client.
The purpose is to make integrating SadCaptcha into your Selenium or Playwright app as simple as one line of code.


Instructions for integrating with Selenium and Playwright are described below in their respective sections.

## Requirements
- Python >= 3.10
- **If using Selenium** - Selenium properly installed and in `PATH`
- **If using Playwright** - Playwright must be properly installed with `playwright install`

## Installation
This project can be installed with `pip`. Just run the following command:
```
pip install tiktok-captcha-solver
```

## Selenium Client 
Import the package, set up the SadCaptcha class, and call it whenever you need.
This turns the entire captcha detection, solution, retry, and verification process into a single line of code.
It is the recommended method if you are using Playwright.

```py
from tiktok_captcha_solver import SeleniumSolver
import undetected_chromedriver as uc

driver = uc.Chrome(headless=False)
api_key = "YOUR_API_KEY_HERE"
sadcaptcha = SeleniumSolver(driver, api_key)

# Selenium code that causes a TikTok captcha...

sadcaptcha.solve_captcha_if_present()
```

That's it!

## Playwright Client
Import the package, set up the SadCaptcha class, and call it whenever you need.
This turns the entire captcha detection, solution, retry, and verification process into a single line of code.
It is the recommended method if you are using Selenium.

```py
from tiktok_captcha_solver import PlaywrightSolver
from playwright.sync_api import Page, sync_playwright

api_key = "YOUR_API_KEY_HERE"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Playwright code that causes a TikTok captcha...

    sadcaptcha = PlaywrightSolver(page, api_key)
    sadcaptcha.solve_captcha_if_present()
```
That's it!

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
```

## Contact
- Homepage: https://www.sadcaptcha.com/
- Email: info@toughdata.net
- Telegram @toughdata
