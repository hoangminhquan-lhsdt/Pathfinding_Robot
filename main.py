import matplotlib.pyplot as plt
import time
from Map import Map
import math
import tkinter as tk
import os


class State:
    def __init__(self, goal, parent=None, position=(int, int), g=100):
        # init unopened state
        self.checked = False
        self.parent = parent

        # current coordinates
        self.position = position

        # heuristic values
        self.g = g
        self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] - goal[1])
        self.f = self.g + self.h

    def __eq__(self, other):
        return (self.position == other.position)


def insert_node(open_list, node):
    if len(open_list) == 0:
        open_list.append(node)
    else:
        open_list.append(node)
        i = len(open_list) - 1
        while i > 0 and open_list[i].f < open_list[i-1].f:
            temp = open_list[i]
            open_list[i] = open_list[i-1]
            open_list[i-1] = temp
            i -= 1


def AStar_Search(Start, Goal, Map, checked_list):
    if Map.isBlocked(Start[0], Start[1]):
        return []

    # Start node, Goal node
    start_state = State(Goal, None, Start, 0)
    goal_state = State(Goal, None, Goal, 0)

    # list of opened and closed points
    open_list = []
    closed_list = []

    # add start to open list
    open_list.append(start_state)

    while len(open_list) > 0:
        # Get current node
        current_node = open_list[0]
        open_list.pop(0)
        closed_list.append(current_node)

        # Check if current node is goal
        if current_node == goal_state:
            # Back track to get path
            parent = current_node.parent
            if parent is None:
                return []
            else:
                path = []
                path.append(goal_state.position)
                while parent != start_state:
                    path.append(parent.position)
                    parent = parent.parent
                return path[::-1]

        # Check if is neighbors of current node, append it to a list
        neighbors_index = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for i in neighbors_index:
            pos = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            # Check walkable
            if Map.isBlocked(pos[0], pos[1]):
                continue
            if pos not in checked_list:
                new_node = State(Goal, current_node, pos, current_node.g + 1)
                neighbors.append(new_node)

        # Check neighbor list
        for child in neighbors:
            # Check if is in closed list
            check = 1  # still can be add to open list
            for i in closed_list:
                if child.__eq__(i):
                    check = 0
                    continue
            # Check if child is in open list
            for index, item in enumerate(open_list):
                if item.__eq__(child):
                    check = 0
                    if child.f < item.f:  # child is optimal
                        open_list.pop(index)
                        insert_node(open_list, child)
                        continue
                    else:
                        continue
            if check:
                insert_node(open_list, child)
    # can not find any path
    return []


def Greedy_BFS_Recursive(checked_List, start_node, current_node, goal_node, Map):
    if Map.isBlocked(start_node.position[0], start_node.position[1]):
        return []
    # Check if current Node is Goal
    # if Map.isBlocked(current_node.position[0], current_node.position[1]):
    #     return []
    elif current_node == goal_node:
        parent = current_node.parent
        path = [goal_node.position]
        while parent != start_node:
            path.append(parent.position)
            parent = parent.parent
        return path
    else:
        checked_List.append(current_node)
        # Check if is neighbors of current node, append it to a list
        neighbors_index = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for i in neighbors_index:
            pos = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            #     continue
            new_node = State(goal_node.position, current_node, pos, 0)
            if new_node not in checked_List and (not Map.isBlocked(pos[0], pos[1])):
                insert_node(neighbors, new_node)
        # Check neighbor list
        for i in neighbors:
            path = Greedy_BFS_Recursive(checked_List, start_node, i, goal_node, Map)
            if path != []:
                return path
        return []


def Greedy_BFS_Search(Start, Goal, Map, checked_List=[]):
    checkedList = []
    for i in checked_List:
        checkedList.append(State(Goal, None, i, 0))
    start_state = State(Goal, None, Start, 0)
    goal_state = State(Goal, None, Goal, 0)
    path = Greedy_BFS_Recursive(checkedList, start_state, start_state, goal_state, Map)
    if path != []:
        checked_List.append(path[len(path) - 1])
        return path[::-1]
    return []


class Node_Dijkstra:
    def __init__(self, parent=None, position=(int, int), distance=1000):
        #
        self.parent = parent
        self.position = position
        self.f = distance

    def __eq__(self, other):
        return (self.position == other.position)


def Dijkstra_Search(Start, Goal, Map, checked_list):
    if Map.isBlocked(Start[0], Start[1]):
        return []
    
    # Create Start and Goal Node
    start_node = Node_Dijkstra(None, Start, 0)
    goal_node = Node_Dijkstra(None, Goal)

    # Create a List of unexplored node
    unexplored_list = []
    explored_list = []

    # Set all node to unexplored
    for i in range(len(Map._map)):
        for j in range(len(Map._map[i])):
            i_node = Node_Dijkstra(None, (i, j))
            if Map.isBlocked(i, j):
                continue
            insert_node(unexplored_list, i_node)
    for index, item in enumerate(unexplored_list):
        if item == start_node:
            unexplored_list.pop(index)
            break
    insert_node(unexplored_list, start_node)

    # Loop until the unexplored set is empty
    while len(unexplored_list) > 0:
        current_node = unexplored_list[0]

        # Remove current node from the unexplored set
        unexplored_list.pop(0)
        explored_list.append(current_node)

        # Check if current Node is Goal
        if current_node == goal_node:
            # Back track to get path
            parent = current_node.parent
            if parent is None:
                return []
            else:
                path = []
                path.append(goal_node.position)
                while parent != start_node:
                    path.append(parent.position)
                    parent = parent.parent
                return path[::-1]

        # Check if neighbors of current node, append it to a list
        neighbors_index = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for i in neighbors_index:
            pos = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            # Check walkable
            if Map.isBlocked(pos[0], pos[1]):
                continue
            if pos not in checked_list:
                dist = current_node.f + 1
                new_node = Node_Dijkstra(current_node, pos, dist)
                neighbors.append(new_node)

        # Check neighbor list
        for child in neighbors:
            # Check if is in explored list
            for i in explored_list:
                if child == i:
                    continue

            # Check if distance is better
            for index, item in enumerate(unexplored_list):
                if item == child:
                    if item.f > child.f:
                        unexplored_list.pop(index)
                        insert_node(unexplored_list, child)
    # Can not find any path
    return []

