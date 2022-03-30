import pygame
import random
from os import path

WIDTH = 700
HEIGHT = 600
FPS = 60

HS_FILE='assets/images/highscore.txt'
hdir=path.dirname(__file__)
img_dir = path.join(path.dirname(__file__), 'meteors')
bg=pygame.image.load('assets/images/galgadas.png')
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
icon=pygame.image.load('assets/images/asteroid invasion.png')
life=pygame.image.load('assets/images/life.png')
meteor_images = []
expl_sounds = []
meteor_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_big2.png','meteorBrown_big3.png',
              'meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png','meteorBrown_tiny2.png']

powerup_images = {}
powerup_images['gun'] = pygame.image.load( 'assets/images/powerpowerup.png')
powerup_images['life'] = pygame.image.load('assets/images/life.png')
pygame.display.set_icon(icon)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/bgspaceshooter.mp3')
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("asteroid invasion")
speed=8
bspeed=12
sspeed=14
powerc=RED
pew=pygame.mixer.Sound('assets/sounds/pew.wav')
astrexpl=pygame.mixer.Sound('assets/sounds/astrexpl.wav')
for meteors in meteor_list:
    meteor_images.append(pygame.image.load(meteors))
    
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/player.png')
        self.rect = self.image.get_rect()
        self.radius=29
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hidden = False
        self.lives=3
        self.soniclaser=0
        self.power=1
        self.hide_timer = pygame.time.get_ticks()
        
    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        #speed=8
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -speed
        if keystate[pygame.K_RIGHT]:
            self.speedx = speed
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1

    
    def shoot(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            pew.play()
        if self.power >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            pew.play()

    def sonicshot(self):
        sonicbull=Sonicshot(self.rect.centerx,self.rect.top)
        all_sprites.add(sonicbull)
        sonicshot.add(sonicbull)
              
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -125 or self.rect.right > WIDTH+ 125:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/laserRed.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -bspeed

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Sonicshot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH*2,10))                       
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -sspeed

    def update(self):
        self.rect.y += self.speedy       
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['life','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
        
font_name = pygame.font.match_font(' InsaneHours2')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


with open('highscore.txt') as f:
    try:
        highscore=int(f.read())
    except:
        highscore=200

def BG():
    screen.fill(WHITE)
    screen.blit(bg,(0,0))

def draw_lives(surf, x, y, lives, img):
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, powerc, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def showscreen():   
    BG()
    draw_text(screen, "asteroid invasion", 50, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "left and right arrow to move", 20,WIDTH / 2, HEIGHT / 2-12.5)
    draw_text(screen, "press space to shoot", 20,WIDTH / 2, HEIGHT / 2-50)
    draw_text(screen, "if red bar turns green ", 20,WIDTH / 2, HEIGHT / 2+22)
    draw_text(screen, "press arrow up to use sonicshot", 20,WIDTH / 2, HEIGHT / 2+44)
    draw_text(screen,'highscore: '+str(highscore),18,WIDTH/2,400)
    draw_text(screen, "Press up arrow to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                pygame.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    waiting = False
                   

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'assets/images/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join('assets/images', filename))
    explosion_anim['player'].append(img)


# Game loop
running = True
game_over=True
while running:
    if game_over:
        showscreen()
        game_over=False
        all_sprites=pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        sonicshot=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        score=0
        powerc=RED
        for i in range(9):
            newmob()
        
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.hidden==False:
                player.shoot()
            if event.key == pygame.K_UP and player.soniclaser==100:
                powerc=RED
                player.soniclaser=0
                player.sonicshot()  
    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        newmob()
        score+=50
        player.soniclaser+=2
        astrexpl.play()
        if random.random() > 0.98:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)


    hits = pygame.sprite.groupcollide(mobs, sonicshot, True, False)
    for hit in hits:
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        newmob()
        score+=10
        astrexpl.play()
        
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False,pygame.sprite.collide_circle)
    if hits :
        death_explosion = Explosion(player.rect.center, 'player')
        astrexpl.play()
        all_sprites.add(death_explosion)
        player.hide()
        player.lives -= 1
        player.power=1
        powerc=RED
        player.soniclaser=0
    if player.lives==0 and not death_explosion.alive():
        game_over = True

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
         if hit.type == 'gun':
            player.powerup()
            score+=100
         if hit.type=='life':
             player.lives+=1

    if score>highscore:
        highscore=score
        
    if player.soniclaser>=100:
        player.soniclaser=100
        powerc=GREEN
        
   
    # Draw / render
    BG()
    draw_text(screen,str(player.lives)+'x',18,648,10)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    screen.blit(life,(665,0))
    all_sprites.draw(screen)
    draw_shield_bar(screen, 5, 5, player.soniclaser)
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
