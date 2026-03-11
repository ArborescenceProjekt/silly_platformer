from config import *

class Particle:
    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [random.uniform(-4, 4), random.uniform(-6, -1)]
        self.life = 255
        self.size = random.randint(4, 8)

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.velocity[1] += 0.2
        self.life -= 10
    
    def draw(self, screen):
        surf = pygame.Surface((self.size, self.size))
        surf.set_alpha(self.life)
        surf.fill((0, 0, 0))
        screen.blit(surf, self.position)

        if self.position[0] > width - self.size:
            screen.blit(surf, (self.position[0] - width, self.position[1]))
        elif self.position[0] < 0:
            screen.blit(surf, (self.position[0] + width, self.position[1]))