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

    def movement(self,dt, platform_rect):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
             dx = -self.velocity * dt
        if keys[pygame.K_d]:
            dx =  self.velocity * dt
        if keys[pygame.K_SPACE] and not self.isJumping:
            self.isJumping = True
            self.gravity = self.jumpPower
        
        self.gravity -= self.gravityStrength * dt
        dy = -self.gravity


        self.pos = (self.pos[0] + dx, self.pos[1])
        self.player_rect.topleft = self.pos
        
        if self.player_rect.colliderect(platform_rect):   
            if dx > 0:
                self.pos = (platform_rect.left - self.size, self.pos[1])
           
            elif dx < 0:
                self.pos = (platform_rect.right, self.pos[1])
            self.player_rect.topleft = self.pos
        

        self.pos = (self.pos[0], self.pos[1] + dy)
        self.player_rect.topleft = self.pos
        
        if self.player_rect.colliderect(platform_rect):
            if dy > 0: 
                self.pos = (self.pos[0], platform_rect.top - self.size)
                self.gravity = 0
                self.isJumping = False
         
            elif dy < 0:
                self.pos = (self.pos[0], platform_rect.bottom)
                self.gravity = 0
        
            self.player_rect.topleft = self.pos  

    def update_surface(self):
        surf = pygame.Surface((self.size,self.size))
        surf.fill(pygame.Color(212, 0, 255))
        return surf        

    def draw(self, surface):
        self.surface.set_alpha(255)
        surface.blit(self.surface,self.pos)


class Platform():
    def __init__(self, pos, size, image_path):
        self.pos = pos
        self.size = size
        self.image_path = image_path
        self.surface = self.update_surface()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update_surface(self):
        if self.image_path:
            image = pygame.image.load(self.image_path).convert_alpha()
            return pygame.transform.scale(image, self.size)
        else:
            surf = pygame.Surface(self.size)
            surf.fill(pygame.Color(0, 255, 0))  
            return surf
    
    def draw(self, surface):
        surface.blit(self.surface,self.pos)

class Game():
    def __init__(self):
        self.player = Player()
        self.platform = Platform((000, 500), (500, 80), "Sprites/Platform/platform1.png")
        self.timer = 10
        self.score = 0
    
    def draw_game(self,screen):
        self.player.draw(screen)
        self.platform.draw(screen)
    
    def update_game(self,dt):
        self.player.update(dt,self.platform.rect)

def main():
    pygame.init()

    info = pygame.display.Info()

    screen_width = info.current_w - 100
    screen_height = info.current_h - 100

    screen = pygame.display.set_mode((screen_width, screen_height - 100), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    background_image = pygame.image.load("Sprites/Background/Background.png").convert()
    background = pygame.transform.scale(background_image, (screen_width, screen_height))

    game = Game()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                background = pygame.transform.scale(background_image, (screen_width, screen_height))
        

        #  Game Logic
        game.update_game(dt)

        # Render
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        game.draw_game(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()