import random
import pygame
import sys
import heapq

WIDTH = 800
HEIGHT = 800
cell_size = 40
black = (0,0,0)
red = (255,0,0)
white = (255, 255, 255)
yellow = (255,255,0)
blue = (0,0,255)
pink = (255, 192, 203)
cells = []
stack = []
region = {}
twice = False
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def getIndex(i,j):
    if (0 <= i < int(HEIGHT / cell_size) and 0 <= j < int(WIDTH / cell_size)):
        return j + i * int(WIDTH / cell_size)
    else:
        return -1


class Node:
    def __init__(self, cell, parent):
        self.cell = cell
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return isinstance(other, Node) and (self.cell.row, self.cell.col) == (other.cell.row, other.cell.col)

    def __hash__(self):
        return hash((self.cell.row, self.cell.col))

    def __lt__(self, other):
        return self.f < other.f


def heuristic(cell, goal):
    x_1 = cell.col
    y_1 = cell.row
    x_2 = goal.col
    y_2 = goal.row
    return abs(x_1 - x_2) + abs(y_1 - y_2)

def distance(cell, neighbour):
    x_1 = cell.col
    y_1 = cell.row
    x_2 = neighbour.col
    y_2 = neighbour.row
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def getValidNeighbours(currentNode, nodeMap):
    validNeighbours = []
    neighbours = currentNode.cell.validNeighbours()

    for neighbour in neighbours:
        if (neighbour.row, neighbour.col) not in nodeMap:
            nodeMap[(neighbour.row, neighbour.col)] = Node(neighbour, None)

        validNeighbours.append(nodeMap[(neighbour.row, neighbour.col)])

    return validNeighbours

def pathFinder(start, goal, ghost):
    startNode = Node(start, None)
    goalNode = Node(goal, None)

    openList = []     # min-heap priority queue
    openSet = set()
    closedSet = set() # NEW: track visited nodes
    nodeMap = {}      # NEW: track all Node objects keyed by (row, col)

    startNode.g = 0
    startNode.h = heuristic(startNode.cell, goalNode.cell)
    if not ghost:
        startNode.f = startNode.g + startNode.h + (startNode.cell.danger * 5)
    if ghost:
        startNode.f = startNode.g + startNode.h

    heapq.heappush(openList, (startNode.f, startNode))
    openSet.add(startNode)
    nodeMap[(start.row, start.col)] = startNode  # add to dict

    while len(openList) > 0:
        value, current = heapq.heappop(openList)
        openSet.remove(current)

        if current == goalNode:
            return reconstruct_path(current)

        closedSet.add(current)

        for neighbor in getValidNeighbours(current, nodeMap):
            if neighbor in closedSet:
                continue

            tentative_g = current.g + distance(current.cell, neighbor.cell)

            if neighbor in openSet and tentative_g >= neighbor.g:
                continue

            neighbor.parent = current
            neighbor.g = tentative_g
            neighbor.h = heuristic(neighbor.cell, goalNode.cell)

            if not ghost:
                neighbor.f = neighbor.g + neighbor.h + (neighbor.cell.danger * 5)
            if ghost:
                neighbor.f = neighbor.g + neighbor.h

            if neighbor not in openSet:
                heapq.heappush(openList, (neighbor.f, neighbor))
                openSet.add(neighbor)



def reconstruct_path(current):
    path = []
    while current is not None:
        path.append(current.cell)
        current = current.parent

    return path


class Character:
    def __init__(self, i, j):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row
        self.target = cells[-1]
        self.path = []
        self.index = 0

    def draw(self):
        pygame.draw.circle(screen, yellow, (self.x + cell_size/2, self.y + cell_size/2), cell_size/2)

    def move(self, i , j):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row

    def chase(self):
        if self.path and self.index < len(self.path):
            next_cell = self.path[self.index]
            self.move(next_cell.row, next_cell.col)
            next_cell.checked = True
            self.index += 1


