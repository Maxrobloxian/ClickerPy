import pygame, time, math

pygame.init()

clock = pygame.time.Clock()
autog = 0
coins = 0

circles = []
squares = []

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("clicky clicks")

class Circle:
    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.radius = radius

    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, self.position, self.radius)

class Square:
    def __init__(self, color, position, size):
        self.color = color
        self.position = position
        self.size = size

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]))

def autominer():
    global coins
    global autog
    time.sleep(0.1)
    coins += autog


def DrawText(text, Textcolor, x, y, fsize):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, Textcolor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(text, textRect)

circles.append(Circle((108, 77, 59), (400, 260), 160))

squares.append(Square((0, 100, 250), (50, 500), (200, 50)))
squares.append(Square((0, 155, 255), (55, 505), (190, 40)))
squares.append(Square((0, 100, 250), (550, 500), (200, 50)))
squares.append(Square((0, 155, 255), (555, 505), (190, 40)))

def main_loop():
    global clock
    global autog
    global color1
    global color2
    global color3
    mong = 1
    cost = 50
    cost2 = 50
    lvl = 0
    lvl2 = 0
    global coins
    coins = 5000
    while True:
        autominer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mPos = pygame.mouse.get_pos()
                if (math.sqrt((mPos[0] - 400) ** 2 + (mPos[1] - 260) ** 2)) <= 160:
                    coins += mong

                if (mPos[0] >= 50 and mPos[1] >= 500) and (mPos[0] <= 250 and mPos[1] <= 550) and coins >= cost:
                    coins -= cost
                    cost *= 1.5
                    cost = round(cost, 0)
                    mong *= 1.1
                    lvl += 1

                if (mPos[0] >= 550 and mPos[1] >= 500) and (mPos[0] <= 750 and mPos[1] <= 550) and coins >= cost2:
                    coins -= cost2
                    cost2 *= 1.5
                    cost2 = round(cost2, 0)
                    autog += 0.5
                    lvl2 += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        gameDisplay.fill((173, 216, 230))

        for i in circles: i.draw()
        for i in squares: i.draw()

        DrawText(str(f'{coins:.2f}') + " coins", (0, 0, 0), 400, 50, 20)
        DrawText("upgrade clicker " + str(lvl), (0, 0, 0), 150, 480, 20)
        DrawText(str(cost), (0, 0, 0), 150, 525, 20)
        DrawText("buy auto miner " + str(lvl2), (0, 0, 0), 650, 480, 20)
        DrawText(str(cost2), (0, 0, 0), 650, 525, 20)

        pygame.display.update()
        clock.tick(60)

main_loop()
pygame.quit()
quit()