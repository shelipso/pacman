import pygame
from constants import BLOCK_SIZE
from walls import WallManager
from sounds import load_sound, play_sound, load_music, play_music, stop_music, make_noise, MOVE_EVENT, EAT_EVENT, HIT_WALL_EVENT    

class PacMan:
    def __init__(self, pacman_texture, wall_manager):
        self.pacman_texture = pacman_texture
        self.rect = pygame.Rect(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.wall_manager = wall_manager
        self.last_direction = None
        self.key_down_active = False
        self.last_key_time = pygame.time.get_ticks()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_down_active = True
        elif event.type == pygame.KEYUP:
            self.key_down_active = False

    def undo_move(self):
        if self.last_direction == "left":
            self.rect.move_ip(BLOCK_SIZE, 0)
        elif self.last_direction == "right":
            self.rect.move_ip(-BLOCK_SIZE, 0)
        elif self.last_direction == "up":
            self.rect.move_ip(0, BLOCK_SIZE)
        elif self.last_direction == "down":
            self.rect.move_ip(0, -BLOCK_SIZE)

    def move(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_key_time

        if self.key_down_active and elapsed_time > 60:
            self.last_key_time = current_time
            move_direction = None

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                move_direction = "left"
            elif keys[pygame.K_RIGHT]:
                move_direction = "right"
            elif keys[pygame.K_UP]:
                move_direction = "up"
            elif keys[pygame.K_DOWN]:
                move_direction = "down"

            if move_direction:
                if move_direction == "left":
                    self.rect.move_ip(-BLOCK_SIZE, 0)
                    self.pacman_texture = pygame.transform.rotate(self.pacman_texture, 0)
                    if self.wall_manager.check_collision(self.rect):
                        self.rect.move_ip(+BLOCK_SIZE, 0)       
                        make_noise(HIT_WALL_EVENT)             
                elif move_direction == "right":
                    self.rect.move_ip(BLOCK_SIZE, 0)
                    if self.wall_manager.check_collision(self.rect):
                        self.rect.move_ip(-BLOCK_SIZE, 0)  
                        make_noise(HIT_WALL_EVENT)                  
                    self.pacman_texture = pygame.transform.rotate(self.pacman_texture, 180)
                elif move_direction == "up":
                    self.rect.move_ip(0, -BLOCK_SIZE)
                    if self.wall_manager.check_collision(self.rect):
                        self.rect.move_ip(0,BLOCK_SIZE) 
                        make_noise(HIT_WALL_EVENT)                        
                    self.pacman_texture = pygame.transform.rotate(self.pacman_texture, 90)
                elif move_direction == "down":
                    self.rect.move_ip(0, BLOCK_SIZE)
                    if self.wall_manager.check_collision(self.rect):
                        self.rect.move_ip(0,-BLOCK_SIZE)
                        make_noise(HIT_WALL_EVENT)                                             
                    self.pacman_texture = pygame.transform.rotate(self.pacman_texture, 270)

                self.last_direction = move_direction

    def draw(self, screen):
        self.pacman_texture = pygame.transform.scale(self.pacman_texture, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(self.pacman_texture, self.rect)
