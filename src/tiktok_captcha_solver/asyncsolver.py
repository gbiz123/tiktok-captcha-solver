"""Abstract base class for Tiktok Captcha Async Solvers"""

import asyncio
from abc import ABC, abstractmethod
from typing import Literal

from undetected_chromedriver import logging

class AsyncSolver(ABC):

    @property
    def captcha_wrappers(self) -> list[str]:
        return [".captcha-disable-scroll"]

    @property
    def rotate_selectors(self) -> list[str]:
        return [
            "[data-testid=whirl-inner-img]",
            "[data-testid=whirl-outer-img]"
        ]

    @property
    def puzzle_selectors(self) -> list[str]:
        return [
            "img.captcha_verify_img_slide"
        ]

    @property
    def shapes_selectors(self) -> list[str]:
        return [
            ".verify-captcha-submit-button" 
        ]


    async def solve_captcha_if_present(self, captcha_detect_timeout: int = 15, retries: int = 3) -> None:
        """Solves any captcha that is present, if one is detected

        Args:
            captcha_detect_timeout: return if no captcha is detected in this many seconds
            retries: number of times to retry captcha
        """
        for _ in range(retries):
            if not await self.captcha_is_present(captcha_detect_timeout):
                logging.debug("Captcha is not present")
                return
            match await self.identify_captcha():
                case "puzzle": 
                    logging.debug("Detected puzzle")
                    await self.solve_puzzle()
                case "rotate": 
                    logging.debug("Detected rotate")
                    await self.solve_rotate()
                case "shapes": 
                    logging.debug("Detected shapes")
                    await self.solve_shapes()
            if await self.captcha_is_not_present(timeout=5):
                return
            else:
                await asyncio.sleep(5)

    @abstractmethod
    async def captcha_is_present(self, timeout: int = 15) -> bool:
        pass

    @abstractmethod
    async def captcha_is_not_present(self, timeout: int = 15) -> bool:
        pass

    @abstractmethod
    async def identify_captcha(self) -> Literal["puzzle", "shapes", "rotate"]:
        pass

    @abstractmethod
    async def solve_shapes(self) -> None:
        pass

    @abstractmethod
    async def solve_rotate(self) -> None:
        pass

    @abstractmethod
    async def solve_puzzle(self) -> None:
        pass

