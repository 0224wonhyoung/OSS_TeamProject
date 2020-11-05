from bangtal import *
import threading

# Game Settings
setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
# Scenes
inGame = Scene('inGame','images/paperBG1.png')    #1280 x 720

# Classes
class Current():
    playerX = 600       # 실제 scene 좌표
    playerX = 250
    mapX = 0            # 상대적 map 좌표
    mapY = 0
    hp = 3
    xp = 0
    day = 1
    turn = 0
    sky = 1             # 1:Sun  2:Moon
    LR = 1              # 1:Right  2:Left
    playerMoving = False
    direction = 0      # current moving direction

class Const():
    INIT_PLAYER_X = 600
    INIT_PLAYER_Y = 250
    BLOCK_SIZE = 84
    ANIMATION_FRAME = 8     # 이동 애니메이션 총 프레임수

class Mob():
    def __init__(self, x, y):
        mapX = x
        mapY = y

class Block(Object):
    def __init__(self, num, x, y):
        super().__init__("images/blocks/block"+str(num)+".png")
        self.num = num
        self.setScale(3.5)        
        self.locate_on_board(x, y)
        self.show()
    def locate_on_board(self, bx, by):
        self.x = bx
        self.y = by
        tx = int(Const.INIT_PLAYER_X + Const.BLOCK_SIZE * (bx-2))
        ty = int(Const.INIT_PLAYER_Y + Const.BLOCK_SIZE * (by-2))
        self.locate(inGame, tx, ty)
    def moveAnimation(self, direction, frame):        
        #if direction == RIGHT        
        dx = [1, -1, 0, 0]
        dy = [0, 0, -1, 1]
        self.x += dx[direction]/Const.ANIMATION_FRAME
        self.y += dy[direction]/Const.ANIMATION_FRAME
        if frame == Const.ANIMATION_FRAME:
            self.x = round(self.x)
            self.y = round(self.y)
        self.locate_on_board(self.x, self.y)       
    def setImageNum(self, num):
        self.num = num
        self.setImage("images/blocks/block"+str(num)+".png")


class BlockBoard():
    def __init__(self):
        self.board = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
        self.spareBoard = [25, 26, 27, 28, 29]
        self.frame = 1

    def locate_spare(self, direction):
        # if direction == RIGHT
        global slist
      
        for i in range(5):
            tblock = blocks[self.spareBoard[i]]
            tx = slist[direction][i][1]
            ty = slist[direction][i][0]
            tblock.setImageNum(mapContents(Current.mapX + tx - 2, Current.mapY + ty-2))
            tblock.locate_on_board(tx, ty)
            tblock.show()

    def update_board(self, direction):
        print("HERE")
        #if direction == RIGHT
        tempSpare = []
        
        if direction == 0:
            for i in range(5):
                tempSpare.append(self.board[i][4])
            for i in range(4, -1, -1):
                for j in range(5):
                    if i==0:
                        self.board[j][i] = self.spareBoard[j]
                    else:
                        self.board[j][i] = self.board[j][i-1]
            for i in range(5):
                self.spareBoard[i] = tempSpare[i]
                blocks[tempSpare[i]].hide()
        
        elif direction == 1:
            for i in range(5):
                tempSpare.append(self.board[i][0])
            for i in range(5):
                for j in range(5):
                    if i==4:
                        self.board[j][i] = self.spareBoard[j]
                    else:
                        self.board[j][i] = self.board[j][i+1]
            for i in range(5):
                self.spareBoard[i] = tempSpare[i]
                blocks[tempSpare[i]].hide()

        elif direction == 2:
            for i in range(5):
                tempSpare.append(self.board[0][i])
            for i in range(5):
                for j in range(5):
                    if i==4:
                        self.board[i][j] = self.spareBoard[j]
                    else:
                        self.board[i][j] = self.board[i+1][j]
            for i in range(5):
                self.spareBoard[i] = tempSpare[i]
                blocks[tempSpare[i]].hide()

        elif direction == 3:
            for i in range(5):
                tempSpare.append(self.board[4][i])
            for i in range(4, -1, -1):
                for j in range(5):
                    if i==0:
                        self.board[i][j] = self.spareBoard[j]
                    else:
                        self.board[i][j] = self.board[i-1][j]
            for i in range(5):
                self.spareBoard[i] = tempSpare[i]
                blocks[tempSpare[i]].hide()

    def boardAnimation(self, direction):
        for i in range(30):
            blocks[i].moveAnimation(direction, self.frame)
        self.frame = self.frame % Const.ANIMATION_FRAME + 1
        if self.frame == 1:            
            self.update_board(direction)            
            return

    def move(self,direction):
        self.locate_spare(direction)
        self.boardAnimation(direction)

