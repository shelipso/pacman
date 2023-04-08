# scoreboard.py
import pygame
from constants import WINDOW_SIZE, FONT_NAME, FONT_SIZE,SCOREBOARD_SIZE

class Scoreboard:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.score = 0
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.timelapsed=0

    def update_score(self, points):
        self.score += points

    def draw(self, screen):
        self.timelapsed=(pygame.time.get_ticks() - self.start_ticks) // 1000
        timer_text = self.font.render(f"Time: { self.timelapsed}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

        screen.blit(timer_text, (10, WINDOW_SIZE[1]-SCOREBOARD_SIZE//2))
        screen.blit(score_text, (WINDOW_SIZE[0] - 150, WINDOW_SIZE[1]-SCOREBOARD_SIZE//2))
