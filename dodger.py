import pygame, random, sys
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
WINDOWWIDTH = 600
WINDOWHEIGHT = 695
RED = (0,0,0)
TEXTCOLOR = GREY
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


BACKGROUNDCOLOR = (BLACK)

all_sprites = pygame.sprite.Group()

# Set title to the window
pygame.display.set_caption("LAMA VS MEXICAINS")

BACKGROUNDIMAGE = pygame.image.load('MP_peinture_off.jpg')
pygame.transform.scale(BACKGROUNDIMAGE, (600, 700))
BACKGROUNDIMAGE_rect = BACKGROUNDIMAGE.get_rect() #localisation background
screen.fill(WHITE)
screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
all_sprites.draw(screen)
BACKGROUNDCELEBRATION = pygame.image.load('celebration-confetti-red.png')
#BACKGROUNDCELEBRATION = pygame.transform.scale(BACKGROUNDCELEBRATION, (900, 1000))
BACKGROUNDCELEBRATION_rect = BACKGROUNDCELEBRATION.get_rect()
screen.blit(BACKGROUNDCELEBRATION, BACKGROUNDCELEBRATION_rect)

BACKGROUNDLAMA = pygame.image.load('lama_marrant4.jpg')
BACKGROUNDLAMA_rect = BACKGROUNDLAMA.get_rect()
screen.blit(BACKGROUNDLAMA, BACKGROUNDLAMA_rect)



FPS = 60
POWERUP_TIME = 5000 #MILISECONDES

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 10
ADDNEWBADDIERATE = 15
PLAYERMOVERATE = 5

score = 0

#Données du jeu chargées
powerup_images = {}
powerup_images['carapace bleu'] = pygame.image.load('carapace bleu.png')
powerup_images['coeur rouge'] = pygame.image.load('coeur-rougeoff.png')
powerup_images['double crachat'] = pygame.image.load('douple_crachat.png')
powerup_images['freeze'] = pygame.image.load('cold-face.png')
coeur_img = pygame.image.load('coeur-rougeoff.png')
coeur_img_mini = pygame.transform.scale(coeur_img, (20, 20))
powerup_images['speed'] = pygame.image.load('RedFace.png')
#gameOverGIF = pygame.movie.Movie('GameOverPinata.mpg')

#class projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.centery += self.speedy
        #make the projectile disappear when it goes off the screen
        if self.rect.bottom < 0:
            self.kill()

#lama
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('lama_player1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH / 2
        self.rect.bottom = WINDOWHEIGHT - 10
        self.speedx=0
        self.power=1
        self.power_time=pygame.time.get_ticks()
        self.lives = 0

    def update(self):
        #Temps maximum du powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -=1
            self.power_time = pygame.time.get_ticks()


        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        self.rect.x += self.speedx
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0

#définition powerup
    def powerup(self):
        self.power += 1 #ajoute 1 tir
        self.power_time=pygame.time.get_ticks()

#action de tirer du lama
    def shoot(self):
        if self.power == 1:
            projectile = Projectile(self.rect.centerx-10, self.rect.top)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            #pewshot.play()

        if self.power >= 2: #s'arrête à 2
            projectile1 = Projectile(self.rect.left, self.rect.top) #spawn 1 du projectile
            projectile2 = Projectile(self.rect.right, self.rect.top) #spawn 2 du projectile
            all_sprites.add(projectile1)
            all_sprites.add(projectile2)
            projectiles.add(projectile1)
            projectiles.add(projectile2)
            #pewshot.play()

#todo bonus malus

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['carapace bleu', 'coeur rouge', 'double crachat'])
        self.image = powerup_images[self.type]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.centery += self.speedy
        #make the projectile disappear when it goes off the screen
        if self.rect.top > WINDOWHEIGHT:
            self.kill()

#powerups=pygame.sprite.Group()

