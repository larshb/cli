from sys import stdout

ESC = '\x1b'
CSI = ESC + '['
SCP = SCOSC = CSI + 's' # Save Current Cursor Position
RCP = SCORC = CSI + 'u' # Restore Saved Cursor Position

# --- CSI Section -------------------------------------------------------------

csi = lambda n, x: f"{CSI}{n}{x}"
cuu = lambda n="": csi(n, 'A') # Cursor Up
cud = lambda n="": csi(n, 'B') # Cursor Down
cuf = lambda n="": csi(n, 'C') # Cursor Forward
cub = lambda n="": csi(n, 'D') # Cursor Back
cnl = lambda n="": csi(n, 'E') # Cursor Next Line
cpl = lambda n="": csi(n, 'F') # Cursor Previous Line
cha = lambda n="": csi(n, 'G') # Cursor Horizontal Absolute
eid = lambda n="": csi(n, 'J') # Erase in Display
eil = lambda n="": csi(n, 'K') # Erase in Line
scu = lambda n="": csi(n, 'S') # Scroll Up
scd = lambda n="": csi(n, 'T') # Scroll Down

# Cursor Position
def cup(n, m):
    return f"{CSI}{n};{m}H"

# Horizontal Vertical Position
def hvp(n, m):
    return f"{CSI}{n};{m}f"

# Set Graphic Rendition
def sgr(*n):
    return f"{CSI}{';'.join(str(x) for x in n)}m"

# --- Standard stream interface -----------------------------------------------

def say(string):
    stdout.write(string)
    stdout.flush()
    return string

# --- Private sequences -------------------------------------------------------

def lh(boolean):
    return 'h' if boolean else 'l'

def show_cursor(show):
    say(CSI + "?25" + lh(show))

def alternate_screen_buffer(enable):
    say(CSI + '?1049' + lh(enable))

def bracketed_paste_mode(on):
    say(CSI + '?2004' + lh(on))

# --- Convenience functions ---------------------------------------------------

def clear_screen():
    say(CSI + "2J")

# --- Colors ------------------------------------------------------------------

# 3-bit colors (BGR)
C3B_BLACK   = 0b000
C3B_RED     = 0b001
C3B_GREEN   = 0b010
C3B_YELLOW  = 0b011
C3B_BLUE    = 0b100
C3B_PURPLE  = 0b101
C3B_CYAN    = 0b110
C3B_WHITE   = 0b111

def c3b_foreground(color):
    return color + 30

def c3b_background(color):
    return color + 40

# SGR-index
def c3b_index(color, background=False):
    return c3b_background(color) if background else c3b_foreground(color)

# Complete SGR escape sequence
def c3b(color, background=False):
    return sgr(c3b_index(color, background=background))

# --- Constants ---------------------------------------------------------------

# Named Numeric Constants for optional SGR-combinations (a;b;c;...;n)
SGR_RESET       = 0
SGR_INCREASE    = 1
SGR_DECREASE    = 2
SGR_ITALIC      = 3
SGR_UNDERLINE   = 4
SGR_BLINK_SLOW  = 5
SGR_BLINK_RAPID = 6
SGR_REVERSE     = 7
SGR_CONCEAL     = 8
SGR_CROSSED     = 9
SGR_FG_BLACK    = c3b_index(C3B_BLACK , background=False)
SGR_FG_RED      = c3b_index(C3B_RED   , background=False)
SGR_FG_GREEN    = c3b_index(C3B_GREEN , background=False)
SGR_FG_YELLOW   = c3b_index(C3B_YELLOW, background=False)
SGR_FG_BLUE     = c3b_index(C3B_BLUE  , background=False)
SGR_FG_PURPLE   = c3b_index(C3B_PURPLE, background=False)
SGR_FG_CYAN     = c3b_index(C3B_CYAN  , background=False)
SGR_FG_WHITE    = c3b_index(C3B_WHITE , background=False)
SGR_BG_BLACK    = c3b_index(C3B_BLACK , background=True)
SGR_BG_RED      = c3b_index(C3B_RED   , background=True)
SGR_BG_GREEN    = c3b_index(C3B_GREEN , background=True)
SGR_BG_YELLOW   = c3b_index(C3B_YELLOW, background=True)
SGR_BG_BLUE     = c3b_index(C3B_BLUE  , background=True)
SGR_BG_PURPLE   = c3b_index(C3B_PURPLE, background=True)
SGR_BG_CYAN     = c3b_index(C3B_CYAN  , background=True)
SGR_BG_WHITE    = c3b_index(C3B_WHITE , background=True)

# Pre-defined escape sequences
NONE      = sgr(SGR_RESET      )
BOLD      = sgr(SGR_INCREASE   )
DIM       = sgr(SGR_DECREASE   )
ITALIC    = sgr(SGR_ITALIC     )
UNDERLINE = sgr(SGR_UNDERLINE  )
BLINK     = sgr(SGR_BLINK_SLOW )
BLINK2    = sgr(SGR_BLINK_RAPID)
INVERT    = sgr(SGR_REVERSE    )
HIDE      = sgr(SGR_CONCEAL    )
STRIKE    = sgr(SGR_CROSSED    )
BLACK     = c3b(C3B_BLACK      )
RED       = c3b(C3B_RED        )
GREEN     = c3b(C3B_GREEN      )
YELLOW    = c3b(C3B_YELLOW     )
BLUE      = c3b(C3B_BLUE       )
PURPLE    = c3b(C3B_PURPLE     )
CYAN      = c3b(C3B_CYAN       )
WHITE     = c3b(C3B_WHITE      )
