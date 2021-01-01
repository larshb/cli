#!/usr/bin/python3
# 24-bit color ANSI escape sequence utility

from ansi import say, sgr, c24, NONE, sgr_c24_fg, sgr_c24_bg


class DoubleBlock:

    def __init__(self, top : tuple, bottom : tuple):
        self.top = map(int, top)
        self.bottom = map(int, bottom)

    def __str__(self, debug=True):
        #if type(self.top) == int:
        #    return sgr(sgr_c24_fg(self.top, self.top, self.top) + ';' + sgr_c24_bg(self.bottom, self.bottom, self.bottom)) + '▀'
        tr, tg, tb = self.top
        br, bg, bb = self.bottom

        #symbol = f"{r:02x}" if debug else '▀'
        symbol = '▀'
        return sgr(sgr_c24_fg(tr, tg, tb) + ';' + sgr_c24_bg(br, bg, bb)) + symbol


class list2d(list):

    def __init__(self, lst):
        self.lst = lst

    def __getitem__(self, index):
        x, y = index
        return self.lst[y][x]


class TerminalImage:

    def load(self, lst):
        self.sz = (len(lst[0]), len(lst))
        self.px = list2d(lst)
        #self.size 
        return self

    def load_pil(self, image):
        self.im = image
        self.sz = self.im.size
        self.px = self.im.load()
        return self

    def __str__(self):
        X, Y = self.sz
        lines = []
        for y2 in range(Y//2):
            lines.append(
                ''.join(
                    str(DoubleBlock(
                        self.px[x, 2*y2],
                        self.px[x, 2*y2+1]))
                    for x in range(X)
                )
            )
        return f'{NONE}\n'.join(lines) + NONE


def fill_console(image):
    from shutil import get_terminal_size
    from logging import info
    width, height = get_terminal_size()
    info(f"Terminal size: {(width, height)}")

    if type(image) == str:
        from PIL import Image
        im = Image.open(image)
        X, Y = im.size
        while X > width:
            im = im.resize((X // 2, Y // 2))
            X, Y = im.size
        ti = TerminalImage().load_pil(im)
    elif type(image) == list:
        ti = TerminalImage().load(image)

    si = str(ti)
    print(si)



if __name__ == '__main__':

    from os.path import abspath, dirname
    HERE = abspath(dirname(__file__))
    # IMAGE_FILE = f"{HERE}/kiss.jpg"
    IMAGE_FILE = f"{HERE}/andreas.jpg"
    # IMAGE_FILE = f"{HERE}/mario.png"

    from ansi import cup
    say(cup(10, 1)) # Row, column

    fill_console(IMAGE_FILE)

    # from pathlib import Path

    # root = Path("/")
    # jpegs = root.rglob("*.jpg")
    # for jpeg in jpegs:
    #     print(jpeg)
    #     fill_console(jpeg)

    # L = [
    #     [(255, 0, 0), (0, 0, 0), (100, 100, 100)],
    #     [(255, 0, 0), (0, 0, 0), (100, 100, 100)],
    #     [(255, 0, 0), (0, 0, 0), (100, 100, 100)],
    #     [(255, 0, 0), (0, 0, 0), (100, 100, 100)],
    #     [(255, 0, 0), (0, 0, 0), (0, 0, 0)],
    #     [(255, 0, 0), (255, 0, 0), (255, 0, 0)]
    # ]
    # fill_console(L)
