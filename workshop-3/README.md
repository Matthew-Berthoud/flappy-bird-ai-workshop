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


## Let's code
Now that we've talked conceptually about what we're going to do, we can dive into doing it! Go ahead and open the `config-feedforward.txt` file we had you copy/download. This file is required by the NEAT Python API in order to conduct the Neuroevolution algorithm. 

Lots of this is the default settings, and we won't get into all of it(again, I encourage you to read more for yourself from [the documentation](https://neat-python.readthedocs.io/en/latest/)), but we'll touch on some key settings. 

First look at