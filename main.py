import pygame
import random

pygame.init()

WINDOW_SIZE = (600, 600)
score = 0
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pac-Man")

BLOCK_SIZE = 20

NUM_BLOCKS_WIDE = 20
NUM_BLOCKS_HIGH = 20

# Load textures
wall_texture = pygame.image.load("wall_texture.png").convert()
wall_texture = pygame.transform.scale(wall_texture, (BLOCK_SIZE, BLOCK_SIZE))
dot_texture = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
dot_texture.fill(pygame.Color("yellow"))

# Generate random coordinates for walls
WALL_COUNT = 5
wall_coordinates = []

for x in range(WINDOW_SIZE[0] // BLOCK_SIZE):
    wall_coordinates.append((x * BLOCK_SIZE, 0))  # Top wall
    wall_coordinates.append((x * BLOCK_SIZE, WINDOW_SIZE[1] - BLOCK_SIZE))  # Bottom wall
for y in range(WINDOW_SIZE[1] // BLOCK_SIZE):
    wall_coordinates.append((0, y * BLOCK_SIZE))  # Left wall
    wall_coordinates.append((WINDOW_SIZE[0] - BLOCK_SIZE, y * BLOCK_SIZE))  # Right wall


for _ in range(WALL_COUNT):
    # Generate a random starting position and direction for the wall
    start_x = random.randint(0, WINDOW_SIZE[0] // BLOCK_SIZE - 1) * BLOCK_SIZE
    start_y = random.randint(0, WINDOW_SIZE[1] // BLOCK_SIZE - 1) * BLOCK_SIZE
    direction = random.choice([(1, 0), (0, 1)])

    # Determine the length of the wall
    length = random.randint(4, 10)

    # Create a rectangle for the wall based on the starting position, direction, and length
    wall_coordinates.extend([(start_x + i * direction[0] * BLOCK_SIZE,
                              start_y + i * direction[1] * BLOCK_SIZE)
                             for i in range(length)])

# Generate dot coordinates
DOT_COUNT = 50

# Initialize dot coordinates
dot_coordinates = []
for i in range(DOT_COUNT):
    dot_coordinate = None
    while not dot_coordinate:
        x = random.randint(0, NUM_BLOCKS_WIDE - 4) * BLOCK_SIZE+BLOCK_SIZE*2
        y = random.randint(0, NUM_BLOCKS_HIGH - 4) * BLOCK_SIZE+BLOCK_SIZE*2
        dot_coordinate = (x, y)
        for wall_coordinate in wall_coordinates:
            if dot_coordinate == wall_coordinate:
                dot_coordinate = None
                break
        for dot_coordinate2 in dot_coordinates:
            if dot_coordinate == dot_coordinate2:
                dot_coordinate = None
                break
    dot_coordinates.append(dot_coordinate)


# Initialize Pac-Man
pacman_color = pygame.Color("yellow")
pacman_radius = BLOCK_SIZE // 2
pacman_rect = pygame.Rect(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
pygame.draw.circle(screen, pacman_color, pacman_rect.center, pacman_radius)

# Initialize variables
last_direction = None
move_event = pygame.USEREVENT + 1
eat_event = pygame.USEREVENT + 2
hit_wall_event = pygame.USEREVENT + 3
stop_sound_event = pygame.USEREVENT + 4



def make_noise(event_type):
    if event_type == move_event:
        # Play a sound effect for moving Pac-Man
        sound = pygame.mixer.Sound("pacman_move.wav")
        #sound.play()
            
    elif event_type == eat_event:
        # Play a sound effect for eating a dot
        sound = pygame.mixer.Sound("dot_eat.wav")
        sound.play()

    elif event_type == hit_wall_event:
        # Play a sound effect for hitting a wall
        pygame.mixer.Sound("wall_hit.wav").play()
        
    waittime = 60# sound.get_length() * 1000 # convert seconds to milliseconds
    pygame.time.set_timer(stop_sound_event, waittime)


def check_collision():
    global pacman_rect, last_direction, dot_coordinates, score

    for wall_coordinate in wall_coordinates:
        wall_rect = pygame.Rect(wall_coordinate[0], wall_coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
        if pacman_rect.colliderect(wall_rect):
            # Move Pac-Man back to the previous block in the direction of movement
            if last_direction == "left":
                pacman_rect.move_ip(BLOCK_SIZE, 0)
            elif last_direction == "right":
                pacman_rect.move_ip(-BLOCK_SIZE, 0)
            elif last_direction == "up":
                pacman_rect.move_ip(0, BLOCK_SIZE)
            elif last_direction == "down":
                pacman_rect.move_ip(0, -BLOCK_SIZE)

            # Reset the last direction of movement
            last_direction = None

            # Play a sound effect for hitting a wall
            make_noise(hit_wall_event)

    for dot_coordinate in dot_coordinates:
        dot_rect = pygame.Rect(dot_coordinate[0], dot_coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
        if pacman_rect.colliderect(dot_rect):
            dot_coordinates.remove(dot_coordinate)
            score += 10

            # Play a sound effect for eating a dot
            make_noise(eat_event)

    if last_direction:
        # Play a sound effect for moving Pac-Man
        make_noise(move_event)

    for event in pygame.event.get():
        if event.type == stop_sound_event:
            pygame.mixer.stop()


# Game loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and last_direction != "right":
                pacman_rect.move_ip(-BLOCK_SIZE, 0)
                last_direction = "left"
            elif event.key == pygame.K_RIGHT and last_direction != "left":
                pacman_rect.move_ip(BLOCK_SIZE, 0)
                last_direction = "right"
            elif event.key == pygame.K_UP and last_direction != "down":
                pacman_rect.move_ip(0, -BLOCK_SIZE)
                last_direction = "up"
            elif event.key == pygame.K_DOWN and last_direction != "up":
                pacman_rect.move_ip(0, BLOCK_SIZE)
                last_direction = "down"

    check_collision()

    # Draw everything on the screen
    screen.fill(pygame.Color("black"))
    for coordinate in wall_coordinates:
        wall_rect = pygame.Rect(coordinate[0], coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
        screen.blit(wall_texture, wall_rect)
    
    for coordinate in dot_coordinates:
        dot_rect = pygame.Rect(coordinate[0], coordinate[1], BLOCK_SIZE, BLOCK_SIZE)
        screen.blit(dot_texture, dot_rect)
        
    pygame.draw.circle(screen, pacman_color, pacman_rect.center, pacman_radius)

    pygame.display.update()

# Clean up
pygame.quit()

