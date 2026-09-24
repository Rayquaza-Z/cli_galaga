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

    def build_formation(level, width):
        enemy_count = 9 + 2 * (level - 1)   # 9, 11, 13, 15...
        pattern = level % 3
        center_x = width // 2
        spacing = 4
        enemies = []
        
        safe_width = width - 4
        max_in_row = max(1, safe_width // spacing)

        def add_row(n, y_pos):
            mid = (n - 1) / 2.0
            for i in range(n):
                offset = int((i - mid) * spacing)
                enemies.append([center_x + offset, y_pos])

        if pattern == 0:
            remaining = enemy_count
            y = 2
            while remaining > 0:
                take = min(remaining, max_in_row)
                add_row(take, y)
                remaining -= take
                y += 2

        elif pattern == 1:
            row1 = enemy_count // 2 + enemy_count % 2
            row2 = enemy_count - row1
            
            y = 2
            for row_count in [row1, row2]:
                remaining = row_count
                while remaining > 0:
                    take = min(remaining, max_in_row)
                    add_row(take, y)
                    remaining -= take
                    y += 2

        else:
            remaining = enemy_count
            take = min(remaining, max_in_row)
            
            mid = (take - 1) / 2.0
            for i in range(take):
                offset = int((i - mid) * spacing)
                row = 2 + int(abs(i - mid))
                enemies.append([center_x + offset, row])
                
            remaining -= take
            y = 2 + int(mid) + 2
            
            while remaining > 0:
                take = min(remaining, max_in_row)
                add_row(take, y)
                remaining -= take
                y += 2

        return enemies

    def fire_chance_for_level(level):
        return min(0.03 + 0.01 * (level - 1), 0.2)

    def new_game():
        x = width // 2
        y = height // 2
        bullets = []
        e_bullets = []
        lives = 3
        game_over = False
        level = 1
        enemies = build_formation(level, width)
        fire_chance = fire_chance_for_level(level)

        return x, y, bullets, e_bullets, enemies, lives, game_over, level, fire_chance

    x, y, bullets, e_bullets, enemies, lives, game_over, level, fire_chance = new_game()

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        if game_over and key == ord('r'):
            x, y, bullets, e_bullets, enemies, lives, game_over, level, fire_chance = new_game()
        elif key == curses.KEY_LEFT:
            if x - 2 >= 1:
                x -= 2
        elif key == curses.KEY_RIGHT:
            if x + 2 <= width - 2:
                x += 2
        elif key == ord(' '):
            bullets.append([x, y + y // 2 - 1])

        if not game_over:

            for b in bullets:
                b[1] -= 1
            bullets = [b for b in bullets if b[1] > 0]

            for eb in e_bullets:
                eb[1] += 1
            e_bullets = [eb for eb in e_bullets if eb[1] < height - 1]

            for b in bullets[:]:
                for e in enemies[:]:
                    if b[0] == e[0] and b[1] == e[1]:
                        bullets.remove(b)
                        enemies.remove(e)
                        break

            for eb in e_bullets[:]:
                if eb[1] == y + y // 2 and eb[0] == x:
                    lives -= 1
                    e_bullets.remove(eb)
                    if lives == 0:
                        game_over = True
                    break

            if enemies and random.random() < fire_chance:
                shooter = random.choice(enemies)
                e_bullets.append([shooter[0], shooter[1] + 1])

            # level up once the formation is cleared
            if not enemies:
                level += 1
                enemies = build_formation(level, width)
                fire_chance = fire_chance_for_level(level)

        stdscr.erase()
        
        # Draw boundaries
        for i in range(1, height - 1):
            try:
                stdscr.addstr(i, 0, '#')
                stdscr.addstr(i, width - 1, '#')
            except curses.error:
                pass
                
        stdscr.addstr(y + y // 2, x, "^")

        for b in bullets:
            stdscr.addstr(b[1], b[0], "*")

        for e in enemies:
            stdscr.addstr(e[1], e[0], "W")
        for eb in e_bullets:
            stdscr.addstr(eb[1], eb[0], "!")

        hud = f"LIVES {lives}   LEVEL {level}"
        stdscr.addstr(0, 0, hud)

        if game_over:
            stdscr.addstr(height // 2, width // 2 - 5, "GAME OVER")

        stdscr.refresh()


curses.wrapper(main)

#--------------------------
#
#--------------------------
