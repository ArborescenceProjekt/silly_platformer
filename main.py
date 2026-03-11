import pygame, random
from file_manager import Sound_Manager

width, height = 1600,900

sm = Sound_Manager()
pygame.mixer.init()

ground = ((0,height-50),(width,50)) # ((x=>pos, y=>pos),(x=>dim, y=>dim))

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

class Player:
    def __init__(self, xpos, ypos, xdim, ydim):
        self.position = [xpos, ypos]
        self.dimension = [xdim, ydim]
        self.speed = 5
        self.velocity = [0, 0] # x and y
        self.gravity = 0.05
        self.on_ground = False
        self.jump_pressed = False
        self.trail = []
        self.trail_length = int(abs(self.velocity[0]) * 10) + 8
        self.can_move = True
        self.surf = pygame.Surface(self.dimension, pygame.SRCALPHA)
        self.sfx = True
        self.crash = False
        self.frame = 0
    
    def get_rect(self):
        return pygame.Rect(self.position[0],
                           self.position[1],
                           self.dimension[0],
                           self.dimension[1])

    def move(self, platform):
        if self.can_move:
            if not self.on_ground: # gravité
                self.velocity[1] += self.gravity 
            self.position[0] = self.position[0] + self.speed * self.velocity[0]
            self.position[1] = self.position[1] + self.speed * self.velocity[1]
        player_rect = self.get_rect()

        if self.position[1] + self.dimension[1] >= height - 50: # collision pour le sol
            self.position[1] = height - ground[1][1] - self.dimension[1]
            if self.sfx and self.velocity[1] > 3:
                sm.play("sfx_big_collision")
                self.crash = True
                self.sfx = False
                return True
            self.velocity[1] = 0
            self.on_ground = True
            return False
            
        elif (player_rect.right > platform.left and player_rect.right < platform.left + 10) and (player_rect.bottom > platform.top) and (player_rect.top < platform.bottom): # collision pour le côté gauche d'une platforme
            self.position[0] = platform.left - self.dimension[0]
            self.velocity[0] = 0
        elif (player_rect.left < platform.right and player_rect.left > platform.right - 10) and (player_rect.bottom > platform.top) and (player_rect.top < platform.bottom): # collision pour le côté droit d'une platforme
            self.position[0] = platform.right
            self.velocity[0] = 0
        elif (player_rect.bottom > platform.top) and (player_rect.right > platform.left and player_rect.left < platform.right) and (player_rect.bottom < platform.top + 20): # collision pour le dessus d'une platforme
            self.position[1] = platform.top - self.dimension[1]
            self.velocity[1] = 0
            if self.position[1] == platform.top - self.dimension[1]:
                self.on_ground = True
            if self.sfx and self.velocity[1] > 3:
                sm.play("sfx_big_collision")
                self.crash = True
                self.sfx = False
                return True
            return False
        elif (player_rect.top < platform.bottom) and (player_rect.right > platform.left and player_rect.left < platform.right) and (player_rect.top > platform.bottom - 20): # collision pour le dessous d'une platforme
            self.position[1] = platform.bottom
            self.velocity[1] = 0

    def jump(self):
        if self.on_ground and self.jump_pressed:
            self.velocity[1] = -2
            self.on_ground = False
            sm.play("sfx_jump")
            self.sfx = True

