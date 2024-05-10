from pydantic import BaseModel

class ShapesCaptchaResponse(BaseModel):
    point_one_proportion_x: float
    point_one_proportion_y: float
    point_two_proportion_x: float
    point_two_proportion_y: float

class RotateCaptchaResponse(BaseModel):
    angle: int

class PuzzleCaptchaResponse(BaseModel):
    slide_x_proportion: float
