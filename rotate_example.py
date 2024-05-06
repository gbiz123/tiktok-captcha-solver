import time
import base64
import requests

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium import webdriver
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager


def download_image_b64(url: str) -> str:
    """Download an image from URL and return as base64 encoded string"""
    r = requests.get(url)
    return base64.b64encode(r.content).decode()


class RotateSolver:

    chromedriver: Chrome
    api_key: str

    def __init__(self, chromedriver: Chrome, sadcaptcha_api_key: str) -> None:
        self.chromedriver = chromedriver
        self.api_key = sadcaptcha_api_key

    def solve(self) -> None:
        outer = download_image_b64(self._get_rotate_outer_image_url())
        inner = download_image_b64(self._get_rotate_inner_image_url())
        angle = self.rotate(outer, inner)
        distance = self._compute_rotate_slide_distance(angle)
        self._drag_element(".secsdk-captcha-drag-icon", distance, 0)

    def _compute_rotate_slide_distance(self, angle: int) -> int:
        slide_length = self._get_slide_length()
        icon_length = self._get_slide_icon_length()
        return int(((slide_length - icon_length) * angle) / 360)

    def _get_slide_length(self) -> int:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, ".captcha_verify_slide--slidebar")
        return e.size['width']

    def _get_slide_icon_length(self) -> int:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, ".secsdk-captcha-drag-icon")
        return e.size['width']

    def _get_rotate_inner_image_url(self) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, "[data-testid=whirl-inner-img]")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Inner image URL was None")
        return url

    def _get_rotate_outer_image_url(self) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, "[data-testid=whirl-outer-img]")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Outer image URL was None")
        return url

    def _drag_element(self, css_selector: str, x: int, y: int) -> None:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, css_selector)
        ActionChains(self.chromedriver, duration=550) \
            .move_to_element(e) \
            .click_and_hold(e) \
            .move_by_offset(x, y) \
            .release() \
            .perform()

    def rotate(self, outer_b46: str, inner_b64: str) -> int:
        """Make rotate request to SadCaptcha

        Args:
            outer_b46: Base64 encoded outer image (str)
            inner_b64: Base64 encoded inner image (str)

        Returns:
            the angle needed to rotate (int)
        """
        url = "https://www.sadcaptcha.com/api/v1/rotate?licenseKey=" + self.api_key
        data = {
            "outerImageB64": outer_b46,
            "innerImageB64": inner_b64
        }       
        resp = requests.post(url, json=data)
        result = resp.json()
        return result.get("angle")


if __name__ == "__main__":
    
    # Add your key here!
    api_key = "YOUR KEY HERE"


    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    options.add_argument("--accept-lang=en-US,en;q=0.5")
    options.add_argument("--dom-automation=disabled")

    def make_driver() -> uc.Chrome:
        return uc.Chrome(service=ChromeDriverManager().install(), headless=False, use_subprocess=False)


    def open_tiktkok_login(driver: uc.Chrome) -> None:
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(10)
        write_username = driver.find_element(By.XPATH, '//input[contains(@name,"username")]');
        write_username.send_keys("greg@toughdata.net");
        time.sleep(2);
        write_password = driver.find_element(By.XPATH, '//input[contains(@type,"password")]');
        write_password.send_keys("th.etoughapi1!");
        time.sleep(2)
        login_btn = driver.find_element(By.XPATH, '//button[contains(@data-e2e,"login-button")]').click();
        time.sleep(8)

    def test_solve_captcha():
        driver = make_driver()
        open_tiktkok_login(driver)
        solver = RotateSolver(driver, api_key)
        solver.solve()

    test_solve_captcha()
