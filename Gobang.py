import pygame
import sys
import os
from pygame.locals import QUIT, KEYDOWN
import numpy as np
import time
from utils import threechess, threeChess, fourChess, fivechess, fiveChess, sixChess, blank
from button.button import Button
import Minimax_Alphabeta

np.random.seed(int(time.time()))
os.environ["SDL_VIDEO_CENTERED"] = '1'  # Window centered
pygame.init()
screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption('All Rules Gobang AI')
myfont = pygame.font.Font(None, 25)

blackColor = (0, 0, 0)
whiteColor = (255, 255, 255)
lineColor = blackColor
occupiedPos = []
fives = []
board = np.zeros((15, 15, 2), dtype=bool)  # (1,1)black, (1,0)white, (0,0)None

fiveScore = 100000
fourScore = 10000
threeScore = 1000
twoScore = 100
oneScore = 10
fourscore = 1000
threescore = 100
twoscore = 10

playBlack = True
autoplay = True


def retract():
    for i in range(2):
        if len(occupiedPos):
            x, y = occupiedPos.pop()
            board[int((x-27)/44)][int((y-27)/44)] = [0, 0]


def playAgain():
    occupiedPos.clear()
    fives.clear()
    global board
    board = np.zeros((15, 15, 2), dtype=bool)


def notAuto():
    global autoplay
    autoplay = False


def Auto():
    global autoplay
    autoplay = True


def playWhite():
    global playBlack
    playBlack = False


def playblack():
    global playBlack
    playBlack = True


def isWin(board):  # 0: None, minus: White, 1: Black
    if len(occupiedPos) < 9:
        return 0

    three = 0
    four = 0
    lastX, lastY = (int((p-27)/44) for p in occupiedPos[-1])
    left = max(0, lastX-4)
    right = min(14, lastX+4)
    up = min(14, lastY+4)
    down = max(0, lastY-4)

    leftDown = min(lastX - left, lastY - down)
    rightUp = min(right - lastX, up - lastY)
    leftUp = min(lastX - left, up - lastY)
    rightDown = min(right - lastX, lastY - down)

    Horizontal = board[left:right+1, lastY, :]
    Vertical = board[lastX, down:up+1, :]

    Diagonal1 = np.array([board[lastX-leftDown+i, lastY-leftDown+i, :] for i in range(leftDown+rightUp+1)])
    Diagonal2 = np.array([board[lastX-leftUp+i, lastY+leftUp-i, :] for i in range(leftUp+rightDown+1)])

    blackWin = False
    for chess in (Horizontal, Vertical, Diagonal1, Diagonal2):
        finish = False
        if len(chess) < 5:
            continue
        elif len(chess) == 5:
            if(chess == threechess).all():
                three += 1
                continue
            elif(chess == fivechess).all():
                blackWin = True
        else:
            for i in range(len(chess) - 5):
                if True in [(chess[i:i+6] == j).all() for j in fiveChess[:4, :, :]]:
                    blackWin = True
                if True in [(chess[i:i+6] == j).all() for j in fiveChess[4:, :, :]]:
                    return -1
                if True in [(chess[i:i+6] == j).all() for j in sixChess]:
                    return -2
                if finish:
                    continue
                if True in [(chess[i:i+6] == j).all() for j in fourChess]:
                    four += 1
                    finish = True
                if True in [(chess[i:i+6] == j).all() for j in threeChess]:
                    three += 1
                    finish = True

    if three > 1:
        return -3
    elif four > 1:
        return -4
    elif blackWin:
        return True
    return 0


def centerPos(x, y):
    if x >= 665:
        return (0, 0)
    if y >= 665:
        y = 664
    return (int((x-49)/44+1)*44 + 27, int((y-49)/44+1)*44 + 27)


