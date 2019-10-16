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

    def atDestination(self, goal):
        if self.position != goal:
            return False
        return True

    def __eq__(self, other):
        if self.position == other.position:
            return True
        return False


def insert_node(open_list, node):
    if len(open_list) == 0:
        open_list.append(node)
    else:
        open_list.append(node)
        i=1
        while i < len(open_list) and open_list[i].f < open_list[i-1].f:
            temp=open_list[i]
            open_list[i]=open_list[i-1]
            open_list[i-1]=temp
            i+=1

def AStar_Search(Map):
    # starting position state
    start_state = State(Map.goal, None, Map.start, 0)

    # list of opened and closed points
    open_list = []
    closed_list = []
    path = []
    
    # add start to open list
    open_list.append(start_state)

    while len(open_list) > 0:
        #Get current node
        current_node = open_list[0]
        open_list.pop(0)
        closed_list.append(current_node)
        
        # current_index = 0
        # for index, item in enumerate(open_list):
        #     if item.f < current_node.f:
        #         current_node = item
        #         current_index = index

        # #Pop current node out of open list, add to closed list
        # open_list.pop(current_index)
        # closed_list.append(current_node)

        #Check if current node is goal
        if current_node.atDestination(Map.goal):
            #Back track
            parent = current_node.parent
            while parent.parent is not None:
                path.append(parent.position)
                parent = parent.parent
            return path[::-1]                       #return reversed path
        
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
                    if child.g < item.g:                #child is optimal
                        check = 0
                        open_list.pop(index)
                        insert_node(open_list, child)
                        continue
                    else:
                        check = 0
                        continue
            if check:
                insert_node(open_list, child)
                        
    #Can not find any path
    return path



class Node_Dijkstra:
    def __init__(self, parent = None, position = (int, int), distance = 100, state = False):
        #
        self.checked = state
        self.parent = parent
        self.position = position
        self.distance = distance

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
    unexplored_list.append(start_node)
    for i in range (len(Map._map)):
        for j in range (len(Map._map[i])):
            i_node = Node_Dijkstra(None, (i, j))
            if i_node.__eq__(start_node):
                continue
            unexplored_list.append(i_node)

    path = []
    #Loop until the unexplored set is empty
    while len(unexplored_list) > 0:
        #Look for the least distance
        current_node = unexplored_list[0]
        current_index = 0
        for index, item in enumerate(unexplored_list):
            if item.distance < current_node.distance:
                current_node = item
                current_index = index
    
        #Remove current node from the unexplored set
        current_node.checked = True
        unexplored_list.pop(current_index)
        explored_list.append(current_node)

        #Check if current Node is Goal
        if current_node.__eq__(goal_node):
            #Back track to get path
            parent = current_node.parent
            while parent.parent is not None:
                path.append(parent.position)
                parent = parent.parent
            return path[::-1]                       #return reversed path

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
            dist = current_node.distance + 1
            new_node = Node_Dijkstra(current_node, pos, dist)
            neighbors.append(new_node)

        #Check neighbor list
        for child in neighbors:
            #Check if is in explored list
            for i in explored_list:
                if child.__eq__(i):
                    continue
            
            #Check if distance is better
            for index, item in enumerate(unexplored_list):
                if item.__eq__(child):
                    if item.distance > child.distance:
                        unexplored_list.pop(index)
                        unexplored_list.append(child)
    
    #Can not find any path
    return path

if __name__ == '__main__':
    Map1 = Map(5, 5, (0, 0), (4, 4))
    Map1.addObstacle([(4,0),(3,1),(2,2),(1,3),(0,4)])
    path = []
    path = Dijkstra_Search(Map1)
    Map1.addPath(path)
    plt.imshow(Map1._map)
    plt.show()