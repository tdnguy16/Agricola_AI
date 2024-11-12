import gym
# import optuna
import random
import numpy as np
from stable_baselines3 import PPO
# from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from gym import spaces
import sys
import matplotlib.pyplot as plt
from collections import Counter
import copy

round = 1

reward = 0

agent_action_used = []
partner_action_used = []
action_used = []


moves_total_names = ['action_a', 'action_b', 'action_c',
                          'action_d', 'action_e', 'action_f',
                          'action_g', 'action_h', 'action_i', 'action_j', 'action_k', 'action_l',
                          'action_m', 'action_n', 'action_o', 'action_1', 'action_2', 'action_3',
                          'action_4', 'action_5', 'action_6', 'action_7', 'action_8', 'action_9',
                          'action_10', 'action_11', 'action_12', 'action_13', 'action_14']


# pasteur price[clay,reed,wood]
pasteur_2 = {'price': [0, 0, 3], 'capacity': 2}
pasteur_4 = {'price': [0, 0, 5], 'capacity': 4}
pasteur_6 = {'price': [0, 0, 6], 'capacity': 6}
pasteur_8 = {'price': [0, 0, 7], 'capacity': 8}
pasteur_list = [pasteur_2, pasteur_4, pasteur_6, pasteur_8]

# improvement = {'price': [0,0,0], 'grain_wood_food': , 'sheep_food': , 'boar_food': , 'cow_food': , 'clay_food': , 'reed_food': , 'wood_food': , 'grain_food': , 'clay_point': , 'reed_point': , 'wood_point': , 'grain_point': , '3_random_point': }
improvement_2 = {'name': 'improvement_2', 'price': [2, 0, 0],
                      'resource_food': {'grain_wood_food': 2, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                        'grain_food': 0},
                      'livestock_food': {'sheep_food': 2, 'boar_food': 2, 'cow_food': 3},
                      'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                '3_random_point': 0}}
improvement_3a = {'name': 'improvement_3a', 'price': [3, 0, 0],
                       'resource_food': {'grain_wood_food': 5, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                         'grain_food': 0},
                       'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                       'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                 '3_random_point': 0}}

improvement_3 = {'name': 'improvement_3', 'price': [3, 0, 0],
                      'resource_food': {'grain_wood_food': 2, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                        'grain_food': 0},
                      'livestock_food': {'sheep_food': 2, 'boar_food': 2, 'cow_food': 3},
                      'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                '3_random_point': 0}}

improvement_4a = {'name': 'improvement_4a', 'price': [4, 0, 0],
                       'resource_food': {'grain_wood_food': 5, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                         'grain_food': 0},
                       'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                       'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                 '3_random_point': 0}}

improvement_4 = {'name': 'improvement_4', 'price': [4, 0, 0],
                      'resource_food': {'grain_wood_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                        'grain_food': 0},
                      'livestock_food': {'sheep_food': 2, 'boar_food': 3, 'cow_food': 4},
                      'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                '3_random_point': 0}}

improvement_5 = {'name': 'improvement_5', 'price': [5, 0, 0],
                      'resource_food': {'grain_wood_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                        'grain_food': 0},
                      'livestock_food': {'sheep_food': 2, 'boar_food': 3, 'cow_food': 4},
                      'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                '3_random_point': 0}}

improvement_7 = {'name': 'improvement_7', 'price': [3, 0, 1],
                      'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                        'grain_food': 3},
                      'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                      'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 1,
                                '3_random_point': 0}}

improvement_9 = {'name': 'improvement_9', 'price': [0, 1, 2],
                      'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 3, 'wood_food': 0,
                                        'grain_food': 0},
                      'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                      'point': {'clay_point': 0, 'reed_point': 1, 'wood_point': 0, 'grain_point': 0,
                                '3_random_point': 0}}

improvement_10 = {'name': 'improvement_10', 'price': [1, 2, 0],
                       'resource_food': {'grain_wood_food': 0, 'clay_food': 2, 'reed_food': 0, 'wood_food': 0,
                                         'grain_food': 0},
                       'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                       'point': {'clay_point': 1, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                 '3_random_point': 0}}

improvement_11 = {'name': 'improvement_11', 'price': [2, 0, 1],
                       'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 2,
                                         'grain_food': 0},
                       'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                       'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 1, 'grain_point': 0,
                                 '3_random_point': 0}}

