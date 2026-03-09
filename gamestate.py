import pygame
from dropdown import Dropdown

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
        self.to_be_reset = None
        self.title = self.smallfont.render(f"Gen: {self.genRN}", True, "white")

        self.cell_width = self.screen.get_width()  // self.cols
        self.cell_height = (self.screen.get_height()-100) // self.rows

        self.visual_grid = [[(50, 50, 50) for _ in range(self.cols)] for _ in range(self.rows)]

        self.speed_dropdown = Dropdown(
            40, self.screen.get_height() - 70,
            150, 40,
            self.mediumfont,
            (60, 60, 60),
            (80, 80, 80),
            ["1x", "2x", "5x", "10x",".5x"]
        )


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
            self.genRN=self.grid.gen
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
        self.draw_generation()


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

        self.speed_dropdown.draw(self.screen)

    def draw_generation(self):
        grid_bottom = self.rows * self.cell_height

        # Left margin: e.g., 10% of screen width from the left
        left_margin = int(self.screen.get_width() * 0.85)

        # Vertical center in the area below the grid
        padding = (self.screen.get_height() - grid_bottom) // 2
        y = grid_bottom + padding

        x = left_margin
        gen_text = self.mediumfont.render(f"Gen: {self.genRN}", True, (255, 255, 255))
        text_rect = gen_text.get_rect(center=(x, y))
        self.screen.blit(gen_text, text_rect)

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
        result = self.speed_dropdown.handle_event(event)
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "StartState"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.grid.update_grid()
                self.grid.next_gen()
            if event.key == pygame.K_r:
                previous_alive = self.grid.reset()
                self.visual_grid = [[(50, 50, 50) for _ in range(self.cols)] for _ in range(self.rows)]
                self.genRN = 0
                self.last_update = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_height = self.rows * self.cell_height
            center_x = self.screen.get_width() // 2
            center_y = grid_height + 50

            if result:  # handle selection first
                self.speed_dropdown.selected = result
                speed_map = {
                    ".5x": 1500,
                    "1x": 1000,
                    "2x": 500,
                    "5x": 200,
                    "10x": 100
                }
                self.update_delay = speed_map[result]
                self.last_update = pygame.time.get_ticks()
                return  # stop here, no grid click

            if self.speed_dropdown.open or result:
                return

            if self.isPlaying:
                bar_width = 12
                bar_height = 40
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (center_x - 20, center_y - bar_height // 2, bar_width, bar_height))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (center_x + 8, center_y - bar_height // 2, bar_width, bar_height))
            else:
                play_triangle = [
                    (center_x - 20, center_y - 25),
                    (center_x - 20, center_y + 25),
                    (center_x + 25, center_y)
                ]
                pygame.draw.polygon(self.screen, (255, 255, 255), play_triangle)

            center_y = self.rows * self.cell_height + 50
            button_rect = pygame.Rect(center_x - 20, center_y - 25, 45, 50)
            if button_rect.collidepoint(mx, my):
                self.isPlaying = not self.isPlaying
                return

            row = my // self.cell_height
            col = mx // self.cell_width

            if row < self.rows and col < self.cols:
                if self.visual_grid[row][col] == (255, 255, 255):
                    self.visual_grid[row][col] = (50, 50, 50)
                    self.grid.set_dead((row, col), True)
                else:
                    self.visual_grid[row][col] = (255, 255, 255)
                    self.grid.set_alive((row, col), True)
