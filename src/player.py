# src/player.py
import pygame
from src.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Membuat kotak biru sebagai perwakilan karakter
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        
        # Mengambil posisi kotak dan menempatkannya di tengah layar
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        # Kecepatan gerak karakter
        self.speed = 5
        
        # --- ATRIBUT NYAWA ---
        self.max_health = 100
        self.health = 100

    def update(self):
        # Deteksi input keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Menjaga agar karakter tidak keluar dari layar
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        # Membuat kotak kecil berwarna kuning sebagai peluru
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0)) # Warna Kuning (RGB)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Posisi awal peluru dalam bentuk vektor float agar pergerakannya mulus
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 10 # Kecepatan peluru terbang
        
        # Hitung arah dari pemain menuju posisi klik mouse
        mouse_vec = pygame.math.Vector2(target_pos)
        
        # Jika posisi mouse sama dengan posisi pemain, peluru diam (mencegah crash)
        if mouse_vec != self.pos:
            self.direction = (mouse_vec - self.pos).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        # Gerakkan peluru sesuai arah dan kecepatannya
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        # Hapus peluru dari memory jika sudah keluar dari batas layar (settings WIDTH & HEIGHT)
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()