import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from gameover import GameOverScreen
from explosion import Explosion


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background_img = pygame.image.load("image.png").convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    explosion_frames = Explosion.generate_placeholder_explosions()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField(explosion_frames)

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player) and not player.invulnerable:
                lives -= 1
                if lives <= 0:
                    game_over = GameOverScreen(screen, font, score)
                    game_over.run()
                    return
                else:
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)   

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 100

        screen.blit(background_img, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(lives_text, (10, 40))    

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

   