class Enemy:
    def __init__(self, i, j, color):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row
        self.target = cells[-1]
        self.color = color
        self.path = []
        self.index = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + cell_size/2, self.y + cell_size/2), cell_size/2)

    def move(self, i , j):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row


    def chase(self):
        if self.path and self.index < len(self.path):
            next_cell = self.path[self.index]
            self.move(next_cell.row, next_cell.col)
            self.index += 1


class Food:
    def __init__(self, i ,j):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row

    def draw(self):
        pygame.draw.circle(screen, pink, (self.x + cell_size/2, self.y + cell_size/2), cell_size/4)

    def move(self, i , j):
        self.row = i
        self.col = j
        self.x = cell_size * self.col
        self.y = cell_size * self.row


class Cell:
    def __init__(self, i, j):
        self.row = i
        self.col = j
        self.visited = False
        self.x = cell_size * self.col
        self.y = cell_size * self.row
        self.walls = [True, True, True, True] #top, right, bottom, left
        self.checked = False
        self.danger = 0

    def draw(self):
        if not self.checked:
            pygame.draw.circle(screen, yellow, (self.x + cell_size/2, self.y + cell_size/2), 3)
        if self.walls[0]:
            pygame.draw.line(screen, blue, (self.x,self.y), (self.x + cell_size, self.y), 3)
        if self.walls[1]:
            pygame.draw.line(screen, blue, (self.x + cell_size,self.y), (self.x+cell_size, self.y + cell_size), 3)
        if self.walls[2]:
            pygame.draw.line(screen, blue, (self.x,self.y + cell_size), (self.x+cell_size, self.y + cell_size), 3)
        if self.walls[3]:
            pygame.draw.line(screen, blue, (self.x,self.y), (self.x, self.y + cell_size), 3)

    def nextNeighbour(self):
        neighbours = []

        top = getIndex(self.row - 1, self.col)
        right = getIndex(self.row, self.col + 1)
        bottom = getIndex(self.row + 1, self.col)
        left = getIndex(self.row, self.col - 1)

        if (top != -1 and not cells[top].visited):
            neighbours.append(cells[top])
        if (right != -1 and not cells[right].visited):
            neighbours.append(cells[right])
        if (bottom != -1 and not cells[bottom].visited):
            neighbours.append(cells[bottom])
        if (left != -1 and not cells[left].visited):
            neighbours.append(cells[left])

        if len(neighbours) > 0:
            return random.choice(neighbours)
        else:
            return None

    def validNeighbours(self):
        neighbours = []

        top = getIndex(self.row - 1, self.col)
        right = getIndex(self.row, self.col + 1)
        bottom = getIndex(self.row + 1, self.col)
        left = getIndex(self.row, self.col - 1)

        if (top != -1 and not self.walls[0] and not cells[top].walls[2]):
            neighbours.append(cells[top])
        if (right != -1 and not self.walls[1] and not cells[right].walls[3]):
            neighbours.append(cells[right])
        if (bottom != -1 and not self.walls[2] and not cells[bottom].walls[0]):
            neighbours.append(cells[bottom])
        if (left != -1 and not self.walls[3] and not cells[left].walls[1]):
            neighbours.append(cells[left])

        return neighbours

    def __str__(self):
        return f"({self.row}, {self.col})"

    def __repr__(self):
        return self.__str__()




id = 1
for i in range(int(HEIGHT/cell_size)):
    for j in range(int(WIDTH/cell_size)):
        cells.append(Cell(i,j))
        region[(i,j)] = id
        id += 1

def removeWalls(cell, neighbour):
    row_dx = cell.row - neighbour.row
    col_dx = cell.col - neighbour.col

    if row_dx == 1:
        neighbour.walls[2] = False
        cell.walls[0] = False
        return True
    elif row_dx == -1:
        neighbour.walls[0] = False
        cell.walls[2] = False
        return True
    if col_dx == 1:
        cell.walls[3] = False
        neighbour.walls[1] = False
        return True
    elif col_dx == -1:
        cell.walls[1] = False
        neighbour.walls[3] = False
        return True

    return False

