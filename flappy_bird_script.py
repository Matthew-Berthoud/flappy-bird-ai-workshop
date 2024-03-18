import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600 # can tweak these later if we notice the screen doesn't fit well
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# after writing this, test to make sure there's not syntax errors
# maybe test showing the images just in case


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25   # how much it will tilt
    ROT_VEL = 20        # how much we tile up/down each frame
    ANIMATION_TIME = 5  # changes how fast or slow bird flaps wings

    def __init__(self, x, y): # initialize the bird at starting location (x,y)
        self.x = x
        self.y = y
        self.tilt = 0 # bird will be looking straight ahead
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0] # starting image of wing flapping animation

    def jump(self):
        self.vel = -10.5 
            # (0,0) in pygame is top left corner
            # therefore, going up requires negative velocity, down is positive
            # left is negative velocity, right is positive
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
            # tells us how much we move up or down based on current velocity
            # TODO need simple physicsy explanation for this

        if d >= 16:
            d = 16
            # don't go off the screen

        if d < 0: # TODO: why is this here?
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50: # TODO: moving upwards... explain why
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # Flap wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # don't flap on the way down
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotate based on if it's going up or down
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # the above rotates around the top left corner
        # fix this with the below
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft) 

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe: # we are considering each pipe to be a top and bottom
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x 
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPG_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

        # hitboxes explanation, make sure we only register collisions when the actual bird collisions happen
        # therefore, use masks
        # masks check for real collisisons by checking if the pixels that "collided" are transparent or not.
        # compare the pixels in 2 2d lists to see what's up

    def collide(self, bird):
        bird_mask = bird.get_mask()

        # now for the pipes
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 
        t_point = bird_mask.overlap(top_mask, top_offset) 
            # if they don't collide these lines return None

        if t_point or b_point:
            return True

        return False

class Base:
    # have to make this move, and it's not infinitely long so it's a little complicated
    # ask kids what they think a good solution for this would be
    # before coding this, show a drawing of what we're doing conceptually
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # red X in top corner of pygame window
                run = False
                # pygame.quit()
            
        # bird.move() # will just fall very quickly for now
            # need to implement clock to make this slower
        draw_window(win, bird)

    pygame.quit()
    quit()

main()