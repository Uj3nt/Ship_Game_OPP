import pygame
import random

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("resources/images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 60))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player:
    def __init__(self, model, h, w, x, y, screen_width, screen_height):
        self.model = pygame.image.load(model).convert_alpha()
        self.model = pygame.transform.scale(self.model, (w, h))
        self.rect = self.model.get_rect(topleft=(x, y))
        self.speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullets = []
        self.dx = 0

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -self.speed
            elif event.key == pygame.K_d:
                self.dx = self.speed
            elif event.key == pygame.K_SPACE:
                self.shoot()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                self.dx = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.append(bullet)

        shoot = pygame.mixer.Sound("resources/sounds/shot.mp3")
        shoot.play()

    def update(self):
        self.rect.x += self.dx
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.rect.bottom > 0]

    def draw(self, screen):
        screen.blit(self.model, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 1500
        self.running = True
        self.player = None
        self.score = 0

    def check_event(self, event):
        if self.player and self.running:
            self.player.check_event(event)

    def update(self, delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.top >= self.height:
                self.running = False

        if self.player:
            self.player.update()
            self.check_collisions()

    def draw(self, screen):
        if self.running:
            for enemy in self.enemies:
                enemy.draw(screen)
            if self.player:
                self.player.draw(screen)

            font = pygame.font.Font(None, 36)
            current_score = font.render(f"{self.score}", True, (255, 255, 255))
            screen.blit(current_score, (860, 10))
        else:
            font = pygame.font.Font("resources/fonts/main_font.ttf", 80)
            end = font.render(f"Конец игры", True, (255, 255, 255))
            score = font.render(f"Ваш счет: {self.score}", True, (255, 255, 255))

            screen.blit(end, (220, 220))
            screen.blit(score, (220, 290))



    def check_collisions(self):
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1

                    kill = pygame.mixer.Sound("resources/sounds/kill.mp3")
                    kill.play()
                    break

    def spawn_enemy(self):
        x = random.randint(10, self.width - 40)
        speed = random.randint(2, 6)
        self.enemies.append(Enemy(x, -40, speed))

    def reset(self):
        self.enemies.clear()
        self.running = True
        self.score = 0
        if self.player:
            self.player.rect.x = 450
            self.player.bullets.clear()