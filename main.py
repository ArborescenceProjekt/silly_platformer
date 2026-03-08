import pygame, random

width, height = 800,600
ground = ((0,height-50),(width,50)) # ((x=>pos, y=>pos),(x=>dim, y=>dim))

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
            self.position[1] = height - self.dimension[1]*2
            self.velocity[1] = 0
            self.on_ground = True
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
        elif (player_rect.top < platform.bottom) and (player_rect.right > platform.left and player_rect.left < platform.right) and (player_rect.top > platform.bottom - 20): # collision pour le dessous d'une platforme
            self.position[1] = platform.bottom
            self.velocity[1] = 0

    def jump(self):
        if self.on_ground and self.jump_pressed:
            self.velocity[1] = -2
            self.on_ground = False
        
class Main:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(0, height-500, 50, 50)
        self.platform_rect = [pygame.Rect(width//8, height-200, width//2, 50), pygame.Rect(width//4, height-350, width//2, 50)]
    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

    def update(self):
        keys = pygame.key.get_pressed()

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
        
        if self.player.position[0] < 0 - self.player.dimension[0]:
            self.player.position[0] = width - self.player.dimension[0] - self.player.speed

        if self.player.position[0] > width:
            self.player.position[0] = self.player.speed
        
        self.player.on_ground = False
        
        for i, platform in enumerate(self.platform_rect):
            if i == 0:
                self.player.can_move = True
            else:
                self.player.can_move = False

            self.player.move(platform)
        
        self.player.trail_length = int(abs(self.player.velocity[0]) * 10) + 8
        self.player.trail.append((self.player.position[0], self.player.position[1]))
        if len(self.player.trail) > self.player.trail_length:
            self.player.trail.pop(0)


        
    def display(self):
        self.screen.fill([50,50,50])
        pygame.draw.rect(screen, (205,205,205), ground)
        for platform in self.platform_rect:
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

        pygame.draw.rect(screen, (0,0,0), ((self.player.position), (self.player.dimension)))
        if self.player.position[0] < 0:
            pygame.draw.rect(screen, (0,0,0), ([self.player.position[0] + width, self.player.position[1]], self.player.dimension))
        if self.player.position[0] > width - self.player.dimension[0]:
            pygame.draw.rect(screen, (0,0,0), ([self.player.position[0] - width, self.player.position[1]], self.player.dimension))
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