def isLegal(x, y):  # x, y have been modified, which means they are at a center.
    if (x, y) == (0, 0):  # special cases
        return False
    if (x, y) in occupiedPos:
        return False
    if (True):
        numChess = len(occupiedPos)
        if numChess == 0 and (x, y) != (335, 335):
            return False
        elif numChess == 1 and not (x >= 291 and x <= 379 and y >= 291 and y <= 379):
            return False
        elif numChess == 2 and not (x >= 247 and x <= 423 and y >= 247 and y <= 423):
            return False

        elif len(fives) == 1 and (x, y) in fives:
            return False
        elif len(fives) == 2 and (x, y) not in fives:
            return False

    return True


def drawBackground():
    screen.fill((238, 154, 73))
    pygame.draw.line(screen, lineColor, [27, 27], [27, 643], 4)
    pygame.draw.line(screen, lineColor, [27, 643], [643, 643], 4)
    pygame.draw.line(screen, lineColor, [643, 643], [643, 27], 4)
    pygame.draw.line(screen, lineColor, [643, 27], [27, 27], 4)
    for i in range(70, 643, 44):
        pygame.draw.line(screen, lineColor, [i, 27], [i, 643], 2)
        pygame.draw.line(screen, lineColor, [27, i], [643, i], 2)

    pygame.draw.circle(screen, lineColor, [335, 335], 8)
    for i, j in ((3, 3), (3, 11), (11, 3), (11, 11)):
        pygame.draw.circle(screen, lineColor, [27+44*i, 27+44*j], 8)

    numChess = len(occupiedPos)
    if numChess < 3:
        textImage = myfont.render(str('Play the first three chess to start'), True, blackColor)
        screen.blit(textImage, (40, 670))
    elif numChess == 3:
        textImage = myfont.render(str('white did not swap'), True, blackColor)
        screen.blit(textImage, (40, 670))
    elif numChess == 4 and not len(fives):
        textImage = myfont.render(str('black give two choices'), True, blackColor)
        screen.blit(textImage, (40, 670))
    elif numChess > 4 and numChess < 8:
        textImage = myfont.render(str('Next is the regular chess game'), True, blackColor)
        screen.blit(textImage, (40, 670))

    if len(fives) == 2:
        textImage = myfont.render(str('click the fifth chess you want to leave'), True, blackColor)
        screen.blit(textImage, (40, 670))


def drawChess():
    for i, (x, y) in enumerate(occupiedPos):
        pygame.draw.circle(screen, whiteColor if i % 2 else blackColor, (x, y), 20)
        textImage = myfont.render(str(i+1), True, blackColor if i % 2 else whiteColor)
        screen.blit(textImage, ((x-4) if i < 11 else (x-10), y-8))
    for (x, y) in fives:
        pygame.draw.circle(screen, blackColor, (x, y), 20)
        textImage = myfont.render(str(5), True, whiteColor)
        screen.blit(textImage, ((x-4) if i < 11 else (x-10), y-8))


def addChess(x, y):
    if len(occupiedPos) != 4:
        occupiedPos.append((x, y))
    elif len(fives) < 2:
        fives.append((x, y))
    elif (x, y) in fives:
        occupiedPos.append((x, y))
        board[int((x-27)/44)][int((y-27)/44)] = [1, 1]
        fives.clear()