def Read_Map():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Open and read file content by line
    f = open(current_dir + '/map.txt', 'r')
    file_content = f.readlines()
    f.close()

    # Get number of rows and columns
    row, col = int(file_content[0].split(' ')[0]), int(file_content[0].split(' ')[1])
    # Get start and goal positions
    start = int(file_content[1].split(' ')[0]), int(file_content[1].split(' ')[1])
    goal = int(file_content[2].split(' ')[0]), int(file_content[2].split(' ')[1])
    # Initialize new map
    new_map = Map(row, col, start, goal)

    # Get list of obstacle points
    obstacle_list = file_content[4].split(' ')
    obstacle_points = []
    i = 0
    while i < obstacle_list.__len__()-1:
        # Add each pair of x y values to list
        obstacle_points.append((int(obstacle_list[i]), int(obstacle_list[i+1])))
        i += 2
    new_map.addObstacle(obstacle_points)

    # Get list of pickup points
    pickup_list = file_content[6].split(' ')
    pickup_points = []
    i = 0
    while i < pickup_list.__len__()-1:
        # Add each pair of x y values to list
        pickup_points.append((int(pickup_list[i]), int(pickup_list[i+1])))
        i += 2
    new_map.addPickupPoint(pickup_points)
    return new_map

def Func(func, text):
    # Map1 = Map(10, 10, (1, 1), (8, 8))
    # # for i in range(2, 8):
    # #     Map1.addObstacle([(i, i)])
    # Map1.addPickupPoint([(2, 2), (4, 5), (7, 8)])
    # start, goal = Map1.start, Map1.goal
    # pickUpPoint, Points = [], []
    # Points.append(start)
    # pickUpPoint = list.copy(Map1.pickupPoints)

    Map1 = Read_Map()
    pickUpPoint, Points = [], []
    start, goal = Map1.start, Map1.goal
    Points.append(start)
    pickUpPoint = list.copy(Map1.pickupPoints)

    while len(pickUpPoint) > 0:
        index_min = 0
        min = abs(pickUpPoint[0][0] - start[0]) + abs(pickUpPoint[0][1] - start[1])
        for i in range(1, len(pickUpPoint)):
            if (abs(pickUpPoint[i][0] - start[0]) + abs(pickUpPoint[i][1] - start[1])) < min:
                min = abs(pickUpPoint[i][0] - start[0]) + abs(pickUpPoint[i][1] - start[1])
                index_min = i
        start = pickUpPoint.pop(index_min)
        Points.append(start)

    Points.append(goal)
    path = []
    fig, ax = plt.subplots(figsize = (10, 5))
    fig.show()
    plt.imshow(Map1._map)
    fig.canvas.draw()
    fig.canvas.draw()
    time.sleep(0.1)
    for i in range(len(Points) - 1):
        check_list = []
        if Points[i + 1] != goal:
            check_list.append(goal)
        path = func(Points[i], Points[i+1], Map1, check_list)
        if path == []:
            time.sleep(1)
            break
        for j in range(len(path)):
            Map1.deStartAndPickup([Points[i]])
            Map1.addPath([path[j]])
            plt.imshow(Map1._map)
            fig.canvas.draw()
            time.sleep(0.5)
            ax.clear()
            Map1.dePath([path[j]])

if __name__ == '__main__':
    file_name = ""
    root=tk.Tk()
    root.title('Menu')
    menu = tk.Menu(root)
    root.config(background = 'blue', menu = menu)

    GreedyMenu = tk.Menu(menu)
    def Greedy1():
        Func(Greedy_BFS_Search, "map1.txt")
    def Greedy2():
        Func(Greedy_BFS_Search, "map2.txt")
    def Greedy3():
        Func(Greedy_BFS_Search, "map3.txt")
    menu.add_cascade(label='Greedy', menu = GreedyMenu)
    GreedyMenu.add_command(label='Map 1', command = Greedy1)
    GreedyMenu.add_command(label='Map 2', command = Greedy2)
    GreedyMenu.add_command(label='Map 3', command = Greedy3)
    
    def Astar1():
        Func(AStar_Search, "map1.txt")
    def Astar2():
        Func(AStar_Search, "map2.txt")
    def Astar3():
        Func(AStar_Search, "map3.txt")
    AstarMenu = tk.Menu(menu)
    menu.add_cascade(label='Astar', menu = AstarMenu, )
    AstarMenu.add_command(label='Map 1', command = Astar1)
    AstarMenu.add_command(label='Map 2', command = Astar2)
    AstarMenu.add_command(label='Map 3', command = Astar3)

    def Dijkstra1():
        Func(Dijkstra_Search, "map1.txt")
    def Dijkstra2():
        Func(Dijkstra_Search, "map2.txt")
    def Dijkstra3():
        Func(Dijkstra_Search, "map3.txt")
    DijkstraMenu = tk.Menu(menu)
    menu.add_cascade(label='Dijkstra', menu = DijkstraMenu)
    DijkstraMenu.add_command(label='Map 1', command = Dijkstra1)
    DijkstraMenu.add_command(label='Map 2', command = Dijkstra2)
    DijkstraMenu.add_command(label='Map 3', command = Dijkstra3)

    root.mainloop()