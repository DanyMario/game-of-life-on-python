import pygame

from state import State
from gridstate import GridState

class GameState(State):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.largefont = pygame.font.Font("font.ttf", 50)
        self.mediumfont = pygame.font.Font("font.ttf", 30)
        self.smallfont = pygame.font.Font("font.ttf", 12)
        self.isPlaying = False
        self.last_update = pygame.time.get_ticks()
        self.update_delay = 1000  # 1000 ms = 1 second
        # Grid
        if self.screen.get_size() == (500,600):
            self.rows, self.cols = 20, 20
        elif self.screen.get_size() == (800,700):
            self.rows, self.cols = 40, 40
        else:
            self.rows, self.cols = 60, 60

        self.grid = GridState((self.rows, self.cols))
        self.genRN=0
        self.title = self.smallfont.render(f"Gen: {self.genRN}", True, "white")

        self.cell_width = self.screen.get_width()  // self.cols
        self.cell_height = (self.screen.get_height()-100) // self.rows

        # Optional: initial colors
        self.visual_grid = [[(50, 50, 50) for _ in range(self.cols)] for _ in range(self.rows)]


    def draw(self):
        self.screen.fill((30, 30, 30))
        for r in range(self.rows):
            mx, my = pygame.mouse.get_pos()
            hover_row = my // self.cell_height
            hover_col = mx // self.cell_width

            for c in range(self.cols):
                rect = pygame.Rect(c * self.cell_width, r *self. cell_height, self.cell_width - 1, self.cell_height - 1)
                pygame.draw.rect(self.screen, self.visual_grid[r][c], rect)

                if r == hover_row and c == hover_col and hover_row < self.rows:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
        if self.genRN != self.grid.gen:
            self.genRN+=1
            for coor,status in self.grid.to_be.items():
                if self.visual_grid[coor[0]][coor[1]] == (255, 255, 255):
                    if not status:
                        self.visual_grid[coor[0]][coor[1]] = (50, 50, 50)
                if self.visual_grid[coor[0]][coor[1]] == (50, 50, 50):
                    if status:
                        self.visual_grid[coor[0]][coor[1]] = (255, 255, 255)

        grid_height = self.rows * self.cell_height
        center_x = self.screen.get_width() // 2
        center_y = grid_height + 50
        self.title = self.mediumfont.render(f"Gen: {self.genRN}", True, "white")
        self.screen.blit(self.title,self.title.get_rect(center=(center_x+150, center_y)))

        if self.isPlaying:
            bar_width = 12
            bar_height = 40

            pygame.draw.rect(self.screen, (255, 255, 255),
                             (center_x - 20, center_y - bar_height // 2, bar_width, bar_height))

            pygame.draw.rect(self.screen, (255, 255, 255),
                             (center_x + 8, center_y - bar_height // 2, bar_width, bar_height))
        else:
            grid_height = self.rows * self.cell_height
            center_x = self.screen.get_width() // 2
            center_y = grid_height + 50

            play_triangle = [
                (center_x - 20, center_y - 25),
                (center_x - 20, center_y + 25),
                (center_x + 25, center_y)
            ]

            pygame.draw.polygon(self.screen, (255, 255, 255), play_triangle)

    def update(self):
        self.draw()
        if self.isPlaying:
            current_time = pygame.time.get_ticks()

            if current_time - self.last_update > self.update_delay:
                self.grid.update_grid()
                self.grid.next_gen()
                self.last_update = current_time

    def userInput(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "StartState"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.grid.update_grid()
                self.grid.next_gen()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_height = self.rows * self.cell_height

            # Click in bottom control bar
            if my > grid_height:
                self.isPlaying = not self.isPlaying
                return

            # Click inside grid
            row = my // self.cell_height
            col = mx // self.cell_width

            if row < self.rows and col < self.cols:
                if self.visual_grid[row][col] == (255, 255, 255):
                    self.visual_grid[row][col] = (50, 50, 50)
                    self.grid.set_dead((row, col), True)
                else:
                    self.visual_grid[row][col] = (255, 255, 255)
                    self.grid.set_alive((row, col), True)