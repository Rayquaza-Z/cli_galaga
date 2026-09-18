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


#==================================
    bullets=[]
    enemies=[]

    enemy_count=9
    enemy_space=4
    center_x=width//2
    middle_ind = enemy_count//2


    for i in range(enemy_count):
        offset= (i-middle_ind)*enemy_space
        enemies.append([center_x + offset,2])

    '''for col in range(8):
        enemies.append([8 + col * 4, 2])'''



    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key== curses.KEY_LEFT:
            x = max(0,x-4)
        elif key== curses.KEY_RIGHT:
            x = min(width-1 , x+4)
        elif key== ord(' '):
            bullets.append([x,y+y//2-1])
        for b in bullets:
            b[1]-=1
        bullets = [b for b in bullets if b[1]>0]


        for b in bullets:
            for e in enemies:
                if b[0]==e[0] and b[1]==e[1]:
                    bullets.remove(b)
                    enemies.remove(e)
                    break

        stdscr.erase()
        stdscr.addstr(y+y//2, x, "A")

        for b in bullets:
            stdscr.addstr(b[1], b[0], "#")

        for e in enemies:
            stdscr.addstr(e[1],e[0],"W")
        stdscr.refresh()

curses.wrapper(main)

#--------------------------
#
#--------------------------
