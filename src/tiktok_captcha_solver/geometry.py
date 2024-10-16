def compute_rotate_slide_distance(angle: int, slide_bar_width: float, slide_button_width: float) -> int:
    return int(((slide_bar_width - slide_button_width) * angle) / 360)


def compute_pixel_fraction(proportion_x: float, container_width: float) -> int:
    return int(proportion_x * container_width)
