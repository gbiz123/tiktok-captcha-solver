"""This class handles the captcha solving for playwright users"""

import random
import time
from typing import Literal
from playwright.sync_api import FloatRect, Page, expect
from undetected_chromedriver import logging

from .solver import Solver

from .api import ApiClient
from .downloader import download_image_b64

class PlaywrightSolver(Solver):

    client: ApiClient
    page: Page

    def __init__(self, page: Page, sadcaptcha_api_key: str) -> None:
        self.page = page
        self.client = ApiClient(sadcaptcha_api_key)

    def captcha_is_present(self, timeout: int = 15) -> bool:
        try:
            locator = self.page.locator(self.captcha_wrappers[0])
            expect(locator.first).to_be_visible(timeout=timeout * 1000)
            return True
        except (TimeoutError, AssertionError):
            return False

    def captcha_is_not_present(self, timeout: int = 15) -> bool:
        try:
            locator = self.page.locator(self.captcha_wrappers[0])
            expect(locator.first).to_have_count(0, timeout=timeout * 1000)
            return True
        except (TimeoutError, AssertionError):
            return False

    def identify_captcha(self) -> Literal["puzzle", "shapes", "rotate"]:
        for _ in range(15):
            if self._any_selector_in_list_present(self.puzzle_selectors):
                return "puzzle"
            elif self._any_selector_in_list_present(self.rotate_selectors):
                return "rotate"
            if self._any_selector_in_list_present(self.shapes_selectors):
                return "shapes"
            else:
                time.sleep(2)
        raise ValueError("Neither puzzle, shapes, or rotate captcha was present.")

    def solve_shapes(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not self._any_selector_in_list_present(["#captcha-verify-image"]):
                logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
                return
            image = download_image_b64(self._get_shapes_image_url())
            solution = self.client.shapes(image)
            image_element = self.page.locator("#captcha-verify-image")
            bounding_box = image_element.bounding_box()
            if not bounding_box:
                raise AttributeError("Image element was found but had no bounding box")
            self._click_proportional(bounding_box, solution.point_one_proportion_x, solution.point_one_proportion_y)
            self._click_proportional(bounding_box, solution.point_two_proportion_x, solution.point_two_proportion_y)
            self.page.locator(".verify-captcha-submit-button").click()
            if self.captcha_is_not_present(timeout=5):
                return
            else:
                time.sleep(5)

    def solve_rotate(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not self._any_selector_in_list_present(["[data-testid=whirl-inner-img]"]):
                logging.debug("Went to solve rotate but whirl-inner-img was not present")
                return
            outer = download_image_b64(self._get_rotate_outer_image_url())
            inner = download_image_b64(self._get_rotate_inner_image_url())
            solution = self.client.rotate(outer, inner)
            logging.debug(f"Solution angle: {solution}")
            distance = self._compute_rotate_slide_distance(solution.angle)
            logging.debug(f"Solution distance: {distance}")
            self._drag_element_horizontal(".secsdk-captcha-drag-icon", distance)
            if self.captcha_is_not_present(timeout=5):
                return
            else:
                time.sleep(5)

    def solve_puzzle(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not self._any_selector_in_list_present(["#captcha-verify-image"]):
                logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
                return
            puzzle = download_image_b64(self._get_puzzle_image_url())
            piece = download_image_b64(self._get_piece_image_url())
            solution = self.client.puzzle(puzzle, piece)
            distance = self._compute_puzzle_slide_distance(solution.slide_x_proportion)
            self._drag_element_horizontal(".secsdk-captcha-drag-icon", distance)
            if self.captcha_is_not_present(timeout=5):
                return
            else:
                time.sleep(5)

    def _compute_rotate_slide_distance(self, angle: int) -> int:
        slide_length = self._get_slide_length()
        icon_length = self._get_slide_icon_length()
        return int(((slide_length - icon_length) * angle) / 360)

    def _compute_puzzle_slide_distance(self, proportion_x: float) -> int:
        e = self.page.locator("#captcha-verify-image")
        box = e.bounding_box()
        if box:
            return int(proportion_x * box["width"])
        raise AttributeError("#captcha-verify-image was found but had no bouding box")

    def _get_slide_length(self) -> int:
        e = self.page.locator(".captcha_verify_slide--slidebar")
        box = e.bounding_box()
        if box:
            return int(box["width"])
        raise AttributeError(".captcha_verify_slide--slidebar was found but had no bouding box")

    def _get_slide_icon_length(self) -> int:
        e = self.page.locator(".secsdk-captcha-drag-icon")
        box = e.bounding_box()
        if box:
            return int(box["width"])
        raise AttributeError(".secsdk-captcha-drag-icon was found but had no bouding box")

    def _get_rotate_inner_image_url(self) -> str:
        e = self.page.locator("[data-testid=whirl-inner-img]")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Inner image URL was None")
        return url

    def _get_rotate_outer_image_url(self) -> str:
        e = self.page.locator("[data-testid=whirl-outer-img]")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Outer image URL was None")
        return url

    def _get_puzzle_image_url(self) -> str:
        e = self.page.locator("#captcha-verify-image")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Puzzle image URL was None")
        return url

    def _get_piece_image_url(self) -> str:
        e = self.page.locator(".captcha_verify_img_slide")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Piece image URL was None")
        return url

    def _get_shapes_image_url(self) -> str:
        e = self.page.locator("#captcha-verify-image")
        url = e.get_attribute("src")
        if not url:
            raise ValueError("Shapes image URL was None")
        return url
    
    def _click_proportional(
            self,
            bounding_box: FloatRect,
            proportion_x: float,
            proportion_y: float
        ) -> None:
        """Click an element inside its bounding box at a point defined by the proportions of x and y
        to the width and height of the entire element

        Args:
            element: FloatRect to click inside
            proportion_x: float from 0 to 1 defining the proportion x location to click 
            proportion_y: float from 0 to 1 defining the proportion y location to click 
        """
        x_origin = bounding_box["x"]
        y_origin = bounding_box["y"]
        x_offset = (proportion_x * bounding_box["width"])
        y_offset = (proportion_y * bounding_box["height"]) 
        self.page.mouse.move(x_origin + x_offset, y_origin + y_offset)
        time.sleep(random.randint(1, 10) / 11)
        self.page.mouse.down()
        time.sleep(0.001337)
        self.page.mouse.up()
        time.sleep(random.randint(1, 10) / 11)

    def _drag_element_horizontal(self, css_selector: str, x: int) -> None:
        e = self.page.locator(css_selector)
        box = e.bounding_box()
        if not box:
            raise AttributeError("Element had no bounding box")
        start_x = (box["x"] + (box["width"] / 1.337))
        start_y = (box["y"] +  (box["height"] / 1.337))
        self.page.mouse.move(start_x, start_y)
        time.sleep(random.randint(1, 10) / 11)
        self.page.mouse.down()
        time.sleep(random.randint(1, 10) / 11)
        self.page.mouse.move(start_x + x, start_y, steps=100)
        time.sleep(0.001)
        self.page.mouse.up()

    def _any_selector_in_list_present(self, selectors: list[str]) -> bool:
        for selector in selectors:
            for ele in self.page.locator(selector).all():
                if ele.is_visible():
                    logging.debug("Detected selector: " + selector + " from list " + ", ".join(selectors))
                    return True
        logging.debug("No selector in list found: " + ", ".join(selectors))
        return False
