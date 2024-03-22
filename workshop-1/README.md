# Flappy Bird AI: Workshop 1: The Flappy Bird Game
Today we're going to build a simple flappy bird game, which you can play by clicking the space bar to jump the bird. Next time we'll code an AI to teach itself how to play, and see if it can beat us!

## Getting Started 
Open a Terminal (or Powershell, for Windows) window, and follow the instructions below, typing the necessary commands in your terminal.

### Install Python
If you've taken a William & Mary CS course, you likely already have python installed. You can check if this is the case with the following command.

MacOS:
```
python3 --version
```

Windows:
```
py --version
```
If this shows a version number at or above 3.7, skip to the `pip` section. If not, you need to install python. Follow the instructions at [this link](https://www.python.org/downloads/) to download an up to date version of python. When you've finished downloading, you should be able to exit your terminal window, open a new one, and retry `python --version`. If it still doesn't work call one of us over.

### Install `pip`
Python's package manager is called `pip`, or Python Install Package. It allows you to essentially install code that other people wrote in order to make your code do more cool stuff.

Most of the time pip will be automatically installed when you download python. To check if you have `pip` installed, run

MacOS:
```
python3 -m pip --version
```

Windows:
```
py -m pip --version
```

If this shows a version number, skip to installing `pygame`. If not, try

MacOS:
```
python3 -m ensurepip --default-pip
```

Windows
```
py -m ensurepip --default-pip
```

Close and reopen terminal, and rerun the `--version`. If that still doesn't work, follow [these instructions](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line). You may need to call one of us over to help you follow these instructions.


### Installing `pygame` 
Once pip is installed, run the following command
```
pip install pygame
```
Let us know if you have any issues. This will install pygame a python library that abstracts away a lot of the hard to code parts of game design like repainting the screen, clock ticks, and more. We'll see a lot of these features in today's workshop.

## Setting up Files
Make a folder somewhere on your computer where you want to store this project. You can do this in File Explorer for Windows or Finder on Mac. If you're comfortable, you can also do this in the terminal by using `cd` to get to the location in which you want to create the folder, then using `mkdir` (make directory) as below:
```
mkdir flappy_bird_ai
```

### Download images
Now, download [this zip file](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3VwX3VlYmZFbkdFTEZsVlZZdFJNUlEzTy1SUXxBQ3Jtc0tuaWlFaFVEY1AzLTJuYnd1b28zN3NkVURIemZST0RaNDh4bF9WbWUydmRiOHVybDF3ZkNKVnloUG9qcEhScjhtX2ViejJHYXU0aXFrZVhnakp0d2NOSDQxdF9OdXhWTl91ZkRYZUd3bzFaSUJrQTBubw&q=https%3A%2F%2Fdev-cms.us-east-1.linodeobjects.com%2Fimgs_b286d95d6d.zip&v=ps55secj7iU) to the directory (folder) you just made. Unzip it by either double clicking on Mac, right clicking and clicking Extract on Windows, or, if you're comfortable:
```
cd flappy_bird_ai
```
```
unzip imgs_b286d95d6d.zip
```
(The zip file might have a different name for you)

Make sure it created an `imgs` folder, and then remove the zip file by moving to trash, or 
```
rm imgs_b286d95d6d.zip
```
Now we have a folder inside our project folder with images that we can use to animate each frame of the game!


### Python file
Make a file titled `flappy_bird.py` in your `flappy_bird_ai` folder. You can do this by creating it and saving it within your favorite text editor, like VSCode, or in the terminal from within that directory:
```
touch flappy_bird.py
```

If you haven't already, open that file in your favorite text editor (I'll be using VSCode).
Let's code up the initial pieces of the program. First we can copy over the following import statements, and constant definitions.

```py
import pygame
import time
import os
import random

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

WIN_WIDTH = 500 # can tweak these later if we notice the screen doesn't fit well
WIN_HEIGHT = 800
FLOOR = 730

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
```

We put these variables in all caps and can refer to them as constants, since by convention we won't be changing them. The widths and heights define measurements for parts of the program, and the IMG constants are references to the image assets we downloaded.

Take a look at the lines of code that get assigned to the IMG variables.
See if you can guess what some of the methods (function names after a `.`) are doing.
Also notice how the `os` and `pygame` library names are on the front of some of this code.
Without having imported these libraries, we wouldn't be able to call these methods.

Go ahead and run the program, just to make sure everything imports and loads in correctly, before we go any further.

```
python flappy_bird.py
```

<!-- ### Simple Game Logic
Before we code any further let's think conceptually about how we want this game to work. One feature we'll definitely need is a **game loop**. In almost any type of game, the program running it is almost constantly recieving input. Maybe that means it's checking for updates to score, listening for user input, like key presses or mouse clicks, or maybe it's checking if a Flappy Bird has collided with a pipe. 

One of the best ways to accomplish all of this in a game is to have a loop that runs with a  -->


## Classes
Let's take a step back and think about what objects we're going to need in this game. If you've ever played flappy bird, you know there's `Pipe`s and a `Bird`, at the very least. These will both need to have to attributes and abilities that we can code in.

