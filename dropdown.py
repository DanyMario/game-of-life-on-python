import pygame

class Dropdown:
    def __init__(self, x, y, w, h, font, main_color, option_color, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main_color = main_color
        self.option_color = option_color
        self.options = options
        self.selected = options[0]
        self.open = False

    def draw(self, screen):
        # main box
        pygame.draw.rect(screen, self.main_color, self.rect)
        text = self.font.render(self.selected, True, "white")
        screen.blit(text, text.get_rect(center=self.rect.center))

        # draw options if open
        if self.open:
            for i, option in enumerate(self.options):
                rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y - (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )

                pygame.draw.rect(screen, self.option_color, rect)

                text = self.font.render(option, True, "white")
                screen.blit(text, text.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # toggle dropdown
            if self.rect.collidepoint(mx, my):
                self.open = not self.open
                return None

            # check options
            if self.open:
                for i, option in enumerate(self.options):
                    rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y - (i+1)*self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )

                    if rect.collidepoint(mx, my):
                        self.selected = option
                        self.open = False
                        return option

                self.open = False
        return None