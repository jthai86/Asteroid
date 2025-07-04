import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, frames, *groups):
        super().__init__(*groups)
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)
        self.timer = 0.05
        self.current_frame = 0
        self.elapsed_time = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)    

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.timer:
            self.elapsed_time = 0
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()

    @staticmethod
    def generate_placeholder_explosions():
        frames = []
        for size in range(10, 50, 5):
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(image, (255, 128, 0), (size // 2, size // 2), size // 2)
            frames.append(image)
        return frames                         