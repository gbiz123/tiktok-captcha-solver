import requests
import logging

from .models import ShapesCaptchaResponse, RotateCaptchaResponse, PuzzleCaptchaResponse

class ApiClient:

    _PUZZLE_URL: str
    _ROTATE_URL: str
    _SHAPES_URL: str

    def __init__(self, api_key: str) -> None:
        self._PUZZLE_URL = "https://www.sadcaptcha.com/api/v1/puzzle?licenseKey=" + api_key
        self._ROTATE_URL = "https://www.sadcaptcha.com/api/v1/rotate?licenseKey=" + api_key
        self._SHAPES_URL = "https://www.sadcaptcha.com/api/v1/shapes?licenseKey=" + api_key

    def rotate(self, outer_b46: str, inner_b64: str) -> RotateCaptchaResponse:
        data = {
            "outerImageB64": outer_b46,
            "innerImageB64": inner_b64
        }        
        resp = requests.post(self._ROTATE_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        return RotateCaptchaResponse(angle=result.get("angle"))

    def puzzle(self, puzzle_b64: str, piece_b64: str) -> PuzzleCaptchaResponse:
        data = {
            "puzzleImageB64": puzzle_b64,
            "pieceImageB64": piece_b64
        }        
        resp = requests.post(self._PUZZLE_URL, json=data)
        result = resp.json()
        logging.debug("Got API response")
        return PuzzleCaptchaResponse(slide_x_proportion=result.get("slideXProportion"))

    def shapes(self, image_b64: str) -> ShapesCaptchaResponse:
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
