#!/usr/bin/python3
# 24-bit color ANSI escape sequence utility

from ansi import say, sgr, c24, NONE, sgr_c24_fg, sgr_c24_bg


ENABLE_TRANSPARENCY = False


class DoubleBlock:

    def __init__(self, top : tuple, bottom : tuple):
        self.top = top
        self.bottom = bottom

    def __str__(self):
        return sgr(sgr_c24_fg(*self.top) + ';' + sgr_c24_bg(*self.bottom)) + '▀'


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
        # if enable_trasnparency: # Does not work for some reason
        #     self.__str__ = self.__str__with_alpha
        return self

    def load_pil(self, image, key=None):
        self.im = image
        self.sz = self.im.size
        self.px = self.im.load()
        self.key = key
        return self

    def __str__(self):
        X, Y = self.sz
        lines = []
        for y2 in range(Y//2):
            lines.append(''.join(
                str(DoubleBlock(self.px[x, 2*y2], self.px[x, 2*y2+1]))
                for x in range(X)))
        return f'{NONE}\n'.join(lines) + NONE


def __TerminalImage_str_alpha(self):
    X, Y = self.sz
    lines = []
    for y2 in range(Y//2):
        line = ''
        for x in range(X):
            pxs = self.px[x, 2*y2], self.px[x, 2*y2+1]
            if self.key:
                pxs = map(lambda c: None if c == self.key else c, pxs)
            line += str(DoubleBlock(*pxs))
        lines.append(line)
    return f'{NONE}\n'.join(lines) + NONE


def __DoubleBlock_str_alpha(self, debug=True):

    sgr_string = '0'
    if self.top:
        symbol = '▀'
        sgr_string += ';' + sgr_c24_fg(*self.top)
        if self.bottom:
            sgr_string += ';' + sgr_c24_bg(*self.bottom)
    elif self.bottom:
        symbol = '▄'
        sgr_string += ';' + sgr_c24_fg(*self.bottom)
    else:
        symbol = ' '
    return sgr(sgr_string) + symbol


if ENABLE_TRANSPARENCY:
    TerminalImage.__str__ = __TerminalImage_str_alpha
    DoubleBlock.__str__ = __DoubleBlock_str_alpha





