
# TODO:
# LEVEL CONSTRUCTOR

# file imports
from config   import *
from particle import *
from player   import *

import json

pygame.mixer.init()

levels = {
    'level 0': [pygame.Rect(width//8, height-200, width//2, 50), pygame.Rect(width//4, height-350, width//2, 50), pygame.Rect(width//1.5, 0, 50, height//2)],
    'level 1': [pygame.Rect(width//8, height-200, width//2, 50)],
    'level 2': [],
    'level 3': []
}

with open("levels/level-2.json") as file:
    data = json.load(file)
    for collider in data["colliders"]:
        levels['level 2'].append(
            pygame.Rect(*map(lambda x: x * 8, collider))
        )



with open("levels/level-3.json") as file:
    data = json.load(file)
    for collider in data["colliders"]:
        levels['level 3'].append(
            pygame.Rect(*map(lambda i: i * 2, collider)) # collider = [x, y, w, h]
        )


class Main:

    def __init__(self, screen):
        self.screen        = screen
        self.running       = True
        self.clock         = pygame.time.Clock()
        self.player        = Player(0, height - 500, 50, 50)
        self.level         = 0
        self.platform_rect = levels
        self.particles     = []

    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
    def update(self):
        keys = pygame.key.get_pressed()

        # Control the player freeze time
        # after falling from a high platform (the orange square)
        if self.player.crash:
            self.player.frame += 1
            if self.player.frame > 20:
                self.player.frame = 0
                self.player.crash = False

        # in case user holds left & right buttons at the same time
        if not (keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]):

            if keys[pygame.K_RIGHT]:
                self.player.velocity[0] = 1
            
            elif keys[pygame.K_LEFT]:
                self.player.velocity[0] = -1
            
            else: 
                self.player.velocity[0] = 0    

        else:    
            self.player.velocity[0] = 0 # very needed

        if keys[pygame.K_UP] and self.player.on_ground:
            self.player.jump_pressed = True
            self.player.jump()
        

        # __ ! TEMPORARY LEVEL SWITCH CODE ! __

        if keys[pygame.K_0]: # NUMPAD 0
            self.level = 0

        if keys[pygame.K_1]: # NUMPAD 1
            self.level = 1
        
        if keys[pygame.K_2]: # NUMPAD 2
            self.level = 2
        
        if keys[pygame.K_3]: # NUMPAD 3
            self.level = 3
        
        # _____________________________________

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

app_caption = "Gloopy platformer" # (formerly "Silly Platformer v.1")
app_icon = pygame.image.load("app_icon.jpg")

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption(app_caption)
    pygame.display.set_icon(app_icon)

    game = Main(screen)

    game.run()
    pygame.quit()

# badass art xD
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