#class baddies par sprite
class Baddie(pygame.sprite.Sprite):
    #caractéristiques des baddies

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Mexicain_pixel.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)
        self.powe = 1
        self.powe_time = pygame.time.get_ticks()
        #pygame.sprite.Sprite.__init__(Baddie.group)

    #def freeze(self):
     #   self.powe += 1 #ajoute 1 tir
     #   self.powe_time = pygame.time.get_ticks()
     #   print("salut")

    #définition des mouvements
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT + 50:
            self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 1

            if score > 500:
                self.speedy = random.randrange(1, 2)
            if score > 1000:
                self.speedy = random.randrange(1, 3)
            if score > 1500:
                self.speedy = random.randrange(2, 4)
            if score > 2000:
                self.speedy = random.randrange(3, 5)
            if score > 2500:
                self.speedy = random.randrange(4, 6)

        if self.rect.top > WINDOWHEIGHT:
            player.lives -= 1
            self.kill()
        #wewe


        #if self.powe == 1:


        if self.powe == 2:
            print("réussite")
            self.speedy = 10

    def destruction(self, Baddie):
        for sprite in self:
            if isinstance(sprite, Baddie):
                sprite.kill()


class Fest(pygame.sprite.Sprite):
    #caractéristiques des baddies

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)

        if score > 500:
            self.speedy = random.randrange(1, 2)
        if score > 1000:
            self.speedy = random.randrange(1, 3)
        if score > 1500:
            self.speedy = random.randrange(2, 4)
        if score > 2000:
            self.speedy = random.randrange(3, 5)
        if score > 2500:
            self.speedy = random.randrange(4, 6)

    #définition des mouvements
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT + 50:
            self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange (1, 3)

        if self.rect.top > WINDOWHEIGHT:
            self.kill()
        #wewe


baddies = pygame.sprite.Group()
fests = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
baddie = Baddie()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
#ba=pygame.sprite.Group(Baddie)


def conf(nconf):
    for i in range(nconf):
        c = Fest()
        all_sprites.add(c)
        fests.add(c)

def ennemis(nbmonstre):
    for i in range(nbmonstre):
        b = Baddie()
        all_sprites.add(b)
        baddies.add(b)

#fonction qui fait qu'on gagne le jeu
def game_win():
    screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
    screen.blit(BACKGROUNDCELEBRATION, BACKGROUNDCELEBRATION_rect)
    pygame.mixer.music.stop()
    WinSound.play()
    drawText('You Win', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.flip()
    waitForPlayerToPressKey()

    WinSound.stop()

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = coeur_img_mini.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(coeur_img_mini, img_rect)


def terminate():
    pygame.quit()
    sys.exit()

def game_over():
    screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
    pygame.mixer.music.stop()
    gameOverSound.play()
    conf(10)
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    conf(10)
    pygame.display.update()
    waitForPlayerToPressKey()
    #if event.key == K_SPACE or event.key == K_LEFT or event.key == K_RIGHT:

    gameOverSound.stop()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def waitForPlayerToPressB():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                 if event.key == K_ESCAPE:# Pressing ESC quits.
                    terminate()
                 if event.key == ord('z'):
                    return

def drawText(text, font2, surface, x, y):
    textobj = font2.render(text, 1, RED)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawTexts(text, font, surface, x, y):
    textobj = font.render(text, 1, (205, 20, 20))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('LAMA VS MEXICAINS')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 22)
font3 = pygame.font.SysFont(None, 28)

# Sons
pygame.mixer.music.load('MusiqueJeu.mp3')
gameOverSound = pygame.mixer.Sound('Paul6.mp3') #gameover sound
WinSound = pygame.mixer.Sound('WinSound.mp3') #win sound
pewshot = pygame.mixer.Sound('LASRGun_Blaster star wars 4 (ID 1760)_LS.wav') #tir de crachat
CarapaceBleuPop = pygame.mixer.Sound ('PopBallon.mp3') #explosion des mexciains
lifeup = pygame.mixer.Sound ('MarioBros1Life.mp3') #gagner une vie
freezeSound = pygame.mixer.Sound ('freeze.wav') #quand les mexicains freeze
mortMexicain = pygame.mixer.Sound ('mortMexicain.mp3') #mexicain meurt
lifeLost = pygame.mixer.Sound ('Paul5.mp3') #quand on perd une vie

