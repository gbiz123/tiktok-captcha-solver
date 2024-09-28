def compute_rotate_slide_distance(angle: int, slide_bar_width: float, slide_button_width: float) -> int:
    return int(((slide_bar_width - slide_button_width) * angle) / 360)


def compute_puzzle_slide_distance(proportion_x: float, puzzle_image_width: float) -> int:
    return int(proportion_x * puzzle_image_width)
