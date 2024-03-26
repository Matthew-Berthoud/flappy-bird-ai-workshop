# Flappy Bird AI: Workshop 2: Finishing Flappy Bird Game
Today we're going to finish building the human-playable flappy bird game we started last time. Next week we'll start implementing an AI that can play the game for us!


## Review

If you missed last week's workshop:
-  [this](https://github.com/gdscwm/flappy-bird-ai-workshop/tree/main/workshop-1) will give you a more detailed explanation than this brief review
- Follow the setup steps in the link above to download the images and set up the file structure needed for this series.
- Once you have it set up, copy the code in `workshop-1/flappy_bird.py` into your local version of the file.
---


Last time 
* implemented bird class with various methods
    * what do each of these methods do?
* we got to the point where we have a game loop that runs at 30 ticks per second
    * What is a tick?


Today, we're going to implement the last two classes of the game: the moving floor, and the pipes!

## `Base` Class
Let's start with the `Base` class, which we defined (but didn't code) last time.

Recall that our bird isn't ever moving left or right, and the way we planned to show that it's moving forward is by moving the scenery backwards.

In our images folder, we have a base image. That image is only a little bit longer than our screen. So, if we want to make the base move left (backwards), we'll have to think of a creative solution so that we don't have the base moving off the screen.

<details>
  <summary>
    What are some good ways we can accomplish this?
  </summary>
  Let's take two instances of the base images, one spanning the bottom of the screen, and one to the right of it just off screen, and move them left. Then, when the first one gets completely offscreen, we can place it to the right of the second one, and repeat the cycle. Let's code this.
</details>

### Constructor

We first can define some constants and initialize the positions of the two base images. Recall from last time that for onscreen coordinates in `pygame`, the top left corner is `(0,0)`.

Our constructor is going to set the first base image to align with the left side of the screen, and the second one to align with the right end of the first one, as we discussed.

We're also going to take in the y coordinate of the base as an argument, and set that so the y coordinate for both the base images is the same.
                                                                        
```py
class Base:
    IMG = BASE_IMG
    WIDTH = IMG.get_width()

    def __init__(self, y):
        self.x1 = 0
        self.x2 = self.WIDTH
        self.y = y
```

### Movement
Now let's get the base moving, since that's like the whole point of it existing.

First we'll define a constant velocity that it will move at, to imply the velocity at which our bird is moving. This will be a class-level constant.

```py
class Base:
    VEL = 5
    ...
```

Like with the `Bird` class, we should update the position of the base every tick. So, we're going to create a method that we'll call every tick, in our game loop. Every tick, we'll move left `5`, by subtracting `VEL` from our current x position, stored in the x variables for both images.

```py
def move(self):
    self.x1 -= self.VEL
    self.x2 -= self.VEL
```

<details>
    <summary>If we were to run this as is, what would we see?</summary>
    The bases would move across the screen, then off the screen, without the replacement that we talked about needing. Let's fix this!
</details>

If the right side of either image falls off the left side of the screen, put the image back at the right side of the other image.

```py
def move(self):

    ...
    
    if self.x1 + self.WIDTH < 0:
        self.x1 = self.x2 + self.WIDTH

    if self.x2 + self.WIDTH < 0:
        self.x2 = self.x1 + self.WIDTH
```

Now that we in theory have the base moving, we probably want to see what that looks like.

### Drawing to Screen
As with `Bird`, we're going to make a `draw` method that will run every tick. It will be relatively simple, we'll just `blit` both base images to the window, at their current positions. Remember, the y is the same for both and never changes, since the ground isn't moving up or down.

```py
def draw(self, win):
    win.blit(self.IMG, (self.x1, self.y))
    win.blit(self.IMG, (self.x2, self.y))
```

In order to call this method, we have to define an object to call it on, so let's do that in main. We pass the `FLOOR` constant in to set the y value of the base image to `730`. Once initialized, we can pass this object into our `draw_window` function.
```py
def main():
    base = Base(FLOOR)

    ...

    while run:

        ...

        base.move()
        draw_window(win, bird, base)

    ...
```

