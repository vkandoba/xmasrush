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

def distance(x1, y1, x2, y2):
    return abs(x2 - x1) +  abs(y2 - y1)

def isCoordinate(x, y):
    return 0 <= x and x <= side and 0 <= y and y <= side

def nearCells(tiles, x, y):
    return filter(lambda dir: isCoordinate(x + dir[0], y + dir[1]), placeDirs)

def canBeLink(tile1, tile2, dirTo):
    dirFrom = opDir[dirTo]
    return tile1[dirTo] == 1 and tile2[dirFrom] == 1

def isClear(tiles, parents, x, y, dx, dy, dirTo):
    return parents[x + dx][y + dy] == 0 and canBeLink(tiles[x][y], tiles[x + dx][y + dy], dirTo)
        
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
    
def getComponent(tiles, startX, startY):
    parents = [[0 for _ in range(side+1)] for _ in range(side+1)]
    parents[startX][startY] = 1
    component = [(startX, startY)];
    neighborings = getNeighborings(tiles, parents, startX, startY)
    points = deque(neighborings)
    while len(points) > 0:
        point = points.popleft()
        component.append(point)
        neighborings = getNeighborings(tiles, parents, *point)
        points.extend(neighborings)
    return component;
    
def getPushX(playerX, playerY, targetX, targetY):
    if playerX > targetX:
        return (playerY, 'LEFT')
    elif playerX < targetX:
        return (playerY, 'RIGHT')
    return None

def getPushY(playerX, playerY, targetX, targetY):
    if playerY > targetY:
        return (playerX, 'UP')
    elif playerY < targetY:
        return (playerX, 'DOWN')
    return None

def getPush(tiles, playerX, playerY, targetX, targetY, questsX, questsY):
    pushX = getPushX(playerX, playerY, targetX, targetY)
    pushY = getPushY(playerX, playerY, targetX, targetY)
    print(pushX, pushY, targetX, targetY, questsX, questsY, file=sys.stderr)     
    if targetX == questsX:
        if pushY != None:
            return pushY
        else:
            return pushX
    if targetY == questsY:    
        if pushX != None:
            return pushX
        else:
            return pushY
    return None

def getTargetsForPoint(tiles, playerX, playerY, pointX, pointY):
    targets = list(map(lambda dir: (pointX + dir[0], pointY + dir[1]), 
                        filter(lambda dir: canBeLink(tiles[pointX][pointY], tiles[playerX][playerY], dir[2]), nearCells(tiles, pointX, pointY))))
    return targets

def getTargets(tiles, playerX, playerY, quest):
    m = [[0 for _ in range(side+1)] for _ in range(side+1)]
    print(quest, file=sys.stderr)    
    component = getComponent(tiles, quest['x'], quest['y'])
    targets = []
    for p in component:
        ptargets = getTargetsForPoint(tiles, playerX, playerY, *p)
        for pt in ptargets:
            if m[pt[0]][pt[1]] == 0:
                targets.append((pt, p))
                m[pt[0]][pt[1]] = 1
    print(targets, file=sys.stderr)
    return dict(targets)
    
def findPathToAny(tiles, playerX, playerY, quests):
    for q in quests:
        path = findPath(tiles, player_x, player_y, q['x'], q['y'])
        if path:
            dirs = list(map(lambda x: x[2].upper(), path))
            return ' '.join(dirs)
    return None;
    
def getPushToQuest(tiles, playerX, playerY, quest):
    targets = getTargets(tiles, playerX, playerY, quest)
    if len(targets) == 0:
        return None
    d = dict(zip(targets, map(lambda c: distance(playerX, playerY, c[0], c[1]), targets)))
    print(d, file=sys.stderr)    
    m = min(d, key=d.get)
    return (getPush(tiles, playerX, playerY, m[0], m[1], targets[m][0], targets[m][1]), d[m]);

def getPushToAny(tiles, playerX, playerY, quests):
    items = [];
    for q in quests:
        items.append(getPushToQuest(tiles, playerX, playerY, q))
    print(items, file=sys.stderr) 
    d = dict(filter(lambda x: x != None, items))
    return min(d, key=d.get)

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
        if dir != None:
            print('PUSH ' + str(dir[0]) + ' ' + dir[1])
        else:
            print('PUSH 6 LEFT')