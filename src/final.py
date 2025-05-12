import pygame

class Player():
    def __init__(self):
        self.pos = (800, 300)
        self.size = 64
        self.frame_size = (self.size,self.size)
        self.frame = pygame.image.load("src/Sprites/Cat/idle/cat_frame_idle_0.png").convert_alpha()
        self.surface = self.update_surface()
        self.velocity = 350
        self.jumpPower = 10
        self.gravity = 0
        self.gravityStrength = 14
        self.y, self.x = (0,0)
        self.isJumping = False
        self.player_rect = pygame.Rect(self.pos[0], self.pos[1], self.frame_size[0], self.frame_size[1])

        self.player_state = "idle"
        self.last_state = "idle"
        self.facing_left = False
        self.current_frame = 0
        self.isattacking = False
        self.timer = 0

    
    def update(self, dt):
        self.movement(dt)
        self.attack()
        self.update_player_state(dt)
        self.surface = self.update_surface()

    def movement(self,dt):    
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
             dx = -self.velocity * dt
             self.facing_left = True
        if keys[pygame.K_d]:
            dx =  self.velocity * dt
            self.facing_left = False
        if keys[pygame.K_SPACE] and not self.isJumping:
            self.isJumping = True
            self.gravity = self.jumpPower
        
        self.gravity -= self.gravityStrength * dt
        dy = -self.gravity

        self.x = dx
        self.y = dy

    
    def check_collision(self, platform_rect):
        dx = self.x
        dy = self.y

        self.pos = (self.pos[0] + dx, self.pos[1])
        self.player_rect.topleft = self.pos
        
        for platform in platform_rect:
            if self.player_rect.colliderect(platform):
                if dx > 0:
                    self.pos = (platform.left - self.size, self.pos[1])
                elif dx < 0:
                    self.pos = (platform.right, self.pos[1])
                self.player_rect.topleft = self.pos
        

        self.pos = (self.pos[0], self.pos[1] + dy)
        self.player_rect.topleft = self.pos
        

        for platform in platform_rect:
            if self.player_rect.colliderect(platform):
                if dy > 0: 
                    self.pos = (self.pos[0], platform.top - self.size)
                    self.gravity = 0
                    self.isJumping = False
            
                elif dy < 0:
                    self.pos = (self.pos[0], platform.bottom)
                    self.gravity = 0
            
                self.player_rect.topleft = self.pos

    def attack(self):
        buttton = pygame.mouse.get_pressed()
        if buttton[0]:
            if self.player_state == "idle" or self.player_state == "walking":
                self.player_state = "attacking"
                self.isattacking = True

    def update_player_state(self,dt):
        keys = pygame.key.get_pressed()
        if not self.isattacking:
            if self.player_state == "idle":
                if keys[pygame.K_a] or keys[pygame.K_d]:
                    self.player_state = "walking"
                elif keys[pygame.K_SPACE]:
                    self.player_state = "jumping"
                elif self.y > 1:
                    self.player_state = "falling"
            
            elif self.player_state == "walking":
                if self.x == 0:
                    self.player_state = "idle"
                elif keys[pygame.K_SPACE]:
                    self.player_state = "jumping"
                elif self.y > 1:
                    self.player_state = "falling"
            
            elif self.player_state == "jumping":
                if self.y > 1:
                    self.player_state = "falling"
            
            elif self.player_state == "falling":
                if self.y > 0 and self.gravity > -1:
                    self.player_state = "idle"

        if self.last_state != self.player_state:
            self.current_frame = 0
            self.timer = 0
            self.last_state = self.player_state
            
        if self.player_state == "idle":
            self.player_animation(dt, 1, "idle_", True)
        elif self.player_state == "walking":
            self.player_animation(dt, 4, "walking_", True)
        elif self.player_state == "jumping":
            self.player_animation(dt, 3, "jumping_", False)
        elif self.player_state == "falling":
            self.player_animation(dt, 3, "falling_", False)
        elif self.player_state == "attacking":
            self.player_animation(dt, 4, "attacking_", False)
        
        
    def player_animation(self,dt, frame_count, frame_prefix, can_loop = False):

        prefix = f"src/Sprites/Cat/{self.player_state}/cat_frame_{frame_prefix}"
            
        self.timer += dt
        if self.timer >= .080:
            if self.current_frame < frame_count:
                image_path = f"{prefix}{self.current_frame}.png"
                self.frame = pygame.image.load(image_path).convert_alpha()
                if not self.facing_left:
                    self.frame = pygame.transform.flip(self.frame, True, False)
                self.current_frame += 1
                self.timer = 0
        
        if self.current_frame >= frame_count:
            if can_loop:
                self.current_frame = 0
            else:
                if self.player_state == "attacking":
                    self.player_state = "idle"
                    self.isattacking = False
                self.current_frame = frame_count - 1

    def update_surface(self):
        return pygame.transform.scale(self.frame, self.frame_size)   

    def draw(self, surface):
        self.surface.set_alpha(255)
        surface.blit(self.surface,self.pos)
    
class Platform():
    def __init__(self, pos,type):
        self.pos = pos
        self.size = 0
        self.type = type
        self.image_path = self.platform_type()
        self.surface = self.update_surface()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1] - 15)

    def update_surface(self):
        if self.image_path:
            image = pygame.image.load(self.image_path).convert_alpha()
            if self.type == 1:
                self.size = (400, 80)
            elif self.type == 2:
                self.size = (100, 80)
            elif self.type == 3:
                self.size = (200, 80)
            return pygame.transform.scale(image, self.size)
        else:
            surf = pygame.Surface(self.size)
            surf.fill(pygame.Color(0, 255, 0))  
            return surf
    
    def draw(self, surface, index = None):
        surface.blit(self.surface,self.pos)
        label = f"T{self.type}"
        if index is not None:
            label = f"T{self.type} {index}"
        text = pygame.font.Font(None, 24).render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2))
        surface.blit(text, text_rect)

    def platform_type(self):
            return f"src/Sprites/Platform/platform{self.type}.png"
        

class Game():
    def __init__(self):
        self.player = Player()

        self.platform_attributes = [
    
    (50, 560, 3), 
    (400, 730, 2),
    (1150, 680, 1), 

    
    (300, 300, 3), 
    (800, 520, 3),

    (650, 350, 2), 
    (900, 800, 2), 
    (650,700,2),     
    (1050, 350, 2),    
    (1400, 450, 2),       
   
    (1250, 180, 3), 
    (1600, 250, 2), 
    
    
    (100, 120, 2), 
    (730, 100, 2), 

    (1700, 700, 2), 
    (1850, 600, 2), 
        ]

        self.platforms = []
        for x,y, type in self.platform_attributes:
            platform = Platform((x,y),type)
            self.platforms.append(platform)

        self.timer = 10
        self.score = 0
       
    
    def draw_game(self,screen):
        self.player.draw(screen)
        for i,platform in enumerate(self.platforms):
            platform.draw(screen, i)
            
    
    def update_game(self,dt):
        self.player.update(dt)
        self.player.check_collision([platform.rect for platform in self.platforms])
        self.lose_game()

    def lose_game(self):
        if self.player.pos[1] > 1000:
            self.player.pos = (800, 300)
            self.timer = 10
            self.score = 0

def main():
    pygame.init()

    info = pygame.display.Info()

    screen_width = info.current_w - 100
    screen_height = info.current_h - 100

    screen = pygame.display.set_mode((screen_width, screen_height - 100))
    clock = pygame.time.Clock()

    background_image = pygame.image.load("src/Sprites/Background/Background.png").convert()
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