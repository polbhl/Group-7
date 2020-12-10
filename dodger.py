import pygame, random, sys
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOWWIDTH = 600
WINDOWHEIGHT = 695
TEXTCOLOR = BLACK
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#todo changer le fond (image, vidéo, …) -> Mathias, peindre
BACKGROUNDCOLOR = (BLACK)

all_sprites = pygame.sprite.Group()



#65
# Set title to the window
pygame.display.set_caption("LAMA VS MEXICAINS")

BACKGROUNDIMAGE = pygame.image.load('MP_peinture_off.jpg')
pygame.transform.scale(BACKGROUNDIMAGE, (600, 700))
BACKGROUNDIMAGE_rect = BACKGROUNDIMAGE.get_rect() #localisation background
screen.fill(WHITE)
screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
all_sprites.draw(screen)



FPS = 60
POWERUP_TIME = 5000 #MILISECONDES

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 10
ADDNEWBADDIERATE = 15
PLAYERMOVERATE = 5

score = 0

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
        self.lives = 2

    def update(self):

        #Temps maximum du powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time >POWERUP_TIME:
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
            projectile = Projectile(self.rect.x, self.rect.top)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            pewshot.play()

        if self.power >= 2: #s'arrête à 2
            projectile1 = Projectile(self.rect.left, self.rect.top) #spawn 1 du projectile
            projectile2 = Projectile(self.rect.right, self.rect.top) #spawn 2 du projectile
            all_sprites.add(projectile1)
            all_sprites.add(projectile2)
            projectiles.add(projectile1)
            projectiles.add(projectile2)
            pewshot.play()



#todo bonus malus

#Données du jeu chargées
powerup_images = {}
powerup_images['carapace bleu'] = pygame.image.load('carapace bleu.png')
powerup_images['coeur rouge'] = pygame.image.load('coeur rouge.png')
powerup_images['double crachat'] = pygame.image.load('douple_crachat.png')
powerup_images['freeze'] = pygame.image.load('cold-face.png')
coeur_img = pygame.image.load('coeur rouge.png')
coeur_img_mini = pygame.transform.scale(coeur_img, (20, 20))


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['carapace bleu', 'coeur rouge', 'double crachat','freeze'])
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

powerups=pygame.sprite.Group()

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
        #pygame.sprite.Sprite.__init__(Baddie.group)

        # augmentation vitesse des baddies
        if score > 500:
            self.speedy = random.randrange(1, 4)
        if score > 1000:
            self.speedy = random.randrange(1, 5)
        if score > 1500:
            self.speedy = random.randrange(2, 5)
        if score > 2000:
            self.speedy = random.randrange(2, 6)

    def freeze(self):
        self.speedy = 0.5
        self.time = pygame.time.get_ticks()

    def screenoff (self):
        if self.rect.top > WINDOWHEIGHT:
            player.lives -=1





    #définition des mouvements
    def update(self):
        self.rect.y += self.speedy
        #les faire respawn quand ils sont hors de l'écran
        if self.rect.top > WINDOWHEIGHT + 10:
            self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            #elf.speedy = random.randrange(1, 3)

            #augmentation vitesse des baddies
        if score > 500:
            self.speedy = random.randrange(1, 4)
        if score > 1000:
            self.speedy = random.randrange(1, 5)
        if score > 1500:
            self.speedy = random.randrange(2, 5)
        if score > 2000:
            self.speedy = random.randrange(2, 6)
    def destruction(self, Baddie):
        #if self.rect.y < WINDOWHEIGHT:
        #self.kill()
        for sprite in self:
            if isinstance(sprite, Baddie):
                sprite.kill()

            #self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            #self.rect.y = random.randrange(-100, -40)


baddies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
baddie = Baddie()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
#ba=pygame.sprite.Group(Baddie)

#baddie = pygame.sprite.Group.sprites(Baddie)



def ennemis(nbmonstre):
    for i in range(nbmonstre):
        b = Baddie()
        all_sprites.add(b)
        baddies.add(b)


#for i in range(nbrdemonstre):  # nombre de baddies
#    b = Baddie()
#    all_sprites.add(b)
 #   baddies.add(b)



#fonction qui fait qu'on gagne le jeu
def game_win():
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
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
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

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
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

# Sons
pygame.mixer.music.load('MusiqueJeu.mp3')

