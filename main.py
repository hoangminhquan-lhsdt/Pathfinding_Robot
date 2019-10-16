import matplotlib.pyplot as plt
from Map import Map
import math

class State:
    def __init__(self, goal, parent = None, position = (int, int), g = 100):
        # init unopened state
        self.checked = False
        self.parent = parent

        # current coordinates
        self.position = position

        # heuristic values
        self.g = g
        self.h = abs(self.position[0] - goal[0]) + abs(self.position[1] + goal[1])
        self.f = self.g + self.h

    def __eq__(self, other):
        return (self.position == other.position)


def insert_node(open_list, node):
    if len(open_list) == 0:
        open_list.append(node)
    else:
        open_list.append(node)
        i= len(open_list) - 1
        while i > 0 and open_list[i].f < open_list[i-1].f:
            temp=open_list[i]
            open_list[i]=open_list[i-1]
            open_list[i-1]=temp
            i -= 1

def AStar_Search(Map):
    # Start node, Goal node
    start_state = State(Map.goal, None, Map.start, 0)
    goal_state = State(Map.goal, None, Map.goal, 0)

    # list of opened and closed points
    open_list = []
    closed_list = []
    
    # add start to open list
    open_list.append(start_state)

    while len(open_list) > 0:
        #Get current node
        current_node = open_list[0]
        open_list.pop(0)
        closed_list.append(current_node)

        #Check if current node is goal
        if current_node == goal_state:
            #Back track to get path
            parent = current_node.parent
            if parent is None:
                return []
            else:
                path = []
                while parent != start_state:
                    path.append(parent.position)
                    parent = parent.parent
                return path[::-1]
        
        #Check if is neighbors of current node, append it to a list
        neighbors_index = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for i in neighbors_index:
            pos = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            #Check out of Map
            if pos[0] < 0 or pos[0] > (len(Map._map) - 1) or pos[1] < 0 or pos[1] > (len(Map._map[0]) - 1):
                continue
            #Check walkable
            if Map.isBlocked(pos[0], pos[1]):
                continue
            new_node = State(Map.goal, current_node, pos, current_node.g + 1)
            neighbors.append(new_node)

        #Check neighbor list
        for child in neighbors:
            #Check if is in closed list
            check = 1                       #still can be add to open list
            for i in closed_list:
                if child.__eq__(i):
                    check = 0
                    continue
            #Check if child is in open list
            for index, item in enumerate(open_list):
                if item.__eq__(child):
                    check = 0
                    if child.g < item.g:                #child is optimal
                        open_list.pop(index)
                        insert_node(open_list, child)
                        continue
                    else:
                        continue
            if check:
                insert_node(open_list, child)
    
    #can not find any path
    return []



class Node_Dijkstra:
    def __init__(self, parent = None, position = (int, int), distance = 1000):
        #
        self.parent = parent
        self.position = position
        self.f = distance

    def __eq__(self, other):
        return (self.position == other.position)

def Dijkstra_Search(Map):
    #Create Start and Goal Node
    start_node = Node_Dijkstra(None, Map.start, 0)
    goal_node = Node_Dijkstra(None, Map.goal)

    #Create a List of unexplored node
    unexplored_list = []
    explored_list = []

    #Set all node to unexplored
    for i in range (len(Map._map)):
        for j in range (len(Map._map[i])):
            i_node = Node_Dijkstra(None, (i, j))
            if Map.isBlocked(i, j):
                continue
            insert_node(unexplored_list, i_node)
    for index, item in enumerate(unexplored_list):
        if item == start_node:
            unexplored_list.pop(index)
            break
    insert_node(unexplored_list, start_node)

    #Loop until the unexplored set is empty
    while len(unexplored_list) > 0:
        current_node = unexplored_list[0]
    
        #Remove current node from the unexplored set
        unexplored_list.pop(0)
        explored_list.append(current_node)

        #Check if current Node is Goal
        if current_node == goal_node:
            #Back track to get path
            parent = current_node.parent
            if parent is None:
                return []
            else:
                path = []
                while parent != start_node:
                    path.append(parent.position)
                    parent = parent.parent
                return path[::-1]

        #Check if neighbors of current node, append it to a list
        neighbors_index = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for i in neighbors_index:
            pos = (current_node.position[0] + i[0], current_node.position[1] + i[1])
            #Check out of Map
            if pos[0] < 0 or pos[0] > (len(Map._map) - 1) or pos[1] < 0 or pos[1] > (len(Map._map[0]) - 1):
                continue
            #Check walkable
            if Map.isBlocked(pos[0], pos[1]):
                continue
            dist = current_node.f + 1
            new_node = Node_Dijkstra(current_node, pos, dist)
            neighbors.append(new_node)

        #Check neighbor list
        for child in neighbors:
            #Check if is in explored list
            for i in explored_list:
                if child == i:
                    continue
            
            #Check if distance is better
            for index, item in enumerate(unexplored_list):
                if item == child:
                    if item.f > child.f:
                        unexplored_list.pop(index)
                        insert_node(unexplored_list, child)
    
    #Can not find any path
    return []

if __name__ == '__main__':
    # Map1 = Map(10, 20, (0, 0), (9, 19))
    Map1 = Map(5, 5, (0, 0), (4, 4))
    Map1.addObstacle([(4, 0),(3, 1),(2, 2),(1, 3), (0, 4)])
    # Map1.addObstacle([(0, 1),(1, 1),(2, 1),(9, 1),(4, 1), (5, 1),(6, 1),(7, 1),(8, 1)])
    # Map1.addObstacle([(2, 2),(2, 3),(2, 4),(2, 5)])
    # Map1.addObstacle([(1, 5),(2, 5),(4, 5),(5, 5),(6, 5),(7, 5),(8, 5), (3, 5)])
    # Map1.addObstacle([(1, 7),(2, 7),(3, 7),(4, 7),(5, 7),(1,8),(1,9),(2, 9),(3, 9),(4, 9),(5, 9), (5, 8)])
    # for i in range(1,8):
    #     if i % 2 == 0:
    #         for j in range(0,8):
    #             Map1.addObstacle([(j,i*2)])
    #     else:
    #         for j in range(1,9):
    #             Map1.addObstacle([(j,i*2)])
    # for i in range (9,15):
    #     for j in range(4,10):
    #         if i+j>18:
    #             Map1.addObstacle([(j,i)])
    # Map1.addObstacle([(9, 4)])

    path = []
    path = Dijkstra_Search(Map1)
    Map1.addPath(path)
    plt.imshow(Map1._map)
    plt.show()