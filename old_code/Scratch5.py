import gym
# import optuna
import random
import numpy as np
# from stable_baselines3 import PPO
# from stable_baselines3.common.env_checker import check_env
# from stable_baselines3.common.evaluation import evaluate_policy
from gym import spaces

moves = ['a','b','c','d','e','f','g','h','i','j']

def update_action_space(playing_order, p1_actions, p2_actions, p3_actions, p4_actions):
    player_actions = [p1_actions, p2_actions, p3_actions, p4_actions]
    remaining_actions = sum(player_actions)

    x = len(moves)

    action_space_list = []

    while remaining_actions > 0:
        for i in playing_order:
            if i == 1 and p1_actions > 0:
                print('Player 1 takes action')
                action_space_list.append(x)
                x -= 1
                p1_actions -= 1
            if i == 2 and p2_actions > 0:
                print('Player 2 takes action')
                x -= 1
                p2_actions -= 1
            if i == 3 and p3_actions > 0:
                print('Player 3 takes action')
                x -= 1
                p3_actions -= 1
            if i == 4 and p4_actions > 0:
                print('Player 4 takes action')
                x -= 1
                p4_actions -= 1
        remaining_actions = p1_actions + p2_actions + p3_actions + p4_actions

    return action_space_list



action_space_list = update_action_space([3, 4, 1, 2], 3, 2, 2, 1)

print(action_space_list)

action_space = spaces.MultiDiscrete(action_space_list)