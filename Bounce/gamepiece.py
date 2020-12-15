import pygame
from pygame.locals import *
import sys
import random
import time
 
pygame.init()
pygame.mixer.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Birthday Vladislav!")


bgm = pygame.mixer.Sound("rock_birthday.wav")
bgm.set_volume(0.7)
bgm.play(loops=-1)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("lilVlad.png"), (18, 30))
        self.image.set_colorkey((100, 100, 1))
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0))
        self.rect = self.image.get_rect()
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1     
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((24,58,55))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0,HEIGHT-20)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True
 
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
 
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
 
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()
        
PT1 = platform()
P1 = Player()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((214,73,51))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.point = False
PT1.moving = False
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)
 
for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(displaysurface, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
        
    else:
        pygame.draw.rect(displaysurface, ic,(x,y,w,h))
        
    smallText = pygame.font.Font("Raleway-Medium.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    displaysurface.blit(textSurf, textRect)

class GameInstance:
    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            displaysurface.fill((146,175,215))
            largeText = pygame.font.Font("Blox2.ttf", 100)
            TextSurf, TextRect = text_objects("Bounce", largeText)
            TextRect.center = ((WIDTH/2),(HEIGHT/4))
            displaysurface.blit(TextSurf, TextRect)

            button("PLAY",152,250,102,30,(24,58,55),(0,255,0),self.game_loop)
            button("MESSAGE",152,300,102,30,(24,58,55),(0,255,0),self.message)

            mouse = pygame.mouse.get_pos()
            
            pygame.display.update()

    def message(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            displaysurface.fill((146,175,215))
            f = pygame.font.Font("SF-Balloons.ttf", 47)
            t = pygame.font.Font("Raleway-Medium.ttf", 15)
            r = pygame.font.SysFont("Verdana", 15)
            head  = f.render(str("Happy birthday!"), True, (0,0,0))
            b1 = t.render(str("Dear Vladislav,"), True, (0,0,0))
            b2 = t.render(str("Happy 17th birthday!"), True, (0,0,0))
            b3 = t.render(str("Each birthday brings you closer to a future full of"), True, (0,0,0))
            b3b = t.render(str("success."), True, (0,0,0))
            b4 = t.render(str("I'm glad to have met you. Thanks for sending me a"), True, (0,0,0))
            b5 = t.render(str("message on Tandem, and for helping me with Russian."), True, (0,0,0))
            b6 = t.render(str("It's a pleasure to teach you English. You're a great"), True, (0,0,0))
            b6b = t.render(str("and fun person."), True, (0,0,0))
            b7 = t.render(str("All the best as you journey through your 18th year of"), True, (0,0,0))
            b7b = t.render(str("life!"), True, (0,0,0))
            b8 = r.render(str("Пусть все твои желания сбудутся! С днем"), True, (0,0,0))
            b8b = r.render(str("рождения, мой друг!"), True, (0,0,0))
            b9 = t.render(str("Leona"), True, (0,0,0))
            
            displaysurface.blit(head,(2, 10))
            displaysurface.blit(b1,(10, 100))
            displaysurface.blit(b2,(10, 130))
            displaysurface.blit(b3,(10, 160))
            displaysurface.blit(b3b,(10, 180))
            displaysurface.blit(b4,(10, 210))
            displaysurface.blit(b5,(10, 230))
            displaysurface.blit(b6,(10, 250))
            displaysurface.blit(b6b,(10, 270))
            displaysurface.blit(b7,(10, 300))
            displaysurface.blit(b7b,(10, 320))
            displaysurface.blit(b8,(10, 350))
            displaysurface.blit(b8b,(10, 370))
            displaysurface.blit(b9,(10, 400))

            pygame.display.update()
            FramePerSec.tick(FPS)

    def game_loop(self):
     
        while True:
        
            P1.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE:
                        P1.jump()
                if event.type == pygame.KEYUP:    
                    if event.key == pygame.K_SPACE:
                        P1.cancel_jump()  
     
            if P1.rect.top <= HEIGHT / 3:
                P1.pos.y += abs(P1.vel.y)
                for plat in platforms:
                    plat.rect.y += abs(P1.vel.y)
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
     
            plat_gen()
            displaysurface.fill((146,175,215))

            f = pygame.font.SysFont("Verdana", 20)     
            g  = f.render(str(P1.score), True, (0,0,0))   
            displaysurface.blit(g, (WIDTH/2, 10))   
         
            for entity in all_sprites:
                if entity == P1:
                    displaysurface.blit(P1.image, (P1.pos.x, P1.pos.y - P1.image.get_height()))
                else:
                    displaysurface.blit(entity.surf, entity.rect)
                entity.move()

            if P1.rect.top > HEIGHT:
                for entity in all_sprites:
                    entity.kill()
                    time.sleep(1)
                    displaysurface.fill((255,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    pygame.quit()
                    sys.exit()

     
            pygame.display.update()
            FramePerSec.tick(FPS)

instance = GameInstance()
instance.game_intro()
