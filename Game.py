import pygame, time, math

pygame.init()

clock = pygame.time.Clock()
autoClickPower = 0
coins = 0
coinsPerClick = 1
deltaTime = 0
mineCooldown = 0
coinsPerSecond = 0

circles = []
squares = []
buttons = []
onClickText = []
coinsPerSecondList = []

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("clicky clicks")

class Circle:
    def __init__(self, color, position, radius, name):
        self.color = color
        self.position = position
        self.radius = radius
        self.name = name

    def draw(self):
        self.drawing = pygame.draw.circle(gameDisplay, self.color, self.position, self.radius)

    def IsColliding(self):
        if self.drawing.collidepoint(pygame.mouse.get_pos()): return True

class Square:
    def __init__(self, color, position, size, name = int, isButton = bool):
        self.color = color
        self.position = position
        self.size = size
        self.name = name
        if (isButton):
            buttons.append(Button(self.name))


    def draw(self):
        self.drawing = pygame.draw.rect(gameDisplay, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]))

    def IsColliding(self):
        if self.drawing.collidepoint(pygame.mouse.get_pos()): return True

def DrawText(text, Textcolor, x, y, fsize, transparency = 255):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, Textcolor)
    text.set_alpha(transparency)
    textRect = text.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(text, textRect)

class OnClickText:
    def __init__(self, mousePos):
        self.x = mousePos[0]
        self.y = mousePos[1]
        self.transparency = 255
        onClickText.append(self)

def OnClickTextAnimation():
    for text in onClickText:
        DrawText(str(f'{coinsPerClick}') + " coins", (0, 0, 0), text.x, text.y, 20, text.transparency)
        text.y -= .1 * deltaTime
        text.transparency -= .6 * deltaTime
        if text.transparency <= 0:
            onClickText.remove(text)

class Button:
    def __init__(self, name):
        self.name = name
        self.price = 0
        self.lvl = 0
    
    def SetPrice(self, price):
        self.price = price

    def IncreaseLevel(self, amount):
        self.lvl += amount

    def IncreasePrice(self, times):
        self.price = round(self.price * times, 0)

    def GetPrice(self):
        return self.price
    
    def GetLevel(self):
        return self.lvl
    
class CoinsPerSecond:
    def __init__(self, amount, time):
        self.amount = amount
        self.time = time

def Autominer():
    global mineCooldown
    if mineCooldown <= 0:
        TouchCoins(autoClickPower)
        mineCooldown = 250
    else:
        mineCooldown -= deltaTime

def IncreaseAutoClick(times):
    global autoClickPower
    if autoClickPower == 0:
        autoClickPower = 1
    else:
        autoClickPower *= times

def IncreaseCoinsPerClick(times):
    global coinsPerClick
    coinsPerClick = round(coinsPerClick * times, 2)

def TouchCoins(amount):
    global coins
    coins += amount
    CoinsPerSecondCalculator(amount)

def CoinsPerSecondCalculator(amount):
    global coinsPerSecond
    if amount > 0:
        coinsPerSecondList.append(CoinsPerSecond(amount, 1000))
        coinsPerSecond = 0
        for i in coinsPerSecondList:
            coinsPerSecond += i.amount
    for i in coinsPerSecondList:
            if i.time <= 0:
                coinsPerSecond -= i.amount
                coinsPerSecondList.pop(coinsPerSecondList.index(i))
            else:
                i.time -= deltaTime

def forCircle(name):
    for circle in circles:
        if circle.name == name:
            return circle
            
def forSquare(name):
    for square in squares:
        if square.name == name:
            return square

def forButton(name):
    for button in buttons:
        if button.name == name:
            return button

circles.append(Circle((108, 77, 59), (400, 260), 160, "cookie"))

squares.append(Square((0, 100, 250), (50, 500), (200, 50), "but1", True))
squares.append(Square((0, 155, 255), (55, 505), (190, 40)))
squares.append(Square((0, 100, 250), (550, 500), (200, 50), "but2", True))
squares.append(Square((0, 155, 255), (555, 505), (190, 40)))

forButton("but1").SetPrice(50)
forButton("but2").SetPrice(50)

def main_loop():
    global coinsPerClick
    coinsPerClick = 1
    global coins
    coins = 50
    global deltaTime
    while True:
        Autominer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (forCircle("cookie").IsColliding()):
                    TouchCoins(coinsPerClick)
                    mousePos = pygame.mouse.get_pos()
                    OnClickText((mousePos[0], mousePos[1]))

                if (forSquare("but1").IsColliding() and coins >= forButton("but1").price):
                    button = forButton("but1")
                    TouchCoins(-button.price)
                    button.IncreasePrice(1.5)
                    button.IncreaseLevel(1)
                    IncreaseCoinsPerClick(1.4)
                
                if (forSquare("but2").IsColliding() and coins >= forButton("but2").price):
                    button = forButton("but2")
                    TouchCoins(-button.price)
                    button.IncreasePrice(1.5)
                    button.IncreaseLevel(1)
                    IncreaseAutoClick(1.3)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        CoinsPerSecondCalculator(0)

        # Draw
        gameDisplay.fill((173, 216, 230))

        for i in circles: i.draw()
        for i in squares: i.draw()

        DrawText(str(f'{coins:.2f}') + " coins", (0, 0, 0), 400, 50, 20)
        DrawText(str(f'{coinsPerSecond:.2f}') + " coins/s", (100, 100, 100), 400, 65, 15, 175)

        DrawText("upgrade clicker " + str(forButton("but1").lvl), (0, 0, 0), 150, 480, 20)
        DrawText(str(forButton("but1").price), (0, 0, 0), 150, 525, 20)
        DrawText(str(f'{coinsPerClick:.2f}'), (0, 0, 0), 150, 570, 20)
        
        DrawText("buy auto miner " + str(forButton("but2").lvl), (0, 0, 0), 650, 480, 20)
        DrawText(str(forButton("but2").price), (0, 0, 0), 650, 525, 20)
        DrawText(str(f'{autoClickPower:.2f}'), (0, 0, 0), 650, 570, 20)

        OnClickTextAnimation()

        pygame.display.update()
        deltaTime = clock.tick(60)

main_loop()
pygame.quit()
quit()