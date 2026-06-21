import pygame
import math # Tambahkan ini untuk rotasi laser
from src.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        
        self.speed = 5
        self.max_health = 100
        self.health = 100
        
        # --- ATRIBUT SKILL LASER ---
        self.laser_active = False
        self.laser_start_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

# --- KELAS PELURU BIASA (Tetap Sama) ---
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect(center=(x, y))
        
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 10 
        
        mouse_vec = pygame.math.Vector2(target_pos)
        if mouse_vec != self.pos:
            self.direction = (mouse_vec - self.pos).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()

# --- KELAS ITEM POWER-UP BARU ---
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Membuat kotak hijau sebagai item power-up
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) # Warna Hijau
        self.rect = self.image.get_rect(center=(x, y))

# --- KELAS PELURU LASER BARU (MENEMBUS MUSUH) ---
class LaserBlast(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        # Membuat bentuk dasar laser: panjang dan berwarna cyan
        self.original_image = pygame.Surface((60, 10), pygame.SRCALPHA)
        self.original_image.fill((0, 255, 255)) 
        
        self.pos = pygame.math.Vector2(x, y)
        mouse_vec = pygame.math.Vector2(target_pos)
        
        if mouse_vec != self.pos:
            self.direction = (mouse_vec - self.pos).normalize()
            # Kalkulasi sudut untuk merotasi gambar laser sesuai arah mouse
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.rotate(self.original_image, angle)
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.image = self.original_image
            
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20 # Laser melesat lebih cepat dari peluru biasa

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()