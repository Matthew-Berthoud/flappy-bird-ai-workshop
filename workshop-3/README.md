# Flappy Bird AI: Workshop 3: Building an AI to Learn the Game
The past couple weeks we've built a flappy bird game with pygame that we can play on our computer by clicking the spacebar. Today we're going to 
1. download a new skeleton file with some of those features removed, so that we can build an AI that will learn the game. Then, 
2. we're going to talk about neural networks, and genetic algorithms
3. we're going to write the code that will have an AI learn our game



## Setup

### Review
Double check you have `pygame` installed with the setup instructions in [Workshop 1](https://github.com/gdscwm/flappy-bird-ai-workshop/tree/main/workshop-1). Also download the `imgs` folder from any workshop's folder in this repository, or the link in workshop 1's instructions.


### NEAT installation
Next, we're going to install a python library called `NEAT`, by running 
```
pip install neat
```
just like how we installed `pygame` in the first workshop.


### Two new files
Make two new files called `flappy_bird_ai.py` and `config-feedforward.txt` in the same directory you've been using for this workshop, and copy over the code from those files in this repo (alternatively, you could download both files).

The python file is a simplified version of the flappy bird code we've been writing, with some features removed, such as accepting user input.
By having two separate files, you can work on your human-playable flappy bird game separately from your AI-playable game, and have both availible.

<details>
<summary>What are the differences between last week's file and this week's file?</summary>

1. Removed the code allowing you to click spacebar to jump
2. Removed "you lost" and `run` parameter in `draw_window`, as well as timer sleep when the loop exits
    1. When we implement the AI, the program is never going to exit, since the birds will learn to play the game perfectly!

</details>

The config file contains some options that we've set for the NEAT model to work with. We'll go over those options in detail once we've discussed NEAT overall.


## What is NEAT?
Now let's talk about NEAT, and neural networks in general.


### Neural Networks
<details>
<summary>What is a neural network?</summary>

A neural network is a Machine Learning (ML) or AI model that tries to make decisions as if it was a human brain. It's a data structure representing a network of connected nodes, or "neurons" that send numbers to one another with various weights (more numbers). This is somewhat analogous to neurons communicating with one another in the human brain.

</details>

<details>
<summary>What are the parts of a neural network?</summary>

1. Input Layer

    <details>
    <summary>What inputs do we need for flappy bird?</summary>

    1. Bird position (y)
    2. Top pipe position (y)
    3. Bottom pipe position (y)

    *Could we do it with less?*

    </details>

2. Hidden Layer(s)

    This is where input data gets transformed into output data, through a series of neurons and weights. Our model will build the hidden layer for us, over the course of "generations." More on this later

3. Output Layer/Node

    <details>
    <summary>What outputs do we need?</summary>

    To jump or not to jump!

    </details> 

</details>

Our flappy bird will get a neural network associated with it. Each time the game loop runs, our network will take in these input layer numbers (bird, and pipe positions), multiply them by some weight numbers, take the sum of all that, and then pass that weighted sum into an **activation function**.

<details>
<summary>What is an activation function?</summary>

Since our outcome needs to be a binary decision (either jump or don't jump) we need some way to convert a numeric output into a essentially a yes or a no. 

We're going to use the `tanh` function, which maps any x value to a value between 0 and -1, with positive values going to 1 and negative values going to -1. 

Then we can select a cutoff point, below which the bird won't jump and above which the bird will jump

</details> 

<details>
<summary>How do we determine the weights?</summary>

NEAT will determine the weights. More on this soon. NEAT will also determine whether we want to split up one of the pathways and make a node in the hidden layer. 

</details>


### NEAT: NeuroEvolution of Augmenting Topologies

We need some way of choosing weights such that weighted sum of our input variables (the positions of the pipe bottom, pipe top, and bird), subject to the activation function, only have a value near one when the bird truly should jump.

There are many many ways to train neural networks, but for this model we've chosen to use a form of NeuroEvolution. The basic idea behind neuroevolution is that there are generations of a species of neural networks, such that successful neural networks prevail and reproduce, and unsuccessful neural networks die out.

This sounds a little abstract. What it means in our case is we're going to run the game with like 20 birds simultaneously. Each bird will have a neural network assigned to it, with randomly selected weights. The birds will play the game, making a decision to jump or not on every tick based on the input data for their current position relative to the pipes. As birds hit the pipes, they "die." Once every bird in the generation dies, the few that made it the furthest "reproduce," meaning essentially that the next generation of birds will have weights similar to theirs, with some randomness thrown in. In theory, if we let this run enough times, there will eventually be a bird that becomes at fit with its environment, and is perfect at flappy bird.

The NEAT model in particular does some specific things we won't get into in order to derive the weights between generations. This is what the "Augmenting Topologies" refers to.

For more information about NEAT, the original researchers who developed NEAT wrote a somewhat digestible 6-page paper you can find [here](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf). Also, refer to the NEAT python API [here](https://neat-python.readthedocs.io/en/latest/). 


### NEAT python configuration
Now that we've talked conceptually about what we're going to do, we can dive into doing it! Go ahead and open the `config-feedforward.txt` file we had you copy/download. This file is required by the NEAT Python API in order to conduct the Neuroevolution algorithm. 

Lots of this is the default settings, and we won't get into all of it(again, I encourage you to read more for yourself from [the documentation](https://neat-python.readthedocs.io/en/latest/)), but we'll touch on some key settings. 

Some notable lines in this config file are:
* `fitness criterion = max` makes sure we're keeping the MOST fit birds, not the least fit. Not sure why we'd keep the least fit, but feel free to look that up
* Whenever we reach a `fitness_threshold` of 100, we'll terminate the program, because this means we have a bird that is performing well enough
* `pop_size` sets the number of birds in each generation
* `reset_on_extinction = False` makes it so that the program doesn't quit if all the birds die
* The `# node activation options` make it so we only use the tanh activation function, and never change that
* The `# node aggregation options` make sure we don't do anything besides a weighted sum to "aggregate" the nodes before passing that into the activation function
* The `# bias options` have to do with bias, which we can think of as another node feeding into the result, like a y-intercept of sorts
* The `# network parameters` are just the starting number of nodes that we talked about, but as we can see there's  some other sections that deal with adding/removing hidden layer nodes
* the `#connection enable options` make it so that 1% of the time, when generating a new bird, a neural network connection is removed (weight set to 0)
* Way at the bottom, the `max_stagnation` is set to `20`, meaning if 20 generations go by without the fitness increasing, the program will terminate.


## Let's code

The first thing we need to do to work with NEAT is load in this configuration file that we just talked about.

Let's make a new main "function" (not really a function) to put this code in. I'll explain why we're making this new main soon.

The first line below gets the directory where the file we're coding is located. The second line creates a filepath from that plus the name of the config file we just talked about. Then, we pass that into a new function we'll write called `run`.

```py
def run(config_path):
    pass

if __name == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
```

Now, in the `run` function, this first line initializes the neat configuration with all the settings we set up in that config file. Notice how the headings in the config file match these parameters we're passing. The second line sets up a neat `Population` with those settings.

```py
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
```

Now we're going to add some "reporters" to the population that will print important information about each generation in the terminal, as we run the code later.

```py
def run(config_path):
    ... 

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

```

The final line of our `run` function is actually going to run something, now that our neat model is all configured and ready to go. The argument that right now is just `???` will be the name of a fitness function to run, and the `50` is how many generations, or times it will run. In our case, we'll probably get a perfect bird well before the 50th generation.

```py 
def run(config_path):
    ...

    winner = p.run(???, 50) 
```

<details>
<summary>What should the function we pass in do?</summary>

Run the game loop, but with 20 birds at the same time. So, we can pass in the main function to this commmand, and the score achieved by each bird will be that bird's fitness!

Be sure to remove the call to `main` from the outermost scope now, since it gets called from in here

</details>

### Collisions and fitness

Now we have to modify `main` to take in `genomes` and `config`. We'll also begin keeping track of generation as a global variable, so it retains its value between calls to main. Each time main runs, however, is a different generation, so we'll increment it at the start.

```py
GEN = 0

...

def main(genomes, config): 
    global GEN
    GEN += 1
```

Now, since we want to run this with multiple birds instead of just 1, we have to make a list of birds that the function will work with. Now, for the collision detection, we have to check pipe collisions for ALL the birds, and floor or ceiling collisions for ALL the birds.

```py
def main(genomes, config):
    global GEN
    GEN += 1

    birds = []

    ...

    for pipe in pipes:
        for x, bird in enumerate(birds):
            if pipe.collide(bird):
                # bird dies
                pass

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
    

    ...

    for x, bird in enumerate(birds):
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0: # don't let birds go outside of top or bottom of screen to get around pipes
            # bird dies
            pass
```

Recall that each bird corresponds to a neural network, and can be referred to as a genome, so we're going to create two more lists to keep track of these things, whose indexes can correspond to that of birds. What I mean is that the bird object at index 2 of `birds` will "have" the neural network at index 2 of `nets` etc. 

```py
birds = []
nets = [] # neural networks
ge = [] # genomes
```

We'll now initialize these lists right below that. The first four lines are just the way we're meant to initialize the networks for each genome, as per the documentation. And the last line makes us a bird who gets added to our birds list.

```py
for _, g in genomes: 
    net = neat.nn.FeedForwardNetwork.create(g, config)
    nets.append(net)
    g.fitness = 0
    ge.append(g)

    birds.append(Bird(230, 350))
```

Now we can write the necessary code to "kill" our birds when they collide with a pipe, or the ground. Write the following code in both locations. The first line removes some fitness if they hit the pipe, so that there is some differentiation between birds who have the same score, one of whom hit the pipe and one of whom continued.

```py
ge[x].fitness -= 1
birds.pop(x)
nets.pop(x)
ge.pop(x)
```

Make sure to change both your for loops to
```py
for x, bird in enumerate(birds):
```
so you can use the `x` index variable.

We're also going to encourage birds to go through the pipe by adding fitness whenever that happens.

```py
if add_pipe:
    score += 1
    for g in ge:
        g.fitness += 5
    pipes.append(Pipe(700))
```

<details>
<summary>Wouldn't this code just add fitness to every bird regardless, since we're looping through all genomes?</summary>

No, since the birds that have already collided get removed earlier.

</details>

### Moving and Jumping

Okay so now we have some fitness-related adjustments happening, but we haven't actually written code to make the bird move, fed anything to the neural networks, or written any code to make the bird jump. Recall that we're going to pass in some input data to the neural network, for each bird at each tick, and based on that it will make a decision to jump. With our tanh activation function we're decidng that a value greater than `0.5` will mean the bird should jump.

Note that output will come in a list, and we have to go to its 0th index. That's because sometimes the output layer has more than one neuron.

```py

while run:

    ...

    for x, bird in enumerate(birds):
        bird.move() # move at every tick
        ge[x].fitness += 0.1 # give it a little fitness when it stays alive at each tick

        # evaluate neural network from input data, get output value

        if output[0] > 0.5:
            bird.jump()

```

Before we can write the code to evaluate the neural network, we have to determine which pipe we're looking at in order to get its top and bottom y values. There will always only be two pipes in the list, so we can choose between index 0 and 1 with the following.

Note that we're also checking if the birds list is empty before doing any of this, because 1) we're using birds as if it's not empty later in the while loop, and 2) that means all birds are dead so we should exit the game loop, since our generation is over.

```py
pipe_ind = 0
if len(birds) > 0:
    if len(pipes) > 1 and birds[0].x  > pipes[0].x + pipes[0].PIPE_TOP.get_width():
        pipe_ind = 1
else:
    run = False
    break
```

Now that we've figured out what pipe in the list we're looking at to determine our neural network inputs, we can replace our comment from earlier with the following to activate a neural network with our 3 inputs:
1. The bird's y
2. The bird's distance from the top pipe
3. The bird's distance from the bottom pipe

```py
output = nets[x].activate((bird.y,
        abs(bird.y - pipes[pipe_ind].height),
        abs(bird.y - pipes[pipe_ind].bottom)))
```


### Drawing
We need to slightly change our draw_window function, by the way, since we have a list of birds instead of a single bird now. We can also print the generation of the model on the screen, along with score. Make sure to change not just the declaration, but where the function is called too!

```py
def draw_window(win, birds, pipes, base, score, gen):

    ...
    
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
```


### Cleaning up

Since `main` is no longer our main function, we can
1. Rename it to `eval_genomes`, just for good practice, so it's clearer what it does
2. Move the `pygame.quit()` and `return` lines from outside the loop, to after our confitional checking for `pygame.QUIT`
    1. We want to run multiple generations, not quit every time we're outside the game loop.
    2. Also change `return` to `quit()` since returning from main won't exit the program anymore
    ```py
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # red X in top corner of pygame window
                run = False
                pygame.quit()
                quit()
    ```

___

With all that done, your code should be done and ready to run! Enjoy watching your generations of birds learn how to flap!


```
python flappy_bird_ai.py
```

Also, feel free to mess with the parameters in the config file and the various places where we add or remove fitness to see if you can get the birds to perform better or worse!

This is likely our last workshop of the semester, so thank you all for coming, and we'll see you next time!