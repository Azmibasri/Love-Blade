import pygame

class Enemy(pygame.sprite.Sprite):
    # --- TAMBAHKAN PARAMETER 'speed=3' DI SINI ---
    def __init__(self, x , y , player_object, speed=3):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=(x,y))

        self.player = player_object
        
        # --- GUNAKAN PARAMETER SPEED ---
        self.speed = speed 

        self.pos = pygame.math.Vector2(x,y)

    def update(self):
        enemy_vec = self.pos
        player_vec = pygame.math.Vector2(self.player.rect.center)

        if enemy_vec.distance_to(player_vec) > 0:
            direction = (player_vec - enemy_vec).normalize()
            self.pos += direction * self.speed
            self.rect.center = (round(self.pos.x), round(self.pos.y))