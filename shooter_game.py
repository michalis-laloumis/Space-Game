#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None,80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))
max_lost = 3
img_bullet = 'bullet.png'
font2=font.Font(None,36)

img_enemy = "ufo.png"
score=0
lost=0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_hero = "rocket.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet1=Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullet2=Bullet(img_bullet, self.rect.centerx-30, self.rect.top + 20, 15,20,-15)
        bullet3=Bullet(img_bullet, self.rect.centerx+30, self.rect.top + 20, 15,20,-15)
        bullets.add(bullet1)
        bullets.add(bullet2)
        bullets.add(bullet3)
        global achieved
        if achieved==10:
            print('ok')
            bullet_sup=Bullet(img_bullet, self.rect.centerx, self.rect.top, 300,400,-30)
            bullets.add(bullet_sup)
            achieved=0


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1          

bullets = sprite.Group()
bullets_super  = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<0:
            self.kill()




win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

finish = False
run = True
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
img_ast = "asteroid.png"
life =3
asteroids = sprite.Group()
for i in range (2):
    asteroid=Enemy(img_ast, randint(30,win_width-30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)
rel_time = False
num_fire = 0
goal = 20
achieved = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type==KEYDOWN and e. key==K_SPACE:
            if num_fire < 5 and not rel_time:
                num_fire+=1
                fire_sound.play()
                ship.fire()
            if num_fire>=5 and not rel_time:
                last_time = timer()
                rel_time=True


    if not finish:
        window.blit(background, (0,0))

        monsters.update()
        monsters.draw(window)
        asteroids.draw(window)
        asteroids.update()
        if rel_time:
            now_time = timer()
            if now_time-last_time<3:
                reload_text = font2.render('Wait, reload...', True, (150,0,0))
                window.blit(reload_text, (260,460))
            else:
                num_fire=0
                rel_time=False
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score+=1
            achieved+=1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80,50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life-=1
        if life == 0  or lost>=max_lost:
            finish = True
            window.blit(lose, (200,200))
        if score>=goal:
            finish = True
            window.blit(win,(200,200))
        text = font2.render("Score:" + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render("Missed:" + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        ship.update()
        ship.reset()
        life_color = (0,150,0) if life == 3 else (150,150,0) if life==2 else (150,0,0)
        text_life = font1.render(str(life), True, life_color)
        window.blit(text_life, (650,10))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire=0
        life=3
        for a in asteroids:
            a.kill()
        for i in range(2):
            asteroid=Enemy(img_ast, randint(30, win_width-30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, win_width-80), -40,80,50, randint(1,5))
            monsters.add(monster)

    time.delay(50)




