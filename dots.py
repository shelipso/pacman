import pygame
import random
from constants import BLOCK_SIZE, WINDOW_SIZE, NUM_BLOCKS_WIDE, NUM_BLOCKS_HIGH, DOT_COUNT

class DotManager:
    def __init__(self, dot_texture, wall_manager):
        self.dot_texture = dot_texture
        self.wall_manager = wall_manager
        self.dot_coordinates = self.generate_dots()

    def generate_dots(self):
        dot_coordinates = []

        for i in range(DOT_COUNT):
            dot_coordinate = None
            while not dot_coordinate:
                x = random.randint(0, NUM_BLOCKS_WIDE - 4) * BLOCK_SIZE + BLOCK_SIZE * 2
                y = random.randint(0, NUM_BLOCKS_HIGH - 4) * BLOCK_SIZE + BLOCK_SIZE * 2
                dot_coordinate = (x, y)

                if dot_coordinate in dot_coordinates or self.wall_manager.is_coordinate_on_wall(dot_coordinate):
                    dot_coordinate = None
                    continue

            dot_coordinates.append(dot_coordinate)

        return dot_coordinates


    def draw(self, screen):
        for coordinate in self.dot_coordinates:
            dot_rect = pygame.Rect(coordinate[0], coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
            screen.blit(self.dot_texture, dot_rect)

    def check_collision(self, pacman_rect):
        for dot_coordinate in self.dot_coordinates:
            dot_rect = pygame.Rect(dot_coordinate[0], dot_coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
            if pacman_rect.colliderect(dot_rect):
                self.dot_coordinates.remove(dot_coordinate)
                return True
        return False
