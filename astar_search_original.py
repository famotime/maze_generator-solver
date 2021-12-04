class Maze:
    """
        说明：
            1.构造方法需要两个参数，即二维数组的宽和高
            2.成员变量w和h是二维数组的宽和高
            3.使用：‘对象[x][y]’可以直接取到相应的值
            4.数组的默认值都是0
    """

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.matrix = []
        self.matrix = [[0 for x in range(w)] for y in range(h)]

    def showMaze(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.matrix[y][x], end=' ')
            print("")

    def __getitem__(self, item):
        return self.matrix[item]


class Point:
    """
    表示一个点
    """

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
    """
    AStar算法的Python3实现
    """

    class Node:  # 描述AStar算法中的节点数据
        def __init__(self, point, endPoint, g=0):
            self.point = point  # 自己的坐标
            self.father = None  # 父节点
            self.g = g  # g值，g值在用到的时候会重新算
            self.h = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y)) * 10    # 计算h值

    def __init__(self, map2d, startPoint, endPoint, passTag=0):
        """
        构造AStar算法的启动条件
        :param map2d: Maze类型的寻路数组
        :param startPoint: Point或二元组类型的寻路起点
        :param endPoint: Point或二元组类型的寻路终点
        :param passTag: int类型的可行走标记（默认为0，表示可走）
        """
        self.openList = []
        self.closeList = []

        self.map2d = map2d
        # 起点、终点
        if isinstance(startPoint, Point) and isinstance(endPoint, Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)

        # 可行走标记
        self.passTag = passTag

    def getMinNode(self):
        """获得openlist中F值最小的节点"""
        currentNode = self.openList[0]
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self, point):
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def pointInOpenList(self, point):
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInOpenList(self):
        for node in self.openList:
            if node.point == self.endPoint:
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY):
        """ 搜索节点周围的点 """
        # 越界检测
        if minF.point.x + offsetX < 0 or minF.point.x + offsetX > self.map2d.w - 1 or minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.map2d.h - 1:
            return
        # 如果是障碍，就忽略
        if self.map2d[minF.point.y + offsetY][minF.point.x + offsetX] != self.passTag:
            return
        # 如果在关闭表中，就忽略
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY)
        if self.pointInCloseList(currentPoint):
            return
        # 设置单位花费
        if offsetX == 0 or offsetY == 0:
            step = 10
        else:
            step = 14
        # 如果不在openList中，就把它加入openlist
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = AStar.Node(currentPoint, self.endPoint, g=minF.g + step)
            currentNode.father = minF
            self.openList.append(currentNode)
            return
        # 如果在openList中，判断minF到当前点的G是否更小
        if minF.g + step < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
            currentNode.g = minF.g + step
            currentNode.father = minF

    def run(self):
        """
        开始寻路
        :return: None或Point列表（路径）
        """
        # 判断寻路终点是否是障碍
        if self.map2d[self.endPoint.y][self.endPoint.x] != self.passTag:
            return None

        # 1.将起点放入开启列表
        startNode = AStar.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        # 2.主循环逻辑
        while True:
            # 找到F值最小的点
            minF = self.getMinNode()
            # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)
            # 判断这个节点的上下左右节点
            self.searchNear(minF, 0, -1)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF, -1, 0)
            self.searchNear(minF, 1, 0)
            # 判断是否终止
            point = self.endPointInOpenList()
            if point:  # 如果终点在关闭表中，就返回结果
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        return list(reversed(pathList))
            if len(self.openList) == 0:
                return None


if __name__ == '__main__':
    # 创建一个10*15的地图
    map2d = Maze(10, 15)
    # 设置障碍
    map2d[4][0] = 1
    map2d[4][1] = 1
    map2d[4][2] = 1
    map2d[4][3] = 1
    map2d[4][4] = 1
    map2d[4][5] = 1
    map2d[4][6] = 1
    # 显示地图当前样子
    map2d.showMaze()
    # 创建AStar对象,并设置起点为0,0终点为9,14
    aStar = AStar(map2d, Point(0, 0), Point(9, 14))
    # 开始寻路
    pathList = aStar.run()
    # 遍历路径点,在map2d上以'#'显示
    for point in pathList:
        map2d[point.y][point.x] = '#'
    print("----------------------")
    # 再次显示地图
    map2d.showMaze()
