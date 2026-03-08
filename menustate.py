import pygame

from state import State


class StartState(State):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen

        # Font
        self.largefont = pygame.font.Font("font.ttf", 50)
        self.mediumfont = pygame.font.Font("font.ttf", 30)
        self.smallfont = pygame.font.Font("font.ttf", 12)



        # Text
        self.title = self.largefont.render("CONWAY'S GAME OF LIVE", True, "white")
        self.textSmall = self.mediumfont.render("SMALL", True, "white")
        self.textMedium = self.mediumfont.render("MEDIUM", True, "white")
        self.textLarge = self.mediumfont.render("LARGE", True, "white")

        # Button size
        button_width = 250
        button_height = 70

        # Buttons
        self.buttonSmall = pygame.Rect(0, 0, button_width, button_height)
        self.buttonMedium = pygame.Rect(0, 0, button_width, button_height)
        self.buttonLarge = pygame.Rect(0, 0, button_width, button_height)

        # Screen center
        self.center_x = self.screen.get_width() // 2
        self.center_y = self.screen.get_height() // 2

        # Vertical spacing
        start_y = 200
        spacing = 100

        self.buttonSmall.center = (self.center_x, start_y)
        self.buttonMedium.center = (self.center_x, start_y + spacing)
        self.buttonLarge.center = (self.center_x, start_y + spacing * 2)


    def userInput(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttonSmall.collidepoint(mouse):
                self.selected_size = (500, 600)
                self.isFinished = True
                self.nextState = "GameState"
            elif self.buttonMedium.collidepoint(mouse):
                self.selected_size = (800, 700)
                self.isFinished = True
                self.nextState = "GameState"
            elif self.buttonLarge.collidepoint(mouse):
                self.selected_size = (1200, 1000)
                self.isFinished = True
                self.nextState = "GameState"

    def drawButton(self, rect, label, font, base, hover):
        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):
            color = hover
            textColor = "black"
        else:
            color = base
            textColor = "white"

        pygame.draw.rect(self.screen, color, rect, border_radius=15)

        text = font.render(label, True, textColor)
        textRect = text.get_rect(center=rect.center)
        self.screen.blit(text, textRect)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.title,self.title.get_rect(center=(self.center_x, self.center_y-200)))
        self.drawButton(self.buttonSmall, "SMALL", self.mediumfont, (0, 0, 0), (255, 255, 255))
        self.drawButton(self.buttonMedium, "MEDIUM", self.mediumfont, (0, 0, 0), (255, 255, 255))
        self.drawButton(self.buttonLarge, "LARGE", self.mediumfont, (0, 0, 0), (255, 255, 255))

    def update(self):
        self.draw()
        return
