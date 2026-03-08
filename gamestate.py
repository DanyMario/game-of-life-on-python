import pygame

from state import State

class GameState(State):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # Grid
        if self.screen.get_size() == (500,600):
            self.rows, self.cols = 20, 20
        elif self.screen.get_size() == (800,700):
            self.rows, self.cols = 40, 40
        else:
            self.rows, self.cols = 60, 60

        self.cell_width = self.screen.get_width()  // self.cols
        self.cell_height = (self.screen.get_height()-100) // self.rows

        # Optional: initial colors
        self.visual_grid = [[(50, 50, 50) for _ in range(self.cols)] for _ in range(self.rows)]


    def update(self):
        return

    def draw(self):
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(c * self.cell_width, r *self. cell_height, self.cell_width - 1, self.cell_height - 1)
                pygame.draw.rect(self.screen, self.visual_grid[r][c], rect)


    def userInput(self, event):
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "StartState"
            self.selected_size = (500, 500)