levels = {'level 0': [pygame.Rect(width//8, height-200, width//2, 50), pygame.Rect(width//4, height-350, width//2, 50), pygame.Rect(width//1.5, 0, 50, height//2)],
          'level 1': [pygame.Rect(width//8, height-200, width//2, 50)]}

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(0, height-500, 50, 50)
        self.level = 0
        self.platform_rect = levels
        self.particles = []
    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

    def update(self):
        keys = pygame.key.get_pressed()

        if self.player.crash:             # Zone contrôle temps pour carré orange
            self.player.frame += 1
            if self.player.frame > 20:
                self.player.frame = 0
                self.player.crash = False

        if not (keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]):
            if keys[pygame.K_RIGHT]:
                self.player.velocity[0] = 1
            elif keys[pygame.K_LEFT]:
                self.player.velocity[0] = -1
            else: 
                self.player.velocity[0] = 0
        else:    
            self.player.velocity[0] = 0
        if keys[pygame.K_UP] and self.player.on_ground:
            self.player.jump_pressed = True
            self.player.jump()
        
        if keys[pygame.K_KP_0]:
            self.level = 0
        if keys[pygame.K_KP_1]:
            self.level = 1
        
        if self.player.position[0] < 0 - self.player.dimension[0]:
            self.player.position[0] = width - self.player.dimension[0] - self.player.speed

        if self.player.position[0] > width:
            self.player.position[0] = self.player.speed
        
        self.player.on_ground = False
        
        for i, platform in enumerate(self.platform_rect[f'level {self.level}']):
            if i == 0:
                self.player.can_move = True
            else:
                self.player.can_move = False

            if not self.player.crash:
                if self.player.move(platform):
                    for _ in range(20):
                        self.particles.append(Particle(self.player.position[0] + random.randint(20,30), self.player.position[1] + 50))
                    break
                
        self.player.trail_length = int(abs(self.player.velocity[0]) * 10) + 8
        self.player.trail.append((self.player.position[0], self.player.position[1]))
        if len(self.player.trail) > self.player.trail_length:
            self.player.trail.pop(0)

        for particles in self.particles[:]:
            particles.update()
            if particles.life <= 0:
                self.particles.remove(particles)

        
    def display(self):
        self.screen.fill([50,50,50])
        pygame.draw.rect(screen, (205,205,205), ground)
        for platform in self.platform_rect[f'level {self.level}']:
            pygame.draw.rect(screen, (205,205,205), platform)
        for i, pos in enumerate(self.player.trail):
            alpha = int((i / len(self.player.trail)) * 255)  
            purple_val = int(50 + (i / len(self.player.trail) * 175))
            color = (purple_val, 0, purple_val, alpha)
            x, y = pos
            if i % 2 == 0:
                pygame.draw.rect(self.player.surf, color, (0, 0, *self.player.dimension)) # (x + (len(self.player.trail) - i), y + (len(self.player.trail) - i)*2, self.player.dimension[0] - (len(self.player.trail) - i)*2, self.player.dimension[1] - (len(self.player.trail) - i)*2) pour un trail qui se rétrécie
                screen.blit(self.player.surf, (x, y))
            # miroir gauche
                if x < 0:
                    screen.blit(self.player.surf, (x + width, y))

            # miroir droite
                if x > width - self.player.dimension[0]:
                    screen.blit(self.player.surf, (x - width, y))
        color = (255, 80, 0) if self.player.crash else (0, 0, 0)
        pygame.draw.rect(screen, color, ((self.player.position), (self.player.dimension)))

        for particles in self.particles:
            particles.draw(self.screen)

        if self.player.position[0] < 0:
            pygame.draw.rect(screen, color, ([self.player.position[0] + width, self.player.position[1]], self.player.dimension))
        if self.player.position[0] > width - self.player.dimension[0]:
            pygame.draw.rect(screen, color, ([self.player.position[0] - width, self.player.position[1]], self.player.dimension))
        pygame.display.flip()
    def run(self):
        while self.running:
            self.handling_event()
            self.update()
            self.display()
            self.clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Silly Platformer v.1")
game = Main(screen)
game.run()
pygame.quit()

# ╔═════════════════════════════════════════════╗
# ║         C   E                 P   _R        ║
# ║          \_/     ____N         \_/          ║
# ║      S    \_____/        E     /            ║
# ║       \___/  \            \/  /             ║
# ║   E___/       \        C  /__/__O           ║
# ║      /         \        \/                  ║
# ║     R       O__/\       /_                  ║
# ║               /  \     /  \   __J           ║
# ║              B    \   /   _\_/              ║
# ║                R__/\ /   /  \               ║
# ║                  /  |   /\   E              ║
# ║                 A   |  T  K                 ║
# ║                    / \                      ║
# ║              _____/___\_____                ║
# ║   A r b o r e s c e n c e   P r o j e k t   ║
# ╚═════════════════════════════════════════════╝