import os
from stuff import *
from sprites import Sprite, AllSprites, BorderSprite
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Test')
        self.clock = pygame.time.Clock()
        self.done = False

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()


        idle_frames = self.load_frames("..\Pygame Project\graphics\Character\Idle\Idle.gif")
        walk_frames = self.load_frames("..\Pygame Project\graphics\Character\Run\Run.gif")
        jump_frames = self.load_frames("..\Pygame Project\graphics\Character\Jumlp-All\Jump-All-Sheet.png", 64, 64)

        self.animations = {
            'idle': idle_frames,
            'walk': walk_frames,
            'jump': jump_frames
        }
        
        self.player = Player(100, 400, self.animations, self.collision_sprites, animation_speed=2)
        self.all_sprites.add(self.player)


        self.import_assets()
        self.setup(self.tmx_maps['world'], 'player_start')

    def load_frames_from_spritesheet(self, filename, frame_width, frame_height):
        frames = []
        sheet = pygame.image.load(filename).convert_alpha()
        sheet_rect = sheet.get_rect()

        for y in range(0, sheet_rect.height, frame_height):
            for x in range(0, sheet_rect.width, frame_width):
                frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame_surface.blit(sheet, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame_surface)
        return frames

    def load_frames_from_gif(self, filename):
        image = Image.open(filename)
        frames = []
        for frame in range(0, image.n_frames):
            image.seek(frame)
            frame_image = image.convert('RGBA')
            frame_surface = pygame.image.fromstring(
                frame_image.tobytes(), frame_image.size, frame_image.mode
            )
            frames.append(frame_surface)
        return frames

    def load_frames(self, filename, frame_width=None, frame_height=None):
        _, ext = os.path.splitext(filename)
        if ext.lower() == '.gif':
            return self.load_frames_from_gif(filename)
        elif ext.lower() in ['.png', '.jpg', '.jpeg']:
            if frame_width and frame_height:
                return self.load_frames_from_spritesheet(filename, frame_width, frame_height)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def debug(self, function_purpose, task):
        print(function_purpose, task)

    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame(join('data', 'maps', 'world.tmx'))
        }
        self.debug('game.py(import_assets): ', self.tmx_maps)

    def setup(self, tmx_map, player_start_pos):
        for layer in ['Terrain', 'Terrain_Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        


        

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

        if keys[pygame.K_SPACE]:
            self.player.jump()
            
        if keys[pygame.K_ESCAPE]:
            self.done = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
           

    def run(self):
        while not self.done:
            self.handle_events()
            self.handle_player_input()

            self.player.game = self  # Pass the game instance to the player

            self.player.update()
            self.all_sprites.update()

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)
