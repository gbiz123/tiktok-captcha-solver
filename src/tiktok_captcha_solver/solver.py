"""Abstract base class for Tiktok Captcha Solvers"""

from abc import ABC, abstractmethod
from typing import Literal

from undetected_chromedriver import logging

class Solver(ABC):

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


    def solve_captcha_if_present(self, captcha_detect_timeout: int = 15, retries: int = 3) -> None:
        """Solves any captcha that is present, if one is detected

        Args:
            captcha_detect_timeout: return if no captcha is detected in this many seconds
            retries: number of times to retry captcha
        """
        if not self.captcha_is_present(captcha_detect_timeout):
            logging.debug("Captcha is not present")
            return
        match self.identify_captcha():
            case "puzzle": 
                logging.debug("Detected puzzle")
                self.solve_puzzle(retries)
            case "rotate": 
                logging.debug("Detected rotate")
                self.solve_rotate(retries)
            case "shapes": 
                logging.debug("Detected shapes")
                self.solve_shapes(retries)

    @abstractmethod
    def captcha_is_present(self, timeout: int = 15) -> bool:
        pass

    @abstractmethod
    def identify_captcha(self) -> Literal["puzzle", "shapes", "rotate"]:
        pass

    @abstractmethod
    def solve_shapes(self, retries: int = 3) -> None:
        pass

    @abstractmethod
    def solve_rotate(self, retries: int = 3) -> None:
        pass

    @abstractmethod
    def solve_puzzle(self, retries: int = 3) -> None:
        pass