def evaluation(x, y, board):
    lastX, lastY = x, y
    left = max(0, lastX-4)
    right = min(14, lastX+4)
    up = min(14, lastY+4)
    down = max(0, lastY-4)

    leftDown = min(lastX - left, lastY - down)
    rightUp = min(right - lastX, up - lastY)
    leftUp = min(lastX - left, up - lastY)
    rightDown = min(right - lastX, lastY - down)

    Horizontal = [board[:, i, :] for i in range(15)]
    Vertical = [board[i, :, :] for i in range(15)]

    Diagonal1 = [[board[i+j][j] for j in range(15-i)] for i in range(11)]
    # for i in range(11):
    #     a = []
    #     for j in range(15 - i):
    #         a.append(board[i+j][j])
    #     Diagonal1.append(a)
    Diagonal2 = [[board[j][i+j] for j in range(15-i)] for i in range(11)]
    # for i in range(11):
    #     a = []
    #     for j in range(15 - i):
    #         a.append(board[j][i+j])
    #     Diagonal2.append(a)
    Diagonal3 = [[board[i-j][j] for j in range(i)] for i in range(4, 15)]
    # for i in range(4, 15):
    #     a = []
    #     for j in range(i):
    #         a.append(board[i-j][j])
    #     Diagonal3.append(a)
    Diagonal4 = [[board[j][i-j] for j in range(i)] for i in range(4, 15)]
    # for i in range(4, 15):
    #     a = []
    #     for j in range(i):
    #         a.append(board[j][i-j])
    #     Diagonal4.append(a)

    result = 0
    for Chess in (Horizontal, Vertical, Diagonal1, Diagonal2, Diagonal3, Diagonal4):
        for chess in Chess:
            if len(chess) < 5:
                continue
            elif len(chess) == 5:
                if (chess == fivechess).all():
                    result += fiveScore
                elif (chess == threechess).all():
                    result += threeChess
            else:
                for i in range(len(chess) - 5):
                    if True in [(chess[i:i+6] == j).all() for j in fiveChess[:4, :, :]]:
                        result += fiveScore
                    if True in [(chess[i:i+6] == j).all() for j in fiveChess[4:, :, :]]:
                        result -= fiveScore
                    if True in [(chess[i:i+6] == j).all() for j in sixChess]:
                        result -= fiveScore

                    if True in [(chess[i:i+6] == j).all() for j in fourChess]:
                        result += fourScore
                    if True in [(chess[i:i+6] == j).all() for j in threeChess]:
                        result += threeScore

    if not playBlack:
        return -result
    return result


def neighbours(x, y, board):
    r = 2
    result = []
    for i in range(max(0, x-r), min(14, x+r)+1):
        for j in range(max(0, y-r), min(14, y+r)+1):
            if (board[i][j] == blank).all():
                result.append((i, j))
    return result


def alphaBeta(x, y, board, depth, alpha, beta, maxPlayer):
    if isWin(board) != 0:
        return evaluation(x, y, board)

    if maxPlayer:
        v = float('-inf')
        for xi, yi in neighbours(x, y, board):
            newboard = board.copy()
            newboard[xi][yi] = [1, 0] if playBlack else [1, 1]
            temp = alphaBeta(xi, yi, newboard, depth, alpha, beta, False)
            if temp > v or temp == v and np.random.rand() > 0.5:
                v = temp
                bestMove = (xi, yi)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        if depth == 1:
            return bestMove
        return v
    else:
        v = float('inf')
        for xi, yi in neighbours(x, y, board):
            newboard = board.copy()
            newboard[xi][yi] = [1, 1] if playBlack else [1, 0]
            if depth < 2:
                v = min(v, alphaBeta(xi, yi, newboard, depth+1, alpha, beta, True))
            else:
                v = min(v, evaluation(xi, yi, newboard))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


