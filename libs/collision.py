from pygame import Vector2, Rect

__all__ = ["circle_circle", "circle_rect", "rect_rect", "point_circle", "point_rect", "orient"]


def orient(c: Vector2, a: Vector2, b: Vector2) -> int:
    lin = b-a
    return (lin.y*c.x-lin.x*c.y+b.x*a.y-b.y*a.x)/lin.length()


def circle_circle(cx1, cy1, cr1, cx2, cy2, cr2) -> bool:
    return Vector2.distance_to((cx1, cy1), (cx2, cy2)) < cr1+cr2


def circle_rect(cx, cy, cr, bx, by, bw, bh) -> bool:
    return ((max(bx, min(cx, bx+bw))-cx)**2+(max(by, min(cy, by+bh))-cy)**2)**0.5 < cr


def rect_rect(bx1, by1, bw1, bh1, bx2, by2, bw2, bh2) -> bool:
    return Rect(bx1, by1, bw1, bh1).colliderect((bx2, by2, bw2, bh2))


def point_circle(px, py, cx, cy, cr) -> bool:
    return Vector2.distance_to((px, py), cx, cy) < cr


def point_rect(px, py, rx, ry, rw, rh) -> bool:
    return Rect(rx, ry, rw, rh).collidepoint(px, py)
