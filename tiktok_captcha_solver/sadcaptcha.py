"""This class handles the captcha solving"""

from typing import Literal
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By

from .api import ApiClient
from .downloader import download_image_b64

class SadCaptcha:

    client: ApiClient
    chromedriver: Chrome

    def __init__(self, chromedriver: Chrome, sadcaptcha_api_key: str) -> None:
        self.chromedriver = chromedriver
        self.client = ApiClient(sadcaptcha_api_key)

    def solve_captcha(self) -> None:
        pass

    def captcha_is_present(self) -> bool:
        return False

    def _identify_captcha(self) -> Literal["puzzle", "shapes", "rotate"]:
        return "rotate"

    def _attempt_rotate(self) -> None:
        outer = download_image_b64(self._get_rotate_outer_image_url())
        inner = download_image_b64(self._get_rotate_inner_image_url())
        solution = self.client.rotate(outer, inner)
        distance = self._compute_rotate_slide_distance(solution.angle)
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

    def _check_captcha_success(self) -> bool:
        return False

    def _drag_element(self, css_selector: str, x: int, y: int) -> None:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, css_selector)
        ActionChains(self.chromedriver) \
            .move_to_element(e) \
            .click_and_hold(e) \
            .move_by_offset(x, y) \
            .release() \
            .perform()

