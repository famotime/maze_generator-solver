import time
import queue
import maze_generator
from general_config import *


def valid(matrix, x, y):
    """返回可通行单元：越界、墙、死路不可通行"""
    if x < 0 or y < 0:
        return False
    if x >= len(matrix) or y >= len(matrix):
        return False
    val = matrix[y][x]
    if val == maze_generator.MazeCellType.WALL.value or val == maze_generator.MazeCellType.DEAD.value:
        return False
    return val, x, y


def neighbors(matrix, pos):
    """返回可走的邻居单元"""
    x, y = pos
    t, r, d, l = valid(matrix, x, y - 1), valid(matrix, x + 1, y), valid(matrix, x, y + 1), valid(matrix, x - 1, y)
    return t, r, d, l


def mark_walked(matrix, pos):
    """标记已走单元"""
    matrix[pos[1]][pos[0]] = maze_generator.MazeCellType.WALKED.value


def mark_dead(matrix, pos):
    """标记死路单元"""
    matrix[pos[1]][pos[0]] = maze_generator.MazeCellType.DEAD.value


def suggest_pos(cells):
    """返回下一步要走的单元"""
    target_pos = False
    for cell in cells:
        if cell:
            # 如果是未走过的路，直接返回推荐
            if cell[0] == maze_generator.MazeCellType.PATH.value:
                return cell
            # 如果是已走过的路，则待定
            elif cell[0] == maze_generator.MazeCellType.WALKED.value:
                target_pos = cell
    # 如果没有未走单元，再走已走过单元
    return target_pos


def reset_maze_status(matrix):
    """重置迷宫探索状态（将已走和死路重设为通路）"""
    size = len(matrix)
    for x in range(size):
        for y in range(size):
            if matrix[y][x] == maze_generator.MazeCellType.WALKED.value or matrix[y][x] == maze_generator.MazeCellType.DEAD.value:
                matrix[y][x] = maze_generator.MazeCellType.PATH.value


def Recursive(matrix, pos, end):
    """递归调用探索迷宫"""
    time.sleep(SOLVE_STEP_TIME)
    # 当前位置与出口位置重叠，说明已到达出口
    if pos[0] == end[0] and pos[1] == end[1]:
        mark_walked(matrix, pos)
        return True
    # 获取相邻4个位置，并计算下一步
    t, r, d, l = neighbors(matrix, pos)
    next_pos = suggest_pos((t, r, d, l))
    if next_pos:
        # 如果下一步是走过的路，把当前位置标记为死胡同，此路不通
        if next_pos[0] == maze_generator.MazeCellType.WALKED.value:
            mark_dead(matrix, pos)
        # 如果是没走过的路，把当前的位置标记为已走过
        else:
            mark_walked(matrix, pos)
        # 绘图
        maze_generator.draw_maze(matrix, (next_pos[1], next_pos[2]))
        # 递归调用Recursive方法，位置参数改为下一步的位置
        Recursive(matrix, (next_pos[1], next_pos[2]), end)
    # 如果没有推荐的路，游戏结束，迷宫无解
    else:
        mark_dead(matrix, pos)
        maze_generator.draw_maze(matrix, next_pos)
        return False


class Point:
    """ 表示一个点，包含行列坐标 """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.father = None

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)


def draw_solution(matrix, path):
    """绘制迷宫探索结果路径"""
    size = len(matrix)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2
    for pos in path:
        x = pos.x
        y = pos.y
        color = COLOR_GREEN
        maze_generator.draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
        pygame.display.flip()
        time.sleep(0.01)


def DFS(matrix, start, end):
    """调用栈探索迷宫（深度优先）"""
    # 当前位置与出口位置重叠，说明已到达出口
    if start[0] == end[0] and start[1] == end[1]:
        return True

    stack = []
    stack.append(Point(*start))
    while len(stack):
        pos = stack.pop()
        # 把可通行的邻居单元（非墙、非死路、非走过）加入栈，并更新其父亲为当前单元
        for cell in neighbors(matrix, (pos.x, pos.y)):
            if cell and cell[0] == maze_generator.MazeCellType.PATH.value:
                next_pos = Point(cell[1], cell[2])
                next_pos.father = pos
                # 如果邻居单元就是出口，则按父亲属性反向汇总路线并绘图
                if next_pos.x == end[0] and next_pos.y == end[1]:
                    path = []
                    path.append(Point(*end))
                    while next_pos.father:
                        path.append(next_pos)
                        next_pos = next_pos.father
                    path.append(Point(*start))
                    draw_solution(matrix, path)
                    return True
                else:
                    stack.append(next_pos)
        # 标记当前单元为走过并绘制最新状态
        mark_walked(matrix, (pos.x, pos.y))
        maze_generator.draw_maze(matrix, (pos.x, pos.y))
        time.sleep(SOLVE_STEP_TIME)
    return False


def BFS(matrix, start, end):
    """调用队列探索迷宫（广度优先）"""
    # 当前位置与出口位置重叠，说明已到达出口
    if start[0] == end[0] and start[1] == end[1]:
        return True

    q = queue.Queue()
    q.put(Point(*start))
    while not q.empty():
        pos = q.get()
        # 把可通行的邻居单元（非墙、非死路、非走过）加入队列，并更新其父亲为当前单元
        for cell in neighbors(matrix, (pos.x, pos.y)):
            if cell and cell[0] == maze_generator.MazeCellType.PATH.value:
                next_pos = Point(cell[1], cell[2])
                next_pos.father = pos
                # 如果邻居单元就是出口，则按父亲属性反向汇总路线并绘图
                if next_pos.x == end[0] and next_pos.y == end[1]:
                    mark_walked(matrix, (pos.x, pos.y))
                    maze_generator.draw_maze(matrix, (pos.x, pos.y))
                    path = []
                    path.append(Point(*end))
                    while next_pos.father:
                        path.append(next_pos)
                        next_pos = next_pos.father
                    path.append(Point(*start))
                    draw_solution(matrix, path)
                    return True
                else:
                    q.put(next_pos)
        # 标记当前单元为走过并绘制最新状态
        mark_walked(matrix, (pos.x, pos.y))
        maze_generator.draw_maze(matrix, (pos.x, pos.y))
        time.sleep(SOLVE_STEP_TIME)
    return False
