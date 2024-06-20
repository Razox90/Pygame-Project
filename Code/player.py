from stuff import *

pygame.init()

# Define color variables
BLACK = (0, 0, 0)

def load_frames_from_spritesheet(filename, frame_width, frame_height):
    frames = []
    sheet = pygame.image.load(filename).convert_alpha()
    sheet_rect = sheet.get_rect()

    for y in range(0, sheet_rect.height, frame_height):
        for x in range(0, sheet_rect.width, frame_width):
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(sheet, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame_surface)
    return frames

def load_frames_from_gif(filename):
    image = Image.open(filename)
    frames = []
    try:
        for frame in range(0, image.n_frames):
            image.seek(frame)
            frame_image = image.convert('RGBA')
            frame_surface = pygame.image.fromstring(
                frame_image.tobytes(), frame_image.size, frame_image.mode
            )
            frames.append(frame_surface)
    except EOFError as e:
        print(f"Error loading GIF frames: {e}")
    return frames

def load_frames(filename, frame_width=None, frame_height=None):
    _, ext = os.path.splitext(filename)
    if ext.lower() == '.gif':
        return load_frames_from_gif(filename)
    elif ext.lower() in ['.png', '.jpg', '.jpeg']:
        if frame_width and frame_height:
            return load_frames_from_spritesheet(filename, frame_width, frame_height)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, collision_sprites, animation_speed=5):
        super().__init__()
        self.animations = animations
        self.current_animation = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_frect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.animation_speed = animation_speed  # Frames to wait before updating animation
        self.animation_counter = 0
        self.direction = 'right'  # Initial direction (can be 'left' or 'right')
        self.jumping = False
        self.collsion_sprites = collision_sprites

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        for collision_sprite in self.collsion_sprites:
            if self.rect.bottom and self.rect.colliderect(collision_sprite):
                self.rect.y -= self.speed_y
                self.speed_y = 0

            if  self.rect.right and self.rect.colliderect(collision_sprite):
                self.rect.x -= self.speed_x
                self.speed_x = 0

            if self.rect.left and self.rect.colliderect(collision_sprite):
                self.rect.x -= self.speed_x
                self.speed_x = 0
            
            #if self.rect.bottomright and self.rect.colliderect(collision_sprite):
                #self.rect.bottomleft >= collision_sprite
                

        #if self.rect.bottom > 600:
            #self.rect.bottom = 600
            #self.speed_y = 0

        #if self.rect.bottom < 100:
            #self.rect.bottom = 100
            #self.speed_y = 0

        # Update animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.frame_index += 1
            try:
                if self.frame_index >= len(self.animations[self.current_animation]):
                    self.frame_index = 0
                self.image = self.animations[self.current_animation][self.frame_index]
            except IndexError:
                print(f"IndexError: Animation: {self.current_animation}, Frame index: {self.frame_index}, Animation length: {len(self.animations[self.current_animation])}")

        # Check if jump animation has completed
        if self.current_animation == 'jump' and self.frame_index == len(self.animations['jump']) - 1:
            self.stop()  # Return to idle animation after jump animation completes

        # Flip animation if facing left
        if self.direction == 'left':
            try:
                self.image = pygame.transform.flip(self.animations[self.current_animation][self.frame_index], True, False)
            except IndexError:
                print(f"IndexError: Animation flip failed - Animation: {self.current_animation}, Frame index: {self.frame_index}, Animation length: {len(self.animations[self.current_animation])}")


    def move_left(self):
        self.speed_x = -5
        self.current_animation = 'walk'
        self.direction = 'left'

    def move_right(self):
        self.speed_x = 5
        self.current_animation = 'walk'
        self.direction = 'right'

    def stop(self):
        self.speed_x = 0
        self.current_animation = 'idle'

    def jump(self):
        self.jumping = True
        self.speed_y = -10
        self.current_animation = 'jump'
        self.frame_index = 0

        