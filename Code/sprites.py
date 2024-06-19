from stuff import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        if isinstance(surf, pygame.Surface):
            self.image = surf
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.copy()
        else:
            raise ValueError("Expected a pygame.Surface object for surf.")

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect.topleft)

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()