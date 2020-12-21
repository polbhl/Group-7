import pygame, random, sys
from pygame.locals import *

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)

# Set up the screen dimensions
WINDOWWIDTH = 600
WINDOWHEIGHT = 695
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

TEXTCOLOR = GREY
BACKGROUNDCOLOR = (BLACK)

all_sprites = pygame.sprite.Group()

# Set title to the window and load background images
pygame.display.set_caption("LAMA VS MEXICAINS")
BACKGROUNDIMAGE = pygame.image.load('MP_peinture_off.jpg')
BACKGROUNDIMAGE_rect = BACKGROUNDIMAGE.get_rect()
screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
all_sprites.draw(screen)
BACKGROUNDCELEBRATION = pygame.image.load('celebration-confetti-red.png')
BACKGROUNDCELEBRATION_rect = BACKGROUNDCELEBRATION.get_rect()
screen.blit(BACKGROUNDCELEBRATION, BACKGROUNDCELEBRATION_rect)

BACKGROUNDLAMA = pygame.image.load('lama_marrant4.jpg')
BACKGROUNDLAMA_rect = BACKGROUNDLAMA.get_rect()
screen.blit(BACKGROUNDLAMA, BACKGROUNDLAMA_rect)

FPS = 60
POWERUP_TIME = 5000 # In milliseconds

score = 0

# Set up the images for our game
powerup_images = {}
powerup_images['carapace bleu'] = pygame.image.load('carapace bleu.png')
powerup_images['coeur rouge'] = pygame.image.load('coeur-rougeoff.png')
powerup_images['double crachat'] = pygame.image.load('douple_crachat.png')
coeur_img = pygame.image.load('coeur-rougeoff.png')
coeur_img_mini = pygame.transform.scale(coeur_img, (20, 20))
powerup_images['speed'] = pygame.image.load('RedFace.png')


# Our Class for the projectiles
class Projectile(pygame.sprite.Sprite):

    # Characteristics of the projectiles
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    # Movements of the projectiles
    def update(self):
        self.rect.centery += self.speedy
        # Make the projectile disappear when it goes off the screen
        if self.rect.bottom < 0:
            self.kill()


# Our class for the player
class Player(pygame.sprite.Sprite):
    # Characteristics of the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('lama_player1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH / 2
        self.rect.bottom = WINDOWHEIGHT - 10
        self.speedx = 0
        self.power = 1
        self.power_time=pygame.time.get_ticks()
        self.lives = 0

    # Movements of the player
    def update(self):
        # Duration of the power
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -=1
            self.power_time = pygame.time.get_ticks()

        # Set up the movements and the speed of the player
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

    # Function of the powerup
    def powerup(self):
        self.power += 1 # Add one projectile when the player shoot
        self.power_time = pygame.time.get_ticks()

    # Function that allows the player to shoot
    def shoot(self):

        # The player shoots just one projectile
        if self.power == 1:
            projectile = Projectile(self.rect.centerx-10, self.rect.top)
            all_sprites.add(projectile)
            projectiles.add(projectile)

        # The player shoots 2 projectiles at the same time
        if self.power >= 2:
            projectile1 = Projectile(self.rect.left, self.rect.top) # Spawn of the first projectile
            projectile2 = Projectile(self.rect.right, self.rect.top) # Spawn of the second projectile
            all_sprites.add(projectile1)
            all_sprites.add(projectile2)
            projectiles.add(projectile1)
            projectiles.add(projectile2)


# Our class for the bonus
class Pow(pygame.sprite.Sprite):

    # Characteristics of the bonus
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['carapace bleu', 'coeur rouge', 'double crachat'])
        self.image = powerup_images[self.type]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    # Movements of the bonus
    def update(self):
        self.rect.centery += self.speedy

        # Make the projectile disappear when it goes off the screen
        if self.rect.top > WINDOWHEIGHT:
            self.kill()


