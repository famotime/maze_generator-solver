"""借助pygame可视化生成迷宫"""
import threading
import random
import pygame
import maze_generator
import maze_solver
from utils import stop_thread
from general_config import *
import astar_search as ast


class Button():
    """操作按钮"""
    def __init__(self, screen, width, height, x, y, type_, click=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.button_color = COLOR_BLUE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = FONT
        self.type_ = type_
        self.option = None      # 按钮选项值
        self.click = click      # 按钮执行函数

        self.text_surface = self.font.render(generator_types[self.type_], True, COLOR_BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center       # 文字居中

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)


class Checkbutton(Button):
    """选项按钮"""
    def __init__(self, screen, width, height, x, y, type_, father):
        super().__init__(screen, width, height, x, y, type_)
        self.button_color = COLOR_GREY
        self.font = checkbutton_font
        self.text_surface = self.font.render(generator_types[self.type_], True, COLOR_BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center       # 文字居中
        self.father = father
        self.type_ = type_

    def check(self):
        self.father.option = self.type_
        self.text_surface = self.font.render(generator_types[self.type_], True, COLOR_RED)
        self.draw()

    def uncheck(self):
        self.text_surface = self.font.render(generator_types[self.type_], True, COLOR_BLACK)
        self.draw()


def check_buttons(mouse_x, mouse_y):
    """分配不同按钮对应操作"""
    for button in major_buttons:
        if button.rect.collidepoint(mouse_x, mouse_y):
            button.click()
    for generate_checkbutton in generate_checkbuttons:
        if generate_checkbutton.rect.collidepoint(mouse_x, mouse_y):
            generate_checkbutton.check()
            for generate_other in generate_checkbuttons:
                if generate_other != generate_checkbutton:
                    generate_other.uncheck()
            break
    for solve_checkbutton in solve_checkbuttons:
        if solve_checkbutton.rect.collidepoint(mouse_x, mouse_y):
            solve_checkbutton.check()
            for solve_other in solve_checkbuttons:
                if solve_other != solve_checkbutton:
                    solve_other.uncheck()
            break
    pygame.display.update()


def restart():
    """重新初始化并创建迷宫"""
    global maze, SOLVE_THREAD, start, end
    SCREEN.fill(COLOR_WHITE, pygame.Rect(0, HEADER, WIDTH, HEIGHT-HEADER))
    # 停止当前线程，以便重新开始
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    # 重新随机设置迷宫大小
    size = random_maze_size()
    maze = maze_generator.Maze(size, size)
    # 设置迷宫入口为左上角，出口为右下角
    start = (0, 1)
    end = (size-1, size-2)
    # 以线程方式运行，以便拖动程序窗口、中途终止创建迷宫等操作可以正常执行
    if start_button.option == MAZE_TYPE.RECURSIVE_BACKTRACKER:
        SOLVE_THREAD = threading.Thread(target=maze_generator.RecursiveBacktracker, args=(maze, start, end))
    elif start_button.option == MAZE_TYPE.RANDOM_PRIM:
        SOLVE_THREAD = threading.Thread(target=maze_generator.RandomPrim, args=(maze, start, end))
    elif start_button.option == MAZE_TYPE.RECURSIVE_DIVISION:
        SOLVE_THREAD = threading.Thread(target=maze_generator.doRecursiveDivision, args=(maze, start, end))
    elif start_button.option == MAZE_TYPE.UNION_FIND_SET:
        SOLVE_THREAD = threading.Thread(target=maze_generator.doUnionFindSet, args=(maze, start, end))
    SOLVE_THREAD.start()


def solve():
    """寻找迷宫通路"""
    global maze, SOLVE_THREAD, start, end
    # 停止当前线程，以便重新开始
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    # 重置迷宫探索状态（将已走和死路重设为通路），以便对同一迷宫可以尝试不同走迷宫方法
    maze_solver.reset_maze_status(maze.matrix)
    maze_generator.draw_maze(maze.matrix, start)

    # 以线程方式运行，以便拖动程序窗口、中途终止创建迷宫等操作可以正常执行
    if solve_button.option == MAZE_TYPE.RECURSIVE:
        SOLVE_THREAD = threading.Thread(target=maze_solver.Recursive, args=(maze.matrix, start, end))
    elif solve_button.option == MAZE_TYPE.DFS:
        SOLVE_THREAD = threading.Thread(target=maze_solver.DFS, args=(maze.matrix, start, end))
    elif solve_button.option == MAZE_TYPE.BFS:
        SOLVE_THREAD = threading.Thread(target=maze_solver.BFS, args=(maze.matrix, start, end))
    elif solve_button.option == MAZE_TYPE.ASTAR:
        # 创建AStar对象,并设置起点、终点
        aStar = ast.AStar(maze, ast.Point(*start), ast.Point(*end))
        SOLVE_THREAD = threading.Thread(target=aStar.run, args=(maze,))
    SOLVE_THREAD.start()


def random_maze_size():
    """随机设置迷宫大小（正方形，边长11~41个单元格）"""
    return random.randint(5, 20) * 2 + 1       # 迷宫宽度和高度必须为奇数


def draw_buttons():
    """绘制按钮"""
    major_buttons = []
    button_width = (WIDTH - BUTTON_MARGIN * 4)/2
    button_height = 26
    start_button = Button(SCREEN, button_width, button_height, 2, 2, MAZE_TYPE.GENERATE, restart)
    major_buttons.append(start_button)
    solve_button = Button(SCREEN, button_width, button_height, button_width+6, 2, MAZE_TYPE.SOLVE, solve)
    major_buttons.append(solve_button)

    generate_checkbuttons = []
    button_width = (WIDTH/2 - BUTTON_MARGIN * 3)/2
    Backtracker_button = Checkbutton(SCREEN, button_width, button_height, 2, button_height+4, MAZE_TYPE.RECURSIVE_BACKTRACKER, start_button)
    generate_checkbuttons.append(Backtracker_button)
    RandomPrim_button = Checkbutton(SCREEN, button_width, button_height, button_width+4, button_height+4, MAZE_TYPE.RANDOM_PRIM, start_button)
    generate_checkbuttons.append(RandomPrim_button)
    Division_button = Checkbutton(SCREEN, button_width, button_height, 2, button_height*2+6, MAZE_TYPE.RECURSIVE_DIVISION, start_button)
    generate_checkbuttons.append(Division_button)
    UnionFind_button = Checkbutton(SCREEN, button_width, button_height, button_width+4, button_height*2+6, MAZE_TYPE.UNION_FIND_SET, start_button)
    generate_checkbuttons.append(UnionFind_button)

    solve_checkbuttons = []
    Recursive_button = Checkbutton(SCREEN, button_width, button_height, button_width*2+8, button_height+4, MAZE_TYPE.RECURSIVE, solve_button)
    solve_checkbuttons.append(Recursive_button)
    DFS_button = Checkbutton(SCREEN, button_width, button_height, button_width*3+10, button_height+4, MAZE_TYPE.DFS, solve_button)
    solve_checkbuttons.append(DFS_button)
    Astar_button = Checkbutton(SCREEN, button_width, button_height, button_width*2+8, button_height*2+6, MAZE_TYPE.ASTAR, solve_button)
    solve_checkbuttons.append(Astar_button)
    BFS_button = Checkbutton(SCREEN, button_width, button_height, button_width*3+10, button_height*2+6, MAZE_TYPE.BFS, solve_button)
    solve_checkbuttons.append(BFS_button)

    SCREEN.fill(COLOR_WHITE)
    for button in major_buttons + generate_checkbuttons + solve_checkbuttons:
        button.draw()
    Backtracker_button.check()
    Recursive_button.check()

    return start_button, solve_button, major_buttons, generate_checkbuttons, solve_checkbuttons


if __name__ == '__main__':
    pygame.init()
    CLOCK.tick(FPS)
    FONT = pygame.font.Font(r".\fonts\msyh.ttf", 18)
    FONT.set_bold(True)
    checkbutton_font = pygame.font.Font(r".\fonts\msyh.ttf", 14)
    pygame.display.set_caption(TITLE)

    SOLVE_THREAD = None

    start_button, solve_button, major_buttons, generate_checkbuttons, solve_checkbuttons = draw_buttons()
    # 程序运行即自动生成迷宫
    restart()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_buttons(mouse_x, mouse_y)
