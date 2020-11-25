import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#todo changer le fond (image, vidéo, …)
BACKGROUNDCOLOR = (224,205,169)

# Set title to the window
pygame.display.set_caption("LAMA VS MEXICAINS")

BACKGROUNDIMAGE = pygame.image.load("Macchu picchu.jpeg").convert()
BACKGROUNDIMAGE_rect = BACKGROUNDIMAGE.get_rect() #localisation background
screen.fill(BACKGROUNDCOLOR)
screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)

#running = True
#while running:
    #screen.fill(BACKGROUNDCOLOR)
    #screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
    #all_sprites.draw(screen)
    #pygame.display.flip()

#paygame.quit()

FPS = 60

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 10
ADDNEWBADDIERATE = 15
PLAYERMOVERATE = 5

#Définir l'écran
#screen=pygame.display.set_mode((WINDOWIDTH, WINDOWHEIGHT))
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

    def update(self):
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

#action de tirer du lama
    def shoot(self):
        projectile = Projectile(self.rect.x, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['carapace bleu', 'coeur rouge'])
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = -10

    def update(self):
        self.rect.centery += self.speedy
        #make the projectile disappear when it goes off the screen
        if self.rect.bottom < 0:
            self.kill()


#class mexicains par sprite
class Baddie(pygame.sprite.Sprite):
    #caractéristiques des mexicains

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Mexicain_pixel.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)

        # augmentation vitesse des mexicains
        if score > 500:
            self.speedy = random.randrange(1, 4)
        if score > 1000:
            self.speedy = random.randrange(1, 5)
        if score > 1500:
            self.speedy = random.randrange(2, 5)
        if score > 2000:
            self.speedy = random.randrange(2, 6)


    #définition des mouvements
    def update(self):
        self.rect.y += self.speedy
        #les faire respawn quand ils sont hors de l'écran
        if self.rect.top > WINDOWHEIGHT + 10:
            self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)

            #augmentation vitesse des mexicains
            if score > 500:
                self.speedy = random.randrange(1, 4)
            if score > 1000:
                self.speedy = random.randrange(1, 5)
            if score > 1500:
                self.speedy = random.randrange(2, 5)
            if score > 2000:
                self.speedy = random.randrange(2, 6)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
baddies = pygame.sprite.Group()

#augmentation nombre de mexicains
nbrdemonstre = 4
if score > 1000:
    nbrdemonstre = nbrdemonstre + 1
if score > 2000:
    nbrdemonstre = nbrdemonstre + 1
for i in range(nbrdemonstre):#nombre de baddies
    b = Baddie()
    all_sprites.add(b)
    baddies.add(b)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
#playerImage = pygame.image.load('lama_player1.png')
#playerRect = playerImage.get_rect()

#baddieImage = pygame.image.load('baddie.png')

#les crachats du lama (tentative en tout cas)
#bullet_image=pygame.image.load('bullet.png')
#bulletX=0
#bulletY=480
#bulletX_change=0
#bulletY_change=10
#playerX=370
#bullet_state="ready"

#def fire_bullet(x,y):
    #global bullet_state
    #bullet_state="fire"
    #windowSurface.blit(bullet_image(x + 16, y + 10))



# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    #baddies = []
    score = 0
    #playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50) #ca fait que le lama apparaisse en bas au milieu de l'écran
    #moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    #baddieAddCounter = 0

    #todo changer la musique du jeu
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
                #if event.key == K_LEFT or event.key == K_a:
                  #  moveRight = False
                 #   moveLeft = True
                #if event.key == K_RIGHT or event.key == K_d:
                #    moveLeft = False
                #    moveRight = True
                #if event.key == K_UP or event.key == K_w:
                #    moveDown = False
                #    moveUp = True
                #if event.key == K_DOWN or event.key == K_s:
                #    moveUp = False
                 #   moveDown = True
                #make that the player shoot projectile when we press space
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

                #if event.key == K_LEFT or event.key == K_a:
                #    moveLeft = False
                #if event.key == K_RIGHT or event.key == K_d:
                #    moveRight = False
                #if event.key == K_UP or event.key == K_w:
                #    moveUp = False
                #if event.key == K_DOWN or event.key == K_s:
                 #   moveDown = False

        all_sprites.update()

        #hitz = pygame.sprite.spritecollideany(WINDOWHEIGHT, baddies, False)
        #if hitz:
         #   break
        if b.rect.top > WINDOWHEIGHT:
            break


        hits = pygame.sprite.groupcollide(baddies, projectiles, True, True)
        for hit in hits:
            b = Baddie()
            all_sprites.add(b)
            baddies.add(b)
        hits = pygame.sprite.spritecollide(player, baddies, False)
        if hits:
            break

            #todo supprimer ou garder
            #if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where to the cursor.
                #playerRect.centerx = event.pos[0]
                #playerRect.centery = event.pos[1]
        # Add new baddies at the top of the screen, if needed.
        #if not reverseCheat and not slowCheat:
            #baddieAddCounter += 1
        #if baddieAddCounter == ADDNEWBADDIERATE:
            #baddieAddCounter = 0
            #baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            #newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        #'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        #'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        #}

            #baddies.append(newBaddie)

        # Move the player around.
        #if moveLeft and playerRect.left > 0:
           # playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        #if moveRight and playerRect.right < WINDOWWIDTH:
         #   playerRect.move_ip(PLAYERMOVERATE, 0)
        #if moveUp and playerRect.top > 0:
         #   playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        #if moveDown and playerRect.bottom < WINDOWHEIGHT:
         #   playerRect.move_ip(0, PLAYERMOVERATE)


        # Move the baddies down.
        #for b in baddies:
            #if not reverseCheat and not slowCheat:
               # b['rect'].move_ip(0, b['speed'])
           # elif reverseCheat:
              #  b['rect'].move_ip(0, -5)
            #elif slowCheat:
               # b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        #for b in baddies[:]:
            #if b['rect'].top > WINDOWHEIGHT:
              #  baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle.
        #windowSurface.blit(playerImage, playerRect)

        all_sprites.draw(screen)
        #pygame.display.flip()

        # Draw each baddie.
        #for b in baddies:
         #   windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        #if playerHasHitBaddie(playerRect, baddies):
        #    if score > topScore:
        #        topScore = score # set new top score
        #    break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()

#todo bonus/malus