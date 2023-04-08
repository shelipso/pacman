import pygame
import random
from constants import BLOCK_SIZE, WINDOW_SIZE, WALL_COUNT,SCOREBOARD_SIZE

class WallManager:
    def __init__(self, wall_texture):
        self.wall_texture = wall_texture
        self.wall_coordinates = self.generate_walls()

    def generate_walls(self):
        wall_coordinates = []
        
        # Generate outer walls
        for x in range(WINDOW_SIZE[0] // BLOCK_SIZE):
            wall_coordinates.append((x * BLOCK_SIZE, 0))  # Top wall
            wall_coordinates.append((x * BLOCK_SIZE, WINDOW_SIZE[1] - SCOREBOARD_SIZE))  # Bottom wall
        for y in range(WINDOW_SIZE[1] // BLOCK_SIZE):
            wall_coordinates.append((0, y * BLOCK_SIZE-SCOREBOARD_SIZE))  # Left wall
            wall_coordinates.append((WINDOW_SIZE[0] - BLOCK_SIZE, y * BLOCK_SIZE-SCOREBOARD_SIZE))  # Right wall

        # Generate inner walls
        for _ in range(WALL_COUNT):
            start_x = random.randint(0, WINDOW_SIZE[0] // BLOCK_SIZE - 1) * BLOCK_SIZE
            start_y = random.randint(0, (WINDOW_SIZE[1]-SCOREBOARD_SIZE) // BLOCK_SIZE - 1) * BLOCK_SIZE
            direction = random.choice([(1, 0), (0, 1)])
            length = random.randint(4, 10)
            
            # check if walls cross the scoreboard area
            if start_y + length * direction[1] * BLOCK_SIZE>WINDOW_SIZE[1]-SCOREBOARD_SIZE:
              length=(BLOCK_SIZE>WINDOW_SIZE[1]-SCOREBOARD_SIZE-start_y)//BLOCK_SIZE

            wall_coordinates.extend([(start_x + i * direction[0] * BLOCK_SIZE,
                                      start_y + i * direction[1] * BLOCK_SIZE)
                                     for i in range(length)])

        return wall_coordinates

    def draw(self, screen):
        for coordinate in self.wall_coordinates:
            wall_rect = pygame.Rect(coordinate[0], coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
            screen.blit(self.wall_texture, wall_rect)

    def check_collision(self, pacman_rect):
        for wall_coordinate in self.wall_coordinates:
            wall_rect = pygame.Rect(wall_coordinate[0], wall_coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
            if pacman_rect.colliderect(wall_rect):
                return True
        return False
    
    def is_coordinate_on_wall(self, coordinate):
        for wall_coordinate in self.wall_coordinates:
            wall_rect = pygame.Rect(wall_coordinate[0], wall_coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
            if wall_rect.collidepoint(coordinate):
                return True
        return False
    
