"""This class handles the captcha solving for playwright users"""

import logging
from optparse import Values
import random
from typing import Any
from playwright.async_api import FloatRect, Page, expect
from playwright.async_api import TimeoutError
from undetected_chromedriver.reactor import asyncio

from . import selectors
from .captchatype import CaptchaType
from .asyncsolver import AsyncSolver
from .api import ApiClient
from .downloader import fetch_image_b64_async_page
from .geometry import compute_pixel_fraction, compute_rotate_slide_distance, get_translateX_from_style

class AsyncPlaywrightSolver(AsyncSolver):

    client: ApiClient
    page: Page

    def __init__(
            self,
            page: Page,
            sadcaptcha_api_key: str,
            headers: dict[str, Any] | None = None,
            proxy: str | None = None,
            mouse_step_size: int = 1,
            mouse_step_delay_ms: int = 10
        ) -> None:
        self.page = page
        self.client = ApiClient(sadcaptcha_api_key)
        self.headers = headers
        self.proxy = proxy
        self.mouse_step_size = mouse_step_size
        self.mouse_step_delay_ms = mouse_step_delay_ms

    async def captcha_is_present(self, timeout: int = 15) -> bool:
        if self.page_is_douyin():
            try:
                douyin_locator = self.page.frame_locator(selectors.DouyinPuzzle.FRAME).locator("*")
                await expect(douyin_locator.first).not_to_have_count(0)
            except (TimeoutError, AssertionError):
                return False
        else:
            try:
                tiktok_locator = self.page.locator(f"{selectors.Wrappers.V1}, {selectors.Wrappers.V2}")
                await expect(tiktok_locator.first).to_be_visible(timeout=timeout * 1000)
                logging.debug("v1 or v2 tiktok selector present")
            except (TimeoutError, AssertionError):
                return False
        return True

    async def captcha_is_not_present(self, timeout: int = 15) -> bool:
        if self.page_is_douyin():
            try:
                douyin_locator = self.page.frame_locator(selectors.DouyinPuzzle.FRAME).locator("*")
                await expect(douyin_locator.first).to_have_count(0)
            except (TimeoutError, AssertionError):
                return False
        else:
            try:
                tiktok_locator = self.page.locator(f"{selectors.Wrappers.V1}, {selectors.Wrappers.V2}")
                await expect(tiktok_locator.first).to_have_count(0, timeout=timeout * 1000)
                logging.debug("v1 or v2 tiktok selector not present")
            except (TimeoutError, AssertionError):
                return False
        return True

    async def identify_captcha(self) -> CaptchaType:
        for _ in range(60):
            try:
                if await self._any_selector_in_list_present([selectors.PuzzleV1.UNIQUE_IDENTIFIER]):
                    logging.debug("detected puzzle")
                    return CaptchaType.PUZZLE_V1
                if await self._any_selector_in_list_present([selectors.PuzzleV2.UNIQUE_IDENTIFIER]):
                    logging.debug("detected puzzle v2")
                    return CaptchaType.PUZZLE_V2
                elif await self._any_selector_in_list_present([selectors.RotateV1.UNIQUE_IDENTIFIER]):
                    logging.debug("detected rotate v1")
                    return CaptchaType.ROTATE_V1
                elif await self._any_selector_in_list_present([selectors.RotateV2.UNIQUE_IDENTIFIER]):
                    logging.debug("detected rotate v2")
                    return CaptchaType.ROTATE_V2
                if await self._any_selector_in_list_present([selectors.ShapesV1.UNIQUE_IDENTIFIER]):
                    img_url = await self._get_image_url(selectors.ShapesV1.IMAGE)
                    if "/icon" in img_url:
                        logging.debug("detected icon v1")
                        return CaptchaType.ICON_V1
                    elif "/3d" in img_url:
                        logging.debug("detected shapes v1")
                        return CaptchaType.SHAPES_V1
                    else:
                        logging.warn("did not see '/3d' in image source url but returning shapes v1 anyways")
                        return CaptchaType.SHAPES_V1
                if await self._any_selector_in_list_present([selectors.ShapesV2.UNIQUE_IDENTIFIER]):
                    img_url = await self._get_image_url(selectors.ShapesV2.IMAGE)
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
                    await asyncio.sleep(0.5)
            except Exception as e:
                logging.debug(f"Exception occurred identifying captcha: {str(e)}. Trying again")
                await asyncio.sleep(0.5)
        raise ValueError("Neither puzzle, shapes, or rotate captcha was present.")

    def page_is_douyin(self) -> bool:
        if "douyin" in self.page.url:
            logging.debug("page is douyin")
            return True
        logging.debug("page is tiktok")
        return False

    async def solve_shapes(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.ShapesV1.IMAGE]):
                logging.debug("Went to solve shapes but #captcha-verify-image was not present")
                return
            image = await fetch_image_b64_async_page(await self._get_image_url(selectors.ShapesV1.IMAGE), self.page)
            solution = self.client.shapes(image)
            image_element = self.page.locator(selectors.ShapesV1.IMAGE)
            bounding_box = await image_element.bounding_box()
            if not bounding_box:
                raise AttributeError("Image element was found but had no bounding box")
            await self._click_proportional(bounding_box, solution.point_one_proportion_x, solution.point_one_proportion_y)
            await self._click_proportional(bounding_box, solution.point_two_proportion_x, solution.point_two_proportion_y)
            await self.page.locator(selectors.ShapesV1.SUBMIT_BUTTON).click()
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    async def solve_shapes_v2(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.ShapesV2.IMAGE]):
                logging.debug("Went to solve shapes but image was not present")
                return
            image = await fetch_image_b64_async_page(await self._get_image_url(selectors.ShapesV2.IMAGE), self.page)
            solution = self.client.shapes(image)
            image_element = self.page.locator(selectors.ShapesV2.IMAGE)
            bounding_box = await image_element.bounding_box()
            if not bounding_box:
                raise AttributeError("Image element was found but had no bounding box")
            await self._click_proportional(bounding_box, solution.point_one_proportion_x, solution.point_one_proportion_y)
            await self._click_proportional(bounding_box, solution.point_two_proportion_x, solution.point_two_proportion_y)
            await self.page.locator(selectors.ShapesV2.SUBMIT_BUTTON).click()
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    async def solve_rotate(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.RotateV1.INNER]):
                logging.debug("Went to solve rotate but whirl-inner-img was not present")
                return

            outer_url, inner_url, slide_bar_width, slide_button_width = await asyncio.gather(
                self._get_image_url(selectors.RotateV1.OUTER),
                self._get_image_url(selectors.RotateV1.INNER),
            )

            outer, inner = await asyncio.gather(
                fetch_image_b64_async_page(outer_url, self.page),
                fetch_image_b64_async_page(inner_url, self.page)
            )

            solution = self.client.rotate(outer, inner)
            logging.debug(f"Solution angle: {solution}")
            slide_bar_width, slide_button_width = await asyncio.gather(
                self._get_element_width(selectors.RotateV1.SLIDE_BAR),
                self._get_element_width(selectors.RotateV1.SLIDER_DRAG_BUTTON)
            )
            distance = compute_rotate_slide_distance(solution.angle, slide_bar_width, slide_button_width)
            logging.debug(f"Solution distance: {distance}")
            await self._drag_element_horizontal(selectors.RotateV1.SLIDER_DRAG_BUTTON, distance)
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    async def solve_rotate_v2(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.RotateV2.INNER]):
                logging.debug("Went to solve rotate but whirl-inner-img was not present")
                return

            outer_url, inner_url, = await asyncio.gather(
                self._get_image_url(selectors.RotateV2.OUTER),
                self._get_image_url(selectors.RotateV2.INNER),
            )

            outer, inner = await asyncio.gather(
                fetch_image_b64_async_page(outer_url, self.page),
                fetch_image_b64_async_page(inner_url, self.page)
            )

            solution = self.client.rotate(outer, inner)
            logging.debug(f"Solution angle: {solution}")
            slide_bar_width, slide_button_width = await asyncio.gather(
                self._get_element_width(selectors.RotateV2.SLIDE_BAR),
                self._get_element_width(selectors.RotateV2.SLIDER_DRAG_BUTTON)
            )
            distance = compute_rotate_slide_distance(solution.angle, slide_bar_width, slide_button_width)
            logging.debug(f"Solution distance: {distance}")
            await self._drag_element_horizontal(selectors.RotateV2.SLIDER_DRAG_BUTTON, distance)
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await self.page.click(selectors.RotateV2.REFRESH_BUTTON)
                logging.debug("clicked refresh button")
                await asyncio.sleep(3)

    async def solve_puzzle(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.PuzzleV1.PIECE]):
                logging.debug("Went to solve puzzle but piece image was not present")
                return
            puzzle_url, piece_url = await asyncio.gather(self._get_image_url(selectors.PuzzleV1.PUZZLE), self._get_image_url(selectors.PuzzleV1.PIECE))

            puzzle, piece = await asyncio.gather(
                fetch_image_b64_async_page(puzzle_url, self.page),
                fetch_image_b64_async_page(piece_url, self.page)
            )

            solution = self.client.puzzle(puzzle, piece)
            puzzle_width = await self._get_element_width(selectors.PuzzleV1.PUZZLE)
            distance = compute_pixel_fraction(solution.slide_x_proportion, puzzle_width)
            await self._drag_element_horizontal(selectors.PuzzleV1.SLIDER_DRAG_BUTTON, distance)
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    async def solve_puzzle_v2(self, retries: int = 3) -> None:
        for _ in range(retries):
            if not await self._any_selector_in_list_present([selectors.PuzzleV2.PIECE]):
                logging.debug("Went to solve puzzle but piece image was not present")
                return

            puzzle_url, piece_url = await asyncio.gather(
                self._get_image_url(selectors.PuzzleV2.PUZZLE),
                self._get_image_url(selectors.PuzzleV2.PIECE),
            )

            puzzle, piece = await asyncio.gather(
                fetch_image_b64_async_page(puzzle_url, self.page),
                fetch_image_b64_async_page(piece_url, self.page)
            )

            solution = self.client.puzzle(puzzle, piece)
            puzzle_width = await self._get_element_width(selectors.PuzzleV2.PUZZLE)
            distance = compute_pixel_fraction(solution.slide_x_proportion, puzzle_width)
            logging.debug("distance = " + str(distance))
            await self._drag_ele_until_watched_ele_has_translateX(
                selectors.PuzzleV2.SLIDER_DRAG_BUTTON,
                selectors.PuzzleV2.PIECE_IMAGE_CONTAINER,
                distance
            )
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    async def solve_icon(self) -> None:
        if not await self._any_selector_in_list_present([selectors.IconV1.IMAGE]):
            logging.debug("Went to solve icon captcha but #captcha-verify-image was not present")
            return

        challenge, image_url = await asyncio.gather(
            self._get_element_text(selectors.IconV1.TEXT),
            self._get_image_url(selectors.IconV1.IMAGE)
        )
        image = await fetch_image_b64_async_page(image_url, self.page) # 이미지는 다운로드 필요
        solution = self.client.icon(challenge, image)
        image_element = self.page.locator(selectors.IconV1.IMAGE)
        bounding_box = await image_element.bounding_box()
        if not bounding_box:
            raise AttributeError("Image element was found but had no bounding box")
        for point in solution.proportional_points:
            await self._click_proportional(bounding_box, point.proportion_x, point.proportion_y)
        await self.page.locator(selectors.IconV1.SUBMIT_BUTTON).click()

    async def solve_icon_v2(self) -> None:
        if not await self._any_selector_in_list_present([selectors.IconV2.IMAGE]):
            logging.debug("Went to solve icon captcha but #captcha-verify-image was not present")
            return

        challenge, image_url = await asyncio.gather(
            self._get_element_text(selectors.IconV2.TEXT),
            self._get_image_url(selectors.IconV2.IMAGE)
        )
        image = await fetch_image_b64_async_page(image_url, self.page)
        solution = self.client.icon(challenge, image)
        image_element = self.page.locator(selectors.IconV2.IMAGE)
        bounding_box = await image_element.bounding_box()
        if not bounding_box:
            raise AttributeError("Image element was found but had no bounding box")
        for point in solution.proportional_points:
            await self._click_proportional(bounding_box, point.proportion_x, point.proportion_y)
        await self.page.locator(selectors.IconV2.SUBMIT_BUTTON).click()

    async def solve_douyin_puzzle(self) -> None:
        puzzle_url, piece_url = await asyncio.gather(
            self._get_douyin_puzzle_image_url(),
            self._get_douyin_piece_image_url()
        )

        puzzle, piece = await asyncio.gather(
            fetch_image_b64_async_page(puzzle_url, self.page),
            fetch_image_b64_async_page(piece_url, self.page)
        )

        solution = self.client.puzzle(puzzle, piece)
        distance = await self._compute_douyin_puzzle_slide_distance(solution.slide_x_proportion)
        await self._drag_element_horizontal(".captcha-slider-btn", distance, frame_selector=selectors.DouyinPuzzle.FRAME)

    async def _get_douyin_puzzle_image_url(self) -> str:
        e = self.page.frame_locator(selectors.DouyinPuzzle.FRAME).locator("#captcha_verify_image")
        url = await e.get_attribute("src")
        if not url:
            raise ValueError("Puzzle image URL was None")
        return url

    async def _compute_douyin_puzzle_slide_distance(self, proportion_x: float) -> int:
        e = self.page.frame_locator(selectors.DouyinPuzzle.FRAME).locator(selectors.DouyinPuzzle.PUZZLE)
        box = await e.bounding_box()
        if box:
            return int(proportion_x * box["width"])
        raise AttributeError("#captcha-verify-image was found but had no bouding box")

    async def _get_douyin_piece_image_url(self) -> str:
        e = self.page.frame_locator(selectors.DouyinPuzzle.FRAME).locator(selectors.DouyinPuzzle.PIECE)
        url = await e.get_attribute("src")
        if not url:
            raise ValueError("Piece image URL was None")
        return url

    async def _get_element_text(self, selector: str) -> str:
        challenge_element = self.page.locator(selector)
        text = await challenge_element.text_content()
        if not text:
            raise ValueError("selector was found but did not have any text.")
        return text

    async def _get_element_width(self, selector: str) -> int:
        e = self.page.locator(selector)
        box = await e.bounding_box()
        if box:
            return int(box["width"])
        raise AttributeError("element was found but had no bouding box")

    async def _get_image_url(self, selector: str) -> str:
        e = self.page.locator(selector)
        url = await e.get_attribute("src")
        if not url:
            raise ValueError("image URL was None")
        return url

    async def _click_proportional(
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
        await self.page.mouse.move(x_origin + x_offset, y_origin + y_offset)
        await asyncio.sleep(random.randint(1, 10) / 11)
        await self.page.mouse.down()
        await asyncio.sleep(0.001337)
        await self.page.mouse.up()
        await asyncio.sleep(random.randint(1, 10) / 11)

    async def _drag_ele_until_watched_ele_has_translateX(self, drag_ele_selector: str, watch_ele_selector: str, target_translateX: int) -> None:
        """This method drags the element drag_ele_selector until the translateX value of watch_ele_selector is equal to translateX_target.
        This is necessary because there is a small difference between the amount the puzzle piece slides and
        the amount of pixels the drag element has been dragged in TikTok puzzle v2."""
        drag_ele = self.page.locator(drag_ele_selector)
        watch_ele = self.page.locator(watch_ele_selector)
        style = await watch_ele.get_attribute("style")
        if not style:
            raise ValueError("element had no attribut style: " + watch_ele_selector)
        current_translateX = get_translateX_from_style(style)
        drag_ele_box = await drag_ele.bounding_box()
        if not drag_ele_box:
            raise AttributeError("element had no bounding box: " + drag_ele_selector)
        start_x = (drag_ele_box["x"] + (drag_ele_box["width"] / 1.337))
        start_y = (drag_ele_box["y"] +  (drag_ele_box["height"] / 1.337))
        await self.page.mouse.move(start_x, start_y)
        await asyncio.sleep(random.randint(1, 10) / 11)
        await self.page.mouse.down()
        current_x = start_x
        while current_translateX <= target_translateX:
            current_x = current_x + self.mouse_step_size
            await self.page.mouse.move(current_x, start_y)
            await self.page.wait_for_timeout(self.mouse_step_delay_ms)
            style = await watch_ele.get_attribute("style")
            if not style:
                raise ValueError("element had no attribut style: " + watch_ele_selector)
            current_translateX = get_translateX_from_style(style)
        await asyncio.sleep(0.3)
        await self.page.mouse.up()


    async def _drag_element_horizontal(self, css_selector: str, x_offset: int, frame_selector: str | None = None) -> None:
        if frame_selector:
            e = self.page.frame_locator(frame_selector).locator(css_selector)
        else:
            e = self.page.locator(css_selector)
        box = await e.bounding_box()
        if not box:
            raise AttributeError("Element had no bounding box")
        start_x = (box["x"] + (box["width"] / 1.337))
        start_y = (box["y"] +  (box["height"] / 1.337))
        await self.page.mouse.move(start_x, start_y)
        await asyncio.sleep(random.randint(1, 10) / 11)
        await self.page.mouse.down()
        for pixel in range(0, x_offset + 5, self.mouse_step_size):
            await self.page.mouse.move(start_x + pixel, start_y)
            await self.page.wait_for_timeout(self.mouse_step_delay_ms)
        await asyncio.sleep(0.25)
        for pixel in range(-5, 2):
            await self.page.mouse.move(start_x + x_offset - pixel, start_y + pixel) # overshoot back
            await self.page.wait_for_timeout(self.mouse_step_delay_ms / 2)
        await asyncio.sleep(0.2)
        await self.page.mouse.move(start_x + x_offset, start_y, steps=75)
        await asyncio.sleep(0.3)
        await self.page.mouse.up()

    async def _any_selector_in_list_present(self, selectors: list[str]) -> bool:
        for selector in selectors:
            for ele in await self.page.locator(selector).all():
                if await ele.is_visible():
                    logging.debug("Detected selector: " + selector + " from list " + ", ".join(selectors))
                    return True
        logging.debug("No selector in list found: " + ", ".join(selectors))
        return False
