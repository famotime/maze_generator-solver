import pygame
from enum import Enum


# 定义一些公共属性
WIDTH = 500
HEADER = 90
HEIGHT = WIDTH + HEADER
BUTTON_MARGIN = 2

TITLE = "迷宫1.5"
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
FPS = 60
CLOCK = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (126, 206, 253)
COLOR_CYAN = (74, 217, 217)
COLOR_GREY = (218, 234, 239)

GENERATE_STEP_TIME = 0
SOLVE_STEP_TIME = 0


class MAZE_TYPE(Enum):
    GENERATE = 0
    RECURSIVE_BACKTRACKER = 1
    RANDOM_PRIM = 2
    RECURSIVE_DIVISION = 3
    UNION_FIND_SET = 4
    SOLVE = 5
    RECURSIVE = 6
    DFS = 7
    ASTAR = 8
    BFS = 9


generator_types = {MAZE_TYPE.GENERATE: "生成迷宫",
                   MAZE_TYPE.SOLVE: "探索迷宫",
                   MAZE_TYPE.RECURSIVE_BACKTRACKER: "Backtrack",
                   MAZE_TYPE.RANDOM_PRIM: "RandomPrim",
                   MAZE_TYPE.RECURSIVE_DIVISION: "Division",
                   MAZE_TYPE.UNION_FIND_SET: "UnionFind",
                   MAZE_TYPE.RECURSIVE: "Recursive",
                   MAZE_TYPE.DFS: "DFS",
                   MAZE_TYPE.ASTAR: "A*",
                   MAZE_TYPE.BFS: "BFS"}
