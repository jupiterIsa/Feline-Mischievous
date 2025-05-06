import pygame

class Player():
    def __init__(self):
        self.pos = (400, 300)
        self.size = 15
        self.surface = self.update_surface()
        self.velocity = 400
        self.jumpPower = 10
        self.gravity = 0
        self.gravityStrength = 10
        self.isJumping = False
        self.player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
    
    def update(self, dt, platform_rect):
        self.movement(dt, platform_rect)
        
if __name__ == "__main__":
    main()