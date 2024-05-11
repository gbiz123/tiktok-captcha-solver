"""Simulate curved mouse movement"""

import random


class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y


def vertex_form(a: float, x: float, vertex: Point) -> Point:
    """y = a(x-h)**2 + k"""
    return Point(x, a*(x - vertex.x)**2 + vertex.y)


def solve_for_a(point: Point, vertex: Point) -> float:
    """Solve for 'a' coefficient of a parabola given a point and a vertex"""
    return (point.y - vertex.y) / (point.x - vertex.x)


def generate_random_parabola(start: Point, end: Point) -> list[Point]:
    """Generate a random parabola connecting two points"""
    l = end.x - start.x
    h = l / 2
    k = l * (random.random() / 4) # Anything between -1/4 and 1/4 of the length
    vertex = Point(h, k)
    a = solve_for_a(start, vertex)
    points = [vertex_form(a, x, vertex) for x in range(int(start.x), int(end.x))]
    points.insert(0, start)
    points.append(end)
    return points
