"""This class handles the captcha solving"""

from typing import Literal
from selenium.webdriver import Chrome

from .api import ApiClient
from .downloader import download_image_b64

class SadCaptcha:

    client: ApiClient

    def __init__(self, sadcaptcha_api_key: str) -> None:
        self.client = ApiClient(sadcaptcha_api_key)

    def solve_captcha(self, chromedriver: Chrome) -> None:
        pass

    def captcha_is_present(self, chromedriver: Chrome) -> bool:
        return False

    def _identify_captcha(self, chromedriver: Chrome) -> Literal["puzzle", "shapes", "rotate"]:
        return "rotate"

    def _compute_rotate_slide_distance(self, slide_length: int, slide_icon_length: int, angle: int) -> int:
        return int(((slide_length - slide_icon_length) * angle) / 360)

    def _get_slide_length(self, chromedriver: Chrome) -> int:
        return 0

    def _get_slide_icon_length(self, chromedriver: Chrome) -> int:
        return 0
