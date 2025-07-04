import pygame
import random
from constants import *
from circleshape import CircleShape
from explosion import Explosion


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.explosion_frames = []

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        Explosion(self.position, self.explosion_frames, *Explosion.containers)
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = a * 1.2
        a1.explosion_frames = self.explosion_frames  # Pass frames to child
        for container in self.containers:
            container.add(a1)

        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a2.velocity = b * 1.2
        a2.explosion_frames = self.explosion_frames
        for container in self.containers:
            container.add(a2)