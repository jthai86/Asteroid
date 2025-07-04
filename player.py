import pygame
import random
import math
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 200
        self.max_speed = 300
        self.friction = 0.99
        self.shoot_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0

    def draw(self, screen):
        t = pygame.time.get_ticks() / 1000

        if self.invulnerable:

            flicker = (math.sin(t * 10) + 1) / 2
            if flicker > 0.5:
                pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)            

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.draw_flame(screen, t)

    def draw_flame(self, screen, t):
        backward = pygame.Vector2(0, 1).rotate(self.rotation + 180)
        flame_tip = self.position + backward * self.radius * 1.2
        left = self.position + backward.rotate(30) * self.radius * 0.5
        right = self.position + backward.rotate(-30) * self.radius * 0.5
        
        flicker =(math.sin(t * 30) + 1) / 2

        r = 255
        g = max(100, min(250, int(100 +flicker * 150)))
        b = 0

        flame_color = (r, g, b)

        pygame.draw.polygon(screen, flame_color, [flame_tip, left, right])            

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.apply_thrust(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.apply_thrust(-dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.velocity *= self.friction
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity * dt

        self.wrap_around_screen()        

    def apply_thrust(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.acceleration * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def wrap_around_screen(self):
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT       

    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable = True
        self.invulnerable_timer = 1.0