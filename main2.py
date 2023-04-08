import pygame
from constants import WINDOW_SIZE
from textures import load_textures
from walls import WallManager
from dots import DotManager
from pacman import PacMan
from sounds import load_sound, play_sound, load_music, play_music, stop_music, make_noise, MOVE_EVENT, EAT_EVENT, HIT_WALL_EVENT, FINSHED_EVENT
from scoreboard import Scoreboard
from button import Button
import sys




# Initialize Pygame
pygame.init()
pygame.font.init()  

scoreboard = Scoreboard()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pac-Man")

def show_end_screen(screen, score, time_elapsed):
    make_noise(FINSHED_EVENT)
    
    screen_copy = screen.copy()
    end_screen = pygame.Surface((400, 200))
    end_screen.set_alpha(200)
    
    font = pygame.font.Font(None, 36)
    message = f"Finished! Score: {score} Time: {time_elapsed:.2f} seconds"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 50))

    quit_button = Button(50, 120, 120, 40, "Quit", (255, 0, 0), font)
    replay_button = Button(230, 120, 120, 40, "Replay", (0, 255, 0), font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
            elif replay_button.is_clicked(event):
                return "replay"

        screen.blit(screen_copy, (0, 0))
        screen.blit(end_screen, ((WINDOW_SIZE[0] - 400) // 2, (WINDOW_SIZE[1] - 200) // 2))
        text_rect.topleft = ((WINDOW_SIZE[0] - 400) // 2 + 200 - text_rect.width // 2, (WINDOW_SIZE[1] - 200) // 2 + 50)
        screen.blit(text, text_rect)

        quit_button.rect.topleft = ((WINDOW_SIZE[0] - 400) // 2 + 50, (WINDOW_SIZE[1] - 200) // 2 + 120)
        quit_button.draw(screen)

        replay_button.rect.topleft = ((WINDOW_SIZE[0] - 400) // 2 + 230, (WINDOW_SIZE[1] - 200) // 2 + 120)
        replay_button.draw(screen)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pacman")

    textures = load_textures()
    wall_manager = WallManager(textures["wall_texture"])
    dot_manager = DotManager(textures["dot_texture"],wall_manager)
    pacman = PacMan(textures["pacman_texture"],wall_manager)

    clock = pygame.time.Clock()
    running = True
    scoreboard = Scoreboard()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pacman.handle_input(event)

        pacman.move()
        if wall_manager.check_collision(pacman.rect):
            pacman.undo_move()
            make_noise(HIT_WALL_EVENT)

        if dot_manager.check_collision(pacman.rect):
            scoreboard.update_score(10)
            make_noise(EAT_EVENT)

        if not dot_manager.dot_coordinates:
            running = False
        
        screen.fill((0, 0, 0))
        scoreboard.draw(screen)
        
        wall_manager.draw(screen)
        dot_manager.draw(screen)
        pacman.draw(screen)
       
        pygame.display.flip()
        clock.tick(60)

    return screen,running, scoreboard.score,scoreboard.timelapsed
   
    
if __name__ == "__main__":
    running=True
    while True:
        
        screen, running, score, timelapsed = main()        
        result = show_end_screen(screen, score, timelapsed)
        if result != "replay":
            break

# Clean up
pygame.quit()
