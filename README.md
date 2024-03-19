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
touch flappy_bird_script.py
```

If you haven't already, open that file in your favorite text editor (I'll be using VSCode).
Let's code up the initial pieces of the program. First we can copy over the following import statements, and constant definitions.

```py
import pygame
import neat
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

*What are some ideas of methods or data these classes should store?*

Let's get started with some real coding!

### The `Bird` Class




## Optional features
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
* optional features beyond this
