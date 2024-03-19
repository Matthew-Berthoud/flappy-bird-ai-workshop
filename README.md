# Workshop 1: Flappy Bird Game
Today we're going to build a simple flappy bird game, which you can play by clicking the space bar to jump the bird.

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


### First python file
Make a file titled `flappy_bird_script.py` in your `flappy_bird_ai` folder. You can do this by creating it and saving it within your favorite text editor, like VSCode, or in the terminal from within that directory:
```
touch flappy_bird_script.py
```

If you haven't already, open that file in your favorite text editor (I'll be using VSCode).

### Game Skeleton
* imports 
* run it
* constants
* image constants
* run it
* set up simple game loop logic and talk conceptually
* run it

## Classes
* whiteboard the different classes, ask a lot of questions
* then go class by class to make the program

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
