import pygame

MOVE_EVENT = "move"
EAT_EVENT = "eat"
HIT_WALL_EVENT = "hit_wall"
FINSHED_EVENT = "finished"

def load_sound(file_path):
    return pygame.mixer.Sound(file_path)

def play_sound(sound):
    sound.play()

def load_music(file_path):
    pygame.mixer.music.load(file_path)

def play_music():
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()


# fiinished.wav is success-fanfare-trumpets-6185.mp3
# It is from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=6185">Pixabay</a>

def success_music():
    pygame.mixer.music.stop()


def make_noise(event_type):
    if event_type == MOVE_EVENT:
        sound = load_sound("pacman_move.wav")
    elif event_type == EAT_EVENT:
        sound = load_sound("dot_eat.wav")
        play_sound(sound)
    elif event_type == HIT_WALL_EVENT:
        sound = load_sound("wall_hit.wav")
        play_sound(sound)
    elif event_type== FINSHED_EVENT:
        sound = load_sound("fiinished.wav")
        play_sound(sound)
    
