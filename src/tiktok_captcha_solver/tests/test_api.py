import base64
import os
import logging

from ..downloader import fetch_image_b64
from ..api import ApiClient
from tiktok_captcha_solver.models import IconCaptchaResponse, PuzzleCaptchaResponse, RotateCaptchaResponse, ShapesCaptchaResponse

api_client = ApiClient(os.environ["API_KEY"])

def test_rotate(caplog):
    caplog.set_level(logging.DEBUG)
    inner = fetch_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/inner_tt.png")
    outer = fetch_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/outer_tt.png")
    res = api_client.rotate(outer, inner)
    assert isinstance(res, RotateCaptchaResponse)


def test_puzzle():
    piece = fetch_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/piece.png")
    puzzle = fetch_image_b64("https://raw.githubusercontent.com/gbiz123/sadcaptcha-code-examples/master/images/puzzle.jpg")
    res = api_client.puzzle(puzzle, piece)
    assert isinstance(res, PuzzleCaptchaResponse)


def test_shapes():
    with open("/home/gregb/ToughdataLLC/SadCaptcha/sadcaptcha-image-processor/src/test/resources/tiktok3d.png", "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode()
        res = api_client.shapes(image)
        assert isinstance(res, ShapesCaptchaResponse)

def test_icon():
    with open("/home/gregb/ToughdataLLC/SadCaptcha/sadcaptcha-image-processor/src/test/resources/tiktokicon.jpg", "rb") as image_file:
        challenge = "Which of these objects has a brim?"
        image = base64.b64encode(image_file.read()).decode()
        res = api_client.icon(challenge, image)
        assert isinstance(res, IconCaptchaResponse)