#gameover sound
gameOverSound = pygame.mixer.Sound('MarioKart64GameOver.mp3')

#win sound
WinSound = pygame.mixer.Sound('WinSound.mp3')

#tir de crachat
pewshot = pygame.mixer.Sound('LASRGun_Blaster star wars 4 (ID 1760)_LS.wav')

#todo sons mort des mexicains
#mort1 = pygame.mixer.Sound('Paul1.wav')
#mort2 = pygame.mixer.Sound('Paul2.wav')
#mort3 = pygame.mixer.Sound('Paul3.wav')
#mort4 = pygame.mixer.Sound('Paul4.wav')
#mort5 = pygame.mixer.Sound('Paul5.wav')
#mort6 = pygame.mixer.Sound('Paul6.wav')
#mort7 = pygame.mixer.Sound('Paul7.wav')
#mort8 = pygame.mixer.Sound('Paul8.wav')

# ÉCRAN DE DÉMARRAGE.
windowSurface.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect) #todo changer fon d'écran
drawText('LAMA VS MEXICAINS', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()



#win = score > 200

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
    nbmonstre=5
    ennemis(nbmonstre)

    #nbrdemonstre =5

    #for i in range(nbrdemonstre):  # nombre de baddies
        #b = Baddie()
        #all_sprites.add(b)
        #baddies.add(b)
    #if score >= 100:
        #ennemis(6)

    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.




        for event in pygame.event.get():
            if event.type == QUIT:
                terminate().append


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
#44




        if score == 100:
            ennemis(1)

        if score == 200:
            ennemis(1)
        #for i in range(nbrdemonstre):  # nombre de baddies
            #b = Baddie()
            #all_sprites.add(b)
            #baddies.add(b)

        # game over when baddies goes off the bottom screen

        #for ba in baddies [1]:
        #if Baddie()[1].rect.top > WINDOWHEIGHT:
            #player.lives -= 1 #le problème c'est qu'il répète l'opération cinq fois (comme le nombre de baddies)
                #break

        if baddie.rect.top > WINDOWHEIGHT:
            terminate()




               # bre

        print("jaienviedemourir")
        #print("ok")








        hits = pygame.sprite.groupcollide(baddies, projectiles, True, True)
        for hit in hits:
            #random.choice(['mort1','mort2','mort3','mort4','mort5','mort6','mort7''mort8']).play()
            b = Baddie()
            all_sprites.add(b)
            baddies.add(b)

            if random.random() > 0.7: # 30% de chance que les powerup apparaissent
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

        # check si le joueur tire sur un powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'double crachat':
                player.powerup()
            if hit.type == 'coeur rouge':
                if player.lives < 3:
                    player.lives += 1

            #todo carapace bleu ça quitte le jeu
            if hit.type == 'carapace bleu':
                for ba in baddies:
                    ba.kill()
                #b.destruction()
                #Baddie().remove() #MDR ça rajoute un baddie au total, c'est ce qu'on cherchait à faire avant
                    b = Baddie()
                    all_sprites.add(b)
                    baddies.add(b)



            if hit.type =='freeze':
                Baddie().freeze()
               # pass


        hitz = pygame.sprite.spritecollide(player, baddies, True)
        if hitz:
            player.lives -= 1

        all_sprites.update()


        # Draw the game world on the window.
        windowSurface.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        draw_lives(screen, WINDOWWIDTH - 100, 5, player.lives, coeur_img_mini)
        all_sprites.draw(screen)


        pygame.display.update()


        #pygame.display.flip() #pas supprimer cette ligne
        # Check if any of the baddies have hit the player.
        #if playerHasHitBaddie(playerRect, baddies):
        if score > topScore:
            topScore = score # set new top score
        if score > 2000:
            break
        if hitz and player.lives < 0:
            break
        #for ba in baddies:
       # if ba.rect.top > WINDOWHEIGHT and player.lives == 0:
        #    break


        #for ba in baddies:
            #if ba.rect.top > WINDOWHEIGHT and player.lives == 0:
                #break

        #if b.rect.top > WINDOWHEIGHT and player.lives > 0:
            #break
        mainClock.tick(FPS)

    if score > 2000 :
        game_win()
        #pass

    # Stop the game and show the "Game Over" screen.
    else:
        game_over()


#todo écrire les règles -> document word et insérer l'image
