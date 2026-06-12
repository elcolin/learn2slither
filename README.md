# Q-Learning in Snake

![Stat Example](doc/performance.png)

This project explores reinforcement learning through the **Q-learning function**.  
Here are the rules:

- The game mimics a snake, the snakes needs to reach a size of 10 in order to win the game.  
- To grow the snake needs to eat green apples, red apples make him smaller.  
- If the snake reaches a null length, goes into a wall, eats himself, he dies.

## Model

![Snake Diagram](doc/snake_state.jpg)

The model will **estimate what will be the best future action in a given state** and sometimes will be choosed randomly.  
Howewer, **whether it is true or not, it will influence the q value of that specific choice**. This allows to introduce a random factor without it being destructive (ie go into a wall).

TODO :

- Add time count
