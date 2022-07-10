from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x_cor, y_cor, width, height, speed1, speed2):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed1 = speed1
        self.speed2 = speed2
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed1
        if keys[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed1
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed1
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed1

    def fire(self):
        bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 15, 20, -15, 0)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        switch = randint(0, 1)
        if switch == 0:
            direction = "left"
        else:
            direction = "right"
        if direction == "left":
            self.rect.y += self.speed1
            self.rect.x -= self.speed2
        else:
            self.rect.y += self.speed1
            self.rect.x += self.speed2
        
        global lost

        if self.rect.y > 450:
            self.rect.x = randint(80, 620)
            self.rect.y = randint(-5, 0)
            lost = lost + 1
            self.speed1 = randint(10, 15)
            self.speed2 = randint(10, 15)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed1
        if self.rect.y < 0:
            self.kill()

font.init()
font_stat = font.SysFont('"Arial', 36)
font_end = font.SysFont("Times New Roman", 130)
lose_text = font_end.render("YOU DIED", True, (200, 55, 55))
win_text = font_end.render("VICTORY", True, (200, 55, 55))

window = display.set_mode((700,500))
background = transform.scale(image.load("fon.jpg"), (700,500))

timer = time.Clock()
finish = False
game = True
lost = 0
score = 0
max_lost = 25
max_score = 1


mixer.init()
mixer.music.load("music.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(loops = -1)
shot = mixer.Sound("shot.ogg")
lose = mixer.Sound("lose.ogg")
win = mixer.Sound("win.ogg")

player_image = "player.png"
enemy_image = "enemy.png"
bullet_image = "bullet.png"
game = True
finish = False

player = Player(player_image, 5, 400, 80, 100, 10, 0)

enemies = sprite.Group()
for i in range(1, 10):
    enemy = Enemy(enemy_image, 300, 0, 50, 50, 5, 5)
    enemies.add(enemy)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shot.set_volume(6000)
                shot.play()
                player.fire()
    
    if not finish:
        window.blit(background, (0,0))

        player.update()
        enemies.update()
        bullets.update()

        player.reset()

        enemies.draw(window)
        bullets.draw(window)

        text_win = font_stat.render("Счет: " + str(score), 1, (255, 0, 255))
        window.blit(text_win, (10, 20))

        text_lose = font_stat.render("Пропущено: " + str(lost), 1, (127, 45, 254))
        window.blit(text_lose, (10, 50))

        if sprite.spritecollide(player, enemies, True) or lost >= max_lost:
          finish = True
          window.blit(lose_text, (30, 200))
          lose.set_volume(600)
          lose.play()  

        collisions = sprite.groupcollide(bullets, enemies, True, True)
        for collision in collisions:
            score += 1
            enemy = Enemy(enemy_image, randint(20, 680), randint(-5, 0), 50, 50, 10, 10)
            enemies.add(enemy)

        if score >= max_score:
            finish = True
            window.blit(win_text, (50, 200))
            win.play()
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        time.delay(1000)
        for i in range(1, 10):
            enemy = Enemy(enemy_image, 300, 0, 50, 50, 10, 10)
            enemies.add(enemy)

    time.delay(50)