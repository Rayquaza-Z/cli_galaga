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

        if pattern == 0:
            mid = (enemy_count - 1) / 2.0
            for i in range(enemy_count):
                offset = int((i - mid) * spacing)
                enemies.append([center_x + offset, 2])

        elif pattern == 1:
            row1 = enemy_count // 2 + enemy_count % 2
            row2 = enemy_count - row1
            mid1 = (row1 - 1) / 2.0
            for i in range(row1):
                offset = int((i - mid1) * spacing)
                enemies.append([center_x + offset, 2])
            mid2 = (row2 - 1) / 2.0
            for i in range(row2):
                offset = int((i - mid2) * spacing)
                enemies.append([center_x + offset, 4])

        else:
            mid = (enemy_count - 1) / 2.0
            for i in range(enemy_count):
                offset = int((i - mid) * spacing)
                row = 2 + int(abs(i - mid))
                enemies.append([center_x + offset, row])

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
            x = max(0, x - 2)
        elif key == curses.KEY_RIGHT:
            x = min(width - 1, x + 2)
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
