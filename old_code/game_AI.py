import random
from enum import Enum
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
import logging
import gym
from gym import spaces
import sys

# Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

### improvement tiles
#   improvement_2, improvement_3a (no livestocks), improvement_3b, improvement_4a (no livestocks), improvement_4b, improvement_5
#   improvement_7, improvement_9, improvement_10, improvement_11, improvement_14
#   price [clay, reed, wood]




class AgricolaAI:

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.reset()

    def reset_game(self):
        self.round = 1
        self.reset()

    def reset(self):
        # Unlock round actions
        self.moves = [self.action_a, self.action_b_1, self.action_b_2, self.action_b_3, self.action_b_4, self.action_b_a, self.action_c_1, self.action_c_2, self.action_c_3, self.action_c_4, self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o]

        # pasteur price[clay,reed,wood]
        self.pasteur_2 = {'price': [0, 0, 3], 'capacity': 2}
        self.pasteur_4 = {'price': [0, 0, 5], 'capacity': 4}
        self.pasteur_6 = {'price': [0, 0, 6], 'capacity': 6}
        self.pasteur_8 = {'price': [0, 0, 7], 'capacity': 8}
        self.pasteur_list = [self.pasteur_2, self.pasteur_4, self.pasteur_6, self.pasteur_8]

        # improvement = {'price': [0,0,0], 'grain_wood_food': , 'sheep_food': , 'boar_food': , 'cow_food': , 'clay_food': , 'reed_food': , 'wood_food': , 'grain_food': , 'clay_point': , 'reed_point': , 'wood_point': , 'grain_point': , '3_random_point': }
        self.improvement_2 = {'name': 'improvement_2', 'price': [2, 0, 0],
                              'resource_food': {'grain_wood_food': 2, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                'grain_food': 0},
                              'livestock_food': {'sheep_food': 2, 'boar_food': 2, 'cow_food': 3},
                              'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                        '3_random_point': 0}}
        self.improvement_3a = {'name': 'improvement_3a', 'price': [3, 0, 0],
                               'resource_food': {'grain_wood_food': 5, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                 'grain_food': 0},
                               'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                               'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                         '3_random_point': 0}}

        self.improvement_3 = {'name': 'improvement_3', 'price': [3, 0, 0],
                              'resource_food': {'grain_wood_food': 2, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                'grain_food': 0},
                              'livestock_food': {'sheep_food': 2, 'boar_food': 2, 'cow_food': 3},
                              'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                        '3_random_point': 0}}

        self.improvement_4a = {'name': 'improvement_4a', 'price': [4, 0, 0],
                               'resource_food': {'grain_wood_food': 5, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                 'grain_food': 0},
                               'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                               'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                         '3_random_point': 0}}

        self.improvement_4 = {'name': 'improvement_4', 'price': [4, 0, 0],
                              'resource_food': {'grain_wood_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                'grain_food': 0},
                              'livestock_food': {'sheep_food': 2, 'boar_food': 3, 'cow_food': 4},
                              'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                        '3_random_point': 0}}

        self.improvement_5 = {'name': 'improvement_5', 'price': [5, 0, 0],
                              'resource_food': {'grain_wood_food': 3, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                'grain_food': 0},
                              'livestock_food': {'sheep_food': 2, 'boar_food': 3, 'cow_food': 4},
                              'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                        '3_random_point': 0}}

        self.improvement_7 = {'name': 'improvement_7', 'price': [3, 0, 1],
                              'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                'grain_food': 3},
                              'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                              'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 1,
                                        '3_random_point': 0}}

        self.improvement_9 = {'name': 'improvement_9', 'price': [0, 1, 2],
                              'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 3, 'wood_food': 0,
                                                'grain_food': 0},
                              'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                              'point': {'clay_point': 0, 'reed_point': 1, 'wood_point': 0, 'grain_point': 0,
                                        '3_random_point': 0}}

        self.improvement_10 = {'name': 'improvement_10', 'price': [1, 2, 0],
                               'resource_food': {'grain_wood_food': 0, 'clay_food': 2, 'reed_food': 0, 'wood_food': 0,
                                                 'grain_food': 0},
                               'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                               'point': {'clay_point': 1, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                         '3_random_point': 0}}

        self.improvement_11 = {'name': 'improvement_11', 'price': [2, 0, 1],
                               'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 2,
                                                 'grain_food': 0},
                               'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                               'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 1, 'grain_point': 0,
                                         '3_random_point': 0}}

        self.improvement_14 = {'name': 'improvement_14', 'price': [1, 1, 1],
                               'resource_food': {'grain_wood_food': 0, 'clay_food': 0, 'reed_food': 0, 'wood_food': 0,
                                                 'grain_food': 0},
                               'livestock_food': {'sheep_food': 0, 'boar_food': 0, 'cow_food': 0},
                               'point': {'clay_point': 0, 'reed_point': 0, 'wood_point': 0, 'grain_point': 0,
                                         '3_random_point': 1}}

        # init game state
        self.round = 1
        # self.moves = [self.action_a,self.action_b_1,self.action_b_2,self.action_c,self.action_d,self.action_e,self.action_f,self.action_g,self.action_h,self.action_i,self.action_j,self.action_k,self.action_l,self.action_m,self.action_n,self.action_o]
        # initial game resources
        self.board_resource = {'2_clay': 2, '1_clay': 1, 'reed': 1, '1_wood': 1, '2_wood': 2, '3_wood': 3, 'food': 1,
                              'sheep': 1, 'boar': 0, 'cow': 0, 'round': 1}
        self.reserve_resource = {'clay': 27, 'reed': 19, 'wood': 34, 'grain': 31, 'food': 71, 'sheep': 25, 'boar': 19,
                                'cow': 17, 'begging': 5}

        self.improvements = [self.improvement_2, self.improvement_3a, self.improvement_3, self.improvement_4a,
                             self.improvement_4, self.improvement_5]
        self.tiles = {'pasteur_2': 20, 'pasteur_4': 13, 'pasteur_6': 2, 'pasteur_8': 1, 'field': 20, 'stable': 10,
                      'room': 12}

        # initial player resources
        self.player1_state = {'point': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0,
                              'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player1_improvements = []
        self.player1_field_dict = {}

        self.player2_state = {'point': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player2_improvements = []
        self.player2_field_dict = {}

        self.player3_state = {'point': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player3_improvements = []
        self.player3_field_dict = {}

        self.player4_state = {'point': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player4_improvements = []
        self.player4_field_dict = {}

        self.player_state_list = [self.player1_state, self.player2_state, self.player3_state, self.player4_state]

        self.player_1_points = 0
        self.player_2_points = 0
        self.player_3_points = 0
        self.player_4_points = 0

        self.action_space_list = [self.action_a, self.action_b_1, self.action_b_2, self.action_b_3, self.action_b_4,
                                  self.action_b_a, self.action_c_1, self.action_c_2, self.action_c_3, self.action_c_4,
                                  self.action_d, self.action_e, self.action_f,
                                  self.action_g, self.action_h, self.action_i, self.action_j, self.action_k,
                                  self.action_l,
                                  self.action_m, self.action_n, self.action_o,
                                  self.action_1, self.action_2, self.action_2_b, self.action_3, self.action_4,
                                  self.action_4_b, self.action_5,
                                  self.action_6, self.action_7, self.action_8, self.action_9, self.action_10,
                                  self.action_11, self.action_12,
                                  self.action_13, self.action_13_b, self.action_14]
        
        self.action_space = self.generate_all_possible_actions(self.action_space_list, self.moves)

        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state, self.board_resource, self.reserve_resource, self.tiles)

        self.previous_parameter = 0

        self.done = False

        return self.obs, self.action_space

    # --------------------------------------------------------------------------------------------------------------------------------------------------#
    ### Moves
    
    def distribute_sum_livestocks(self, total_sum, num_variables):
        if num_variables <= 1:
            return [total_sum]

        # Generate random integers for each variable except the last one
        values = [random.randint(0, total_sum) for _ in range(num_variables - 1)]  # randomzzz

        # Sort the values in ascending order
        values.sort()

        # Calculate the differences between consecutive values to get the allocated amounts
        allocated_amounts = [values[0]] + [values[i] - values[i - 1] for i in range(1, num_variables - 1)] + [
            total_sum - values[-1]]

        return allocated_amounts

    def distribute_sum_stable(self, target_sum, num_variables):
        # Initialize an array of zeros
        allocated_amounts = [0] * num_variables

        # Check if target_sum is greater than num_variables
        if target_sum > num_variables:
            target_sum = num_variables

        # Randomly select 'target_sum' unique indices to set to 1
        random_indices = random.sample(range(num_variables), target_sum)  # randomzzz

        # Set the value at the randomly selected indices to 1
        for index in random_indices:
            allocated_amounts[index] = 1

        return allocated_amounts

    def assign_stables(self, player_state, player_expanded_pasteur_list):
        if len(player_expanded_pasteur_list) > 0:
            # Pick a random integer between 1 and 10 (inclusive)
            stables_tobe_assigned = random.randint(0, len(player_expanded_pasteur_list) - 1)  # randomzzz

            # Pick a pasteur to add stable to
            random_pasteur = random.sample(range(0, len(player_expanded_pasteur_list) - 1), stables_tobe_assigned)

            for x in random_pasteur:
                player_expanded_pasteur_list[x] = player_expanded_pasteur_list[x] * 2

            return player_expanded_pasteur_list
        else:
            return player_expanded_pasteur_list

    # def assign_livestock(self, player_state, acquired_sheeps, acquired_boars, acquired_cows):
    #     pasteur_arrays = np.array([[1], [1], [1], ])
    #
    #     player_pasteur_list = [player_state['pasteur_2'], player_state['pasteur_4'], player_state['pasteur_6'],
    #                            player_state['pasteur_8']]
    #
    #     player_expanded_pasteur_list = []
    #     for x in range(player_pasteur_list[0]):
    #         player_expanded_pasteur_list.append(2)
    #     for x in range(player_pasteur_list[1]):
    #         player_expanded_pasteur_list.append(4)
    #     for x in range(player_pasteur_list[2]):
    #         player_expanded_pasteur_list.append(6)
    #     for x in range(player_pasteur_list[3]):
    #         player_expanded_pasteur_list.append(8)
    #
    #     # Assign stables
    #     player_expanded_pasteur_list = self.assign_stables(player_state, player_expanded_pasteur_list)
    #
    #     player_pasteur_capacity_arrays = np.array(player_expanded_pasteur_list)
    #
    #     # Pasteurs that players have
    #     # [pasteur2_number, pasteur4_number, pasteur6_number, pasteur8_number]
    #
    #     # Show the available spaces that players have
    #     player_available_space_arrays = player_pasteur_capacity_arrays * pasteur_arrays
    #     print('Here is the available spaces')
    #     print(player_available_space_arrays)
    #     # print('-------------------------------------------------------------')
    #
    #     # -----------------------------------------------------------------------------------------------
    #     #   Player's livestocks count
    #     sheeps_tobe_assigned = acquired_sheeps + player_state['sheep']
    #     sheep_list = self.distribute_sum_livestocks(sheeps_tobe_assigned, len(player_expanded_pasteur_list))
    #
    #     boars_tobe_assigned = acquired_boars + player_state['boar']
    #     boar_list = self.distribute_sum_livestocks(boars_tobe_assigned, len(player_expanded_pasteur_list))
    #
    #     cows_tobe_assigned = acquired_cows + player_state['cow']
    #     cow_list = self.distribute_sum_livestocks(cows_tobe_assigned, len(player_expanded_pasteur_list))
    #
    #     x1 = 0
    #     for sheep in sheep_list:
    #         if sheep > 0:
    #             x1 = x1 + sheep
    #     # print(f'{x1} sheeps to be assigned')
    #
    #     x2 = 0
    #     for boar in boar_list:
    #         if boar > 0:
    #             x2 = x2 + boar
    #     # print(f'{x2} boars to be assigned')
    #
    #     x3 = 0
    #     for cow in cow_list:
    #         if cow > 0:
    #             x3 = x3 + cow
    #     # print(f'{x3} cows to be assigned')
    #
    #     # TODO: randomize livestock priority
    #     # Create a list of integers representing each while loop
    #     loop_order = ['sheeps', 'boars', 'cows']
    #
    #     # Shuffle the list to randomize the order
    #     random.shuffle(loop_order)
    #
    #     # Iterate through the shuffled list
    #     no_joined_array = np.full(len(player_pasteur_capacity_arrays), 0)
    #     for loop_num in loop_order:
    #         if loop_num == 'sheeps':
    #             while True:
    #                 player_livestock_arrays = np.array([
    #                     sheep_list,
    #                     sheep_list,
    #                     sheep_list,
    #                 ])
    #
    #                 original_array = player_available_space_arrays.copy()
    #
    #                 # Where the player choose to put their livestocks
    #                 player_available_space_arrays = player_available_space_arrays - player_livestock_arrays
    #
    #                 # Change all negative values of the arrays to 0
    #                 player_available_space_arrays[player_available_space_arrays < 0] = 0
    #
    #                 player_on_hand_sheeps_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
    #                 no_joined_array = player_on_hand_sheeps_array.copy()
    #                 no_joined_array[no_joined_array != 0] = -99
    #                 player_on_hand_sheeps_array[player_on_hand_sheeps_array < 0] = 0
    #
    #                 print('Here is the the sheeps on hand')
    #                 print(player_on_hand_sheeps_array)
    #
    #                 print('Here is the available spaces after adding the sheeps')
    #                 print(player_available_space_arrays)
    #
    #                 break
    #
    #         if loop_num == 'boars':
    #             while True:
    #                 player_livestock_arrays = np.array([
    #                     boar_list,
    #                     boar_list,
    #                     boar_list,
    #                 ])
    #
    #                 original_array = player_available_space_arrays.copy()
    #
    #                 # Where the player choose to put their livestocks
    #                 player_available_space_arrays = player_available_space_arrays - player_livestock_arrays
    #
    #                 # Change all negative values of the arrays to 0
    #                 player_available_space_arrays[player_available_space_arrays < 0] = 0
    #
    #                 player_on_hand_boars_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
    #                 no_joined_array = player_on_hand_boars_array.copy()
    #                 no_joined_array[no_joined_array != 0] = -99
    #                 player_on_hand_boars_array[player_on_hand_boars_array < 0] = 0
    #
    #                 print('Here is the the boars on hand')
    #                 print(player_on_hand_boars_array)
    #
    #                 print('Here is the available spaces after adding the boars')
    #                 print(player_available_space_arrays)
    #
    #                 break
    #
    #         if loop_num == 'cows':
    #             while True:
    #                 player_livestock_arrays = np.array([
    #                     cow_list,
    #                     cow_list,
    #                     cow_list,
    #                 ])
    #
    #                 original_array = player_available_space_arrays.copy()
    #
    #                 # Where the player choose to put their livestocks
    #                 player_available_space_arrays = player_available_space_arrays - player_livestock_arrays
    #
    #                 # Change all negative values of the arrays to 0
    #                 player_available_space_arrays[player_available_space_arrays < 0] = 0
    #
    #                 player_on_hand_cows_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
    #                 no_joined_array = player_on_hand_cows_array.copy()
    #                 no_joined_array[no_joined_array != 0] = -99
    #                 player_on_hand_cows_array[player_on_hand_cows_array < 0] = 0
    #
    #                 print('Here is the the cows on hand')
    #                 print(player_on_hand_cows_array)
    #
    #                 print('Here is the available spaces after adding the cows')
    #                 print(player_available_space_arrays)
    #
    #                 break
    #
    #     player_on_hand_livestock_arrays = np.array([
    #         player_on_hand_sheeps_array,
    #         player_on_hand_boars_array,
    #         player_on_hand_cows_array,
    #     ])
    #
    #     discarded_sheeps = sheeps_tobe_assigned - sum(player_on_hand_sheeps_array)
    #     discarded_boars = boars_tobe_assigned - sum(player_on_hand_boars_array)
    #     discarded_cows = cows_tobe_assigned - sum(player_on_hand_cows_array)
    #     print(f'{discarded_sheeps} sheeps discarded')
    #     print(f'{discarded_boars} boars discarded')
    #     print(f'{discarded_cows} cows discarded')
    #
    #     # update inventory with new livestocks arrangement
    #     player_state['sheep'] = sum(player_on_hand_sheeps_array)
    #     player_state['boar'] = sum(player_on_hand_boars_array)
    #     player_state['cow'] = sum(player_on_hand_cows_array)
    #
    #     print('Here is all the livestocks on hand')
    #     print(player_on_hand_livestock_arrays)

    def assign_livestock(self, player_state, acquired_sheeps, acquired_boars, acquired_cows):
        total_slot = player_state['pasteur_2']*2 + player_state['pasteur_4']*4 + player_state['pasteur_6']*6 + player_state['pasteur_8']*8
        current_livestock = player_state['sheep'] + player_state['boar'] + player_state['cow']

        available_slot = total_slot - current_livestock
        
        if acquired_sheeps > 0:
            # Add acquired animals to player's inventory
            player_state['sheep'] += min(available_slot, acquired_sheeps)
            
            if available_slot >= acquired_sheeps:
                return
            else:
                # Return animals to reserved resource
                self.reserve_resource['sheep'] += acquired_sheeps - available_slot

        if acquired_boars > 0:
            # Add acquired animals to player's inventory
            player_state['boar'] += min(available_slot, acquired_boars)

            if available_slot >= acquired_boars:
                return
            else:
                # Return animals to reserved resource
                self.reserve_resource['boar'] += acquired_boars - available_slot

        if acquired_cows > 0:
            # Add acquired animals to player's inventory
            player_state['cow'] += min(available_slot, acquired_cows)

            if available_slot >= acquired_cows:
                return
            else:
                # Return animals to reserved resource
                self.reserve_resource['cow'] += acquired_cows - available_slot
            

    def remove_actions(self, actions_to_remove):
        self.moves = [action for action in self.moves if action.__name__ not in actions_to_remove]

    def action_a(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_a'])

        # Check resource availability
        if self.reserve_resource['wood'] > 0:
            # Player gain
            player_state['wood'] = player_state['wood'] + 1
            # Deduct from global resources
            self.reserve_resource['wood'] = self.reserve_resource['wood'] - 1
        else:
            print('out of woods')

        if self.reserve_resource['clay'] > 0:
            # Player gain
            player_state['clay'] = player_state['clay'] + 1
            # Deduct from global resources
            self.reserve_resource['clay'] = self.reserve_resource['clay'] - 1
        else:
            print('out of clays')

        if self.reserve_resource['reed'] > 0:
            # Player gain
            player_state['reed'] = player_state['reed'] + 1
            # Deduct from global resources
            self.reserve_resource['reed'] = self.reserve_resource['reed'] - 1
        else:
            print('out of reeds')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_a']

    #TODO: asssumption, action b, always take a stable if have enough resources, only by 1 tile of any types

    def action_b_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        print(f'The player chose pasteur_2')

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][1] and \
                    player_state['wood'] >= self.pasteur_2["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_2["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_2["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_2["price"][2]
                # Player gain
                player_state['pasteur_2'] = player_state['pasteur_2'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out stables')

    def action_b_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        print(f'The player chose pasteur_4')

        # Check resource availability
        if self.tiles['pasteur_4'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= self.pasteur_4["price"][1] and \
                    player_state['wood'] >= self.pasteur_4["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_4["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_4["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_4["price"][2]
                # Player gain
                player_state['pasteur_4'] = player_state['pasteur_4'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')


        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out stables')

    def action_b_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        print(f'The player chose pasteur_6')

        # Check resource availability
        if self.tiles['pasteur_6'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= self.pasteur_6["price"][1] and \
                    player_state['wood'] >= self.pasteur_6["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_6["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_6["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_6["price"][2]
                # Player gain
                player_state['pasteur_6'] = player_state['pasteur_6'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')


        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out stables')

    def action_b_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        print(f'The player chose pasteur_8')

        # Check resource availability
        if self.tiles['pasteur_8'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= self.pasteur_8["price"][1] and \
                    player_state['wood'] >= self.pasteur_8["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_8["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_8["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_8["price"][2]
                # Player gain
                player_state['pasteur_8'] = player_state['pasteur_8'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out stables')

    def action_b_a(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')


    # TODO: asssumption, action c, only by 1 tile of any types
    def action_c_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        print(f'The player chose pasteur_2')

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][1] and \
                    player_state['wood'] >= self.pasteur_2["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_2["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_2["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_2["price"][2]
                # Player gain
                player_state['pasteur_2'] = player_state['pasteur_2'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

    def action_c_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        print(f'The player chose pasteur_4')

        # Check resource availability
        if self.tiles['pasteur_4'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= self.pasteur_4["price"][1] and \
                    player_state['wood'] >= self.pasteur_4["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_4["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_4["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_4["price"][2]
                # Player gain
                player_state['pasteur_4'] = player_state['pasteur_4'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

    def action_c_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        print(f'The player chose pasteur_6')

        # Check resource availability
        if self.tiles['pasteur_6'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= self.pasteur_6["price"][1] and \
                    player_state['wood'] >= self.pasteur_6["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_6["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_6["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_6["price"][2]
                # Player gain
                player_state['pasteur_6'] = player_state['pasteur_6'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

    def action_c_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        print(f'The player chose pasteur_8')

        # Check resource availability
        if self.tiles['pasteur_8'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= self.pasteur_8["price"][1] and \
                    player_state['wood'] >= self.pasteur_8["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_8["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_8["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_8["price"][2]
                # Player gain
                player_state['pasteur_8'] = player_state['pasteur_8'] + 1

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

            else:
                print('you cannot afford it')

        else:
            print('out of tiles')

    def action_d(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_d'])

        # Check resource availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            print('out of fields')

    def action_e(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_e'])

        # Player gain
        player_state['clay'] = player_state['clay'] + self.board_resource['2_clay']
        # Deduct from global resources
        self.board_resource['2_clay'] = 0

    def action_f(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_f'])

        # Player gain
        player_state['clay'] = player_state['clay'] + self.board_resource['1_clay']
        # Deduct from global resources
        self.board_resource['1_clay'] = 0

    def action_g(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_g'])

        if player_state['grain'] < 1:
            print('Not enough grains')
            return

        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        y = 0
        for x in range(min(grains, len(player_field_dict))):
            if len(player_field_dict) > 0:
                # take 1 grain from player's inventory
                player_state['grain'] = player_state['grain'] - 1
                # check if there is enough grains in global inventory
                if self.reserve_resource['grain'] >= 2:
                    # sow grains on field
                    player_field_dict[f'field_{y + 1}'] = player_field_dict[f'field_{y + 1}'] + 3
                    # take grain from global inventory
                    self.reserve_resource['grain'] = self.reserve_resource['grain'] - 2
                    y = y + 1

                else:
                    # sow grains on field
                    player_field_dict[f'field_{y + 1}'] = player_field_dict[f'field_{y + 1}'] + 3
                    # take grain from global inventory
                    self.reserve_resource['grain'] = 0
                    y = y + 1
            else:
                print('plow a field first')
                break

    def action_h(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_h'])

        # Check resource availability
        if self.reserve_resource['grain'] > 0:
            # Player gain
            player_state['grain'] = player_state['grain'] + 1
            # Deduct from global resources
            self.reserve_resource['grain'] = self.reserve_resource['grain'] - 1
        else:
            print('out of grains')

    def action_i(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_i'])

        # Player gain
        player_state['reed'] = player_state['reed'] + self.board_resource['reed']
        # Deduct from global resources
        self.board_resource['reed'] = 0

    def action_j(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_j'])

        # Player gain
        player_state['wood'] = player_state['wood'] + self.board_resource['1_wood']
        # Deduct from global resources
        self.board_resource['1_wood'] = 0

    def action_k(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_k'])

        acquired_sheeps = self.board_resource['sheep']
        acquired_boars = 0
        acquired_cows = 0

        # Assign livestocks
        self.assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows)

        # Player gain
        player_state['sheep'] = player_state['sheep'] + acquired_sheeps

        # Deduct from global resources
        self.board_resource['sheep'] = 0

    def action_l(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_l'])

        # Player gain
        player_state['wood'] = player_state['wood'] + self.board_resource['2_wood']
        # Deduct from global resources
        self.board_resource['2_wood'] = 0

    def action_m(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_m'])

        # Player gain
        player_state['wood'] = player_state['wood'] + self.board_resource['3_wood']
        # Deduct from global resources
        self.board_resource['3_wood'] = 0

    def action_n(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_n'])

        # Player gain
        player_state['food'] = player_state['food'] + self.board_resource['food']
        # Deduct from global resources
        self.board_resource['food'] = 0

    def action_o(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_o'])

        # Check resource availability
        if self.reserve_resource['food'] > 0:
            # Player gain
            player_state['food'] = player_state['food'] + 1
            # Deduct from global resources
            self.reserve_resource['food'] = self.reserve_resource['food'] - 1
        else:
            print('out of foods')

        # Take rooster from all players
        for player in self.player_state_list:
            player['rooster'] = 0

        # Give rooster to new player
        player_state['rooster'] = 1

    def action_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_1'])

        try:
            chosen_improvement = self.improvements[random.randint(0, len(self.improvements) - 1)]
            print(f"The player chose {chosen_improvement}")

            if chosen_improvement in self.improvements:
                # Check player's payment
                if player_state['clay'] >= chosen_improvement["price"][0] and player_state['reed'] >= \
                        chosen_improvement["price"][1] and player_state['wood'] >= chosen_improvement["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - chosen_improvement["price"][0]
                    player_state['reed'] = player_state['reed'] - chosen_improvement["price"][1]
                    player_state['wood'] = player_state['wood'] - chosen_improvement["price"][2]

                    # Add to reserved resources
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + chosen_improvement["price"][0]
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + chosen_improvement["price"][1]
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + chosen_improvement["price"][2]

                    # Deduct from global resources
                    element_to_remove = chosen_improvement
                    self.improvements = [x for x in self.improvements if x != element_to_remove]

                    # Player gain
                    player_improvements.append(chosen_improvement)

        except:
            print('out of improvements')

    def action_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_2', 'action_2_b'])

        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 0:

            # Check resource availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 2 and player_state['wood'] >= 5:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 2
                    player_state['wood'] = player_state['wood'] - 5
                    # Player gain
                    player_state['wood_room'] = player_state['wood_room'] + 1

                    # Add to reserved resources
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + 2
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + 5

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1

                else:
                    print('you cannot afford it')

            else:
                print('out of rooms')

        else:
            print('player has already coverted to clay, cannot take this action')

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')

    def action_2_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_2', 'action_2_b'])

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')


    def action_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_3'])

        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 0:
            # Check resource availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 1 and player_state['clay'] >= 3:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 1
                    player_state['clay'] = player_state['clay'] - 3
                    # Player gain
                    player_state['clay_conversion'] = 1

                    # Add to reserved resources
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + 1
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + 3

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1
                else:
                    print('you cannot afford it')
            else:
                print('out of rooms')
        else:
            print('player has already coverted to clay, cannot take this action')

        if self.tiles['stable'] > 0:
            # Player gain
            player_state['stable'] = player_state['stable'] + 1
            # Deduct from global resources
            self.tiles['stable'] = self.tiles['stable'] - 1
        else:
            print('out of stables')

    def action_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_4', 'action_4_b'])

        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 1:
            # Check resource availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 1 and player_state['clay'] >= 3:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 1
                    player_state['clay'] = player_state['clay'] - 3
                    # Player gain
                    player_state['clay_room'] = player_state['clay_room'] + 1

                    # Add to reserved resources
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + 1
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + 3

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1

                else:
                    print('you cannot afford it')

            else:
                print('out of rooms')
        else:
            print('convert to clay first before take this action')

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')

    def action_4_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_4', 'action_4_b'])

        # Check resource availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')

    def action_5(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_5'])

        if player_state['farmer'] < 5:
            if player_state['room_space'] > player_state['farmer']:
                player_state['farmer'] = player_state['farmer'] + 1
            else:
                print('not enough rooms')
        else:
            print('no more farmers')

    def action_6(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_6'])

        acquired_sheeps = 0
        acquired_boars = self.board_resource['boar']
        acquired_cows = 0
        # Assign livestocks
        self.assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows)

        # Player gain
        player_state['boar'] = player_state['boar'] + acquired_boars

        # Deduct from global resources
        self.board_resource['boar'] = 0

    def action_7(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_7'])

        if self.improvement_7 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_7["price"][0] and player_state['reed'] >= \
                    self.improvement_7["price"][1] and player_state['wood'] >= self.improvement_7["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_7["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_7["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_7["price"][2]

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.improvement_7["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.improvement_7["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.improvement_7["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_7
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_7)

            else:
                print('you cannot afford it')

        else:
            print(f'improvement_7 is not available')

    def action_8(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_8'])

        acquired_sheeps = 0
        acquired_boars = 0
        acquired_cows = self.board_resource['cow']
        # Assign livestocks
        self.assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows)

        # Player gain
        player_state['cow'] = player_state['cow'] + acquired_cows

        # Deduct from global resources
        self.board_resource['cow'] = 0

    def action_9(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_9'])

        if self.improvement_9 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_9["price"][0] and player_state['reed'] >= \
                    self.improvement_9["price"][1] and player_state['wood'] >= self.improvement_9["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_9["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_9["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_9["price"][2]

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.improvement_9["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.improvement_9["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.improvement_9["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_9
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(improvement_9)

            else:
                print('you cannot afford it')

        else:
            print(f'improvement_9 is not available')

    def action_10(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_10'])

        if self.improvement_10 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_10["price"][0] and player_state['reed'] >= \
                    self.improvement_10["price"][1] and player_state['wood'] >= self.improvement_10["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_10["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_10["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_10["price"][2]

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.improvement_10["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.improvement_10["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.improvement_10["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_10
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_10)

            else:
                print('you cannot afford it')

        else:
            print(f'improvement_10 is not available')

    def action_11(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_11'])

        if self.improvement_11 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_11["price"][0] and player_state['reed'] >= \
                    self.improvement_11["price"][1] and player_state['wood'] >= self.improvement_11["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_11["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_11["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_11["price"][2]

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.improvement_11["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.improvement_11["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.improvement_11["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_11
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_11)

            else:
                print('you cannot afford it')

        else:
            print(f'improvement_11 is not available')

    def action_12(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_12'])

        if player_state['farmer'] < 5:
            player_state['farmer'] = player_state['farmer'] + 1
        else:
            print('no more farmers')

    def action_13(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_13', 'action_13_b'])

        # Check resource availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0


        else:
            print('out of fields')

        if player_state['grain'] < 1:
            print('Not enough grains')
            return

        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        y = 0
        for x in range(min(grains, len(player_field_dict))):
            if len(player_field_dict) > 0:
                # take 1 grain from player's inventory
                player_state['grain'] = player_state['grain'] - 1
                # check if there is enough grains in global inventory
                if self.reserve_resource['grain'] >= 2:
                    # sow grains on field
                    player_field_dict[f'field_{y + 1}'] = player_field_dict[f'field_{y + 1}'] + 3
                    # take grain from global inventory
                    self.reserve_resource['grain'] = self.reserve_resource['grain'] - 2
                    y = y + 1

                else:
                    # sow grains on field
                    player_field_dict[f'field_{y + 1}'] = player_field_dict[f'field_{y + 1}'] + 3
                    # take grain from global inventory
                    self.reserve_resource['grain'] = 0
                    y = y + 1
            else:
                print('plow a field first')
                break

    def action_13_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_13', 'action_13_b'])

        if player_state['grain'] < 1:
            print('Not enough grains')
            return

        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        if grains <= player_state['grain']:
            y = 0
            for x in range(min(grains, len(player_field_dict))):
                if len(player_field_dict) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resource['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                               f'{player_field_dict[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resource['grain'] = self.reserve_resource['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                           f'{player_field_dict[y]}'] + 1 + \
                                                                       self.reserve_resource['grain']
                        # take grain from global inventory
                        self.reserve_resource['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        else:
            y = 0
            for x in range(min(player_state['grain'], len(player_field_dict))):
                if len(player_field_dict) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resource['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                               f'{player_field_dict[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resource['grain'] = self.reserve_resource['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                           f'{player_field_dict[y]}'] + 1 + \
                                                                       self.reserve_resource['grain']
                        # take grain from global inventory
                        self.reserve_resource['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

    def action_14(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_14'])

        if self.improvement_14 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_14["price"][0] and player_state['reed'] >= \
                    self.improvement_14["price"][1] and player_state['wood'] >= self.improvement_14["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_14["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_14["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_14["price"][2]

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.improvement_14["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.improvement_14["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.improvement_14["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_14
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_14)

            else:
                print('you cannot afford it')

        else:
            print(f'improvement_14 is not available')

    def find_livestock_feeding_options(self, player_state, player_missing_foods, improvement):
        sheep = player_state['sheep']
        boar = player_state['boar']
        cow = player_state['cow']

        sheep_to_food = improvement['livestock_food']['sheep_food']
        boar_to_food = improvement['livestock_food']['boar_food']
        cow_to_food = improvement['livestock_food']['cow_food']

        valid_combinations = []

        # Define reasonable upper bounds for x, y, z. Assuming up to 100 for each for demonstration.
        # You might want to adjust these bounds based on the actual values and needs.
        for x in range(sheep + 1):
            for y in range(boar + 1):
                # Calculate minimum z needed after choosing x and y
                needed_from_cows = max(0, player_missing_foods - x * sheep_to_food - y * boar_to_food)
                min_z = (
                                needed_from_cows + cow_to_food - 1) // cow_to_food  # Ceiling division to ensure inequality holds

                for z in range(min_z, cow + 1):
                    if x * sheep_to_food + y * boar_to_food + z * cow_to_food >= player_missing_foods:
                        valid_combinations.append([x, y, z])
                    else:
                        break  # No point in checking higher values of z if this one doesn't satisfy


        if len(valid_combinations) > 0:
            return random.choice(valid_combinations)
        else:
            return [0,0,0]

    def find_positive_resource_food(self, improvements):
        positive_improvements = []
        for improvement in improvements:
            # Check each key in the 'resource_food' dictionary
            for key, value in improvement['resource_food'].items():
                if value > 0:
                    positive_improvements.append(improvement['name'])
                    break  # Exit the inner loop if a positive value is found
        return positive_improvements

    def find_positive_livestock_food(self, improvements):
        positive_improvements = []
        for improvement in improvements:
            # Check each key in the 'livestock_food' dictionary
            for key, value in improvement['livestock_food'].items():
                if value > 0:
                    positive_improvements.append(improvement['name'])
                    break  # Exit the inner loop if a positive value is found
        return positive_improvements

    def use_improvement_to_feed(self, player_state, player_missing_foods, player_improvements):
        # TODO: assumption, only use 1 improvement
        # randomly pick an improvement
        if len(player_improvements) < 1:
            return player_missing_foods

        usable_improvements = self.find_positive_resource_food(player_improvements)

        x = random.choice(usable_improvements)

        improvement = getattr(AgricolaAI(), x)

        acquired_food = 0

        if improvement['resource_food']['grain_wood_food'] > 0:
            x = min([player_state['grain'], player_state['wood']])

            y = 0
            for i in range(1, x + 1):
                acquired_food = i * improvement['resource_food']['grain_wood_food']
                if acquired_food + player_missing_foods >= 0:
                    y = i
                    break
                y = i

            # Take the used resources from player's inventory
            player_state['grain'] = player_state['grain'] - y
            player_state['wood'] = player_state['wood'] - y

        if improvement['resource_food']['clay_food'] > 0:
            y = 0
            for i in range(1, player_state['clay'] + 1):
                acquired_food = i * improvement['resource_food']['clay_food']
                if acquired_food + player_missing_foods >= 0:
                    y = i
                    break
                y = i
            player_state['clay'] = player_state['clay'] - y

        if improvement['resource_food']['reed_food'] > 0:
            y = 0
            for i in range(1, player_state['reed'] + 1):
                acquired_food = i * improvement['resource_food']['reed_food']
                if acquired_food + player_missing_foods >= 0:
                    y = i
                    break
                y = i
            player_state['reed'] = player_state['reed'] - y

        if improvement['resource_food']['wood_food'] > 0:
            y = 0
            for i in range(1, player_state['wood'] + 1):
                acquired_food = i * improvement['resource_food']['wood_food']
                if acquired_food + player_missing_foods >= 0:
                    y = i
                    break
                y = i
            player_state['wood'] = player_state['wood'] - y

        if improvement['resource_food']['grain_food'] > 0:
            y = 0
            for i in range(1, player_state['grain'] + 1):
                acquired_food = i * improvement['resource_food']['grain_food']
                if acquired_food + player_missing_foods >= 0:
                    y = i
                    break
                y = i
            player_state['grain'] = player_state['grain'] - y

        player_missing_foods = acquired_food + player_missing_foods

        return player_missing_foods

    def use_grain_to_feed(self, player_state, player_missing_foods):
        if player_state['grain'] < 1:
            print('Not enough grains')
            return player_missing_foods

        if player_state['grain'] + player_missing_foods == 0:
            print(f"{player_state['grain']} grain was used to feed")
            player_state['grain'] = 0
            player_missing_foods = 0

        if player_state['grain'] + player_missing_foods > 0:
            print(f'{player_missing_foods} grain was used to feed')
            player_state['grain'] = player_state['grain'] + player_missing_foods
            player_missing_foods = 0
        if player_state['grain'] + player_missing_foods < 0:
            print(f"{player_state['grain']} grain was used to feed")
            player_state['grain'] = 0
            player_missing_foods = player_state['grain'] + player_missing_foods

        return player_missing_foods

    def use_livestock_to_feed(self, player_state, player_missing_foods, player_improvements):
        # TODO: assumption, priortize the use of livestock for food in this order: cow, boar, sheep
        # TODO: assumption, priortize the use of improvements for food in this order:
        if len(player_improvements) < 1:
            return player_missing_foods

        usable_improvements = self.find_positive_livestock_food(player_improvements)

        if len(usable_improvements) < 1:
            print('No appropriate improvement found!')
            return player_missing_foods

        x = random.choice(usable_improvements)

        improvement = getattr(AgricolaAI(), x)

        # Find all the possible feeding combination and randomly pick 1
        feeding_option = self.find_livestock_feeding_options(player_state, player_missing_foods, improvement)

        # Acquired foods
        acquired_food = feeding_option[0] * improvement['livestock_food']['sheep_food'] + feeding_option[1] * \
                        improvement['livestock_food']['boar_food'] + feeding_option[2] * improvement['livestock_food'][
                            'cow_food']

        print(
            f'{improvement} was used on {feeding_option[0]} sheeps, {feeding_option[1]} boars, and {feeding_option[2]} cows to exchanged for {acquired_food} foods')

        # Update livestocks
        player_state['sheep'] = player_state['sheep'] - feeding_option[0]
        player_state['boar'] = player_state['boar'] - feeding_option[1]
        player_state['cow'] = player_state['cow'] - feeding_option[2]

        player_missing_foods = acquired_food + player_missing_foods

        return player_missing_foods

    def harvesting(self, player_state, player_field_dict, player_improvements):
        ##  Do grains
        #   Take grains off the fields
        player_taken_grains = 0
        for key in player_field_dict:
            if player_field_dict[key] > 0:
                player_field_dict[key] -= 1
                player_taken_grains += 1

        #   Add taken grains to players' inventory
        player_state['grain'] += player_taken_grains

        ##  Feeding
        #   Feed the farmers using foods
        player_required_foods = player_state['farmer'] * 2
        player_missing_foods = player_state['food'] - player_required_foods
        # TODO: Assumption, always feed with foods first
        # TODO: Assumption, getting begging tokens is the last option
        if player_missing_foods == 0:
            player_state['food'] = 0
        if player_missing_foods > 0:
            player_state['food'] = player_missing_foods

        # Not enough foods, players have to use either grains or livestocks to feed
        if player_missing_foods < 0:
            player_state['food'] = 0
            #   Feed the farmers using improvements
            player_missing_foods = self.use_improvement_to_feed(player_state, player_missing_foods, player_improvements)

            if player_missing_foods == 0:
                print('Done feeding!')

            if player_missing_foods > 0:
                player_state['food'] = player_missing_foods
                print('Done feeding!')

            if player_missing_foods < 0:
                #   Feed the farmers using livestock
                player_missing_foods = self.use_livestock_to_feed(player_state, player_missing_foods,
                                                                  player_improvements)

                if player_missing_foods == 0:
                    print('Done feeding!')

                if player_missing_foods > 0:
                    player_state['food'] = player_missing_foods
                    print('Done feeding!')

                if player_missing_foods < 0:
                    #   Feed the farmers using grains
                    player_missing_foods = self.use_grain_to_feed(player_state, player_missing_foods)

                    if player_missing_foods == 0:
                        print('Done feeding!')

                    if player_missing_foods > 0:
                        player_state['food'] = player_missing_foods
                        print('Done feeding!')

                    if player_missing_foods < 0:
                        #   Still not enough foods, get begging tokens
                        player_state['begging'] += (-1) * player_missing_foods

        ## Offsprings
        # Assigning offsprings
        sheep_offspring = player_state['sheep'] // 2
        boar_offspring = player_state['boar'] // 2
        cow_offspring = player_state['cow'] // 2

        player_state['sheep'] = player_state['sheep'] + sheep_offspring
        player_state['boar'] = player_state['boar'] + boar_offspring
        player_state['cow'] = player_state['cow'] + cow_offspring

        # Re-assign livestocks
        # Assign livestocks
        self.assign_livestock(player_state, sheep_offspring, boar_offspring, cow_offspring)

        return

    def point_cal(self, player_state):
        # TODO: assumption, counts all livestocks and grains, no need to be in pastuers or on fields.
        player_points = player_state['farmer'] * 3 - player_state['begging'] * 3 + \
                        player_state['clay_conversion'] + player_state['clay_room'] + player_state['pasteur_2'] + \
                        player_state['pasteur_4'] + player_state['pasteur_6'] + player_state['pasteur_8'] + \
                        player_state['stable'] + player_state['field'] + \
                        player_state['sheep'] + player_state['boar'] + player_state['cow'] + player_state['grain']

        return player_points

    def generate_all_possible_actions(self, action_space_list, moves):
        action_space_index = []
        for action in action_space_list:
            if action in moves:
                action_space_index.append(1)
            else:
                action_space_index.append(0)

        # Step 1: Identify all indices with value 1
        valid_indices = [index for index, value in enumerate(action_space_index) if value == 1]

        # Step 2: Create a new list for each valid index with only that index set to 1
        all_possible_actions = []
        for index in valid_indices:
            new_action_space_index = [0] * len(action_space_index)
            new_action_space_index[index] = 1
            all_possible_actions.append(new_action_space_index)

        return all_possible_actions

    # def generate_all_possible_actions(self, action_space_list, moves):
    #     action_space_index = []
    #     for action in action_space_list:
    #         if action in moves:
    #             action_space_index.append(1)
    #         else:
    #             action_space_index.append(0)
    #
    #     # Step 1: Identify all indices with value 1
    #     valid_indices = [index for index, value in enumerate(action_space_index) if value == 1]
    #
    #     # Step 2: Create a new list for each valid index with only that index set to 1
    #     all_possible_actions = []
    #     for index in valid_indices:
    #         new_action_space_index = [0] * len(action_space_index)
    #         new_action_space_index[index] = 1
    #         all_possible_actions.append(new_action_space_index)

        return all_possible_actions
    
    def generate_obs(self, player1_state, player2_state, player3_state, player4_state, board_resource, reserve_resource, tiles):
        observation = []
        observation.extend(player1_state.values())
        observation.extend(player2_state.values())
        observation.extend(player3_state.values())
        observation.extend(player4_state.values())
        observation.extend(board_resource.values())
        observation.extend(reserve_resource.values())
        observation.extend(tiles.values())
        obs = np.array(observation, dtype=np.float32)
        return obs

    def check_negative_resource(self, data):
        ignore_indices = [0, 24, 48, 72]  # Indices to be ignored
        for i, value in enumerate(data):
            if i not in ignore_indices and value < 0:
                print(f"Breaking at index {i}, value: {value}")
                sys.exit("Terminating script due to negative value")  # Break the function

    def calculate_reward(self, parameter):

        # Example reward logic
        reward = (self.player1_state[parameter] - self.previous_parameter) * 5
        self.previous_parameter = self.player1_state[parameter]

        return reward

    ### Gameplay
    def step(self, round):

        # Reset actions list for new round
        self.moves = [self.action_a, self.action_b_1, self.action_b_2, self.action_b_3, self.action_b_4,
                      self.action_b_a, self.action_c_1, self.action_c_2, self.action_c_3, self.action_c_4,
                      self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o]

        if round >= 1:
            self.moves.append(self.action_1)
        if round >= 2:
            self.moves.append(self.action_2)
            self.moves.append(self.action_2_b)
        if round >= 3:
            self.moves.append(self.action_3)
        if round >= 4:
            self.moves.append(self.action_4)
            self.moves.append(self.action_4_b)
        if round >= 5:
            self.moves.append(self.action_5)
        if round >= 6:
            self.moves.append(self.action_6)
        if round >= 7:
            self.moves.append(self.action_7)
        if round >= 8:
            self.moves.append(self.action_8)
        if round >= 9:
            self.moves.append(self.action_9)
        if round >= 10:
            self.moves.append(self.action_10)
        if round >= 11:
            self.moves.append(self.action_11)
        if round >= 12:
            self.moves.append(self.action_12)
        if round >= 13:
            self.moves.append(self.action_13)
            self.moves.append(self.action_13_b)
        if round >= 14:
            self.moves.append(self.action_14)


        self.player1_number_actions = self.player1_state['farmer']
        self.player2_number_actions = self.player2_state['farmer']
        self.player3_number_actions = self.player3_state['farmer']
        self.player4_number_actions = self.player4_state['farmer']
        self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

        # Assign order in which player take actions based on rooster assignment
        # print(self.player1_state['rooster'])
        # print(self.player2_state['rooster'])
        # print(self.player3_state['rooster'])
        # print(self.player4_state['rooster'])

        self.order_list = [1, 2, 3, 4]

        if self.player1_state['rooster'] == 1:
            self.order_list[0] = 1
        if self.player2_state['rooster'] == 1:
            self.order_list[0] = 2
        if self.player3_state['rooster'] == 1:
            self.order_list[0] = 3
        if self.player4_state['rooster'] == 1:
            self.order_list[0] = 4

        if self.order_list[0] == 4:
            self.order_list[1] = 1
        else:
            self.order_list[1] = self.order_list[0] + 1

        if self.order_list[1] == 4:
            self.order_list[2] = 1
        else:
            self.order_list[2] = self.order_list[1] + 1

        if self.order_list[2] == 4:
            self.order_list[3] = 1
        else:
            self.order_list[3] = self.order_list[2] + 1

        # self.order_list = [1, 2, 3, 4]
        # random.shuffle(self.order_list)

        self.player_order = [f'player{self.order_list[0]}', f'player{self.order_list[1]}',
                             f'player{self.order_list[2]}', f'player{self.order_list[3]}']
        # print(self.player_order)


        # Players take actions
        while self.remain_actions > 0:
            for order in self.player_order:
                # Player 1 take action
                print('Actions:')
                print(self.moves)

                if order == 'player1':
                    if self.player1_number_actions != 0:
                        self.player1_action = self.moves[random.randint(0, len(self.moves) - 1)]  # randomzzz
                        print(f"player 1 take action {self.player1_action}")
                        self.player1_action(self.player1_state, self.player1_field_dict, self.player1_improvements)
                        print(len(self.moves))
                        self.player1_number_actions -= 1

                # Player 2 take action
                if order == 'player2':
                    if self.player2_number_actions != 0:
                        self.player2_action = self.moves[random.randint(0, len(self.moves) - 1)]  # randomzzz
                        print(f"player 2 take action {self.player2_action}")
                        self.player2_action(self.player2_state, self.player2_field_dict, self.player2_improvements)
                        print(len(self.moves))
                        self.player2_number_actions -= 1

                # Player 3 take action
                if order == 'player3':
                    if self.player3_number_actions != 0:
                        self.player3_action = self.moves[random.randint(0, len(self.moves) - 1)]  # randomzzz
                        print(f"player 3 take action {self.player3_action}")
                        self.player3_action(self.player3_state, self.player3_field_dict, self.player3_improvements)
                        print(len(self.moves))
                        self.player3_number_actions -= 1

                # Player 4 take action
                if order == 'player4':
                    if self.player4_number_actions != 0:
                        self.player4_action = self.moves[random.randint(0, len(self.moves) - 1)]  # randomzzz
                        print(f"player 4 take action {self.player4_action}")
                        self.player4_action(self.player4_state, self.player4_field_dict, self.player4_improvements)
                        print(len(self.moves))
                        self.player4_number_actions -= 1

            self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

        # Harvesting:
        print('------------------------------------------------------')
        print('player 1 - harvesting')
        self.harvesting(self.player1_state, self.player1_field_dict, self.player1_improvements)
        print('------------------------------------------------------')
        print('player 2 - harvesting')
        self.harvesting(self.player2_state, self.player2_field_dict, self.player2_improvements)
        print('------------------------------------------------------')
        print('player 3 - harvesting')
        self.harvesting(self.player3_state, self.player3_field_dict, self.player3_improvements)
        print('------------------------------------------------------')
        print('player 4 - harvesting')
        self.harvesting(self.player4_state, self.player4_field_dict, self.player4_improvements)

        # Refill board resources after each round
        self.board_resource['2_clay'] = self.board_resource['2_clay'] + 2
        self.board_resource['1_clay'] = self.board_resource['1_clay'] + 1
        self.board_resource['reed'] = self.board_resource['reed'] + 1
        self.board_resource['1_wood'] = self.board_resource['1_wood'] + 1
        self.board_resource['2_wood'] = self.board_resource['2_wood'] + 2
        self.board_resource['3_wood'] = self.board_resource['3_wood'] + 3
        self.board_resource['food'] = self.board_resource['food'] + 1
        self.board_resource['sheep'] = self.board_resource['sheep'] + 1
        if self.round >= 6:
            self.board_resource['boar'] = self.board_resource['boar'] + 1
        if self.round >= 8:
            self.board_resource['cow'] = self.board_resource['cow'] + 1

        # Calculate points
        # logger.info('------------------------------------------------------')
        # logger.info('Here are final points:')
        # for i in range(1, 5):
        #     points = self.point_cal(getattr(self, f'player{i}_state'))
        #     setattr(self, f'player_{i}_points', points)
        #     logger.info(f'Player {i} got {points} points')

        self.player1_state['point'] = self.point_cal(self.player1_state)
        self.player2_state['point'] = self.point_cal(self.player2_state)
        self.player3_state['point'] = self.point_cal(self.player3_state)
        self.player4_state['point'] = self.point_cal(self.player4_state)

        self.action_space = self.generate_all_possible_actions(self.action_space_list, self.moves)

        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state,
                                     self.board_resource, self.reserve_resource, self.tiles)


        # Check if any resource values are negative
        self.check_negative_resource(self.obs)

        reward = self.calculate_reward('stable')

        # Check if the game is done
        if self.round > 14:
            self.done = True

        return self.obs, reward, self.done, self.action_space


# TODO: randomimze number of pasteur to take for action c, right now the players only take 1 pasteur
# TODO: harvesting: feeding/begging, field work, offsprings/assigning or converting offsprings to foods.
# TODO: offspring after each harvest and players have to assign livestocks right away
# TODO: when take/offspring livestock and not enough space, choose to keep one and discard another or use stoves to convert to foods
# TODO: make sure to shuffle field list before action_g
# TODO: make sure update field list after action_d
# TODO: calculating points after round 14
# TODO: converting discarded livestock to food if the player has improvements (after every livestock assignment)

#==============================================================================================================
while False:
    ## Agent
    game = AgricolaAI()

    round = 1
    states = {player: {resource: [] for resource in game.player1_state} for player in range(1, 5)}


    while round < 15:
        print(f'This is round {round}')

        # Initial states
        # print('Board resource:')
        # print(game.board_resource)
        # print('Player 1 state:')
        # print(game.player1_state)
        # print('Player 2 state:')
        # print(game.player2_state)
        # print('Player 3 state:')
        # print(game.player3_state)
        # print('Player 4 state:')
        # print(game.player4_state)

        print('------------------------------------------------------')
        obs, reward, done, action_space = game.step(round)

        print('**************')
        print(obs)
        print(len(action_space))
        print(action_space)
        print('**************')
        print(f'Reward: {reward}')


        # End states
        print('------------------------------------------------------')
        print('Board resource:')
        print(game.board_resource)
        print('Player 1 state:')
        print(game.player1_state)
        print('Player 2 state:')
        print(game.player2_state)
        print('Player 3 state:')
        print(game.player3_state)
        print('Player 4 state:')
        print(game.player4_state)

        print('================================================================================================')
        round += 1

    break

#==============================================================================================================
def run_single_game(game):
    round = 1
    states = {player: {resource: [] for resource in game.player1_state} for player in range(1, 5)}
    parameters_to_show = ['clay', 'reed', 'wood', 'grain', 'food']
    points = {player: [] for player in range(1, 5)}

    while round < 15:

        # print_state('Board resource', game.board_resource)
        # for i in range(1, 5):
        #     print_state(f'Player {i} state', getattr(game, f'player{i}_state'))

        game.step(round)

        for player, state in enumerate([game.player1_state, game.player2_state, game.player3_state, game.player4_state],
                                       start=1):
            for resource, value in state.items():
                if resource in parameters_to_show:
                    states[player][resource].append(value)

        # for i in range(1, 5):
        #     print_state(f'Player {i} state', getattr(game, f'player{i}_state'))
        #     print_state(f'Player {i} fields', getattr(game, f'player{i}_field_dict'))

        round += 1

    # Store points at the end of the game
    for i in range(1, 5):
        points[i].append(getattr(game, f'player_{i}_points'))

    return states, points


def plot_results(all_states, all_points, parameters_to_show):
    fig, axes = plt.subplots(len(parameters_to_show) + 1, 1, figsize=(12, (len(parameters_to_show) + 1) * 3),
                             sharex=True)
    rounds = list(range(1, 15))

    for idx, resource in enumerate(parameters_to_show):
        for player in range(1, 5):
            avg_values = [sum(states[player][resource][round] for states in all_states) / len(all_states) for round in
                          range(14)]
            axes[idx].plot(rounds, avg_values, label=f'Player {player}')
        axes[idx].set_ylabel(resource)
        axes[idx].legend(loc='upper right')

    # Plot average points
    avg_points = {player: sum(all_points[player]) / len(all_points[player]) for player in range(1, 5)}
    axes[-1].bar(avg_points.keys(), avg_points.values(), label=[f'Player {player}' for player in avg_points.keys()])
    axes[-1].set_ylabel('Average Points')
    axes[-1].legend(loc='upper right')

    axes[-1].set_xlabel('Players')
    plt.tight_layout()

    # # Save the plot as a file
    # plt.savefig('/home/tien2791/my-google-drive/Agricola_AI/venv/plot.png')
    #
    # # Close the plot
    # plt.close()

    plt.show()


def run_multiple_iterations(num_iterations):
    all_states = []
    all_points = {player: [] for player in range(1, 5)}

    for _ in range(num_iterations):
        game = AgricolaAI()
        states, points = run_single_game(game)
        all_states.append(states)
        for player in range(1, 5):
            all_points[player].extend(points[player])

    parameters_to_show = ['clay', 'reed', 'wood', 'grain', 'food']
    plot_results(all_states, all_points, parameters_to_show)


# Run multiple iterations
run_multiple_iterations(1)


#==============================================================================================================
# num_iterations = 1  # Specify the number of iterations

# for iteration in range(num_iterations):
#     print(f"Starting iteration {iteration + 1}")
#
#     ## Agent
#     game = AgricolaAI()
#
#     round = 1
#     states = {player: {resource: [] for resource in game.player1_state} for player in range(1, 5)}
#
#     while round < 15:
#         print(f'This is round {round}')
#
#         print('------------------------------------------------------')
#         obs, reward, done, action_space = game.step(round)
#
#         print('**************')
#         print(obs)
#         print(len(action_space))
#         print(action_space)
#         print('**************')
#         print(f'Reward: {reward}')
#
#         # End states
#         print('------------------------------------------------------')
#         print('Board resource:')
#         print(game.board_resource)
#         print('Player 1 state:')
#         print(game.player1_state)
#         print('Player 2 state:')
#         print(game.player2_state)
#         print('Player 3 state:')
#         print(game.player3_state)
#         print('Player 4 state:')
#         print(game.player4_state)
#
#         print('================================================================================================')
#         round += 1
#
#     print(f"Ending iteration {iteration + 1}")
#     print("##########################################################\n")