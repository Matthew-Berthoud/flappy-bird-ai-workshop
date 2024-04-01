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
2. Hidden Layer(s)
3. Output Layer/Node

</details>




For more information about NEAT, the original researchers who developed NEAT wrote a somewhat digestible 6-page paper you can find [here](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf). Also, refer to NEAT python API [here](https://neat-python.readthedocs.io/en/latest/). 


## Let's code