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
    startScreen = StartState(screen)
    curScreen = startScreen

    while True:
        for event in pygame.event.get():
            curScreen.userInput(event)

        curScreen.update()
        curScreen.draw()
        pygame.display.update()
        clock.tick(60)

        if curScreen.isFinished:
            if curScreen.nextState == "GameState":
                # Resize window based on selection
                if hasattr(curScreen, "selected_size"):
                    screen = pygame.display.set_mode(curScreen.selected_size)

                # Go to game state
                curScreen = GameState(screen)

            elif curScreen.nextState == "StartState":
                curScreen = StartState(screen)
            else:
                quit()