blockBoard = BlockBoard()

# Map Controls
MapSize = 9
MapSizeX = MapSize
MapSizeY = MapSize

Contents = []
for x in range(MapSizeX+2):
    Contents.append([])
    for y in range(MapSizeY+2):
        if x==0 or x==MapSizeX+1 or y==0 or y==MapSizeY+1:
            num = -1
        else:
            num = 0
        Contents[x].append(num)
Contents[2][2] = 1
Contents[3][5] = 2
Contents[2][8] = 3
Contents[8][6] = 4

def mapContents(x, y):
    global MapSizeX
    global MapSizeY
    X = int(x + 1+(MapSizeX-1)/2)
    Y = int(y + 1+(MapSizeY-1)/2)
    #print("x, y : %d, %d -> X, Y : %d, %d"%(x, y, X, Y))
    if (0 <= X <= (MapSizeX+1)) and (0 <= Y <= (MapSizeY+1)):
        return Contents[X][Y]
    print("X, Y is over map : %d %d, so using block0 image"%(X, Y))
    return 0

print(mapContents(-6,0))
print(mapContents(-5,0))
print(mapContents(-4,0))

def showmap():
    global MapSizeX
    global MapSizeY
    for y in range(MapSizeY+2):
        print(Contents[y])
showmap()

