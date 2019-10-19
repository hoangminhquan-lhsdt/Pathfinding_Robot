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
            # Check out of Map
            if pos[0] < 0 or pos[0] > (len(Map._map) - 1) or pos[1] < 0 or pos[1] > (len(Map._map[0]) - 1):
                continue
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
    # Check if current Node is Goal
    if Map.isBlocked(current_node.position[0], current_node.position[1]):
        return []
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
            # Check out of Map
            if pos[0] < 0 or pos[0] > (len(Map._map) - 1) or pos[1] < 0 or pos[1] > (len(Map._map[0]) - 1):
                continue
            new_node = State(goal_node.position, current_node, pos, 0)
            if new_node not in checked_List:
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
            # Check out of Map
            if pos[0] < 0 or pos[0] > (len(Map._map) - 1) or pos[1] < 0 or pos[1] > (len(Map._map[0]) - 1):
                continue
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
        obstacle_points.append([int(obstacle_list[i]), int(obstacle_list[i+1])])
        i += 2
    new_map.addObstacle(obstacle_points)

    # Get list of pickup points
    pickup_list = file_content[6].split(' ')
    pickup_points = []
    i = 0
    while i < pickup_list.__len__()-1:
        # Add each pair of x y values to list
        pickup_points.append([int(pickup_list[i]), int(pickup_list[i+1])])
        i += 2
    new_map.addPickupPoint(pickup_points)

    return new_map

def Func(func):
    # Map1 = Map(10, 10, (0, 0), (9, 9))
    # for i in range(1, 9):
    #     Map1.addObstacle([(i, i)])
    # Map1.addPickupPoint([(9, 8), (7, 9)])
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
    fig.canvas.draw()
    ax.clear()
    plt.imshow(Map1._map)
    fig.canvas.draw()
    time.sleep(1)
    for i in range(len(Points) - 1):
        check_list = []
        if Points[i + 1] != goal:
            check_list.append(goal)
        path = func(Points[i], Points[i+1], Map1, check_list)
        for j in range(len(path)):
            Map1.deStartAndPickup([Points[i]])
            Map1.addPath([path[j]])
            plt.imshow(Map1._map)
            fig.canvas.draw()
            ax.clear()
            Map1.dePath([path[j]])

if __name__ == '__main__':
    root=tk.Tk()
    root.title("Menu")
    root.configure(background = "blue")

    def Greedy():
        Func(Greedy_BFS_Search)
    def Astar():
        Func(AStar_Search)
    def Dijkstra():
        Func(Dijkstra_Search)

    tk.Label(root, width = 20, text = "Choose an algorithm", bg = "yellow").grid(row = 0, column = 0)
    tk.Button(root, width = 20, text="Greedy Search",command=Greedy) .grid(row = 1, column = 0)
    tk.Button(root, width = 20, text="Astar Search",command=Astar) .grid(row = 2, column = 0)
    tk.Button(root, width = 20, text="Dijkstra Search",command=Dijkstra) .grid(row = 3, column = 0)

    def close_window():
        root.destroy()
        return 1

    tk.Label(root, width = 20, text = "Click to exit", bg = "yellow").grid(row = 0, column = 1)
    tk.Button(root, width = 5, text = "Exit", command = close_window, bg = "red").grid(row = 1, column = 1)

    root.mainloop()