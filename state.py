import pygame
from abc import ABC, abstractmethod

class State(ABC):
    screen = None
    screenshot = None
    @classmethod
    def set_screen(cls, screen: pygame.Surface):
        cls.screen = screen
    def __init__(self, next_state: str = ""):
        self.nextState = next_state
        self.isFinished = False

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def userInput(self, events):
        pass