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

if __name__ == "__main__":
    main()