We'll have to add a base argument to the `draw_window` signature, for the above to work. Now within `draw_window`, we can run the method. 

```py
def draw_window(win, bird, base):
    win.blit(BG_IMG, (0,0))

    base.draw(win)
    bird.draw(win)

    pygame.display.update()
```

Similar to `bird.draw(win)`, this will run every time `draw_window` does, which as we can see from main is every tick. This will keep the screen updated for our user.

Now our `Base` should be on screen, and moving. Go ahead and test it! If it doesn't run, or something looks buggy, go back through the steps or call one of us over to help.

```
python flappy_bird.py
```


## `Pipe` Class

Onto our final class, `Pipe`!

<details>
    <summary>
    Based on what we know about Flappy Bird and what we have written so far, what kind of information and functions is `Pipe` going to need to hold?
    <!-- init, move, draw are obvi, talk about the objective of the pipe - needs to have random height and know when bird collides with it -->
    </summary>

```python
class Pipe:
    # constants

    def __init__(self, x):
        pass

    def set_height(self):
        pass
    
    def move(self):
        pass
    
    def draw(self, win):
        pass
    
    def collide(self, bird):
        pass
```
</details>

Like `Base`, pipes are going to move left at a constant speed to give the illusion that the bird is moving. Pipes should move at the same rate as the ground, so let's define a class constant for `Pipe`'s velocity with the same value as `Base`:

```python
class Pipe:
    VEL = 5
```

One `Pipe` object contains both the top and bottom pipes, including the gap between them that the bird flies through. We'll define another class constant that will set the gap between the pipes. While we're at it, let's write the initializer as well. We'll throw zeroes in for values we'll fill in later.

```python
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):  # param x is the x-coordinate on the screen
        self.x = x
        self.height = 0     # height of the top of the gap
        
        self.top = 0        # the top of the top pipe
        self.bottom = 0     # the top of the bottom pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)   # flip our pipe.png image to use for the top pipe
        self.PIPE_BOTTOM = PIPE_IMG     # image for bottom pipe

        self.passed = False     # whether the bird has cleared the pipe
        self.set_height()
```

### Set Height

Notice that we call `set_height()` at the bottom of our init function. This function is going to set the variables we set to 0 above: `height`, `top`, and `bottom`.
- `height` is the top of the gap between the pipes, or in other words, the bottom of the top pipe. Each pipe should have a random height, but we want to limit it so the pipes don't go offscreen. *What range would be appropriate?*
- `top` and `bottom` are the top left coordinates of their respective pipe images. We'll need to do some simple math with `height` to determine what their values will be.

```python
    def set_height(self):
        self.height = ?
        self.top = ?
        self.bottom = ?
```

Next, we'll write our `move` and `draw` functions. These'll be pretty simple and similar to `Base`'s functions.

### Move
Every game tick, the pipe should move left a constant amount, its velocity. We don't need to have any special movement code like we did in Base, since each pipe only exists for the time it's on the screen. 

