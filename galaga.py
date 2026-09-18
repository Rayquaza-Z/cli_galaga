#-------------------------
#INITAL BLOCK
#------------------------

import random
import curses

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)
    stdscr.timeout(50)


    height, width = stdscr.getmaxyx()

    def new_game():
        x = width // 2
        y = height // 2



        bullets=[]
        enemies=[]
        e_bullets=[]

    

        enemy_count=9
        enemy_space=4
        center_x=width//2
        middle_ind = enemy_count//2


        for i in range(enemy_count):
            offset= (i-middle_ind)*enemy_space
            enemies.append([center_x + offset,2])

        lives=3
        game_over=False


        return x,y,bullets,e_bullets,enemies , lives , game_over

    x, y, bullets, e_bullets, enemies, lives, game_over = new_game()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        if game_over and key == ord('r'):
            x, y, bullets, e_bullets, enemies, lives, game_over = new_game()
        elif key== curses.KEY_LEFT:
            x = max(0,x-4)
        elif key== curses.KEY_RIGHT:
            x = min(width-1 , x+4)
        elif key== ord(' '):
            bullets.append([x,y+y//2-1])

        if not game_over:
            


            for b in bullets:
                b[1]-=1
            bullets = [b for b in bullets if b[1]>0]

            for eb in e_bullets:
                eb[1]+=1
            e_bullets=[eb for eb in e_bullets if eb[1]<height-1] 


            for b in bullets[:]:
                for e in enemies[:]:
                    if b[0]==e[0] and b[1]==e[1]:
                        bullets.remove(b)
                        enemies.remove(e)
                        break

            for eb in e_bullets[:]:
                if eb[1]==y+y//2 and eb[0]==x:
                    lives-=1
                    e_bullets.remove(eb)
                    if lives==0:
                        game_over=True
                    break

            if enemies and random.random()<0.08:
                shooter=random.choice(enemies)
                e_bullets.append([shooter[0],shooter[1]+1])



        stdscr.erase()
        stdscr.addstr(y+y//2, x, "A")

        for b in bullets:
            stdscr.addstr(b[1], b[0], "#")

        

        for e in enemies:
            stdscr.addstr(e[1],e[0],"W")
        for eb in e_bullets:
            stdscr.addstr(eb[1],eb[0],"!")

        if game_over:
            stdscr.addstr(height//2, width//2 - 5 , "GAME OVER")

        stdscr.refresh()




curses.wrapper(main)

#--------------------------
#
#--------------------------
