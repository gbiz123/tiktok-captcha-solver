"""This class handles the captcha solving"""

import time
from typing import Literal
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import logging

from .api import ApiClient
from .downloader import download_image_b64

class SadCaptcha:

    client: ApiClient
    chromedriver: Chrome

    def __init__(self, chromedriver: Chrome, sadcaptcha_api_key: str) -> None:
        self.chromedriver = chromedriver
        self.client = ApiClient(sadcaptcha_api_key)

    def solve_captcha_if_present(self, captcha_detect_timeout: int = 15, retries: int = 3) -> None:
        """Solves any captcha that is present, if one is detected

        Args:
            captcha_detect_timeout: return if no captcha is detected in this many seconds
            retries: number of times to retry captcha
        """
        if not self.captcha_is_present(captcha_detect_timeout):
            return
        match self.identify_captcha():
            case "puzzle": 
                self.solve_puzzle(retries)
            case "rotate": 
                self.solve_rotate(retries)
            case "shapes": 
                self.solve_shapes(retries)

    def captcha_is_present(self, timeout: int = 15) -> bool:
        for _ in range(timeout):
            if len(self.chromedriver.find_elements(By.CSS_SELECTOR, "div#captcha_container")) > 0:
                return True
        return False

    def identify_captcha(self) -> Literal["puzzle", "shapes", "rotate"]:
        rotate_selector = "[data-testid=whirl-inner-img]"
        puzzle_selector = "img.captcha_verify_img_slide"
        shapes_selector = "#verify-points"
        for _ in range(15):
            if len(self.chromedriver.find_elements(By.CSS_SELECTOR, puzzle_selector)) > 0:
                return "puzzle"
            elif len(self.chromedriver.find_elements(By.CSS_SELECTOR, rotate_selector)) > 0:
                return "rotate"
            elif len(self.chromedriver.find_elements(By.CSS_SELECTOR, shapes_selector)) > 0:
                return "shapes"
            else:
                time.sleep(2)
        raise ValueError("Neither puzzle, shapes, or rotate captcha was present.")

    def solve_shapes(self, retries: int = 3) -> None:
        for _ in range(retries):
            image = download_image_b64(self._get_shapes_image_url())
            solution = self.client.shapes(image)
            image_element = self.chromedriver.find_element(By.CSS_SELECTOR, "#captcha-verify-image")
            self._click_proportional(image_element, solution.point_one_proportion_x, solution.point_one_proportion_y)
            self._click_proportional(image_element, solution.point_two_proportion_y, solution.point_two_proportion_y)
            self.chromedriver.find_element(By.CSS_SELECTOR, ".verify-captcha-submit-button").click()
            if self._check_captcha_success():
                return

    def solve_rotate(self, retries: int = 3) -> None:
        for _ in range(retries):
            outer = download_image_b64(self._get_rotate_outer_image_url())
            inner = download_image_b64(self._get_rotate_inner_image_url())
            solution = self.client.rotate(outer, inner)
            distance = self._compute_rotate_slide_distance(solution.angle)
            self._drag_element(".secsdk-captcha-drag-icon", distance, 0)
            if self._check_captcha_success():
                return

    def solve_puzzle(self, retries: int = 3) -> None:
        for _ in range(retries):
            puzzle = download_image_b64(self._get_puzzle_image_url())
            piece = download_image_b64(self._get_piece_image_url())
            solution = self.client.puzzle(puzzle, piece)
            distance = self._compute_puzzle_slide_distance(solution.slide_x_proportion)
            self._drag_element(".secsdk-captcha-drag-icon", distance, 0)
            if self._check_captcha_success():
                return

    def _compute_rotate_slide_distance(self, angle: int) -> int:
        slide_length = self._get_slide_length()
        icon_length = self._get_slide_icon_length()
        return int(((slide_length - icon_length) * angle) / 360)

    def _compute_puzzle_slide_distance(self, proportion_x: float) -> int:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, "#captcha-verify-image")
        return int(proportion_x * e.size["width"])

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

    def _get_puzzle_image_url(self) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, "#captcha-verify-image")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Puzzle image URL was None")
        return url

    def _get_piece_image_url(self) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, ".captcha_verify_img_slide")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Piece image URL was None")
        return url

    def _get_shapes_image_url(self) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, "#captcha-verify-image")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Shapes image URL was None")
        return url

    def _check_captcha_success(self) -> bool:
        success_xpath = "//*[contains(text(), 'Verification complete')]"
        for _ in range(20):
            if self.chromedriver.find_elements(By.XPATH, success_xpath):
                return True
            time.sleep(1)
        return False

    def _click_proportional(
            self,
            element: WebElement,
            proportion_x: float,
            proportion_y: float
        ) -> None:
        """Click an element inside its bounding box at a point defined by the proportions of x and y
        to the width and height of the entire element

        Args:
            element: WebElement to click inside
            proportion_x: float from 0 to 1 defining the proportion x location to click 
            proportion_y: float from 0 to 1 defining the proportion y location to click 
        """
        offset_x = (proportion_x * element.size["width"])
        offset_y = (proportion_y * element.size["height"]) 
        ActionChains(self.chromedriver) \
            .move_to_element_with_offset(element, offset_x, offset_y) \
            .click() \
            .perform()
        time.sleep(1.337)

    def _drag_element(self, css_selector: str, x: int, y: int) -> None:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, css_selector)
        actions = ActionChains(self.chromedriver, duration=500)
        actions.click_and_hold(e)
        actions.move_by_offset(x - 15, 0)
        time.sleep(0.001)
        for _ in range(0, 15):
            actions.move_by_offset(1, 0)
            time.sleep(0.1)
        actions.release().perform()
