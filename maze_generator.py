"""用递归回溯算法生成迷宫"""
import time
from random import randint, choice
from enum import Enum
from general_config import *


class MazeCellType(Enum):
    """单元格类型"""
    PATH = 0
    WALL = 1
    WALKED = 2
    DEAD = 3


class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[0 for x in range(self.width)] for y in range(self.height)]

    def resetMaze(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMaze(x, y, value)

    def setMaze(self, x, y, maze_type):
        self.matrix[y][x] = maze_type.value

    def isVisited(self, x, y):
        # 一开始迷宫所有位置均设为墙（1），迷宫单元为墙（1）表示未访问，为路（0）表示已访问
        return self.matrix[y][x] != MazeCellType.WALL.value

    def isMovable(self, x, y):
        return self.matrix[y][x] != 1

    def isValid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def __str__(self):
        """打印迷宫"""
        s = ''
        for row in self.matrix:
            for cell in row:
                if cell == 0:
                    s += ' 0'
                elif cell == 1:
                    s += ' 1'
                else:
                    s += ' #'
            s += '\n'
        return s

    def __getitem__(self, item):
        """支持‘对象[x][y]’方式索引取值，x行y列"""
        return self.matrix[item]


def check_neighbors(maze, x, y, checklist):
    """检查相邻迷宫单元（上下左右）是否有未访问单元并处理"""
    # 将未访问的相邻迷宫单元（上下左右）加入列表
    directions = []
    if y > 0:
        if not maze.isVisited(2*x+1, 2*(y-1)+1):
            directions.append(Direction.UP)
    if y < (maze.height-1)//2 - 1:
        if not maze.isVisited(2*x+1, 2*(y+1)+1):
            directions.append(Direction.DOWN)
    if x > 0:
        if not maze.isVisited(2*(x-1)+1, 2*y+1):
            directions.append(Direction.LEFT)
    if x < (maze.width-1)//2 - 1:
        if not maze.isVisited(2*(x+1)+1, 2*y+1):
            directions.append(Direction.RIGHT)

    # 如果当前迷宫单元有未被访问过的相邻迷宫单元
    if len(directions):
        # 随机选择一个未访问的相邻迷宫单元
        direction = choice(directions)
        # 去掉当前迷宫单元与相邻迷宫单元之间的墙（设为路），标记相邻迷宫单元为路（表示已访问状态），并将它加入栈
        if direction == Direction.LEFT:
            maze.setMaze(2*(x-1)+1, 2*y+1, MazeCellType.PATH)
            maze.setMaze(2*x, 2*y+1, MazeCellType.PATH)
            checklist.append((x-1, y))
        elif direction == Direction.UP:
            maze.setMaze(2*x+1, 2*(y-1)+1, MazeCellType.PATH)
            maze.setMaze(2*x+1, 2*y, MazeCellType.PATH)
            checklist.append((x, y-1))
        elif direction == Direction.RIGHT:
            maze.setMaze(2*(x+1)+1, 2*y+1, MazeCellType.PATH)
            maze.setMaze(2*x+2, 2*y+1, MazeCellType.PATH)
            checklist.append((x+1, y))
        elif direction == Direction.DOWN:
            maze.setMaze(2*x+1, 2*(y+1)+1, MazeCellType.PATH)
            maze.setMaze(2*x+1, 2*y+2, MazeCellType.PATH)
            checklist.append((x, y+1))
        return False
    else:
        return True


def generate_maze_byRecursiveBacktracker(maze):
    """用递归回溯算法生成迷宫(不使用Pygame可视化)"""
    # 迷宫初始化，所有位置均设为墙（1）
    maze.resetMaze(MazeCellType.WALL)

    # 用(2*x+1, 2*y+1)来表示迷宫单元坐标, x取值范围从0到(maze.width-1)//2-1，y取值范围从0到(maze.height-1)//2-1
    # 随机选择一个迷宫单元作为起点，加入堆栈并设为路（标记为已访问）
    startx, starty = randint(0, (maze.width-1)//2-1), randint(0, (maze.height-1)//2-1)
    maze.setMaze(2*startx+1, 2*starty+1, MazeCellType.PATH)
    # print("start(%d, %d)" % (startx, starty))
    checklist = []
    checklist.append((startx, starty))

    # 当堆栈非空时，从栈顶获取一个迷宫单元（不用出栈），进行循环
    while len(checklist):
        cell = checklist[-1]
        all_visited = check_neighbors(maze, cell[0], cell[1], checklist)
        # 如果当前迷宫单元没有未访问的相邻迷宫单元，则出栈
        if all_visited:
            checklist.remove(cell)


def RecursiveBacktracker(maze, start, end):
    """用递归回溯算法生成迷宫(借助pygame可视化执行步骤)"""
    # 迷宫初始化，所有位置均设为墙（1）
    maze.resetMaze(MazeCellType.WALL)

    # 用(2*x+1, 2*y+1)来表示迷宫单元坐标, x取值范围从0到(maze.width-1)//2-1，y取值范围从0到(maze.height-1)//2-1
    # 随机选择一个迷宫单元作为起点，加入栈并设为路（标记为已访问）
    startx, starty = randint(0, (maze.width-1)//2-1), randint(0, (maze.height-1)//2-1)
    maze.setMaze(2*startx+1, 2*starty+1, MazeCellType.PATH)
    checklist = []
    checklist.append((startx, starty))

    # 当堆栈非空时，从栈顶获取一个迷宫单元（不用出栈），进行循环
    while len(checklist):
        cell = checklist[-1]
        # 绘制当前迷宫状态
        cur_pos = (2*cell[0]+1, 2*cell[1]+1)
        draw_maze(maze.matrix, cur_pos)
        time.sleep(GENERATE_STEP_TIME)

        all_visited = check_neighbors(maze, cell[0], cell[1], checklist)
        # 如果当前迷宫单元没有未访问的相邻迷宫单元，则出栈
        if all_visited:
            checklist.remove(cell)

    # 设置迷宫入口和出口
    maze.setMaze(start[0], start[1], MazeCellType.PATH)
    maze.setMaze(end[0], end[1], MazeCellType.PATH)
    draw_maze(maze.matrix, cur_pos)


def RandomPrim(maze, start, end):
    """用随机Prim算法生成迷宫(借助pygame可视化执行步骤)"""
    global cur_pos
    maze.resetMaze(MazeCellType.WALL)

    startx, starty = randint(0, (maze.width-1)//2-1), randint(0, (maze.height-1)//2-1)
    maze.setMaze(2*startx+1, 2*starty+1, MazeCellType.PATH)
    checklist = []
    checklist.append((startx, starty))

    while len(checklist):
        # 跟递归回溯算法唯一的差别是不从栈顶取数，而是从列表中随机取数
        cell = choice(checklist)

        cur_pos = (2*cell[0]+1, 2*cell[1]+1)
        draw_maze(maze.matrix, cur_pos)
        time.sleep(GENERATE_STEP_TIME)

        all_visited = check_neighbors(maze, cell[0], cell[1], checklist)
        if all_visited:
            checklist.remove(cell)

    maze.setMaze(start[0], start[1], MazeCellType.PATH)
    maze.setMaze(end[0], end[1], MazeCellType.PATH)
    draw_maze(maze.matrix, cur_pos)


def recursiveDivision(maze, x, y, width, height, wall):
    """用递归分割算法生成迷宫"""

    def getWallIndex(start, length):
        """ 随机获取偶数作为十字分割墙的行列 """
        assert length >= 3
        # start必须是奇数（迷宫单元行列），wall_index必须是偶数（墙单元行列）
        wall_index = randint(start + 1, start + length - 2)
        if wall_index % 2 == 1:
            wall_index -= 1
        return wall_index

    def generateHoles(maze, x, y, width, height, wall_x, wall_y):
        """在分割出的4个矩阵的相邻四条边上随机选择三条边来打通（每条边上去掉一个单元的墙）"""
        holes = []
        # 在十字墙的4条棱上随机选择4个位置
        hole_entrys = [(randint(x, wall_x - 1), wall_y), (randint(wall_x + 1, x + width - 1), wall_y), (wall_x, randint(y, wall_y - 1)), (wall_x, randint(wall_y + 1, y + height - 1))]
        # 与外层矩阵单元邻接的十字墙单元
        margin_entrys = [(x, wall_y), (x+width-1, wall_y), (wall_x, y), (wall_x, y + height-1)]
        # 与十字墙相交位置的外层矩阵单元
        adjacent_entrys = [(x-1, wall_y), (x+width, wall_y), (wall_x, y - 1), (wall_x, y + height)]

        # 当外层的矩阵和十字墙相邻的单元是连通的情况下，邻接的十字墙单元必须打通
        # 相应位置设为孔位（替代对应棱的随机位置），否则会导致迷宫不连通
        for i in range(4):
            adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
            if maze.isValid(adj_x, adj_y) and maze.isMovable(adj_x, adj_y):
                maze.setMaze(margin_entrys[i][0], margin_entrys[i][1], MazeCellType.PATH)
                # 绘图
                cur_pos = [margin_entrys[i][0], margin_entrys[i][1]]
                draw_maze(maze.matrix, cur_pos)
            else:
                holes.append(hole_entrys[i])
        # 去掉一个随机位置，并在其他随机位置打孔（4条棱上选3条棱打通）
        ignore_hole = randint(0, len(holes)-1)
        for i in range(0, len(holes)):
            if i != ignore_hole:
                maze.setMaze(holes[i][0], holes[i][1], MazeCellType.PATH)
                cur_pos = [holes[i][0], holes[i][1]]
                draw_maze(maze.matrix, cur_pos)

    # 判断矩阵是否能继续分割(长度或宽度>1)，不能直接返回
    if width <= 1 or height <= 1:
        return

    # 随机生成十字墙的行列（必须是偶数），并设为墙
    wall_x, wall_y = (getWallIndex(x, width), getWallIndex(y, height))
    for i in range(x, x+width):
        maze.setMaze(i, wall_y, wall)
    for i in range(y, y+height):
        maze.setMaze(wall_x, i, wall)
    # 绘图
    cur_pos = [wall_x, wall_y]
    draw_maze(maze.matrix, cur_pos)

    generateHoles(maze, x, y, width, height, wall_x, wall_y)
    time.sleep(GENERATE_STEP_TIME)

    # 如果能继续分割，对分割出的4个矩形进行递归操作
    recursiveDivision(maze, x, y, wall_x - x, wall_y - y, wall)
    recursiveDivision(maze, x, wall_y + 1, wall_x - x, y + height - wall_y - 1, wall)
    recursiveDivision(maze, wall_x + 1, y, x + width - wall_x - 1, wall_y - y, wall)
    recursiveDivision(maze, wall_x + 1, wall_y + 1, x + width - wall_x - 1, y + height - wall_y - 1, wall)
    draw_maze(maze.matrix, cur_pos)


def doRecursiveDivision(maze, start, end):
    """调用递归分割算法生成迷宫(借助pygame可视化执行步骤)"""
    # 设置最外围的四面墙
    for x in range(0, maze.width):
        maze.setMaze(x, 0, MazeCellType.WALL)
        maze.setMaze(x, maze.height-1, MazeCellType.WALL)
    for y in range(0, maze.height):
        maze.setMaze(0, y, MazeCellType.WALL)
        maze.setMaze(maze.width-1, y, MazeCellType.WALL)
    # 借助pygame绘图
    cur_pos = [None, None]
    draw_maze(maze.matrix, cur_pos)

    recursiveDivision(maze, 1, 1, maze.width - 2, maze.height - 2, MazeCellType.WALL)

    # 设置迷宫入口和出口
    maze.setMaze(start[0], start[1], MazeCellType.PATH)
    maze.setMaze(end[0], end[1], MazeCellType.PATH)
    draw_maze(maze.matrix, cur_pos)


def unionFindSet(maze, width, height):
    """生成树+并查集算法生成迷宫"""
    def findSet(parent, index):
        """返回迷宫单元所在树的根节点"""
        if index != parent[index]:
            return findSet(parent, parent[index])
        return parent[index]

    def getNodeIndex(x, y):
        """返回迷宫单元 (x, y) 的树节点index"""
        return x * height + y

    def unionSet(parent, index1, index2, weightlist):
        """合并两颗树"""
        root1 = findSet(parent, index1)
        root2 = findSet(parent, index2)
        if root1 == root2:
            return
        if root1 != root2:
            # take the high weight tree as the root,
            # make the whole tree balance to achieve everage search time O(logN)
            if weightlist[root1] > weightlist[root2]:
                parent[root2] = root1
                weightlist[root1] += weightlist[root2]
            else:
                parent[root1] = root2
                weightlist[root2] += weightlist[root2]

    def checkAdjacentPos(maze, x, y, width, height, parentlist, weightlist):
        """检查相邻迷宫单元"""
        directions = []
        node1 = getNodeIndex(x, y)
        root1 = findSet(parentlist, node1)
        # 检查当前迷宫单元和它的相邻迷宫单元，不属于同一棵树则加入列表
        if x > 0:
            root2 = findSet(parentlist, getNodeIndex(x-1, y))
            if root1 != root2:
                directions.append(Direction.LEFT)
        if y > 0:
            root2 = findSet(parentlist, getNodeIndex(x, y-1))
            if root1 != root2:
                directions.append(Direction.UP)
        if x < width - 1:
            root2 = findSet(parentlist, getNodeIndex(x+1, y))
            if root1 != root2:
                directions.append(Direction.RIGHT)
        if y < height - 1:
            root2 = findSet(parentlist, getNodeIndex(x, y+1))
            if root1 != root2:
                directions.append(Direction.DOWN)

        if len(directions):
            # 从列表中随机选择一个相邻迷宫单元，使用并查集方法合并成一颗树
            direction = choice(directions)
            if direction == Direction.LEFT:
                adj_x, adj_y = (x-1, y)
                maze.setMaze(2*x, 2*y+1, MazeCellType.PATH)
            elif direction == Direction.UP:
                adj_x, adj_y = (x, y-1)
                maze.setMaze(2*x+1, 2*y, MazeCellType.PATH)
            elif direction == Direction.RIGHT:
                adj_x, adj_y = (x+1, y)
                maze.setMaze(2*x+2, 2*y+1, MazeCellType.PATH)
            elif direction == Direction.DOWN:
                adj_x, adj_y = (x, y+1)
                maze.setMaze(2*x+1, 2*y+2, MazeCellType.PATH)
            node2 = getNodeIndex(adj_x, adj_y)
            unionSet(parentlist, node1, node2, weightlist)
            return True
        else:
            # 表示当前迷宫单元和相邻的迷宫单元都属于同一棵树，则从检查列表删除当前迷宫单元
            return False

    # 表示每个迷宫单元的父节点，初始化为迷宫单元自己，即单独的一棵树
    parentlist = [x*height+y for x in range(width) for y in range(height)]
    # 表示每个迷宫单元的权重，初始化为1，在合并子树时使用，保证生成树的平衡，防止生成树的高度过大
    weightlist = [1 for x in range(width) for y in range(height)]
    # 将每个迷宫单元都加入检查列表
    checklist = []
    for x in range(width):
        for y in range(height):
            checklist.append((x, y))
            # 设置所有单元为路
            maze.setMaze(2*x+1, 2*y+1, MazeCellType.PATH)

    # 算法主循环，当检查列表非空时，随机取出一个迷宫单元，检查当前迷宫单元和它的相邻迷宫单元
    while len(checklist):
        entry = choice(checklist)
        # 当前迷宫单元和相邻的迷宫单元都属于同一棵树，则从检查列表删除当前迷宫单元
        if not checkAdjacentPos(maze, entry[0], entry[1], width, height, parentlist, weightlist):
            checklist.remove(entry)
        # 绘图
        cur_pos = [None, None]
        draw_maze(maze.matrix, cur_pos)
        time.sleep(GENERATE_STEP_TIME)


def doUnionFindSet(maze, start, end):
    """调用生成树+并查集算法生成迷宫(借助pygame可视化执行步骤)"""
    # 初始化，全部单元设为墙
    maze.resetMaze(MazeCellType.WALL)
    # 绘图
    cur_pos = [None, None]
    draw_maze(maze.matrix, cur_pos)

    unionFindSet(maze, (maze.width-1)//2, (maze.height-1)//2)

    # 设置迷宫入口和出口
    maze.setMaze(start[0], start[1], MazeCellType.PATH)
    maze.setMaze(end[0], end[1], MazeCellType.PATH)
    draw_maze(maze.matrix, cur_pos)


def draw_rect(x, y, len, color):
    """绘制单元方块"""
    global SCREEN
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)


def draw_maze(matrix, cur_pos):
    """绘制迷宫所有方格单元"""
    global WIDTH, HEADER
    size = len(matrix)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2

    for y in range(size):
        for x in range(size):
            cell = matrix[y][x]
            color = COLOR_BLACK if cell == 1 else COLOR_RED if cell == 3 else COLOR_CYAN if cell == 2 else COLOR_WHITE
            if (x, y) == cur_pos:
                color = COLOR_GREEN
            draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
    pygame.display.flip()


if __name__ == "__main__":
    maze = Maze(13, 19)
    generate_maze_byRecursiveBacktracker(maze)
    print(maze)
    print(maze[1][2])
