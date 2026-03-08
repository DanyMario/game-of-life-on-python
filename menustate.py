import pygame
from state import State


class StartState(State):
    def __init__(self):
        State.__init__(self)

    def userInput(self, event):
        if event.type == pygame.QUIT:
            self.nextState = ""

    def draw(self):
        return

    def update(self):
        return