import curses
import math
import time
from curses import wrapper

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
]


PLAYER_X = 1.5
PLAYER_Y = 1.5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.1
ROTATION_SPEED = 0.1


WALL_CHARS = ['█', '▓', '▒', '░']
FOV = math.pi / 3
MAX_DEPTH = 12

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

def cast_ray(angle, player_x, player_y):
    ray_x = player_x
    ray_y = player_y
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    vert_x = int(ray_x) + (1 if cos_a > 0 else 0)
    vert_y = ray_y + (vert_x - ray_x) * sin_a / (cos_a if cos_a != 0 else 1e-6)
    vert_dist = float('inf')
    while 0 <= vert_x < len(MAP[0]) and 0 <= int(vert_y) < len(MAP):
        if MAP[int(vert_y)][vert_x] == 1:
            vert_dist = math.sqrt((vert_x - player_x) ** 2 + (vert_y - player_y) ** 2)
            break
        vert_x += 1 if cos_a > 0 else -1
        vert_y += sin_a / (cos_a if cos_a != 0 else 1e-6) * (1 if cos_a > 0 else -1)
    horz_y = int(ray_y) + (1 if sin_a > 0 else 0)
    horz_x = ray_x + (horz_y - ray_y) * cos_a / (sin_a if sin_a != 0 else 1e-6)
    horz_dist = float('inf')
    while 0 <= int(horz_x) < len(MAP[0]) and 0 <= horz_y < len(MAP):
        if MAP[horz_y][int(horz_x)] == 1:
            horz_dist = math.sqrt((horz_x - player_x) ** 2 + (horz_y - player_y) ** 2)
            break
        horz_y += 1 if sin_a > 0 else -1
        horz_x += cos_a / (sin_a if sin_a != 0 else 1e-6) * (1 if sin_a > 0 else -1)
    return min(vert_dist, horz_dist)

def main(stdscr):
    global PLAYER_X, PLAYER_Y, PLAYER_ANGLE
    
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.keypad(True)
    init_colors()
    
    last_time = time.time()
    frame_count = 0
    fps = 0
    
    while True:
        current_time = time.time()
        frame_count += 1
        
        if current_time - last_time >= 1.0:
            fps = frame_count
            frame_count = 0
            last_time = current_time
        
        
        key = stdscr.getch()
        move_x, move_y = 0, 0
        if key == curses.KEY_UP:
            move_x = math.cos(PLAYER_ANGLE) * PLAYER_SPEED
            move_y = math.sin(PLAYER_ANGLE) * PLAYER_SPEED
        elif key == curses.KEY_DOWN:
            move_x = -math.cos(PLAYER_ANGLE) * PLAYER_SPEED
            move_y = -math.sin(PLAYER_ANGLE) * PLAYER_SPEED
        elif key == curses.KEY_LEFT:
            PLAYER_ANGLE -= ROTATION_SPEED
        elif key == curses.KEY_RIGHT:
            PLAYER_ANGLE += ROTATION_SPEED
        elif key == ord('q'):
            break
        
        
        new_x = PLAYER_X + move_x
        new_y = PLAYER_Y + move_y
        if 0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP):
            if MAP[int(new_y)][int(new_x)] == 0:
                PLAYER_X, PLAYER_Y = new_x, new_y
        
        stdscr.clear()
        
        height, width = stdscr.getmaxyx()
        for x in range(width - 1):
            ray_angle = PLAYER_ANGLE - FOV/2 + (FOV * x / (width - 1))
            distance = cast_ray(ray_angle, PLAYER_X, PLAYER_Y)
            
            wall_height = min(int(height / (distance + 0.0001)), height - 1)
            wall_char = WALL_CHARS[min(int(distance * len(WALL_CHARS) / MAX_DEPTH), len(WALL_CHARS) - 1)]
            
            color_pair = min(int(distance * 3 / MAX_DEPTH) + 1, 4)
            for y in range((height - wall_height) // 2, (height + wall_height) // 2):
                if 0 <= y < height - 1:
                    stdscr.addstr(y, x, wall_char, curses.color_pair(color_pair))
        
        stdscr.addstr(0, 0, f"FPS: {fps}", curses.color_pair(1))
        
        stdscr.refresh()
        time.sleep(0.016)

if __name__ == "__main__":
    wrapper(main) 
