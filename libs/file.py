from tkinter.filedialog import askopenfilename, asksaveasfilename
from platform import system
from pathlib import Path
from tkinter import Tk


__all__ = ["Path",
           "open_file_as", "save_file_as"]


def open_file_as(file_type: str) -> str:
    "Ask the user to select a file to open"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or system() == "Darwin":
        file_path = askopenfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image"else\
                     [("Micdustry save file", "*.msav")] if file_type == "msave" else\
                     [("All files", "*")]
        file_path = askopenfilename(parent=root, filetypes=file_types)
    root.update()

    return file_path if file_path else None


def save_file_as(file_type: str) -> str:
    "Ask the user to select a file to save"
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if file_type is None or system() == "Darwin":
        file_path = asksaveasfilename(parent=root)
    else:
        file_types = [("Image file", "*.png;*.jpg;*.jpeg;*.ico;*.gif;*.bmp"), ("All files", "*")]\
            if file_type == "image" else\
                     [("Micdustry save file", "*.msav")]if file_type == "msave"else\
                     [("All files", "*")]
        file_path = asksaveasfilename(parent=root, filetypes=file_types)
    root.update()
    return file_path if file_path else None
