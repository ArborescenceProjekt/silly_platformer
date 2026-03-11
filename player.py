from config import *

class Player:
    def __init__(self, xpos, ypos, xdim, ydim):
        self.position     = [xpos, ypos]
        self.dimension    = [xdim, ydim]
        self.speed        = 5
        self.velocity     = [0, 0] # x and y
        self.gravity      = 0.05
        self.on_ground    = False
        self.jump_pressed = False
        self.trail        = []
        self.trail_length = int(abs(self.velocity[0]) * 10) + 8
        self.can_move     = True
        self.surf         = pygame.Surface(self.dimension, pygame.SRCALPHA)
        self.sfx          = True
        self.crash        = False
        self.frame        = 0
    
    def get_rect(self):
        return pygame.Rect(self.position[0],
                           self.position[1],
                           self.dimension[0],
                           self.dimension[1])

    def move(self, platform):
        if self.can_move:
            # logique de la gravité)
            if not self.on_ground: 
                self.velocity[1] += self.gravity 
            self.position[0] = self.position[0] + self.speed * self.velocity[0]
            self.position[1] = self.position[1] + self.speed * self.velocity[1]
        
        player_rect = self.get_rect()

        # ground collision (collision pour le sol)
        if self.position[1] + self.dimension[1] >= height - 50: 
            self.position[1] = height - ground[1][1] - self.dimension[1]
            
            # ground collision sound effect
            if self.sfx and self.velocity[1] > 3:
                sm.play("sfx_big_collision")
                self.crash = True
                self.sfx = False
                return True
            
            self.velocity[1] = 0
            self.on_ground = True
            return False
        
        # collision logic:
        # for the left side of platform (collision pour le côté gauche d'une platforme)
        elif (player_rect.right > platform.left and player_rect.right < platform.left + 10) and (player_rect.bottom > platform.top) and (player_rect.top < platform.bottom): 
            self.position[0] = platform.left - self.dimension[0]
            self.velocity[0] = 0
        
        # for the right side of platform (collision pour le côté droit d'une platforme)
        elif (player_rect.left < platform.right and player_rect.left > platform.right - 10) and (player_rect.bottom > platform.top) and (player_rect.top < platform.bottom):
            self.position[0] = platform.right
            self.velocity[0] = 0
        
        # for the top side of platform (collision pour le dessus d'une platforme)
        elif (player_rect.bottom > platform.top) and (player_rect.right > platform.left and player_rect.left < platform.right) and (player_rect.bottom < platform.top + 20):
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
        
        # for the bottom side of platform (collision pour le dessous d'une platforme)
        elif (player_rect.top < platform.bottom) and (player_rect.right > platform.left and player_rect.left < platform.right) and (player_rect.top > platform.bottom - 20):
            self.position[1] = platform.bottom
            self.velocity[1] = 0

    def jump(self):
        if self.on_ground and self.jump_pressed:
            self.velocity[1] = -2
            self.on_ground = False
            sm.play("sfx_jump")
            self.sfx = True