def autoPlay():
    global playBlack
    numChess = len(occupiedPos)
    if numChess % 2 and playBlack or not numChess % 2 and not playBlack:
        if numChess >= 5:
            newboard = [[0 for i in range(15)] for j in range(15)]
            for i, (x, y) in enumerate(occupiedPos):
                newboard[int((x-27)/44)][int((y-27)/44)] = 1 if i % 2 else 2
            x, y, _ = Minimax_Alphabeta.MAB().GetBestPos(newboard, not playBlack)
            board[x, y] = [1, 0] if numChess % 2 else [1, 1]
            addChess(x*44+27, y*44+27)
    if numChess == 0 and not playBlack:
        opening = int(np.random.choice(3, 1))
        opening = [[(7, 7), (7, 6), (9, 5)], [(7, 7), (7, 6), (7, 8)], [(7, 7), (7, 6), (7, 9)]][opening]
        for x, y in opening:
            addChess(x*44+27, y*44+27)
    if numChess == 3 and playBlack:
        if np.random.rand() > 0.5:
            # global playBlack
            playBlack = False
            text = 'White player chose to swap'
            textImage = myfont.render(text, True, blackColor)
            screen.blit(textImage, (100, 670))
        else:
            newboard = [[0 for i in range(15)] for j in range(15)]
            for i, (x, y) in enumerate(occupiedPos):
                newboard[int((x-27)/44)][int((y-27)/44)] = 1 if i % 2 else 2
            x, y, _ = Minimax_Alphabeta.MAB().GetBestPos(newboard, not playBlack)
            board[x, y] = [1, 0] if numChess % 2 else [1, 1]
            addChess(x*44+27, y*44+27)
    if numChess == 4 and not playBlack and len(fives) != 2:
        newboard = [[0 for i in range(15)] for j in range(15)]
        for i, (x, y) in enumerate(occupiedPos):
            newboard[int((x-27)/44)][int((y-27)/44)] = 1 if i % 2 else 2
        x, y, _ = Minimax_Alphabeta.MAB().GetBestPos(newboard, not playBlack)
        # board[x, y] = [1, 0] if numChess % 2 else [1, 1]
        addChess(x*44+27, y*44+27)

        newboard[x][y] = 2 if i % 2 else 1
        x, y, _ = Minimax_Alphabeta.MAB().GetBestPos(newboard, not playBlack)
        # board[x, y] = [1, 0] if numChess % 2 else [1, 1]
        addChess(x*44+27, y*44+27)
    if numChess == 4 and playBlack and len(fives) == 2:
        addChess(*fives[int(np.random.choice(2, 1))])



def playonce():
    buttons = [Button(20, retract, "Retract"),
               Button(80, playAgain, "PlayAgain"),
               Button(140, notAuto, "Stop auto"),
               Button(200, Auto, "autoPlay"),
               Button(260, playWhite, "play White"),
               Button(320, playblack, "play Black")]
    clicked = False

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                pygame.quit()
                sys.exit()
        if not pygame.mouse.get_pressed()[0]:
            clicked = False

        drawBackground()

        drawChess()

        if autoplay:
            autoPlay()

        for button in buttons:
            button.drawAndCheck(screen)

        x, y = centerPos(*pygame.mouse.get_pos())

        if isLegal(x, y):
            pygame.draw.rect(screen, (0, 229, 238), [x-22, y-22, 44, 44], 2, 1)

            if pygame.mouse.get_pressed()[0] and not clicked:  # left click
                clicked = True
                addChess(x, y)

                numChess = len(occupiedPos)
                board[int((x-27)/44), int((y-27)/44)] = [1, 1] if numChess % 2 else [1, 0]

        numChess = len(occupiedPos)
        if numChess:
            x, y = occupiedPos[-1]
            win = isWin(board.copy())
            if win != 0:
                pygame.draw.circle(screen, blackColor if numChess % 2 else whiteColor, (x, y), 20)
                textImage = myfont.render(str(numChess), True, whiteColor if numChess % 2 else blackColor)
                screen.blit(textImage, ((x-4) if numChess < 11 else (x-10), y-8))
            if win == 1:
                textImage = myfont.render('Black Win!', True, blackColor)
                screen.blit(textImage, (5, 2))
                pygame.display.update()
                break
            elif win < 0:
                text = 'White Win!    '
                text += ['Black make two threes', 'Black make two fours',
                         'Black Long Row', ''][win]
                textImage = myfont.render(text, True, blackColor)
                screen.blit(textImage, (5, 2))
                pygame.display.update()
                break

        pygame.time.Clock().tick(24)
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                pygame.quit()
                sys.exit()

        for button in buttons:
            button.drawAndCheck(screen)

        pygame.time.Clock().tick(24)
        pygame.display.update()

        if not isWin(board.copy()):
            return


while True:
    playonce()
