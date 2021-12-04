import time
import maze_generator
from general_config import *


class Point:
    """ 表示一个点，包含行列坐标 """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __str__(self):
        return "x:"+str(self.x)+",y:"+str(self.y)


class AStar:
    """ AStar算法实现 """

    class Node:
        """描述AStar算法中的节点数据"""
        def __init__(self, point, endPoint, g=0):
            self.point = point  # 自己的坐标
            self.father = None  # 父节点
            self.g = g  # g值，g值在用到的时候会重新算
            self.h = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y)) * 10    # 计算h值

    def __init__(self, maze, startPoint, endPoint, passTag=0):
        """ 构造AStar算法的启动条件 """
        self.openList = []
        self.closeList = []
        self.maze = maze
        # 设置起点和终点（Point或二元组类型）
        if isinstance(startPoint, Point) and isinstance(endPoint, Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)
        # passTag: 通行标记（0表示可走）
        self.passTag = passTag

    def getMinNode(self):
        """获得openlist中F值最小的节点"""
        currentNode = self.openList[0]
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self, point):
        """检测点是否包含在closeList中"""
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def pointInOpenList(self, point):
        """检测点是否包含在openList中"""
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInOpenList(self):
        """检测终点是否在openList中(说明已找到路径)"""
        for node in self.openList:
            if node.point == self.endPoint:
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY):
        """ 搜索节点周围的点 """
        # 如果越界，就忽略
        if minF.point.x + offsetX < 0 or minF.point.x + offsetX > self.maze.width - 1 or minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.maze.height - 1:
            return
        # 如果是障碍，就忽略
        if self.maze[minF.point.y + offsetY][minF.point.x + offsetX] != self.passTag:
            return
        # 如果在closelist中，就忽略
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY)
        if self.pointInCloseList(currentPoint):
            return
        # 设置单位花费
        if offsetX == 0 or offsetY == 0:
            step = 10
        else:
            step = 14
        # 如果不在openList中，就把它加入openlist，并把当前方格设置为它的父亲
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = AStar.Node(currentPoint, self.endPoint, g=minF.g + step)
            currentNode.father = minF
            self.openList.append(currentNode)
            return
        # 如果已在openList中，判断当前minF到这个点的G值是否更小
        # 如果更小，就重新计算g值，并且改变father为当前节点
        if minF.g + step < currentNode.g:
            currentNode.g = minF.g + step
            currentNode.father = minF

    def draw_maze(self, maze):
        """绘制迷宫探索状态"""
        global WIDTH, HEADER
        size = len(maze.matrix)
        cell_size = int(WIDTH / size)
        cell_padding = (WIDTH - (cell_size * size)) / 2

        for node in self.openList:
            x = node.point.x
            y = node.point.y
            color = COLOR_GREEN
            maze_generator.draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
        for node in self.closeList:
            x = node.point.x
            y = node.point.y
            color = COLOR_CYAN
            maze_generator.draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
        pygame.display.flip()
        time.sleep(SOLVE_STEP_TIME)

    def draw_solution(self, maze, pathList):
        """绘制迷宫探索结果路径"""
        size = len(maze.matrix)
        cell_size = int(WIDTH / size)
        cell_padding = (WIDTH - (cell_size * size)) / 2

        for point in pathList:
            x = point.x
            y = point.y
            color = COLOR_GREEN
            maze_generator.draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
            pygame.display.flip()
            time.sleep(0.01)

    def run(self, maze):
        """ 开始寻路，返回None或Point列表（路径） """
        # 判断寻路终点是否是障碍
        if self.maze[self.endPoint.y][self.endPoint.x] != self.passTag:
            return None

        # 1.将起点放入openlist
        startNode = AStar.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        # 2.主循环逻辑
        while True:
            # 遍历openlist，查找F值最小的节点
            minF = self.getMinNode()
            # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)
            # 判断这个节点的上下左右节点并操作
            self.searchNear(minF, 0, -1)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF, -1, 0)
            self.searchNear(minF, 1, 0)
            # 绘制最新状态
            self.draw_maze(maze)

            # 如果终点在openList中，说明路径已经找到了，就返回路径结果
            point = self.endPointInOpenList()
            if point:
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        # 重绘openlist剩余单元格颜色，以免跟最终路径混淆
                        size = len(maze.matrix)
                        cell_size = int(WIDTH / size)
                        cell_padding = (WIDTH - (cell_size * size)) / 2
                        for node in self.openList:
                            x = node.point.x
                            y = node.point.y
                            color = COLOR_CYAN
                            maze_generator.draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
                        # 绘制最终探索路径
                        start = (0, 1)
                        pathList.append(Point(*start))
                        self.draw_solution(maze, pathList)
                        return list(reversed(pathList))
            # 如果openlist是空的，说明最终没有找到路径
            if len(self.openList) == 0:
                return None


if __name__ == '__main__':
    # 创建一个15*15的地图
    maze = maze_generator.Maze(15, 15)
    # 设置障碍
    maze[4][0] = 1
    maze[4][1] = 1
    maze[4][2] = 1
    maze[4][3] = 1
    maze[4][4] = 1
    maze[5][7] = 1
    maze[14][9] = 1
    print(maze)
    # 创建AStar对象,并设置起点、终点
    aStar = AStar(maze, Point(0, 0), Point(14, 14))
    # 开始寻路
    pathList = aStar.run(maze)
    # 遍历路径点,在maze上设为8
    for point in pathList:
        maze[point.y][point.x] = 8
    print("----------------------")
    # 再次显示地图
    print(maze)
