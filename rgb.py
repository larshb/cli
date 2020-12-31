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


if __name__ == '__main__':
    from os.path import abspath, dirname

    HERE = abspath(dirname(__file__))
    # IMAGE_FILE = f"{HERE}/kiss.jpg"
    IMAGE_FILE = f"{HERE}/andreas.jpg"

    im = Image.open(IMAGE_FILE)
    X, Y = im.size
    res = 5
    im = im.resize((X//res, Y//res))
    X, Y = im.size
    ti = TerminalImage(im)
    si = str(ti)
    print(si)