# Our class for the baddies
class Baddie(pygame.sprite.Sprite):

    # Characteristics of the baddies
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Mexicain_pixel.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)

    # Movements of the baddies
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT + 50:
            self.rect.x = random.randrange(WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 1

            # The speed of the baddies increases when the score increases
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

        # The baddies don't exist no more when they go off the screen
        if self.rect.top > WINDOWHEIGHT:
            player.lives -= 1
            self.kill()

    # All the baddies disappears because of the "carapace bleue"
    def destruction(self, Baddie):
        for sprite in self:
            if isinstance(sprite, Baddie):
                sprite.kill()

baddies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
baddie = Baddie()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
powerups = pygame.sprite.Group()


# Function that makes the baddies spawn
def ennemis(nbmonstre):
    for i in range(nbmonstre):
        b = Baddie()
        all_sprites.add(b)
        baddies.add(b)

# Function that shows the "Game win screen"
def game_win():
    screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
    screen.blit(BACKGROUNDCELEBRATION, BACKGROUNDCELEBRATION_rect)
    pygame.mixer.music.stop()
    WinSound.play()
    drawText3('You Win', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText3('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.flip()
    waitForPlayerToPressKey()

    WinSound.stop()

# Function that draws the lives on the top right of the screen
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = coeur_img_mini.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(coeur_img_mini, img_rect)

# Function that stops the game
def terminate():
    pygame.quit()
    sys.exit()

# Function that shows the "Game Over" screen
def game_over():
    screen.blit(BACKGROUNDIMAGE, BACKGROUNDIMAGE_rect)
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText3('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText3('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()

# Function that makes the game restart when we press a key
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

# Set up the different functions that draw the text
def drawText(text, font2, surface, x, y):
    textobj = font2.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawText2(text, font, surface, x, y):
    textobj = font.render(text, 1, (205, 20, 20))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawText3(text, font, surface, x, y):
    textobj = font.render(text, 1, WHITE)
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

# Set up the sounds
pygame.mixer.music.load('MusiqueJeu.mp3')
gameOverSound = pygame.mixer.Sound('Paul6.mp3') # Gameover sound
WinSound = pygame.mixer.Sound('WinSound.mp3') # Win sound
CarapaceBleuPop = pygame.mixer.Sound ('PopBallon.mp3') # Sound of the 'carapace bleue' bonus
lifeup = pygame.mixer.Sound ('MarioBros1Life.mp3') # Sound when we win a life
lifeLost = pygame.mixer.Sound ('Paul5.mp3') # Sound when we loose a life

# Set up the start screen and the rules
screen.blit(BACKGROUNDLAMA, BACKGROUNDLAMA_rect)
drawText2('LAMA VS MEXICAINS', font, windowSurface, (WINDOWWIDTH / 4) - 20, (WINDOWHEIGHT / 3) - 100)
drawText('BONUS : ', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) - 10)
drawText('HEART : You win an extra life', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 15)
drawText('BLUE TURTLE : All Mexicans die', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 40)
drawText('DOUBLE SPIT : You shoot two bullet at a time', font3, windowSurface, (WINDOWWIDTH / 3) - 150, (WINDOWHEIGHT / 3) + 65)
drawText('Press space to shoot', font3, windowSurface, (WINDOWWIDTH / 3) , (WINDOWHEIGHT / 3) + 110)
drawText('Press the right and left arrows to move around', font3, windowSurface, (WINDOWWIDTH / 3) - 115, (WINDOWHEIGHT / 3) + 140)

drawText('If a Mexican touches you or leaves the screen you lose a life', font3, windowSurface, (WINDOWWIDTH / 3) - 180, (WINDOWHEIGHT / 3) + 190)
drawText('If you do not have a life anymore it is game over', font3, windowSurface, (WINDOWWIDTH / 3) - 130, (WINDOWHEIGHT / 3) + 220)
drawText('You must reach 3000 points to win, good luck', font3, windowSurface, (WINDOWWIDTH / 3) - 120, (WINDOWHEIGHT / 3) + 270)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 50, (WINDOWHEIGHT / 3) + 320)

pygame.display.update()
waitForPlayerToPressKey()

# The topScore is 0 when we launch the game
topScore = 0

while True:

    # Set up the parameters when the game starts
    score = 0 # The score is 0 when we start the game
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    projectiles = pygame.sprite.Group()
    baddies = pygame.sprite.Group()
    baddie = Baddie()
    nbmonstre = 5 # The number of baddies when we start the game
    ennemis(nbmonstre)
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                # The player shoot when we press space
                if event.key == K_SPACE:
                    player.shoot()

            if event.type == KEYUP:
                # The game stop when we press ESC
                if event.key == K_ESCAPE:
                        terminate()

        # More baddies spawn when the score increase
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

        # Collision between the projectiles and the baddies
        hits = pygame.sprite.groupcollide(baddies, projectiles, True, True)
        # Make the baddies respawn when we shoot them
        for hit in hits:
            b = Baddie()
            all_sprites.add(b)
            baddies.add(b)

            # The probability of a bonus spawn from a baddie
            if random.random() > 0.85: # 15% chance that a bonus spawn
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)

        # Collision if a projectile hits a bonus
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:

            # Bonus 'double crachat'
            if hit.type == 'double crachat':
                player.powerup()

            # Bonus 'coeur rouge'
            if hit.type == 'coeur rouge':
                lifeup.play()
                if player.lives < 3: # The player can't have more than 3 lives
                    player.lives += 1 # The player win a life

            # Bonus 'carapace bleue'
            if hit.type == 'carapace bleu':
                # Make the baddies disappear and respawn
                for ba in baddies:
                    ba.kill()
                    b = Baddie()
                    all_sprites.add(b)
                    baddies.add(b)
                    CarapaceBleuPop.play()

        # Collision between the player and the baddies
        hitz = pygame.sprite.spritecollide(player, baddies, True)
        # The player loose a life when a baddie hits him
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

        if score > topScore:
            topScore = score # set new top score

        # The game stops if the player lose and has no more lives
        if player.lives < 0:
            break

        mainClock.tick(FPS)

        all_sprites.update()
        pygame.display.update()

        # The game stops when the score is 3000
        if score > 3000:
            break

    # We win the game when we reach the score of 3000 and show the "Game Win" screen
    if score > 3000:
        game_win()


    # Stop the game and show the "Game Over" screen.
    else:
        game_over()

    pygame.display.flip()
    all_sprites.draw(screen)


