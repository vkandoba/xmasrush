import sys
import math
from collections import deque

side = 6

opDir = {
            'up': 'down',
            'right': 'left',
            'down': 'up',
            'left': 'right'
        }

placeDirs = [(0, -1, 'up'), (1, 0, 'right'), (0, 1, 'down'), (-1, 0, 'left')]

def safeInt(str):
    try:
        return int(str)
    except ValueError:
        return str

def isCoordinate(x, y):
    return 0 <= x and x <= side and 0 <= y and y <= side

def nearCells(tiles, x, y):
    return filter(lambda dir: isCoordinate(x + dir[0], y + dir[1]), placeDirs)

def isLinked(tiles, x, y, dx, dy, dirTo):
    dirFrom = opDir[dirTo]
    return tiles[x][y][dirTo] == 1 and tiles[x + dx][y + dy][dirFrom] == 1

def isClear(tiles, parents, x, y, dx, dy, dirTo):
    return parents[x + dx][y + dy] == 0 and isLinked(tiles, x, y, dx, dy, dirTo)

def canBeNeighborings(parents, x, y):
    return isCoordinate(x, y) and parents[x][y] == 0
        
def getNeighborings(tiles, parents, x, y):
    # print(tiles[x][y], file=sys.stderr)
    neighborings = list(map(lambda dir: (x + dir[0], y + dir[1], dir[2]), filter(lambda dir: isClear(tiles, parents, x, y, *dir), nearCells(tiles, x, y))))
    for n in neighborings:
        parents[n[0]][n[1]] = (x, y, n[2])
    return map(lambda x: x[0:2], neighborings);

def getPath(parents, startX, startY, targetX, targetY):
    path = []
    pos = parents[startX][startY]
    while pos[0:2] != (targetX, targetY):
        path.insert(0, pos)
        pos = parents[pos[0]][pos[1]]
    path.insert(0, pos)
    return path

def findPath(tiles, startX, startY, targetX, targetY):
    parents = [[0 for _ in range(side+1)] for _ in range(side+1)]
    parents[startX][startY] = ();
    neighborings = getNeighborings(tiles, parents, startX, startY)
    points = deque(neighborings)
    while len(points) > 0:
        p = points.popleft()
        if p == (targetX, targetY):
            return getPath(parents, targetX, targetY, startX, startY);
        neighborings = getNeighborings(tiles, parents, *p)
        points.extend(neighborings)
    return None

def getPush(tiles, playerX, playerY, targetX, targetY):
    if playerX != targetX:
        if playerY > targetY+1:
            return (playerX, 'UP')
        elif playerY < targetY-1:
            return (playerX, 'DOWN')
    if playerY != targetY:
        if playerX > targetX+1:
            return (playerY, 'LEFT')
        elif playerX < targetX-1:
            return (playerY, 'RIGHT')
    return False
   
def findPathToAny(tiles, playerX, playerY, quests):
    for q in quests:
        path = findPath(tiles, player_x, player_y, q['x'], q['y'])
        if path:
            dirs = list(map(lambda x: x[2].upper(), path))
            return ' '.join(dirs)
    return None;
    
def getPushToAny(tiles, playerX, playerY, quests):
    for q in quests:
        push = getPush(tiles, player_x, player_y, q['x'], q['y'])
        if push != False:
            return str(push[0]) + ' ' + push[1]
    return False;  

# Help the Christmas elves fetch presents in a magical labyrinth!
# game loop
while True:
    turn_type = int(input())
    tiles1 = [list(map(lambda s: dict(zip(['up', 'right', 'down', 'left'], map(int, s))), input().split())) for i in range(side+1)]
  
    tiles = list(zip(*tiles1))
    
    # num_player_cards: the total number of quests for a player (hidden and revealed)
    num_player_cards, player_x, player_y, player_tile = input().split()
    num_player_cards = int(num_player_cards)
    player_x = int(player_x)
    player_y = int(player_y)
    
    input().split() #other player
    num_items = int(input())  # the total number of items available on board and on player tiles

    items = dict(list(map(lambda item: (f"{item['name']}.{item['player']}", item), 
                           [dict(zip(['name', 'x', 'y', 'player'], map(safeInt, input().split()))) for _ in range(num_items)])))
    
    num_quests = int(input())  # the total number of revealed quests for both players
    myQuests = list(map(lambda x: items[f'{x[0]}.{x[1]}'], filter(lambda x: x[1] == 0, [list(map(safeInt, input().split())) for _ in range(num_quests)])))
    
    if turn_type == 1:
        path = findPathToAny(tiles, player_x, player_y, myQuests)
        if path:
            print("MOVE " + path)
        else:
            print("PASS")
    else:
        dir = getPushToAny(tiles, player_x, player_y, myQuests)
        if dir:
            print('PUSH ' + dir)
        else:
            print('PUSH 6 LEFT')