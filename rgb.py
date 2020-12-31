#!/usr/bin/python3
# 24-bit color ANSI escape sequence utility

from ansi import say, sgr, c24, NONE, sgr_c24_fg, sgr_c24_bg
from PIL import Image


class DoubleBlock:

    def __init__(self, top : tuple, bottom : tuple):
        self.top = top
        self.bottom = bottom

    def __str__(self):
        return sgr(sgr_c24_fg(*self.top) + ';' + sgr_c24_bg(*self.bottom)) + '▀'


class TerminalImage:

    def __init__(self, image : Image.Image):
        self.img = image

    def __str__(self):
        px = self.img.load()
        X, Y = self.img.size
        lines = []
        for y2 in range(Y//2):
            lines.append(
                ''.join(
                    str(DoubleBlock(px[x, 2*y2], px[x, 2*y2+1]))
                    for x in range(X)
                )
            )
        return f'{NONE}\n'.join(lines) + NONE


def fill_console(image_file):
    from shutil import get_terminal_size

    width, height = get_terminal_size()

    im = Image.open(image_file)
    X, Y = im.size
    while X > width:
        im = im.resize((X // 2, Y // 2))
        X, Y = im.size
    ti = TerminalImage(im)
    si = str(ti)
    print(si)



if __name__ == '__main__':

    # from os.path import abspath, dirname
    # HERE = abspath(dirname(__file__))
    # IMAGE_FILE = f"{HERE}/kiss.jpg"
    # # IMAGE_FILE = f"{HERE}/andreas.jpg"

    # fill_console(IMAGE_FILE)

    from pathlib import Path

    root = Path("/")
    jpegs = root.rglob("*.jpg")
    for jpeg in jpegs:
        print(jpeg)
        fill_console(jpeg)
