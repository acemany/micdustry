from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime, timedelta, timezone
from pygame import Vector2, Rect
from platform import system
from tkinter import Tk


__all__ = ["c_c_c", "c_c_r", "c_r_r", "c_p_c", "c_p_r", "orient",
           "log", "open_file_as", "save_file_as"]


def log(e: str) -> None:
    with open("log.txt", "a") as file:
        file.write(f"\n{datetime.now(timezone(timedelta(hours=3, minutes=0), 'Moscow'))} - {e}\n")


def open_file_as(file_type: str) -> str:
    "Ask the user to select a file to open"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or (system() == "Darwin"):
        file_path = askopenfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image"else\
                     [("Micdustry save file", "*.msav"), ("All files", "*")] if file_type == "msave" else\
                     [("All files", "*")]
        file_path = askopenfilename(parent=root, filetypes=file_types)
    root.update()

    return file_path if file_path else None


def save_file_as(file_type: str) -> str:
    "Ask the user to select a file to save"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or (system() == "Darwin"):
        file_path = asksaveasfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image" else\
                     [("Micdustry save file", "*.msav"), ("All files", "*")]if file_type == "msave"else\
                     [("All files", "*")]
        file_path = asksaveasfilename(parent=root, filetypes=file_types)
    root.update()
    return file_path if file_path else None


def orient(c: Vector2, a: Vector2, b: Vector2) -> int:
    lin = b-a
    return (lin.y*c.x-lin.x*c.y+b.x*a.y-b.y*a.x)/lin.length()


def c_c_c(cx1, cy1, cr1, cx2, cy2, cr2) -> bool:
    return Vector2.distance_to((cx1, cy1), (cx2, cy2)) < cr1+cr2


def c_c_r(cx, cy, cr, bx, by, bw, bh) -> bool:
    return ((max(bx, min(cx, bx+bw))-cx)**2+(max(by, min(cy, by+bh))-cy)**2)**0.5 < cr


def c_r_r(bx1, by1, bw1, bh1, bx2, by2, bw2, bh2) -> bool:
    return Rect(bx1, by1, bw1, bh1).colliderect((bx2, by2, bw2, bh2))


def c_p_c(px, py, cx, cy, cr) -> bool:
    return Vector2.distance_to((px, py), cx, cy) < cr


def c_p_r(px, py, rx, ry, rw, rh) -> bool:
    return Rect(rx, ry, rw, rh).collidepoint(px, py)
