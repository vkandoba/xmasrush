import sys
import math
from collections import deque

side = 6

def safeInt(str):
    try:
        return int(str)
    except ValueError:
        return str

def isCoordinate(x, y):
    return 0 <= x and x <= side and 0 <= y and y <= side

def canBeNeighborings(parents, x, y):
    return isCoordinate(x, y) and parents[x][y] == 0

def parseTile(tile):
    parsed = {'up' : int(tile[0]), 'right': int(tile[1]), 'down': int(tile[2]), 'left': int(tile[3])}
    return parsed

def getNeighborings(tiles, parents, x, y):
    # print(tiles[x][y], file=sys.stderr)
    neighborings = []
    if canBeNeighborings(parents, x, y-1) and tiles[x][y]['up'] == 1 and tiles[x][y-1]['down'] == 1:
        parents[x][y-1] = (x, y, 'UP')
        neighborings.append((x, y-1))
    if canBeNeighborings(parents, x+1, y) and tiles[x][y]['right'] == 1 and tiles[x+1][y]['left'] == 1:
        parents[x+1][y] = (x, y, 'RIGHT')
        neighborings.append((x+1, y))
    if canBeNeighborings(parents, x, y+1) and tiles[x][y]['down'] == 1 and tiles[x][y+1]['up'] == 1:
        parents[x][y+1] = (x, y, 'DOWN')
        neighborings.append((x, y+1))        
    if canBeNeighborings(parents, x-1, y) and tiles[x][y]['left'] == 1 and tiles[x-1][y]['right'] == 1:
        parents[x-1][y] = (x, y, 'LEFT')
        neighborings.append((x-1, y))
    return neighborings;

def getPath(parents, startX, startY, targetX, targetY):
    print(startX, startY, targetX, targetY, file=sys.stderr)
    path = []
    pos = parents[startX][startY]
    while (pos[0], pos[1]) != (targetX, targetY):
        # print(pos, file=sys.stderr)
        path.insert(0, pos)
        pos = parents[pos[0]][pos[1]]
    path.insert(0, pos)
    return path

def findPath(tiles, startX, startY, targetX, targetY):
    parents = []
    for i in range(7):
        parents.append([])
        for j in range(7):
            parents[i].append(0)
    parents[startX][startY] = ();
    # print("find path", startX, startY, targetX, targetY, file=sys.stderr)
    neighborings = getNeighborings(tiles, parents, startX, startY)
    # for n in neighborings:
        # print("find path neighborings", n, parents[n[0]][n[1]], file=sys.stderr)
    points = deque(neighborings)
    while len(points) > 0:
        p = points.popleft()
        # print("find path p", p, file=sys.stderr)
        if p[0] == targetX and p[1] == targetY:
            return getPath(parents, targetX, targetY, startX, startY);
        neighborings = getNeighborings(tiles, parents, p[0], p[1])
        # for n in neighborings:
            # print("find path neighborings", n, parents[n[0]][n[1]], file=sys.stderr)
        points.extend(neighborings)
    return False

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
        if path != False:
            dirs = list(map(lambda x: x[2], path))
            return ' '.join(dirs)
    return False;
    
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
    tiles1 = [list(map(parseTile, input().split())) for i in range(7)]

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
    myQuests = []
    for i in range(num_quests):
        quest_item_name, quest_player_id = input().split()
        # print(quest_item_name, quest_player_id, file=sys.stderr)
        quest_player_id = quest_player_id
        if quest_player_id == '0':
            tname = f'{quest_item_name}.{quest_player_id}'
            myQuests.append(items[tname])

    # print(tname, items[tname], file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # print(items[tname]['x'], items[tname]['y'], file=sys.stderr)

    # PUSH <id> <direction> | MOVE <direction> | PASS
    
    if turn_type == 1:
        path = findPathToAny(tiles, player_x, player_y, myQuests)
        if path != False:
            print("MOVE " + path)
        else:
            print("PASS")
    else:
        dir = getPushToAny(tiles, player_x, player_y, myQuests)
        if dir:
            print('PUSH ' + dir)
        else:
            print('PUSH 6 LEFT')