In addition to these two classes we're going to make one for the ground called `Base`, since we want it to move with the game, so that the bird can stay in the center of the screen and still look like it's moving.

```py
class Bird:
    pass

class Pipe:
    pass

class Base:
    pass
```

*What are some ideas of methods or data these classes should store?*

## Game Loop
Once we have a handle on the structure of what is and going in  class, let's think about how we can run the game itself. When a game is running, it's constantly recieving input and producing output. This input consists of key presses, in our case the space bar, as well as input from within its own code, such as checking the positions of things like birds or pipes. The outputs in our case are things like movement of the bird and the score, and the general repainting of the screen.

*What are some ways we could code our game to properly handle all this simultaneous/constant checking and updating?*

One super common way is with a **game loop**. Basically, the loop runs and we check for various inputs, perform various actions and give various outputs, repeatedly, until the game is over. Here's some pseudocode for what our game loop could look like for Flappy Bird.

*What should happen every time the loop runs?*

```
loop
    move the bird
    if spacebar pressed
        bird jumps

    check for pipe collisions
        if so, exit loop
    check for passing pipes
        if so, add 1 to score
    move pipes forward

    check for ground or ceiling collision
        if so, exit loop

    move base (ground) forward
    print/paint/draw all this to screen
```

Let's comment this out, but keep it here for reference, and get started with some real coding! Before we code up the loop we need the objects used within it to actually be something.

## The `Bird` Class
Immediately inside the `Bird` class we're going to define some more constants. These ones are specific to the `Bird`s, so other classes won't be able to access these numbers directly.

```py
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25   # how much it will tilt
    ROT_VEL = 20        # how much we tile up/down each frame
    ANIMATION_TIME = 5  # changes how fast or slow bird flaps wings
```

First we reassign `BIRD_IMGS` to a shorter variable just for convenience.
The next two have to do with rotation.
When the bird is flying on the screen we want it to tilt a bit up right after we hit jump, and down when we haven't hit jump in a while, since it's falling.
We refer to this as rotation because it corresponds to how much the image rotates on screen.
`MAX_ROTATION` is the maximum it can tilt, and `ROT_VEL` is how much it till tilt per frame.
Finally, animation time has to do with the speed at which the bird will flap its wings, or in other words how often we switch from one picture of the bird, with its wings folded, to another, with its wings extended.

## `Bird` Constructor
Now we can write a constructor for the `Bird` class.


<details>
  <summary>What do you think we should include here to be initialized? (click to see code)</summary>

``` py
def __init__(self, x, y): # initialize the bird at starting location (x,y)
    self.x = x              # make x and y position attributes of the class
    self.y = y
    self.tilt = 0           # bird will be looking straight ahead
    self.tick_count = 0     # more later...
    self.vel = 0            # velocity = 0, bird starts at rest
    self.height = self.y    # more later...
    self.img_count = 0      # start with first image in array
    self.img = self.IMGS[self.img_count] # starting image of wing flapping animation
```
</details>

## `Bird` class `jump` method
When we click spacebar, we want the bird to jump. In other words, we want to give it some upwards velocity when this method is called.
In pygame, there is a coordinate system starting at (0,0) in the top left corner of the screen.
This means that moving up on the screen is going in the negative direction, so to jump up we need to give the bird a negative velocity. A bit counterintuitive!

```py
def jump(self):
    self.vel = -10
```

Let's set this as the velocity now, and we can come back to it later if the bird jumps too high or not high enough when we hit space.

Just like we did in the constructor, we're going to set the `tick_count` to 0 here, as well as setting `height` to `y`.

```py
def jump(self):
    self.vel = -10
    self.tick_count = 0
    self.height = self.y
```

We do this because we'll use these variables to do some physics calculations later. The tick count refers to how many *game ticks* since the most recent jump. This is the jump method, so the jump is happening now, so we reset it to 0. We'll increment it every *game tick* until the next jump.

The height stores the height value where the bird jumped from. More on this in the `move` method.


## `Bird` class `move` method
We're going to move once per tick.

```py
def move(self):
    self.tick_count += 1
```

We're going to use a kind of physicsy gravity equation to represent the movement of the bird. The `if` statement gives it a "terminal velocity" of sorts, at least when the bird is falling (remmeber, positive number means moving down in y direction).

```py
d = self.vel*self.tick_count + 1.5*self.tick_count**2
if d >= 16:
    d = 16
```

And we're going to give it a little extra spring in its step when it's jumping upward. Feel free to get rid of this or change it later, but I think it make the motion look good.

```py
if d < 0: # moving up
    d -= 2 # move up more
```

And now we update the position of the bird to match the outcome of this position function.

```py
self.y = self.y + d
```

Next, we want to use the information we have availible to us in this function to figure out which way we want to tilt the bird, and then indicate that.

*How should we decide which way to tilt the bird?*

The way we're going to do it is based on the initial point of the jump, stored in `self.height`. Above that, we'll face up, and once we fall below that we'll face down.

