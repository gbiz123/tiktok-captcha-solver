# TikTok Captcha Solver API
This project is the [SadCaptcha TikTok Captcha Solver](https://www.sadcaptcha.com?ref=ghclientrepo) API client.
The purpose is to make integrating SadCaptcha into your selenium app as simple as one line of code.

## Requirements
- Python >= 3.10
- Selenium properly installed and in `PATH`

## Installation
This project will be available as a `pip` package soon. 
For now, just clone the repo and build it using the following commands:
```
git clone https://github.com/gbiz123/tiktok-captcha-solver
cd tiktok-captcha-solver
pip install -e .
```

## Usage
Import the package, set up the SadCaptcha class, and call it whenever you need.

```py
from sadcaptcha import SadCaptcha
import undetected_chromedriver as uc

driver = uc.Chrome(headless=False)
api_key = "YOUR_API_KEY_HERE"
sadcaptcha = SadCaptcha(driver, api_key)

# Selenium code that causes a TikTok captcha...

sadcaptcha.solve_captcha_if_present()
```

That's it!

## Contact
- Homepage: https://www.sadcaptcha.com/
- Email: info@toughdata.net
- Telegram @toughdata
