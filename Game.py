import pygame
import time
 
pygame.init()
 
clock = pygame.time.Clock()
autog = 0
coins = 0
 
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("clicky clicks")
 
def circle(display, color, x, y, radius):
    pygame.draw.circle(display, color, [x, y], radius)
 
def autominer():
    global coins
    global autog
    time.sleep(0.1)
    coins = coins + autog
 
 
def DrawText(text, Textcolor, x, y, fsize):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, Textcolor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(text, textRect)
 
 
def rectangle(display, color, x, y, w, h):
    pygame.draw.rect(display, color, (x, y, w, h))
 
 
def main_loop():
    global clock
    global autog
    global color1
    global color2
    global color3
    mong = 1
    cost = 50
    cost2 = 50
    global coins
    while True:
        autominer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPos = pygame.mouse.get_pos()
                if mPos >= (350, 0):
                    if mPos <= (450, 0):
                        coins += mong
 
                if mPos <= (800, 0):
                    if mPos >= (600, 0):
                        if coins >= cost:
                            coins = coins - cost
                            cost = cost * 1.5
                            mong = mong * 1.1
                            cost = round(cost, 0)
 
                if mPos >= (50, 0):
                    if mPos <= (245, 0):
                        if coins >= cost2:
                            coins = coins - cost2
                            cost2 = cost2 * 1.5
                            autog = autog + 0.5
                            cost2 = round(cost2, 0)
 
                if coins == 2147483647:
                    print("You Beat the game")
                    return False
 
        gameDisplay.fill((173, 216, 230))
        DrawText(str(f'{coins:.2f}') + " coins", (0, 0, 0), 400, 50, 20)
        DrawText("upgrade clicker " + str(cost), (0, 0, 0), 650, 480, 20)
        DrawText("buy auto miner " + str(cost2), (0, 0, 0), 150, 480, 20)
        rectangle(gameDisplay, (0, 100, 250), 50, 500, 200, 50)
        rectangle(gameDisplay, (0, 155, 255), 55, 505, 190, 40)
        circle(gameDisplay, (108, 77, 59), 400, 260, 160)
        rectangle(gameDisplay, (0, 100, 250), 550, 500, 200, 50)
        rectangle(gameDisplay, (0, 155, 255), 555, 505, 190, 40)
        pygame.display.update()
        clock.tick(60)
 
main_loop()
pygame.quit()
quit()