# 30 blocks[y][x] (5x5 blocks + 5 spare blocks)
blocks = []
for i in range(30):    
    blocks.append(Block(i//5, i%5, i//5))
    blocks[i].setImageNum(mapContents((i%5) - 2, (i//5) -2))
    if i > 24:
        blocks[i].hide()


# BlockBoard and slist
blockBoard = BlockBoard()
slist = []

def init_slist():
    global slist
    tlist = []
    for i in range(5):
        tlist.append([i, -1])
    slist.append(tlist)
    tlist = []
    for i in range(5):
        tlist.append([i, 5])
    slist.append(tlist)
    tlist = []
    for i in range(5):
        tlist.append([5, i])
    slist.append(tlist)
    tlist = []
    for i in range(5):
        tlist.append([-1, i])
    slist.append(tlist)
init_slist()



# All Objects
player = Object('images/playerR1.png')
player.locate(inGame, 600, 250)
player.setScale(0.5)
player.show()

weather = Object('images/weathers/sun.png')
weather.locate(inGame, 570, 590)
weather.setScale(0.25)
weather.show()

DAY = Object('images/day.png')
DAY.locate(inGame, 470, 660)
DAY.setScale(0.14)
DAY.show()

TURN = Object('images/turn.png')
TURN.locate(inGame, 700, 660)
TURN.setScale(0.15)
TURN.show()

Days10 = Object('images/numbers/0.png')
Days1 = Object('images/numbers/1.png')
Days10.locate(inGame, 480, 600)
Days1.locate(inGame, 520, 600)
Days10.setScale(0.15)
Days1.setScale(0.15)
Days10.show()
Days1.show()

turns10 = Object('images/numbers/0.png')
turns1 = Object('images/numbers/0.png')
turns1.locate(inGame, 760, 600)
turns10.locate(inGame, 720, 600)
turns10.setScale(0.15)
turns1.setScale(0.15)
turns10.show()
turns1.show()

HP = Object('images/hearts/3.png')
HP.locate(inGame, 10, 640)
HP.setScale(0.15)
HP.show()

XP = Object('images/xp.png')
XP.locate(inGame, 1200, 640)
XP.setScale(0.13)
XP.show()
xp100 = Object('images/numbers/0.png')
xp10 = Object('images/numbers/0.png')
xp1 = Object('images/numbers/0.png')
xp100.locate(inGame, 1070, 640)
xp10.locate(inGame, 1110, 640)
xp1.locate(inGame, 1150, 640)
xp100.setScale(0.18)
xp10.setScale(0.18)
xp1.setScale(0.18)

# Player Controls
def keyboardPressed(key, pressed):
    global MapSizeX
    global MapSizeY
    wallLeft = Current.mapX <= -1*(MapSizeX-1)/2
    wallRight = Current.mapX >= (MapSizeX-1)/2
    wallDown = Current.mapY <= -1*(MapSizeY-1)/2
    wallUp = Current.mapY >= (MapSizeY-1)/2
    if pressed:
        if (not Current.playerMoving):
            if key==82:
                if not wallLeft:
                    Current.LR = 2                    
                    Current.direction = 0
                    blockBoard.locate_spare(Current.direction)
                    playerAnimation()
                    Current.mapX -= 1
                    playerTurn()
            elif key==83:
                if not wallRight:
                    Current.LR = 1                    
                    Current.direction = 1
                    blockBoard.locate_spare(Current.direction)
                    playerAnimation()
                    Current.mapX += 1
                    playerTurn()
            elif key==84:
                if not wallUp:                    
                    Current.direction = 2
                    blockBoard.locate_spare(Current.direction)
                    playerAnimation()
                    Current.mapY += 1
                    playerTurn()
            elif key==85:
                if not wallDown:                    
                    Current.direction = 3
                    blockBoard.locate_spare(Current.direction)
                    playerAnimation()
                    Current.mapY -= 1
                    playerTurn()
            print(Current.mapX, Current.mapY)
inGame.onKeyboard = keyboardPressed

animationFrame = 1
def playerAnimation():
    global animationFrame
    animationTimer = threading.Timer(0.125, playerAnimation)
    if animationFrame==8:
        Current.playerMoving = False
    else:
        Current.playerMoving = True
        pass
    
    blockBoard.boardAnimation(Current.direction)

    if Current.LR==2:
        if animationFrame==1:
            player.setImage('images/playerL2.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==2:
            player.setImage('images/playerL1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==3:
            player.setImage('images/playerL3.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==4:
            player.setImage('images/playerL1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==5:
            player.setImage('images/playerL2.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==6:
            player.setImage('images/playerL1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==7:
            player.setImage('images/playerL3.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==8:
            player.setImage('images/playerL1.png')
            animationFrame = 1
            animationTimer._stop()
    elif Current.LR==1:
        if animationFrame==1:
            player.setImage('images/playerR2.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==2:
            player.setImage('images/playerR1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==3:
            player.setImage('images/playerR3.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==4:
            player.setImage('images/playerR1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==5:
            player.setImage('images/playerR2.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==6:
            player.setImage('images/playerR1.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==7:
            player.setImage('images/playerR3.png')
            animationFrame += 1
            animationTimer.start()
        elif animationFrame==8:
            player.setImage('images/playerR1.png')
            animationFrame = 1
            animationTimer._stop()

# Interface Controls
def setNumImage(num):
    if num==0:
        image = 'images/numbers/0.png'
    elif num==1:
        image = 'images/numbers/1.png'
    elif num==2:
        image = 'images/numbers/2.png'
    elif num==3:
        image = 'images/numbers/3.png'
    elif num==4:
        image = 'images/numbers/4.png'
    elif num==5:
        image = 'images/numbers/5.png'
    elif num==6:
        image = 'images/numbers/6.png'
    elif num==7:
        image = 'images/numbers/7.png'
    elif num==8:
        image = 'images/numbers/8.png'
    elif num==9:
        image = 'images/numbers/9.png'
    return image

def dayChange():
    Current.day += 1
    Days10.setImage(setNumImage(Current.day//10))
    Days1.setImage(setNumImage(Current.day%10))

def skyChange():
    if Current.sky == 1:
        Current.sky = 2
        weather.setImage('images/weathers/moon.png')
        inGame.setImage('images/paperBG2.png')
    elif Current.sky == 2:
        dayChange()
        Current.sky = 1
        weather.setImage('images/weathers/sun.png')
        inGame.setImage('images/paperBG1.png')
    else:               # 해, 달 외의 다른 날씨 추가 (비, 흐림 등등)
        pass    

def playerTurn():
    Current.turn += 1
    if Current.turn==20:
        skyChange()
        Current.turn = 0
    else:
        if 0<=Current.turn<=4:
            if Current.sky==1:
                inGame.setLight(0.85)
            else:
                inGame.setLight(0.65)
        elif 15<=Current.turn<=19:
            if Current.sky==2:
                inGame.setLight(0.85)
            else:
                inGame.setLight(0.65)
        else:
            if Current.sky==1:
                inGame.setLight(1)
            else:
                inGame.setLight(0.5)
    turns10.setImage(setNumImage(Current.turn//10))
    turns1.setImage(setNumImage(Current.turn%10))
    
def showXP():
    XP = Current.xp
    if XP<10:       
        xp1.setImage(setNumImage(XP))
        xp1.show()
        xp10.hide()
        xp100.hide()
    elif XP<100:
        xp10.setImage(setNumImage(XP//10))
        xp1.setImage(setNumImage(XP%10))
        xp1.show()
        xp10.show()
        xp100.hide()
    else:
        x = XP-(XP//100*100)
        xp100.setImage(setNumImage(XP//100))
        xp10.setImage(setNumImage(x//10))
        xp1.setImage(setNumImage(x%10))
        xp1.show()
        xp10.show()
        xp100.show()






# ///// Game Start /////
XP = 365
showXP()
inGame.setLight(0.85)
startGame(inGame)