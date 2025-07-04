import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverScreen:
    def __init__(self, screen, font, score):
        self.screen = screen
        self.font = font
        self.score = score

    def run(self):
        print("GameOverScreen.run() called")
        self.screen.fill("black")
        game_over_text = self.font.render("GAME OVER", True, "red")
        score_text = self.font.render(f"Final Score: {self.score}", True, "blue")
        prompt_text = self.font.render("Press any key to quit", True, "yellow")

        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2))
        self.screen.blit(prompt_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False    