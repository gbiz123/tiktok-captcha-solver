import requests
import logging

from .models import ProportionalPoint, ShapesCaptchaResponse, RotateCaptchaResponse, PuzzleCaptchaResponse, IconCaptchaResponse

class ApiClient:

    _PUZZLE_URL: str
    _ROTATE_URL: str
    _SHAPES_URL: str
    _ICON_URL: str

    def __init__(self, api_key: str) -> None:
        self._PUZZLE_URL = "https://www.sadcaptcha.com/api/v1/puzzle?licenseKey=" + api_key
        self._ROTATE_URL = "https://www.sadcaptcha.com/api/v1/rotate?licenseKey=" + api_key
        self._SHAPES_URL = "https://www.sadcaptcha.com/api/v1/shapes?licenseKey=" + api_key
        self._ICON_URL = "https://www.sadcaptcha.com/api/v1/icon?licenseKey=" + api_key

    def rotate(self, outer_b46: str, inner_b64: str) -> RotateCaptchaResponse:
        """Slide the slider to rotate the images"""
        data = {
            "outerImageB64": outer_b46,
            "innerImageB64": inner_b64
        }        
        resp = requests.post(self._ROTATE_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        return RotateCaptchaResponse(angle=result.get("angle"))

    def puzzle(self, puzzle_b64: str, piece_b64: str) -> PuzzleCaptchaResponse:
        """Slide the puzzle piece"""
        data = {
            "puzzleImageB64": puzzle_b64,
            "pieceImageB64": piece_b64
        }        
        resp = requests.post(self._PUZZLE_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        return PuzzleCaptchaResponse(slide_x_proportion=result.get("slideXProportion"))

    def shapes(self, image_b64: str) -> ShapesCaptchaResponse:
        """Click the two matching points"""
        data = { "imageB64": image_b64 }        
        resp = requests.post(self._SHAPES_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        return ShapesCaptchaResponse(
            point_one_proportion_x=result.get("pointOneProportionX"),
            point_one_proportion_y=result.get("pointOneProportionY"),
            point_two_proportion_x=result.get("pointTwoProportionX"),
            point_two_proportion_y=result.get("pointTwoProportionY")
        )

    def icon(self, challenge_text: str, image_b64: str) -> IconCaptchaResponse:
        """Which of these objects has a... type captcha. Shown at video upload."""
        data = { "challenge": challenge_text, "imageB64": image_b64 }        
        resp = requests.post(self._ICON_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        resp = IconCaptchaResponse(proportional_points=[])
        for point in result.get("proportionalPoints"):
            resp.proportional_points.append(
                ProportionalPoint(
                    proportion_x=point.get("proportionX"),
                    proportion_y=point.get("proportionY")
                )
            )
        return resp
