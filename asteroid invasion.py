import pygame
import random
from os import *

WIDTH = 700
HEIGHT = 600
FPS = 60

HS_FILE='highscore.txt'

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
pew=pygame.mixer.Sound('assets/sounds/pew.wav')
astrexpl=pygame.mixer.Sound('assets/sounds/astrexpl.wav')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/player.png')
        self.rect = self.image.get_rect()
        self.radius=30
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hidden = False
        self.lives=3
        self.hide_timer = pygame.time.get_ticks()


        # unhide if hidden
        
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

    
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        pew.play()
        all_sprites.add(bullet)
        bullets.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/images/meteorBrown_med1.png')
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
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
        
font_name = pygame.font.match_font(' InsaneHours2')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

hdir = path.dirname(path.abspath(__file__))
with open(path.join(hdir,HS_FILE),'w') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0

def BG():
    screen.fill(WHITE)
    screen.blit(bg,(0,0))

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y
        surf.blit(img, img_rect)

def showscreen():   
    BG()
    draw_text(screen, "asteroid invasion", 50, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,WIDTH / 2, HEIGHT / 2)
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
                   


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

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
    explosion_anim['player'].append(img)

    
player = Player()
all_sprites.add(player)

    
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
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score=0
            
        
    #print(clock)
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

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score+=50
        astrexpl.play()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False,pygame.sprite.collide_circle)
    if hits:
        death_explosion = Explosion(player.rect.center, 'player')
        astrexpl.play()
        all_sprites.add(death_explosion)
        player.hide()
        player.lives -= 1
    if player.lives==0 and not death_explosion.alive():
        game_over = True
        

    if score>highscore:
        highscore=score
        

    # Draw / render
    BG()
    draw_text(screen,str(player.lives)+'x',18,648,10)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    screen.blit(life,(665,0))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
