import pygame

class Button:
    def __init__(self, x, y, w, h, image, hover_sound=None, click_sound=None, action=None):
        self.base_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.base_image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hover_sound = None
        self.click_sound = None

        if hover_sound:
            self.hover_sound = pygame.mixer.Sound(hover_sound)
        if click_sound:
            self.click_sound = pygame.mixer.Sound(click_sound)

        self.action = action
        self.hovered = False
        self.base_size = (w, h)
        self.was_hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            prev_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)

            # Воспроизведение звука при наведении
            if self.hovered and not prev_hovered:
                if self.hover_sound:
                    self.hover_sound.play()

            # Изменение размера
            if self.hovered != prev_hovered:
                if self.hovered:
                    new_size = (int(self.base_size[0] * 1.01), int(self.base_size[1] * 1.01))
                    self.image = pygame.transform.scale(self.base_image, new_size)
                    self.rect = self.image.get_rect(center=self.rect.center)
                else:
                    self.image = pygame.transform.scale(self.base_image, self.base_size)

        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.click_sound:
                self.click_sound.play()
            if self.action:
                self.action()

class Menu:
    def __init__(self, background, screen, display = False):
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (900, 750))
        self.screen = screen
        self.elements = []
        self.display = display

    def draw(self):
        if self.display:
            self.screen.blit(self.background, (0, 0))
            for element in self.elements:
                element.draw(self.screen)

    def add_element(self, element):
        self.elements.append(element)

    def game(self, tick):
        for element in self.elements:
            if hasattr(element, 'update'):
                element.update(tick)
    def update(self, event):
        if self.display:
            for element in self.elements:
                element.check_event(event)

    def activate(self):
        self.display = True

    def deactivate(self):
        self.display = False

    def scene_change(self, menu):
        menu.activate()
        self.deactivate()