def generateMaze():
    current = cells[0]
    current.visited = True
    stack.append(current)

    while (len(stack) > 0):
        current = stack.pop()
        next = current.nextNeighbour()
        if next != None:
            stack.append(current)
            removeWalls(current, next)
            next.visited = True
            stack.append(next)

def collision():
    if pacman.row == food.row and pacman.col == food.col:
        print("ate food, yum !")
        food.move(random.randint(0, int(HEIGHT/cell_size) - 1), random.randint(0, int(WIDTH/cell_size) - 1))
        pacman.target = cells[getIndex(food.row, food.col)]



generateMaze()
for cell in cells:
    cell.visited = False

current = cells[0]
current.visited = True
stack.append(current)

while (len(stack) > 0):
    current = stack.pop()
    next = current.nextNeighbour()
    if next != None:
         stack.append(current)
         if region[(current.row, current.col)] != region[(next.row, next.col)]:
             if random.randint(0, 1) == 1:
                 result = removeWalls(current, next)
                 if result:
                     min_val = min(region[(current.row, current.col)], region[(next.row, next.col)])
                     max_val = max(region[(current.row, current.col)], region[(next.row, next.col)])
                     for key in region:
                         if region[key] == max_val:
                             region[key] = min_val
                 else:
                     continue
         next.visited = True
         stack.append(next)

pacman = Character(0,0)
last_pacman_pos = (pacman.row, pacman.col)
start_cell = cells[getIndex(pacman.row, pacman.col)]
food = Food(random.randint(0, int(HEIGHT/cell_size) - 1), random.randint(0, int(WIDTH/cell_size) - 1))
pacman.target = cells[getIndex(food.row, food.col)]
pacman.path = pathFinder(start_cell, pacman.target, False)
pacman.path.reverse()
ghost_list = []
ghost = Enemy(int(HEIGHT/cell_size) - 1, int(WIDTH/cell_size) - 1, red)
ghost_list.append(ghost)
ghost2 = Enemy(int(HEIGHT/cell_size) - 1, int(WIDTH/cell_size) - 10, blue)
ghost_list.append(ghost2)
run = True
path_index = 0
ghost_update_counter = 0
pacman_update_counter = 0
ghost2_update_counter = 0
def danger():
    for cell in cells:
        max_d = 0

        for ghost in ghost_list:
            d = distance(cell, ghost)
            D = 50 / ((0.0001 * d) + 0.0001)
            if D > max_d:
                max_d = D

        cell.danger = max_d

def gameOver():
    pass


while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(black)
    #danger()
    gameOver()
    new_start_cell = cells[getIndex(pacman.row, pacman.col)]


    collision()

    ghost_update_counter += 1
    if ghost_update_counter % 4 == 0:  # every ~1.5s if 10 FPS
        ghost_path = pathFinder(cells[getIndex(ghost.row, ghost.col)], new_start_cell, True)
        if ghost_path:
            ghost.path = list(reversed(ghost_path))
            ghost.index = 0

    ghost2_update_counter += 1
    if ghost2_update_counter % 4 == 0:  # every ~1.5s if 10 FPS
        ghost2_path = pathFinder(cells[getIndex(ghost2.row, ghost2.col)], cells[getIndex(new_start_cell.row, new_start_cell.col + 4)], True)
        if ghost2_path:
            ghost2.path = list(reversed(ghost2_path))
            ghost2.index = 0

    danger()

    if new_start_cell.danger > 20:
        print("fuck, hes close")
    pacman_update_counter += 1
    if pacman_update_counter % 3 == 0:  # every ~1.5s if 10 FPS
        new_path = pathFinder(new_start_cell, cells[getIndex(pacman.target.row, pacman.target.col)], False)
        if new_path:
            pacman.path = list(reversed(new_path))
            pacman.index = 0


    for cell in cells:
        cell.draw()

    food.draw()
    pacman.draw()
    pacman.chase()


    ghost.draw()
    ghost.chase()
    ghost2.draw()
    ghost2.chase()

    pygame.display.flip()


pygame.quit()
sys.exit()