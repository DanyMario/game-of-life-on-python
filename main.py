import pygame

from gamestate import GameState
from menustate import StartState


if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()


    # Main Window setup
    screen_width = 500  # Screen width (can be adjusted)
    screen_height = 500  # Screen height (can be adjusted)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game of Life")

    gameState = 0
    startScreen = StartState()
    curScreen = startScreen

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                curScreen.isFinished = True
            curScreen.userInput(event)

        if curScreen.isFinished:
            if curScreen.nextState == "GameState":
                curScreen.isFinished = False
                curScreen.nextState = ""
                curScreen = StartState
            elif curScreen.nextState == "StartState":
                curScreen.isFinished = False
                curScreen = startScreen
            else:
                quit()

        curScreen.update()
        pygame.display.update()
