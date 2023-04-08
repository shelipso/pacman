import pygame
from constants import BLOCK_SIZE

def load_textures():
    # Load wall texture
    wall_texture = pygame.image.load("wall_texture.png").convert()
    wall_texture = pygame.transform.scale(wall_texture, (BLOCK_SIZE, BLOCK_SIZE))

    # Create dot texture
    #dot_texture = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    #dot_texture.fill(pygame.Color("green"))
    
    dot_texture = pygame.image.load("pizza.png").convert()
    dot_texture=pygame.transform.scale(dot_texture, (BLOCK_SIZE, BLOCK_SIZE))

    # Load Pac-Man texture
    pacman_texture = pygame.image.load("pacman.png").convert()
    pacman_texture = pygame.transform.scale(pacman_texture, (BLOCK_SIZE, BLOCK_SIZE))

    # Return a dictionary containing the textures
    return {
        "wall_texture": wall_texture,
        "dot_texture": dot_texture,
        "pacman_texture": pacman_texture
    }