```py
if d < 0 or self.y < self.height + 50:
    if self.tilt < self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION
else:
    if self.tilt > -90: # tilt all the way, beyond max rotation
        self.tilt -= self.ROT_VEL
```

That's it for moving the bird. Now let's draw things to the screen to see our results.

## `Bird` class `draw` method
First we want to increment a counter since this is something we're calling every iteration of the loop. Then we want to flap the bird's wings by switching to a different image depending on what the count is.

*Can you explain how the code below works?*

```py
if self.img_count < self.ANIMATION_TIME:
    self.img = self.IMGS[0]
elif self.img_count < self.ANIMATION_TIME*2:
    self.img = self.IMGS[1]
elif self.img_count < self.ANIMATION_TIME*3:
    self.img = self.IMGS[2]
elif self.img_count < self.ANIMATION_TIME*4:
    self.img = self.IMGS[1]
elif self.img_count == self.ANIMATION_TIME*4 + 1:
    self.img = self.IMGS[0]
    self.img_count = 0
```

<details>
    <summary>Are there any times where we don't want the bird flapping?</summary>
    Sure, when it nosedives
</details>

```py
if self.tilt <= -80:
    self.img = self.IMGS[1]
    self.img_count = self.ANIMATION_TIME*2
```

Now we can rotate the image according to the tilt we calculated.

```py 
rotated_image = pygame.transform.rotate(self.img, self.tilt)
new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
win.blit(rotated_image, new_rect.topleft) 
```

The win.blit line takes an image and coordinate as arguments, and puts them on the screen (or at least gets them ready to be put on the screen when the display updates).

## `draw_window` function and `main` game loop
Let's write a simple draw_window function that we'll call on every iteration of our game loop.

```py
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()
```

We use `blit` again to put the background image on there, and then draw the bird on top of it with the method we just made. That technically won't change the screen until we call update, which reveals all the "drawing" we just did to the user.

Now let's start filling in our pseudocode from before. First we're going to put it all in a `main` function, which we'll call below.

```py
def main():
    #loop
    #move the bird
    #if spacebar pressed
    #    bird jumps

    #check for pipe collisions
    #    if so, exit loop
    #check for passing pipes
    #    if so, add 1 to score
    #move pipes forward

    #check for ground or ceiling collision
    #    if so, exit loop

    #move base (ground) forward
    #print/paint/draw all this to screen

main()
```

Now we can fill main with some initialization code, before the loop, and properly initialize the loop, as well as quit once we're out of the loop.

```py
bird = Bird(230, 350)
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

run = True
while run:
    # pseudocode....

pygame.quit()
return
```

Since we can tell pygame to quit by exiting the loop, let's make sure that clicking the red X will exit the program by adding this code.

Let's also call draw window on every iteration of the loop, like we said we would in pseudocode.

```py
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # pseudocode...
    draw_window(win, bird)
```

Now this code should be ready to run. Before we run it, let's think about what we should see.

Now take run it with `python flappy_bird.py` Cool! That's a flappy bird. There are three things we can fix here before we end for today.

1. We haven't used `move`
1. The bird is flapping crazy fast
3. We haven't used `jump`

Let's fix number one by calling `bird.move()` in the loop, like we said we would earlier in pseudocode.

```py
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    bird.move()
    draw_window(win, bird)
```

Now we see the bird is falling, due to our little fun with physics earlier, but it's still going really fast, just like how its wings were flapping.

We can implement a clock so that the loop only really runs once per "tick", or in our case 30 times per second. This is plenty of time for code to run through a whole block of execution, so we should expect pretty consistent results.

Adding that in, our main function will look like this

```py
def main():
    bird = Bird(230, 350)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        bird.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    return
```

Now if we run it again with `python flappy_bird.py`, we should see it more slow and steady. You can even comment out the move part to see the wings flapping slower in a more clear way.

The final thing we wanted to add today was jumping. So, let's start overwriting our pseudocode. `pygame` provides some methods to register keypress events, so all we have to do is put our jump method under a conditional.

```py
while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()

        bird.move()
        draw_window(win, bird, pipes, base, score)
```

After this you should be able to jump the bird when you run the program. We'll pick up adding in pipes and start talking about the AI next time!

---

<!-- ## Optional features
On your own time, see if you want to implement some of the following:
* Play again button
    * Instead of exiting after showing "You lost" for a few seconds, 
    * HINT: wrap main's contents in another loop
* Add sounds
    * Maybe a "wa wa wa" or "splat" for losing?
    * Perhaps a "flap flap flap" for jumping?
    * Maybe some background noises/music?
* Leaderboard
    * Requires players to enter a name after finishing
    * Requires some storage of player and score data in files
* Something else
    * show us next time!

## Next time
Next time we'll talk about how we would train an AI to play this game, and begin the process of coding one.
Steps (DON'T INCLUDE in workshop readme, might end up not doing git stuff)
* init git repo:
* commit this to main
* make neat-ai branch
    * going to get rid of user input stuff, change things around to implement AI
* talk conceptually / whiteboard about AI and NN
* download config file, explain NEAT
* do NEAT boilerplate (go thru this fast)
* etc... (there isn't much else)
* optional features beyond this -->