<details>
    <summary>
    What should this function look like? (Hint: it's a one-liner.)
    </summary>

```python
    def move(self):
        self.x -= self.VEL
```
</details>


### Draw
The pipe is really just two images with a gap between them. All we need to do for the draw function is draw the top and bottom pipes at the correct heights. We already defined variables in `set_height` to tell us where the top of each pipe segment should be -- now we just need to fill them in here.

Remember, the syntax for the `blit` function is `blit(image, (x, y))`, where (x, y) is the top-left coordinate of the image.

```python
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
```


### Collide
Last, but most definitely not least, we need a function that'll tell us when our bird rams into a pipe. Before we get into coding it, let's do a quick lesson on collision detection and masks.

Imagine each of our objects we see on the screen is contained in a box. The box has straight edges and is as small as possible, with the edges of the box touching as many of the object's edges as possible. This is how our pngs are structured. 

To detect collisions, we want to check if there is any overlap between objects.  We could do this just using our pngs with their tiny perimeter boxes, and many games do. But, since Flappy Bird is all about collisions, being a few pixels off in what the player sees as a collision and what the game reads as a collision matters a good deal.

Instead, we can use a **mask**. A mask is a bitmap that takes our png and sets all the opaque pixels and does not set transparent pixels. In other words, our mask takes our straight-edged box and vacuum-seals the interior around the visible object. Pygame has a built-in module to create and manage masks, called `Mask` (very descriptive).

Let's make use of this module, first in the `Bird` class. We're going to write a simple function that uses the `Mask` module to create a mask from the bird png. Here's what that's going to look like:

```python
    def get_mask(self):
        return pygame.mask.from_surface(self.img)   # Create a mask from a given surface (bird png)
```

Next, we'll write the `collide` function in our `Pipe` class. 

```python
    def collide(self, bird):
        # Get bird mask
        bird_mask = bird.get_mask()

        # Create pipe masks
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Find offset of each pipe in relation to bird
        top_offset = (self.x - bird.x, solf.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Check if bird mask overlaps with pipe mask. If they don't, these lines return None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 
        t_point = bird_mask.overlap(top_mask, top_offset) 

        # If either t_point or b_point are not None, we have a collision
        if t_point or b_point:
            return True

        return False
```

[Visualization of offsets.](https://www.pygame.org/docs/ref/mask.html#mask-offset-label)


### Back to main

The last thing we need to do is add the pipes to our game loop. In `main`, we're going to define the pipes as a list, so that we can add and remove to it as needed. Add this line to the top of the `main` function:

```python
    def main():
        bird = Bird(230, 350)
        base = Base(FLOOR)
        pipes = [Pipe(600)]     # Addition here. 600 is the x-coordinate for the pipe.
        ...
```

Next, we're going to add some logic to the game loop to check 

(a) if the bird has collided with the pipe, using our nice `collide` function we just wrote, 

(b) if a set of pipes has gone offscreen and needs to be removed, and 

(c) if the bird has successfully cleared a pipe and we need to add a new one. We can do this with a series of if statements.

```python
def main():
    ...
        
    add_pipe = False
    rem = []  # list of pipes to remove
    for pipe in pipes:
        if pipe.collide(bird):                      # (a)
            run = False
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # (b)
            rem.append(pipe)
        if not pipe.passed and pipe.x < bird.x:     # (c)
            pipe.passed = True
            add_pipe = True

        pipe.move()

    # Add a new pipe offscreen if necessary
    if add_pipe:
        pipes.append(Pipe(700))

    # Remove pipes that have gone offscreen
    for r in rem:
        pipes.remove(r)
    
    base.move()
    draw_window(win, bird, pipes, base)  # Change here!
```

Notice that we added another parameter to the `draw_window` function call. Let's go back and edit `draw_window` to reflect that.

<details>
<summary>
Remember that `pipes` is a list. How will the code look for drawing each pipe onscreen?
</summary>

```python
def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    ...
```
</details>


Our game is now playable! 

However, *are there any bugs or missing features we might want to include?*


## Score
Right now the game might be fun, but we don't keep score, so how are we supposed to know if we're the best flappy birder in the workshop? Let's solve this glaring issue.

<details>
<summary>Where should we (1) initialize and (2) increment this score variable?</summary>

We want to declare this varible in main, set it to 0. Then we can increment it every time we pass a pipe in the game loop. We already set the `add_pipe` Boolean whenever the bird moves under the pipe, so we can use that to be our condition for the score to increment. We'll add a print line to make sure it's updating.

```py
def main():
    
    ...

    score = 0
    run = True
    while run:
        
        ...

        if add_pipe:
            score += 1
            print(score)
            pipes.append(Pipe(700))
        
        ...
```
</details>

*Would a volunteer like to come up and play the game to see if the score is working?* (I am bad at this game and cannot do it myself)

We can do better for our players than just printing score to the terminal. Let's display some text to the screen showing the score, whenever we update the display. To do that, first make sure you have the `STAT_FONT` constant defined at the top of your file. 

```py
STAT_FONT = pygame.font.SysFont("comicsans", 50)
```

If you want, you can change this to another font besides comic sans. Just look up the `SysFont` documentation!

Next, let's make use of our `draw_window` function again, since this is a drawing action. We have to pass in `score`, since it's locally defined in `main`. Go ahead and change the function definition **and** function call to look like this:

```py
def draw_window(win, bird, pipes, base, score):
```

```py
draw_window(win, bird, pipes, base, score)
```

Now we can the score argument within `draw_window`.

```py
def draw_window(win, bird, pipes, base, score):
    
    ...

    bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()
```

We're now showing the player the score, and actively updating it when they pass a new pipe! Go ahead and run your code to see what it looks like.


## User Friendly Ending
Another problem we notice is that when you hit a pipe, the game ends and the program quits immediately. You barely even have time to look at your final score so you can brag to your friends!

There are a number of ways we could change our game design to handle this, like playing some sad music before quitting, or sending the user to a home screen where they could choose to play again, etc. For our purposes, we're going to keep it simple and just tell the player they lost, wait a few seconds, then quit the program as normal.

<details>
<summary>How can we tell when the game is over?</summary>

1. When `run` is `False`
2. When we've exited the game loop (because `run` is `False`)

</details>

Let's use option 2 to implement a couple seconds of delay before quitting. The following approach is a bit hacky, but it's simple. We're going to import the `time` library, and call `sleep` for 3 seconds, or however long you like. This just makes the process stall there and not do anything for however many seconds you specify.

We'll call `sleep` right before `pygame.quit`, so we leave the window up, motionless, for a bit when the game is over before quitting.

```py
def main():

    ...

    while:

        ...

    time.sleep(3)
    pygame.quit()
    quit()
```

Be careful to ensure that you don't indent this line into the scope of the while loop, since we only want it to run when the game is over.


Next, let's use option 1 to print a "You lost!" message. Since our drawing happens in the `draw_window` function, and that's within the game loop, let's simply pass in `run`.

```py
base.move()
draw_window(win, bird, pipes, base, score, run)
```

Now, in draw_window itself, let's add some code to print "You lost", if `run` is False, and therefore the game is over.

Be sure to change the argument list to include `run` in both the place where we define `draw_window`, and where we call it.

```py
def draw_window(win, bird, pipes, base, score, run):

    ...
    
    if not run:
        text = STAT_FONT.render("You lost.", 1, (255,255,255))
        # win.blit(text, (middle_of_screen))

    pygame.display.update()
```

<details>
<summary>How can we get the coordinates of the middle of the screen?</summary>

Divide the width and the height of the window by two, and use those values as x and y coordinates.

Let's code that in and run it.

```py
win.blit(text, (WIN_WIDTH / 2, WIN_HEIGHT / 2))
```

</details>


<details>
<summary>Okay that looks off-center. Why?</summary>

It's placing the top left corner of the textfield in the center.

</details>

<details>
<summary>How can we fix it?</summary>

Subtract half the length and width of the textfield itself, so the center of the text field is the true center.

```py
win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, WIN_HEIGHT / 2 - text.get_height() / 2))
```

Let's run that.
</details>

That looks great!

## More Collisions
As it stands right now, players can fly over or under the pipe images and never die. This isn't desired behavior! 

<details>
<summary>How can we fix this?</summary>
Let's add some code that makes colliding with the floor or the ceiling just as dangerous as colliding with a pipe.


```py
def main():

    ...

    while run:

        ... 

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= FLOOR or bird.y <=0:
            run = False

        base.move()

        ...

```

This will make our game loop end when we hit the ground, the ceiling, or a pipe.
</details>
Let's test it!



## Fun Ideas
If you find yourself bored over the next week, see if you can implement some of the following:
* Playing again without the program quitting in between
* A leaderboard
* Sound effects and/or music

Next time, we're going to redownload a simple version of the code, without any user input, so that we can have an AI run the game.
