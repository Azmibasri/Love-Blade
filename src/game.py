import pygame
import sys
import random
import os  # Tambahkan os untuk mengecek file highscore
from src.settings import *
from src.player import Player, Bullet, PowerUp, LaserBlast
from src.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Love Blade")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        # Tambahkan ini di dalam __init__ dan reset_game (di bawah self.current_time = 0)
        self.enemies_killed = 0
        self.difficulty_level = 0

        # --- SISTEM WAKTU & HIGH SCORE ---
        self.high_score = self.load_high_score()
        self.start_time = pygame.time.get_ticks() # Mencatat waktu mulai
        self.current_time = 0

        # Inisialisasi Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()    # Grup khusus laser
        self.powerups = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Musuh awal
        self.my_enemy_1 = Enemy(100, 100, self.player)
        self.my_enemy_3 = Enemy(700, 500, self.player)
        self.all_sprites.add(self.my_enemy_1, self.my_enemy_3)
        self.enemies.add(self.my_enemy_1, self.my_enemy_3)
        
        # Timer musuh otomatis
        self.SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_ENEMY_EVENT, 2000)

        self.SPAWN_POWERUP_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPAWN_POWERUP_EVENT, 20000)


    # --- FUNGSI LOAD & SAVE HIGH SCORE ---
    def load_high_score(self):
        # Mengecek apakah file highscore.txt ada, jika ada baca angkanya
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as file:
                try:
                    return int(file.read())
                except:
                    return 0
        return 0

    def save_high_score(self):
        # Menyimpan high score baru ke dalam file
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def reset_game(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.my_enemy_1 = Enemy(100, 100, self.player)
        self.my_enemy_3 = Enemy(700, 500, self.player)
        self.all_sprites.add(self.my_enemy_1, self.my_enemy_3)
        self.enemies.add(self.my_enemy_1, self.my_enemy_3)
        
        self.game_over = False
        
        # Reset waktu mulai ke waktu sekarang
        self.start_time = pygame.time.get_ticks()
        self.current_time = 0

        # Tambahkan ini di dalam __init__ dan reset_game (di bawah self.current_time = 0)
        self.enemies_killed = 0
        self.difficulty_level = 0

    def events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.reset_game()
                    continue 

                if event.type == self.SPAWN_ENEMY_EVENT:
                    self.spawn_new_enemy()
                    
                # --- MUNCULKAN ITEM POWER-UP ---
                if event.type == self.SPAWN_POWERUP_EVENT:
                    self.spawn_powerup()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        # Cek apakah mode laser aktif
                        if self.player.laser_active:
                            new_laser = LaserBlast(self.player.rect.centerx, self.player.rect.centery, mouse_pos)
                            self.all_sprites.add(new_laser)
                            self.lasers.add(new_laser)
                        else:
                            new_bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, mouse_pos)
                            self.all_sprites.add(new_bullet)
                            self.bullets.add(new_bullet)

    def spawn_new_enemy(self):
            # Base jumlah musuh adalah 1, ditambah level kesulitan
            spawn_amount = 1 + self.difficulty_level
            
            # Base kecepatan adalah 3, ditambah 0.5 untuk setiap level
            enemy_speed = 3.0 + (self.difficulty_level * 0.5)

            # Looping sebanyak jumlah musuh yang harus muncul
            for _ in range(spawn_amount):
                random_x = random.randint(50, WIDTH - 50)
                random_y = random.randint(50, HEIGHT - 50)
                
                # Berikan nilai kecepatan yang baru ke objek Enemy
                new_enemy = Enemy(random_x, random_y, self.player, speed=enemy_speed)
                
                self.all_sprites.add(new_enemy)
                self.enemies.add(new_enemy)

    def spawn_powerup(self):
            random_x = random.randint(50, WIDTH - 50)
            random_y = random.randint(50, HEIGHT - 50)
            new_powerup = PowerUp(random_x, random_y)
            self.all_sprites.add(new_powerup)
            self.powerups.add(new_powerup)

    def update(self):
            if not self.game_over:
                self.current_time = (pygame.time.get_ticks() - self.start_time) // 1000
                self.all_sprites.update()

                # --- CEK TABRAKAN PEMAIN DENGAN ITEM POWERUP ---
                power_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
                if power_hits:
                    self.player.laser_active = True
                    self.player.laser_start_time = pygame.time.get_ticks() # Catat waktu ambil item

                # --- CEK DURASI 10 DETIK LASER ---
                if self.player.laser_active:
                    waktu_sekarang = pygame.time.get_ticks()
                    if waktu_sekarang - self.player.laser_start_time > 10000: # 10.000 ms = 10 detik
                        self.player.laser_active = False

                # Tabrakan Peluru Biasa (Peluru hilang, Musuh mati)
                killed_by_bullet = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
                if killed_by_bullet:
                    self.enemies_killed += len(killed_by_bullet)
                    self.difficulty_level = self.enemies_killed // 15

                # --- TABRAKAN LASER (Laser TIDAK HILANG, Musuh mati - Tembus/Piercing) ---
                # Parameter False pada grup laser membuat laser tidak hancur saat menabrak
                killed_by_laser = pygame.sprite.groupcollide(self.enemies, self.lasers, True, False)
                if killed_by_laser:
                    self.enemies_killed += len(killed_by_laser)
                    self.difficulty_level = self.enemies_killed // 15

                # Tabrakan Pemain vs Musuh
                hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
                if hits:
                    self.player.health -= 1.5 
                    if self.player.health <= 0:
                        self.player.health = 0
                        self.game_over = True
                        if self.current_time > self.high_score:
                            self.high_score = self.current_time
                            self.save_high_score()

    def draw_health_bar(self, x, y, health, max_health):
        BAR_LENGTH = 200
        BAR_HEIGHT = 20
        fill = (health / max_health) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

    def draw(self):
        self.screen.fill(BLACK)             
        self.all_sprites.draw(self.screen)  
        
        # --- UI WAKTU & HIGH SCORE ---
        font_ui = pygame.font.SysFont(None, 30)
        
        if not self.game_over:
            self.draw_health_bar(10, 10, self.player.health, self.player.max_health)
            kill_text = font_ui.render(f"Kill: {self.enemies_killed}", True, WHITE)
            self.screen.blit(kill_text, (10, 40))
            # Render teks waktu saat ini (di tengah atas)
            time_text = font_ui.render(f"Waktu: {self.current_time}s", True, WHITE)
            self.screen.blit(time_text, (WIDTH // 2 - 50, 10))
            
            # Render teks High Score (di pojok kanan atas)
            hs_text = font_ui.render(f"High Score: {self.high_score}s", True, WHITE)
            self.screen.blit(hs_text, (WIDTH - 180, 10))
            if self.player.laser_active:
                            sisa_waktu = 10 - ((pygame.time.get_ticks() - self.player.laser_start_time) // 1000)
                            laser_text = font_ui.render(f"LASER AKTIF: {sisa_waktu}s", True, (0, 255, 255))
                            self.screen.blit(laser_text, (WIDTH // 2 - 80, HEIGHT - 40))
            
        else:
            self.player.kill() 
            font_big = pygame.font.SysFont(None, 74)
            text_go = font_big.render("GAME OVER", True, (255, 0, 0))
            rect_go = text_go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            
            font_small = pygame.font.SysFont(None, 36)
            text_restart = font_small.render("Klik Kiri Untuk Main Lagi", True, WHITE)
            rect_restart = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            
            # Tampilkan skor akhir saat mati
            text_score = font_small.render(f"Kamu bertahan selama: {self.current_time} detik", True, (255, 255, 0))
            rect_score = text_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            self.screen.blit(text_go, rect_go)
            self.screen.blit(text_score, rect_score)
            self.screen.blit(text_restart, rect_restart)

        pygame.display.flip()               

    def run(self):
        while self.running:
            self.clock.tick(FPS)  
            self.events()         
            self.update()         
            self.draw()           
            
        pygame.quit()
        sys.exit()