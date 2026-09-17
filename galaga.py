#-------------------------
#INITAL BLOCK
#------------------------


import curses

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)
    stdscr.timeout(50)

    height, width = stdscr.getmaxyx()
    x = width // 2
    y = height // 2

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key== curses.KEY_LEFT:
            x = max(0,x-4)
        elif key== curses.KEY_RIGHT:
            x = min(width-1 , x+4)
        stdscr.erase()
        stdscr.addstr(y+y//2, x, "A")
        stdscr.refresh()

curses.wrapper(main)


#--------------------------
#
#--------------------------
