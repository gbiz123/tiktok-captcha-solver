"""This class handles the captcha solving for selenium users"""

import time
from typing import Any, override

from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import logging
from undetected_chromedriver.patcher import random

from . import selectors
from .geometry import compute_puzzle_slide_distance, compute_rotate_slide_distance
from .captchatype import CaptchaType
from .api import ApiClient
from .downloader import fetch_image_b64
from .solver import Solver


class SeleniumSolver(Solver):

    client: ApiClient
    chromedriver: Chrome

    def __init__(
            self, 
            chromedriver: Chrome,
            sadcaptcha_api_key: str,
            headers: dict[str, Any] | None = None,
            proxy: str | None = None
        ) -> None:
        self.chromedriver = chromedriver
        self.client = ApiClient(sadcaptcha_api_key)
        self.headers = headers
        self.proxy = proxy

    @override
    def captcha_is_present(self, timeout: int = 15) -> bool:
        for _ in range(timeout * 2):
            if self.page_is_douyin():
                if self._any_selector_in_list_present([selectors.DouyinPuzzle.FRAME]):
                    return True
            else:
                if self._any_selector_in_list_present([selectors.Wrappers.V1]):
                    logging.debug("Captcha detected v1")
                    return True
                if self._any_selector_in_list_present([selectors.Wrappers.V2]):
                    logging.debug("Captcha detected v2")
                    return True
            time.sleep(0.5)
        logging.debug("Captcha not found")
        return False

    @override
    def captcha_is_not_present(self, timeout: int = 15) -> bool:
        for _ in range(timeout * 2):
            if self.page_is_douyin():
                if len(self.chromedriver.find_elements(By.CSS_SELECTOR, selectors.DouyinPuzzle.FRAME)) == 0:
                    logging.debug("Captcha detected")
                    return True
            else:
                if len(self.chromedriver.find_elements(By.CSS_SELECTOR, selectors.Wrappers.V1)) == 0:
                    logging.debug("Captcha not present")
                    return True
                if len(self.chromedriver.find_elements(By.CSS_SELECTOR, selectors.Wrappers.V2)) == 0:
                    logging.debug("Captcha not present")
                    return True
            time.sleep(0.5)
        logging.debug("Captcha not found")
        return False

    @override
    def identify_captcha(self) -> CaptchaType:
        for _ in range(60):
            if self._any_selector_in_list_present([selectors.PuzzleV1.UNIQUE_IDENTIFIER]):
                logging.debug("detected puzzle")
                return CaptchaType.PUZZLE_V1
            if self._any_selector_in_list_present([selectors.PuzzleV2.UNIQUE_IDENTIFIER]):
                logging.debug("detected puzzle v2")
                return CaptchaType.PUZZLE_V2
            elif self._any_selector_in_list_present([selectors.RotateV1.UNIQUE_IDENTIFIER]):
                logging.debug("detected rotate v1")
                return CaptchaType.ROTATE_V1
            elif self._any_selector_in_list_present([selectors.RotateV2.UNIQUE_IDENTIFIER]):
                logging.debug("detected rotate v2")
                return CaptchaType.ROTATE_V2
            if self._any_selector_in_list_present([selectors.ShapesV1.UNIQUE_IDENTIFIER]):
                img_url = self._get_image_url(selectors.ShapesV1.IMAGE)
                if "/icon" in img_url:
                    logging.debug("detected icon v1")
                    return CaptchaType.ICON_V1
                elif "/3d" in img_url:
                    logging.debug("detected shapes v1")
                    return CaptchaType.SHAPES_V1
                else:
                    logging.warn("did not see '/3d' in image source url but returning shapes v1 anyways")
                    return CaptchaType.SHAPES_V1
            if self._any_selector_in_list_present([selectors.ShapesV2.UNIQUE_IDENTIFIER]):
                img_url = self._get_image_url(selectors.ShapesV2.IMAGE)
                if "/icon" in img_url:
                    logging.debug("detected icon v2")
                    return CaptchaType.ICON_V2
                elif "/3d" in img_url:
                    logging.debug("detected shapes v2")
                    return CaptchaType.SHAPES_V2
                else:
                    logging.warn("did not see '/3d' in image source url but returning shapes v2 anyways")
                    return CaptchaType.SHAPES_V2
            else:
                time.sleep(0.5)
        raise ValueError("Neither puzzle, shapes, or rotate captcha was present.")

    @override
    def page_is_douyin(self) -> bool:
        if "douyin" in self.chromedriver.current_url:
            logging.debug("page is douyin")
            return True
        logging.debug("page is tiktok")
        return False

    @override
    def solve_shapes(self) -> None:
        if not self._any_selector_in_list_present([selectors.ShapesV1.IMAGE]):
            logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
            return
        image = fetch_image_b64(self._get_image_url(selectors.ShapesV1.IMAGE), headers=self.headers, proxy=self.proxy)
        solution = self.client.shapes(image)
        image_element = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.ShapesV1.IMAGE)
        self._click_proportional(image_element, solution.point_one_proportion_x, solution.point_one_proportion_y)
        self._click_proportional(image_element, solution.point_two_proportion_x, solution.point_two_proportion_y)
        self.chromedriver.find_element(By.CSS_SELECTOR, selectors.ShapesV1.SUBMIT_BUTTON).click()

    @override
    def solve_shapes_v2(self) -> None:
        if not self._any_selector_in_list_present([selectors.ShapesV2.IMAGE]):
            logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
            return
        image = fetch_image_b64(self._get_image_url(selectors.ShapesV2.IMAGE), headers=self.headers, proxy=self.proxy)
        solution = self.client.shapes(image)
        image_element = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.ShapesV2.IMAGE)
        self._click_proportional(image_element, solution.point_one_proportion_x, solution.point_one_proportion_y)
        self._click_proportional(image_element, solution.point_two_proportion_x, solution.point_two_proportion_y)
        self.chromedriver.find_element(By.CSS_SELECTOR, selectors.ShapesV2.SUBMIT_BUTTON).click()

    @override
    def solve_rotate(self) -> None:
        if not self._any_selector_in_list_present([selectors.RotateV1.INNER]):
            logging.debug("Went to solve rotate but whirl-inner-img was not present")
            return
        outer = fetch_image_b64(self._get_image_url(selectors.RotateV1.OUTER), headers=self.headers, proxy=self.proxy)
        inner = fetch_image_b64(self._get_image_url(selectors.RotateV1.INNER), headers=self.headers, proxy=self.proxy)
        solution = self.client.rotate(outer, inner)
        slide_bar_width = self._get_element_width(selectors.RotateV1.SLIDE_BAR)
        slider_button_width = self._get_element_width(selectors.RotateV1.SLIDER_DRAG_BUTTON)
        distance = compute_rotate_slide_distance(solution.angle, slide_bar_width, slider_button_width)
        self._drag_element_horizontal(selectors.RotateV1.SLIDER_DRAG_BUTTON, distance)

    @override
    def solve_rotate_v2(self) -> None:
        if not self._any_selector_in_list_present([selectors.RotateV2.INNER]):
            logging.debug("Went to solve rotate but whirl-inner-img was not present")
            return
        outer = fetch_image_b64(self._get_image_url(selectors.RotateV2.OUTER), headers=self.headers, proxy=self.proxy)
        inner = fetch_image_b64(self._get_image_url(selectors.RotateV2.INNER), headers=self.headers, proxy=self.proxy)
        solution = self.client.rotate(outer, inner)
        slide_bar_width = self._get_element_width(selectors.RotateV2.SLIDE_BAR)
        slider_button_width = self._get_element_width(selectors.RotateV2.SLIDER_DRAG_BUTTON)
        distance = compute_rotate_slide_distance(solution.angle, slide_bar_width, slider_button_width)
        self._drag_element_horizontal(selectors.RotateV2.SLIDER_DRAG_BUTTON, distance)

    @override
    def solve_puzzle(self) -> None:
        if not self._any_selector_in_list_present([selectors.PuzzleV1.PIECE]):
            logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
            return
        puzzle = fetch_image_b64(self._get_image_url(selectors.PuzzleV1.PUZZLE), headers=self.headers, proxy=self.proxy)
        piece = fetch_image_b64(self._get_image_url(selectors.PuzzleV1.PIECE), headers=self.headers, proxy=self.proxy)
        solution = self.client.puzzle(puzzle, piece)
        puzzle_width = self._get_element_width(selectors.PuzzleV1.PUZZLE)
        distance = compute_puzzle_slide_distance(solution.slide_x_proportion, puzzle_width)
        self._drag_element_horizontal(selectors.PuzzleV1.SLIDER_DRAG_BUTTON, distance)

    @override
    def solve_puzzle_v2(self) -> None:
        if not self._any_selector_in_list_present([selectors.PuzzleV2.PIECE]):
            logging.debug("Went to solve puzzle but #captcha-verify-image was not present")
            return
        puzzle = fetch_image_b64(self._get_image_url(selectors.PuzzleV2.PUZZLE), headers=self.headers, proxy=self.proxy)
        piece = fetch_image_b64(self._get_image_url(selectors.PuzzleV2.PIECE), headers=self.headers, proxy=self.proxy)
        solution = self.client.puzzle(puzzle, piece)
        puzzle_width = self._get_element_width(selectors.PuzzleV2.PUZZLE)
        distance = compute_puzzle_slide_distance(solution.slide_x_proportion, puzzle_width)
        self._drag_element_horizontal(selectors.PuzzleV2.SLIDER_DRAG_BUTTON, distance)

    @override
    def solve_icon(self) -> None:
        if not self._any_selector_in_list_present([selectors.ShapesV1.IMAGE]):
            logging.debug("Went to solve icon but #captcha-verify-image was not present")
            return
        challenge = self._get_element_text(selectors.IconV1.TEXT)
        image = fetch_image_b64(self._get_image_url(selectors.IconV1.IMAGE), headers=self.headers, proxy=self.proxy)
        solution = self.client.icon(challenge, image)
        image_element = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.IconV1.IMAGE)
        for point in solution.proportional_points:
            self._click_proportional(image_element, point.proportion_x, point.proportion_y)
        self.chromedriver.find_element(By.CSS_SELECTOR, selectors.IconV1.SUBMIT_BUTTON).click()

    @override
    def solve_icon_v2(self) -> None:
        if not self._any_selector_in_list_present([selectors.ShapesV2.IMAGE]):
            logging.debug("Went to solve icon but #captcha-verify-image was not present")
            return
        challenge = self._get_element_text(selectors.IconV2.TEXT)
        image = fetch_image_b64(self._get_image_url(selectors.IconV2.IMAGE), headers=self.headers, proxy=self.proxy)
        solution = self.client.icon(challenge, image)
        image_element = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.IconV2.IMAGE)
        for point in solution.proportional_points:
            self._click_proportional(image_element, point.proportion_x, point.proportion_y)
        self.chromedriver.find_element(By.CSS_SELECTOR, selectors.IconV2.SUBMIT_BUTTON).click()

    @override
    def solve_douyin_puzzle(self) -> None:
        puzzle = fetch_image_b64(self._get_douyin_puzzle_image_url(), headers=self.headers, proxy=self.proxy)
        piece = fetch_image_b64(self._get_douyin_piece_image_url(), headers=self.headers, proxy=self.proxy)
        solution = self.client.puzzle(puzzle, piece)
        distance = self._compute_douyin_puzzle_slide_distance(solution.slide_x_proportion)
        self._drag_element_horizontal(".captcha-slider-btn", distance, frame_selector=selectors.DouyinPuzzle.FRAME)

    def _get_element_text(self, selector: str) -> str:
        challenge_element = self.chromedriver.find_element(By.CSS_SELECTOR, selector)
        text = challenge_element.text
        if not text:
            raise ValueError("element was found but did not have any text.")
        return text

    def _get_element_width(self, selector: str) -> int:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, selector)
        return e.size['width']

    def _get_image_url(self, selector: str) -> str:
        e = self.chromedriver.find_element(By.CSS_SELECTOR, selector)
        url = e.get_attribute("src")
        if not url:
            raise ValueError("image URL was None")
        return url

    def _get_douyin_puzzle_image_url(self) -> str:
        frame = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.FRAME)
        self.chromedriver.switch_to.frame(frame)
        try:
            e = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.PUZZLE)
            url = e.get_attribute("src")
            if not url:
                raise ValueError("Puzzle image URL was None")
            return url
        finally:
            self.chromedriver.switch_to.default_content()

    def _compute_douyin_puzzle_slide_distance(self, proportion_x: float) -> int:
        frame = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.FRAME)
        self.chromedriver.switch_to.frame(frame)
        try:
            e = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.PUZZLE)
            return int(proportion_x * e.size["width"])
        finally:
            self.chromedriver.switch_to.default_content()

    def _get_douyin_piece_image_url(self) -> str:
        frame = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.FRAME)
        self.chromedriver.switch_to.frame(frame)
        try:
            e = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.PIECE)
            url = e.get_attribute("src")
            if not url:
                raise ValueError("Piece image URL was None")
            return url
        finally:
            self.chromedriver.switch_to.default_content()

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
        x_origin = element.location["x"]
        y_origin = element.location["y"]
        x_offset = (proportion_x * element.size["width"])
        y_offset = (proportion_y * element.size["height"]) 
        action = ActionBuilder(self.chromedriver)
        action.pointer_action \
            .move_to_location(x_origin + x_offset, y_origin + y_offset) \
            .pause(random.randint(1, 10) / 11) \
            .click() \
            .pause(random.randint(1, 10) / 11)
        action.perform()

    def _drag_element_horizontal(self, css_selector: str, x: int, frame_selector: str | None = None) -> None:
        try:
            if frame_selector:
                frame = self.chromedriver.find_element(By.CSS_SELECTOR, selectors.DouyinPuzzle.FRAME)
                self.chromedriver.switch_to.frame(frame)
                e = self.chromedriver.find_element(By.CSS_SELECTOR, css_selector)
            else:
                e = self.chromedriver.find_element(By.CSS_SELECTOR, css_selector)
            actions = ActionChains(self.chromedriver, duration=0)
            actions.click_and_hold(e)
            time.sleep(0.1)
            for _ in range(0, x - 15):
                actions.move_by_offset(1, 0)
            for _ in range(0, 20):
                actions.move_by_offset(1, 0)
                actions.pause(0.01)
            actions.pause(0.7)
            for _ in range(0, 5):
                actions.move_by_offset(-1, 0)
                actions.pause(0.05)
            actions.pause(0.1)
            actions.release().perform()
        finally:
            self.chromedriver.switch_to.default_content()

    def _any_selector_in_list_present(self, selectors: list[str]) -> bool:
        for selector in selectors:
            for ele in self.chromedriver.find_elements(By.CSS_SELECTOR, selector):
                if ele.is_displayed():
                    logging.debug("Detected selector: " + selector + " from list " + ", ".join(selectors))
                    return True
        logging.debug("No selector in list found: " + ", ".join(selectors))
        return False