improvement_14 = {'name': 'improvement_14', 'price': [1, 1, 1],
                       'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                         'grain_food': 0},
                       'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                       'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                 '3_random_point': 1}}

# init game state
round = 1
previous_round = 0

# initial game resources
board_resource = {'2_clay': 2, '1_clay': 1, 'reed': 1, '1_wood': 1, '2_wood': 2, '3_wood': 3, 'food': 1,
                       'sheep': 1, 'boar': 0, 'cow': 0, 'round': 1}
reserve_resource = {'clay': 27, 'reed': 19, 'wood': 34, 'grain': 31, 'food': 71, 'sheep': 25, 'boar': 19,
                         'cow': 17, 'begging': 5}

improvements = [improvement_2, improvement_3a, improvement_3, improvement_4a,
                     improvement_4, improvement_5]
tiles = {'pasteur_2': 20, 'pasteur_4': 13, 'pasteur_6': 2, 'pasteur_8': 1, 'field': 20, 'stable': 10,
              'room': 12}


# initial player resources
player1_state = {'valid_action': 0, 'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0,
                      'grain': 0, 'food': 0,
                      'sheep': 0, 'boar': 0,
                      'cow': 0,
                      'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                      'room_space': 2, 'livestock_space': 1, 'farmer': 3,
                      'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 1, 'pasteur_6': 0, 'pasteur_8': 0,
                      'stable': 0, 'field': 0}
player1_improvements = []
player1_field_dict = {}

player1_previous_state = copy.deepcopy(player1_state)

player2_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                      'food': 0,
                      'sheep': 0, 'boar': 0,
                      'cow': 0,
                      'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                      'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                      'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                      'stable': 0, 'field': 0}
player2_improvements = []
player2_field_dict = {}

player3_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                      'food': 0,
                      'sheep': 0, 'boar': 0,
                      'cow': 0,
                      'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                      'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                      'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                      'stable': 0, 'field': 0}
player3_improvements = []
player3_field_dict = {}

player4_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                      'food': 0,
                      'sheep': 0, 'boar': 0,
                      'cow': 0,
                      'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                      'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                      'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                      'stable': 0, 'field': 0}
player4_improvements = []
player4_field_dict = {}

player_state_list = [player1_state, player2_state, player3_state, player4_state]

player_1_points = 0
player_2_points = 0
player_3_points = 0
player_4_points = 0

player_1_harvesting_check = {4 :1, 7 :1, 9 :1, 11 :1, 13: 1, 14 :1}
player_2_harvesting_check = {4 :1, 7 :1, 9 :1, 11 :1, 13: 1, 14 :1}
player_3_harvesting_check = {4 :1, 7 :1, 9 :1, 11 :1, 13: 1, 14 :1}
player_4_harvesting_check = {4 :1, 7 :1, 9 :1, 11 :1, 13: 1, 14 :1}

# --------------------------------------------------------------------------------------------------------------------------------------------------#
def remove_actions(self, actions_to_remove):
    moves = [action for action in moves if action.__name__ not in actions_to_remove]


def action_5(player_state, player_field_dict, player_improvements):
    # Remove this action from the current round
    # remove_actions(['action_5'])

    if player_state['farmer'] < 5:
        if (player_state['room_space'] + player_state['clay_room'] + player_state['wood_room']) > player_state['farmer']:
            player_state['farmer'] = player_state['farmer'] + 1
        else:
            print('not enough rooms')
            pass
    else:
        print('no more farmers')
        pass




player1_state = {'valid_action': 0, 'action': 0, 'point': 0, 'round': 0, 'clay': 3, 'reed': 0, 'wood': 1,
                      'grain': 3, 'food': 2,
                      'sheep': 0, 'boar': 2,
                      'cow': 0,
                      'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 2, 'wood_room': 1,
                      'room_space': 2, 'livestock_space': 1, 'farmer': 5,
                      'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 1, 'pasteur_6': 0, 'pasteur_8': 0,
                      'stable': 0, 'field': 0}
player1_improvements = [improvement_3a]
player1_field_dict = {}


print(reserve_resource)
print(player1_state)

action_5(player1_state, player1_field_dict, player1_improvements)

print(player1_state)

print(reserve_resource)
