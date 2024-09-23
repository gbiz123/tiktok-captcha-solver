class Wrappers:
    V1 = ".captcha-disable-scroll"
    V2 = ".captcha-verify-container"

class RotateV1:
    INNER = "[data-testid=whirl-inner-img]"
    OUTER = "[data-testid=whirl-outer-img]"
    SLIDE_BAR = ".captcha_verify_slide--slidebar"
    SLIDER_DRAG_BUTTON = ".secsdk-captcha-drag-icon"

class RotateV2:
    INNER = ".captcha-verify-container > div > div > div > img.cap-absolute"
    OUTER = ".captcha-verify-container > div > div > div > img:first-child"
    SLIDE_BAR = ".captcha-verify-container > div > div > div.cap-w-full > div.cap-rounded-full"
    SLIDER_DRAG_BUTTON = ".secsdk-captcha-drag-icon"

class PuzzleV1:
    PIECE = "img.captcha_verify_img_slide"
    PUZZLE = "#captcha-verify-image"
    SLIDER_DRAG_BUTTON = ".secsdk-captcha-drag-icon"

class PuzzleV2:
    PIECE = ".captcha-verify-container > div > div > div > div > img"
    PUZZLE = "#captcha-verify-image"
    SLIDER_DRAG_BUTTON = ".secsdk-captcha-drag-icon"

class ShapesV1:
    IMAGE = "#captcha-verify-image"
    SUBMIT_BUTTON = ".verify-captcha-submit-button" 

class ShapesV2:
    IMAGE = ".captcha-verify-container > div > div > div > img.cap-absolute"
    SUBMIT_BUTTON = ".captcha-verify-container > div > div > div > button.cap-w-full" 

class IconV1:
    IMAGE = "#captcha-verify-image"
    SUBMIT_BUTTON = ".verify-captcha-submit-button" 
    TEXT = ".captcha_verify_bar"

class IconV2:
    IMAGE = ".captcha-verify-container > div > div > div > img.cap-absolute"
    SUBMIT_BUTTON = ".captcha-verify-container > div > div > div > button.cap-w-full" 
    TEXT = ".captcha-verify-container > div > div > span"

class DouyinPuzzle:
    FRAME = "#captcha_container > iframe"
    PUZZLE = "#captcha_verify_image"
    PIECE = "#captcha-verify_img_slide"