# ÉCRAN DE DÉMARRAGE.
#windowSurface.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
#screen.fill(BLACK)
screen.blit(BACKGROUNDLAMA, BACKGROUNDLAMA_rect)
drawTexts('LAMA VS MEXICAINS', font, windowSurface, (WINDOWWIDTH / 4) - 20, (WINDOWHEIGHT / 3) - 100)
drawText('BONUS : ', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) - 10)
drawText('HEART : You win an extra life', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 15)
drawText('BLUE TURTLE : All Mexicans die', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 40)
drawText('DOUBLE SPIT : You shoot two bullet at a time', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 65)
drawText('Press space to shoot', font3, windowSurface, (WINDOWWIDTH / 3) , (WINDOWHEIGHT / 3) + 110)
drawText('Press the right and left arrows to move around', font3, windowSurface, (WINDOWWIDTH / 3) - 115, (WINDOWHEIGHT / 3) + 140)

#drawText('FREEZE : Mexicans are moving slower', font2, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 150)
drawText('If a Mexican touches you or leaves the screen you lose a life', font3, windowSurface, (WINDOWWIDTH / 3) - 180, (WINDOWHEIGHT / 3) + 190)
drawText('If you do not have a life anymore it is game over', font3, windowSurface, (WINDOWWIDTH / 3) - 130, (WINDOWHEIGHT / 3) + 220)
drawText('You must reach 3000 points to win, good luck', font3, windowSurface, (WINDOWWIDTH / 3) - 120, (WINDOWHEIGHT / 3) + 270)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 50, (WINDOWHEIGHT / 3) + 320)

pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:

    score = 0

    reverseCheat = slowCheat = False
    #baddieAddCounter = 0
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    projectiles = pygame.sprite.Group()
    baddies = pygame.sprite.Group()
    baddie = Baddie()
    nbmonstre=5
    ennemis(nbmonstre)


    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()


            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True

                if event.key == K_SPACE:
                    player.shoot()

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()
        if score == 400:
            ennemis(1)

        if score == 800:
            ennemis(1)

        if score == 1200:
            ennemis(1)

        if score == 1600:
            ennemis(1)

        if score == 2000:
            ennemis(1)

        if score == 2400:
            ennemis(1)

        hits = pygame.sprite.groupcollide(baddies, projectiles, True, True)
        for hit in hits:
            b = Baddie()
            all_sprites.add(b)
            baddies.add(b)
            #mortMexicain.play()

            if random.random() > 0.85: # 15% de chance que les powerup apparaissent
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

        # check si le joueur tire sur un powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'double crachat':
                player.powerup()

            if hit.type == 'coeur rouge':
                lifeup.play()
                if player.lives < 3:
                    player.lives += 1


            if hit.type == 'carapace bleu':
                for ba in baddies:
                    ba.kill()
                    b = Baddie()
                    all_sprites.add(b)
                    baddies.add(b)
                    CarapaceBleuPop.play()

            if hit.type =='freeze':
                Baddie().freeze()

        hitz = pygame.sprite.spritecollide(player, baddies, True)
        if hitz:
            player.lives -= 1
            lifeLost.play()

        # Draw the game world on the window.
        windowSurface.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        draw_lives(screen, WINDOWWIDTH - 100, 5, player.lives, coeur_img_mini)
        all_sprites.draw(screen)

        # Check if any of the baddies have hit the player.
        #if playerHasHitBaddie(playerRect, baddies):
        if score > topScore:
            topScore = score # set new top score
        if player.lives < 0:
            break

        mainClock.tick(FPS)

        all_sprites.update()
        pygame.display.update()

        if score > 3000:
            break
        # pas supprimer cette ligne
    if score > 3000:
        game_win()


    # Stop the game and show the "Game Over" screen.
    else:
        game_over()
    pygame.display.flip()
    all_sprites.draw(screen)


#todo écrire les règles -> document word et insérer l'image