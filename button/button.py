import pygame

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)

BUTTON_STYLE = {"hover_color": BLUE,
                "clicked_color": GREEN,
                "clicked_font_color": BLACK,
                "hover_font_color": ORANGE}

class Button():
    def __init__(self, top, function, text):
        self.rect = pygame.Rect((670, top, 100, 50))
        self.color = RED
        self.function = function
        self.clicked = False
        self.hovered = False
        self.clicked_text = None
        self.setKwargs(BUTTON_STYLE)
        self.text = text
        self.hover_text = self.font.render(self.text, True, self.hover_font_color)
        self.clicked_text = self.font.render(self.text, True, self.clicked_font_color)
        self.text = self.font.render(self.text, True, self.font_color)

    def drawAndCheck(self, surface):
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.function is not None:
                    self.function()
                    self.clicked = True
        self.update(surface)

    def setKwargs(self, kwargs):
        settings = {"text": None,
                    "font": pygame.font.Font(None, 25),
                    "call_on_release": True,
                    "hover_color": None,
                    "clicked_color": None,
                    "font_color": pygame.Color("white"),
                    "hover_font_color": None,
                    "clicked_font_color": None,
                    "click_sound": None,
                    "hover_sound": None}
        for kwarg in kwargs:
            settings[kwarg] = kwargs[kwarg]
        self.__dict__.update(settings)

    def update(self, surface):
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        surface.fill(pygame.Color("black"), self.rect)
        surface.fill(color, self.rect.inflate(-4, -4))
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False
