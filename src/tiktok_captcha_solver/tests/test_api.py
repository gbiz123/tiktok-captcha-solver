import base64
import os
import logging

from ..downloader import download_image_b64
from ..api import ApiClient
from tiktok_captcha_solver.models import PuzzleCaptchaResponse, RotateCaptchaResponse, ShapesCaptchaResponse

api_client = ApiClient(os.environ["API_KEY"])

def test_rotate(caplog):
    caplog.set_level(logging.DEBUG)
    inner = download_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/inner_tt.png")
    outer = download_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/outer_tt.png")
    res = api_client.rotate(outer, inner)
    assert isinstance(res, RotateCaptchaResponse)


def test_puzzle():
    piece = download_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/piece.png")
    puzzle = download_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/puzzle.jpg")
    res = api_client.puzzle(puzzle, piece)
    assert isinstance(res, PuzzleCaptchaResponse)


def test_shapes():
    # image = download_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/tiktok3d.png")
    with open("/home/gregb/ToughdataLLC/SadCaptcha/sadcaptcha-image-processor/src/test/resources/tiktok3d.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode()
        res = api_client.shapes(image)
        assert isinstance(res, ShapesCaptchaResponse)
