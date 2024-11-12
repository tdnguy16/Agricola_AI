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

class AgricolaAI:

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

        self.reset()

    def reset(self):

        self.round = 1

        self.reward = 0

        self.action_used = []

        self.moves = [self.action_a, self.action_b, self.action_c,
                      self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o, self.action_1]

        self.moves_total = [self.action_a, self.action_b, self.action_c,
                      self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o, self.action_1, self.action_2, self.action_3, self.action_4, self.action_5, self.action_6, self.action_7, self.action_8, self.action_9, self.action_10, self.action_11, self.action_12, self.action_13, self.action_14]

        self.moves_total_names = ['action_a', 'action_b', 'action_c',
                            'action_d', 'action_e', 'action_f',
                            'action_g', 'action_h', 'action_i', 'action_j', 'action_k', 'action_l',
                            'action_m', 'action_n', 'action_o', 'action_1', 'action_2', 'action_3',
                            'action_4', 'action_5', 'action_6', 'action_7', 'action_8', 'action_9',
                            'action_10', 'action_11', 'action_12', 'action_13', 'action_14']

        self.action_name_dict = {
            self.action_a: 'action_a', self.action_b: 'action_b', self.action_c: 'action_c',
            self.action_d: 'action_d', self.action_e: 'action_e', self.action_f: 'action_f',
            self.action_g: 'action_g', self.action_h: 'action_h', self.action_i: 'action_i',
            self.action_j: 'action_j', self.action_k: 'action_k', self.action_l: 'action_l',
            self.action_m: 'action_m', self.action_n: 'action_n', self.action_o: 'action_o',
            self.action_1: 'action_1', self.action_2: 'action_2', self.action_3: 'action_3',
            self.action_4: 'action_4', self.action_5: 'action_5', self.action_6: 'action_6',
            self.action_7: 'action_7', self.action_8: 'action_8', self.action_9: 'action_9',
            self.action_10: 'action_10', self.action_11: 'action_11', self.action_12: 'action_12',
            self.action_13: 'action_13', self.action_14: 'action_14'
        }

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

        # initial game resources
        self.board_resource = {'2_clay': 2, '1_clay': 1, 'reed': 1, '1_wood': 1, '2_wood': 2, '3_wood': 3, 'food': 1,
                               'sheep': 1, 'boar': 0, 'cow': 0, 'round': 1}
        self.reserve_resource = {'clay': 27, 'reed': 19, 'wood': 34, 'grain': 31, 'food': 71, 'sheep': 25, 'boar': 19,
                                 'cow': 17, 'begging': 5}

        self.improvements = [self.improvement_2, self.improvement_3a, self.improvement_3, self.improvement_4a,
                             self.improvement_4, self.improvement_5]
        self.tiles = {'pasteur_2': 20, 'pasteur_4': 13, 'pasteur_6': 2, 'pasteur_8': 1, 'field': 20, 'stable': 10,
                      'room': 12}

        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)

        # initial player resources
        self.player1_state = {'valid_action': 0, 'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 40, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player1_improvements = []
        self.player1_field_dict = {}

        self.player2_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player2_improvements = []
        self.player2_field_dict = {}

        self.player3_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player3_improvements = []
        self.player3_field_dict = {}

        self.player4_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
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

        self.determine_order(self.player1_state, self.player2_state, self.player3_state, self.player4_state)

        # Reset actions list for new round
        self.new_round_action_set()
        # self.action_space = spaces.Discrete(len(self.moves))

        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state,
                                     self.board_resource, self.reserve_resource, self.tiles, self.moves_check)

        self.determine_order(self.player1_state, self.player2_state, self.player3_state, self.player4_state)

        # Set up initial value for reward
        self.previous_parameter = 0

        self.done = False

        return self.obs

    # --------------------------------------------------------------------------------------------------------------------------------------------------#
    ### Moves
    def generate_moves_check_dict(self, moves, moves_total):
        return {self.action_name_dict[move]: 1 if move in moves else 0 for move in moves_total}

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

    def assign_livestock(self, player_state, acquired_sheeps, acquired_boars, acquired_cows):
        # TODO: prioritize to save cows, then boars, then sheeps
        # Define the priority order: cow first, then boar, then sheep
        priority_order = ['cow', 'boar', 'sheep']

        # Dictionary to store acquired livestock
        acquired_livestock = {
            'cow': acquired_cows,
            'boar': acquired_boars,
            'sheep': acquired_sheeps
        }

        # Calculate the total number of slots available for livestock
        total_slot = player_state['pasteur_2'] * 2 + player_state['pasteur_4'] * 4 + player_state['pasteur_6'] * 6 + \
                     player_state['pasteur_8'] * 8
        current_livestock = player_state['sheep'] + player_state['boar'] + player_state['cow']

        # Determine available slots after accounting for current livestock
        available_slot = total_slot - current_livestock

        if available_slot > 0:
            for livestock in priority_order:
                if acquired_livestock[livestock] > 0:
                    if available_slot > acquired_livestock[livestock]:
                        # Add the livestock to player's resource
                        player_state[livestock] += acquired_livestock[livestock]

                        available_slot -= acquired_livestock[livestock]
                    else:
                        # Add the livestock to player's resource
                        player_state[livestock] += available_slot

                        available_slot = 0

                        if available_slot == 0:
                            break

        if available_slot == 0:
            # No available slots, return unassigned livestock to reserved resource
            for livestock in priority_order:
                self.reserve_resource[livestock] += acquired_livestock[livestock]

    # def assign_livestock(self, player_state, acquired_sheeps, acquired_boars, acquired_cows):
    #     # TODO: prioritize to save cows, then boars, then sheeps
    #     total_slot = player_state['pasteur_2'] * 2 + player_state['pasteur_4'] * 4 + player_state['pasteur_6'] * 6 + \
    #                  player_state['pasteur_8'] * 8
    #     current_livestock = player_state['sheep'] + player_state['boar'] + player_state['cow']
    #
    #     available_slot = total_slot - current_livestock
    #
    #     if available_slot > 0:
    #
    #         if acquired_cows > 0:
    #             if available_slot > acquired_cows:
    #                 # Add the cows to player's resource
    #                 player_state['cow'] += acquired_cows
    #                 # Remove cows from global resource
    #                 self.reserve_resource['cow'] -= acquired_cows
    #
    #                 available_slot = available_slot - acquired_cows
    #
    #             else:
    #                 # Add the cows to player's resource
    #                 player_state['cow'] += available_slot
    #                 # Remove cows from global resource
    #                 self.reserve_resource['cow'] -= available_slot
    #
    #                 available_slot = 0
    #
    #         if acquired_boars > 0:
    #             if available_slot > acquired_boars:
    #                 # Add the boars to player's resource
    #                 player_state['boar'] += acquired_boars
    #                 # Remove boars from global resource
    #                 self.reserve_resource['boar'] -= acquired_boars
    #
    #                 available_slot = available_slot - acquired_boars
    #
    #             else:
    #                 # Add the boars to player's resource
    #                 player_state['boar'] += available_slot
    #                 # Remove boars from global resource
    #                 self.reserve_resource['boar'] -= available_slot
    #
    #                 available_slot = 0
    #
    #         if acquired_sheeps > 0:
    #             if available_slot > acquired_sheeps:
    #                 # Add the sheeps to player's resource
    #                 player_state['sheep'] += acquired_sheeps
    #                 # Remove sheeps from global resource
    #                 self.reserve_resource['sheep'] -= acquired_sheeps
    #
    #                 available_slot = available_slot - acquired_sheeps
    #
    #             else:
    #                 # Add the sheeps to player's resource
    #                 player_state['sheep'] += available_slot
    #                 # Remove sheeps from global resource
    #                 self.reserve_resource['sheep'] -= available_slot
    #
    #                 available_slot = 0
    #
    #     else:
    #         # No available slots, return livestocks to reserved resource
    #         self.reserve_resource['sheep'] += acquired_sheeps
    #         self.reserve_resource['boar'] += acquired_boars
    #         self.reserve_resource['cow'] += acquired_cows

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
            #!!print('out of woods')
            pass

        if self.reserve_resource['clay'] > 0:
            # Player gain
            player_state['clay'] = player_state['clay'] + 1
            # Deduct from global resources
            self.reserve_resource['clay'] = self.reserve_resource['clay'] - 1
        else:
            #!!print('out of clays')
            pass

        if self.reserve_resource['reed'] > 0:
            # Player gain
            player_state['reed'] = player_state['reed'] + 1
            # Deduct from global resources
            self.reserve_resource['reed'] = self.reserve_resource['reed'] - 1
        else:
            #!!print('out of reeds')
            pass

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_a']

    # TODO: asssumption, action b, always take 1 pasteur and 1 stable if have enough resources, prioritize 2, 4, 6 then 8 slot pasteur

    def action_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b'])

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][
                1] and \
                    player_state['wood'] >= self.pasteur_2["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_2["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_2["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_2["price"][2]
                # Player gain
                player_state['pasteur_2'] = player_state['pasteur_2'] + 1
                #!!print(f'The player chose pasteur_2')

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                #!!print('you cannot afford the pasteur 2')
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
                        #!!print('you cannot afford the stable')
                        pass
                else:
                    #!!print('out of stables')
                    pass

        else:
            #!!print('out of pasteur_2')

            if self.tiles['pasteur_4'] > 0:
                # Check player's payment
                if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= \
                        self.pasteur_4["price"][
                            1] and \
                        player_state['wood'] >= self.pasteur_4["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - self.pasteur_4["price"][0]
                    player_state['reed'] = player_state['reed'] - self.pasteur_4["price"][1]
                    player_state['wood'] = player_state['wood'] - self.pasteur_4["price"][2]
                    # Player gain
                    player_state['pasteur_4'] = player_state['pasteur_4'] + 1
                    #!!print(f'The player chose pasteur_4')

                    # Add to reserved resources
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

                else:
                    #!!print('you cannot afford the pasteur 4')
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
                            #!!print('you cannot afford the stable')
                            pass
                    else:
                        #!!print('out of stables')
                        pass

            else:
                #!!print('out of pasteur_4')

                if self.tiles['pasteur_6'] > 0:
                    # Check player's payment
                    if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= \
                            self.pasteur_6["price"][
                                1] and \
                            player_state['wood'] >= self.pasteur_6["price"][2]:
                        # Player pays
                        player_state['clay'] = player_state['clay'] - self.pasteur_6["price"][0]
                        player_state['reed'] = player_state['reed'] - self.pasteur_6["price"][1]
                        player_state['wood'] = player_state['wood'] - self.pasteur_6["price"][2]
                        # Player gain
                        player_state['pasteur_6'] = player_state['pasteur_6'] + 1
                        #!!print(f'The player chose pasteur_6')

                        # Add to reserved resources
                        self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                        self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                        self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                        # Deduct from global resources
                        self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

                    else:
                        #!!print('you cannot afford the pasteur 6')
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
                                #!!print('you cannot afford the stable')
                                pass
                        else:
                            #!!print('out of stables')
                            pass

                else:
                    #!!print('out of pasteur_6')

                    if self.tiles['pasteur_8'] > 0:
                        # Check player's payment
                        if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= \
                                self.pasteur_8["price"][
                                    1] and \
                                player_state['wood'] >= self.pasteur_8["price"][2]:
                            # Player pays
                            player_state['clay'] = player_state['clay'] - self.pasteur_8["price"][0]
                            player_state['reed'] = player_state['reed'] - self.pasteur_8["price"][1]
                            player_state['wood'] = player_state['wood'] - self.pasteur_8["price"][2]
                            # Player gain
                            player_state['pasteur_8'] = player_state['pasteur_8'] + 1
                            #!!print(f'The player chose pasteur_8')

                            # Add to reserved resources
                            self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                            self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                            self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                            # Deduct from global resources
                            self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

                        else:
                            #!!print('you cannot afford the pasteur 8')
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
                                    #!!print('you cannot afford the stable')
                                    pass
                            else:
                                #!!print('out of stables')
                                pass

                    else:
                        #!!print('out of pasteur_8')
                        pass

    def action_b_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        #!!print(f'The player chose pasteur_2')

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

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
            #!!print('out stables')
            pass

    def action_b_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        #!!print(f'The player chose pasteur_4')

        # Check resource availability
        if self.tiles['pasteur_4'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= self.pasteur_4["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

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
            #!!print('out stables')
            pass

    def action_b_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        #!!print(f'The player chose pasteur_6')

        # Check resource availability
        if self.tiles['pasteur_6'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= self.pasteur_6["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

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
            #!!print('out stables')
            pass

    def action_b_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        #!!print(f'The player chose pasteur_8')

        # Check resource availability
        if self.tiles['pasteur_8'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= self.pasteur_8["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

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
            #!!print('out stables')
            pass

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
            #!!print('out of stables')
            pass

    # TODO: asssumption, action c, only by 1 tile of any types
    def action_c(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c'])

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][
                1] and \
                    player_state['wood'] >= self.pasteur_2["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.pasteur_2["price"][0]
                player_state['reed'] = player_state['reed'] - self.pasteur_2["price"][1]
                player_state['wood'] = player_state['wood'] - self.pasteur_2["price"][2]
                # Player gain
                player_state['pasteur_2'] = player_state['pasteur_2'] + 1
                #!!print(f'The player chose pasteur_2')

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                #!!print('you cannot afford the pasteur 2')
                pass

        else:
            #!!print('out of pasteur_2')

            if self.tiles['pasteur_4'] > 0:
                # Check player's payment
                if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= \
                        self.pasteur_4["price"][
                            1] and \
                        player_state['wood'] >= self.pasteur_4["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - self.pasteur_4["price"][0]
                    player_state['reed'] = player_state['reed'] - self.pasteur_4["price"][1]
                    player_state['wood'] = player_state['wood'] - self.pasteur_4["price"][2]
                    # Player gain
                    player_state['pasteur_4'] = player_state['pasteur_4'] + 1
                    #!!print(f'The player chose pasteur_4')

                    # Add to reserved resources
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

                else:
                    #!!print('you cannot afford the pasteur 4')
                    pass

            else:
                #!!print('out of pasteur_4')

                if self.tiles['pasteur_6'] > 0:
                    # Check player's payment
                    if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= \
                            self.pasteur_6["price"][
                                1] and \
                            player_state['wood'] >= self.pasteur_6["price"][2]:
                        # Player pays
                        player_state['clay'] = player_state['clay'] - self.pasteur_6["price"][0]
                        player_state['reed'] = player_state['reed'] - self.pasteur_6["price"][1]
                        player_state['wood'] = player_state['wood'] - self.pasteur_6["price"][2]
                        # Player gain
                        player_state['pasteur_6'] = player_state['pasteur_6'] + 1
                        #!!print(f'The player chose pasteur_6')

                        # Add to reserved resources
                        self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                        self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                        self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                        # Deduct from global resources
                        self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

                    else:
                        #!!print('you cannot afford the pasteur 6')
                        pass

                else:
                    #!!print('out of pasteur_6')

                    if self.tiles['pasteur_8'] > 0:
                        # Check player's payment
                        if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= \
                                self.pasteur_8["price"][
                                    1] and \
                                player_state['wood'] >= self.pasteur_8["price"][2]:
                            # Player pays
                            player_state['clay'] = player_state['clay'] - self.pasteur_8["price"][0]
                            player_state['reed'] = player_state['reed'] - self.pasteur_8["price"][1]
                            player_state['wood'] = player_state['wood'] - self.pasteur_8["price"][2]
                            # Player gain
                            player_state['pasteur_8'] = player_state['pasteur_8'] + 1
                            #!!print(f'The player chose pasteur_8')

                            # Add to reserved resources
                            self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                            self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                            self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                            # Deduct from global resources
                            self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

                        else:
                            #!!print('you cannot afford the pasteur 8')
                            pass

                    else:
                        #!!print('out of pasteur_8')
                        pass

    def action_c_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        #!!print(f'The player chose pasteur_2')

        # Check resource availability
        if self.tiles['pasteur_2'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_2["price"][0] and player_state['reed'] >= self.pasteur_2["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

    def action_c_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        #!!print(f'The player chose pasteur_4')

        # Check resource availability
        if self.tiles['pasteur_4'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_4["price"][0] and player_state['reed'] >= self.pasteur_4["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

    def action_c_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        #!!print(f'The player chose pasteur_6')

        # Check resource availability
        if self.tiles['pasteur_6'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_6["price"][0] and player_state['reed'] >= self.pasteur_6["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

    def action_c_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        #!!print(f'The player chose pasteur_8')

        # Check resource availability
        if self.tiles['pasteur_8'] > 0:
            # Check player's payment
            if player_state['clay'] >= self.pasteur_8["price"][0] and player_state['reed'] >= self.pasteur_8["price"][
                1] and \
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
                #!!print('you cannot afford it')
                pass

        else:
            #!!print('out of tiles')
            pass

    def action_d(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_d'])

        # Check resource availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1
            self.tiles['pasteur_2'] = self.tiles['pasteur_2'] -1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            #!!print('out of fields')
            pass

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
            #!!print('Not enough grains')
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
                #!!print('plow a field first')
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
            #!!print('out of grains')
            pass

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
            #!!print('out of foods')
            pass

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
            #!!print(f"The player chose {chosen_improvement}")

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
            #!!print('out of improvements')
            pass

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
                    #!!print('you cannot afford it')
                    pass

            else:
                #!!print('out of rooms')
                pass

        else:
            #!!print('player has already coverted to clay, cannot take this action')
            pass

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
            #!!print('out of stables')
            pass

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
            #!!print('out of stables')
            pass

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
                    #!!print('you cannot afford it')
                    pass
            else:
                #!!print('out of rooms')
                pass
        else:
            #!!print('player has already coverted to clay, cannot take this action')
            pass

        if self.tiles['stable'] > 0:
            # Player gain
            player_state['stable'] = player_state['stable'] + 1
            # Deduct from global resources
            self.tiles['stable'] = self.tiles['stable'] - 1
        else:
            #!!print('out of stables')
            pass

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
                    #!!print('you cannot afford it')
                    pass

            else:
                #!!print('out of rooms')
                pass
        else:
            #!!print('convert to clay first before take this action')
            pass

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
            #!!print('out of stables')
            pass

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
            #!!print('out of stables')
            pass

    def action_5(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_5'])

        if player_state['farmer'] < 5:
            if player_state['room_space'] > player_state['farmer']:
                player_state['farmer'] = player_state['farmer'] + 1
            else:
                #!!print('not enough rooms')
                pass
        else:
            #!!print('no more farmers')
            pass

    def action_6(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_6'])

        acquired_sheeps = 0
        acquired_boars = self.board_resource['boar']
        acquired_cows = 0
        # Assign livestocks
        self.assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows)

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
                self.improvements = [x for x in self.improvements if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_7)

            else:
                #!!print('you cannot afford it')
                pass

        else:
            #!!print(f'improvement_7 is not available')
            pass

    def action_8(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_8'])

        acquired_sheeps = 0
        acquired_boars = 0
        acquired_cows = self.board_resource['cow']
        # Assign livestocks
        self.assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows)

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
                self.improvements = [x for x in self.improvements if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_9)

            else:
                #!!print('you cannot afford it')
                pass

        else:
            #!!print(f'improvement_9 is not available')
            pass

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
                self.improvements = [x for x in self.improvements if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_10)

            else:
                #!!print('you cannot afford it')
                pass

        else:
            #!!print(f'improvement_10 is not available')
            pass

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
                self.improvements = [x for x in self.improvements if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_11)

            else:
                #!!print('you cannot afford it')
                pass

        else:
            #!!print(f'improvement_11 is not available')
            pass

    def action_12(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_12'])

        if player_state['farmer'] < 5:
            player_state['farmer'] = player_state['farmer'] + 1
        else:
            #!!print('no more farmers')
            pass

    def action_13(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_13', 'action_13_b'])

        # Check resource availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1
            self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            #!!print('out of fields')
            pass

        if player_state['grain'] < 1:
            #!!print('Not enough grains')
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
                #!!print('plow a field first')
                break

    def action_13_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_13', 'action_13_b'])

        if player_state['grain'] < 1:
            #!!print('Not enough grains')
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
                            #!!print('plow more fields')
                            pass

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                           f'{player_field_dict[y]}'] + 1 + \
                                                                       self.reserve_resource['grain']
                        # take grain from global inventory
                        self.reserve_resource['grain'] = 0
                        y = y + 1
                else:
                    #!!print('plow a field first')
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
                            #!!print('plow more fields')
                            pass

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_dict[y]}'] = player_field_dict[
                                                                           f'{player_field_dict[y]}'] + 1 + \
                                                                       self.reserve_resource['grain']
                        # take grain from global inventory
                        self.reserve_resource['grain'] = 0
                        y = y + 1
                else:
                    #!!print('plow a field first')
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
                self.improvements = [x for x in self.improvements if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_14)

            else:
                #!!print('you cannot afford it')
                pass

        else:
            #!!print(f'improvement_14 is not available')
            pass

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
            return [0, 0, 0]

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
        # Assumption: only use 1 improvement
        if len(player_improvements) < 1:
            return player_missing_foods

        usable_improvements = self.find_positive_resource_food(player_improvements)

        if not usable_improvements:
            return player_missing_foods

        x = random.choice(usable_improvements)

        # Assuming `improvement` is a dictionary already
        improvement = next((imp for imp in player_improvements if imp['name'] == x), None)

        if improvement is None:
            return player_missing_foods

        acquired_food = 0

        # Create a list of resource types and corresponding improvement keys
        resources = [
            ('grain', 'wood', 'grain_wood_food'),
            ('clay', 'clay_food'),
            ('reed', 'reed_food'),
            ('wood', 'wood_food'),
            ('grain', 'grain_food')
        ]

        for resource in resources:
            if len(resource) == 3:
                res1, res2, key = resource
                if improvement['resource_food'].get(key, 0) > 0:
                    max_possible_use = min(player_state[res1], player_state[res2])
                    y = 0
                    for i in range(1, max_possible_use + 1):
                        acquired_food = i * improvement['resource_food'][key]
                        if acquired_food + player_missing_foods >= 0:
                            y = i
                            break
                        y = i

                    # Ensure we don't take more than available
                    y = min(y, player_state[res1], player_state[res2])

                    # Take the used resources from player's inventory
                    player_state[res1] -= y
                    player_state[res2] -= y

            else:
                res, key = resource
                if improvement['resource_food'].get(key, 0) > 0:
                    max_possible_use = player_state[res]
                    y = 0
                    for i in range(1, max_possible_use + 1):
                        acquired_food = i * improvement['resource_food'][key]
                        if acquired_food + player_missing_foods >= 0:
                            y = i
                            break
                        y = i

                    # Ensure we don't take more than available
                    y = min(y, player_state[res])

                    player_state[res] -= y

        player_missing_foods += acquired_food

        return player_missing_foods

    def use_grain_to_feed(self, player_state, player_missing_foods):
        if player_state['grain'] < 1:
            #!!print('Not enough grains')
            return player_missing_foods

        # Amount of grain to be used
        grains_to_use = min(player_state['grain'], -player_missing_foods)

        if grains_to_use == 0:
            return player_missing_foods

        #!!print(f"{grains_to_use} grain was used to feed")
        player_state['grain'] -= grains_to_use
        player_missing_foods += grains_to_use

        return player_missing_foods

    def use_livestock_to_feed(self, player_state, player_missing_foods, player_improvements):
        #TODO Assumption: prioritize the use of livestock for food in this order: cow, boar, sheep
        if len(player_improvements) < 1:
            return player_missing_foods

        usable_improvements = self.find_positive_livestock_food(player_improvements)

        if len(usable_improvements) < 1:
            #!!print('No appropriate improvement found!')
            return player_missing_foods

        x = random.choice(usable_improvements)

        # Assuming `improvement` is a dictionary already
        improvement = next((imp for imp in player_improvements if imp['name'] == x), None)

        if improvement is None:
            return player_missing_foods

        # Find all the possible feeding combinations and randomly pick one
        feeding_option = self.find_livestock_feeding_options(player_state, player_missing_foods, improvement)

        # Acquired foods
        acquired_food = (
                feeding_option[0] * improvement['livestock_food']['sheep_food'] +
                feeding_option[1] * improvement['livestock_food']['boar_food'] +
                feeding_option[2] * improvement['livestock_food']['cow_food']
        )

        #!!print(f"{improvement['name']} was used on {feeding_option[0]} sheep, {feeding_option[1]} boar, and {feeding_option[2]} cow to exchange for {acquired_food} food")

        # Ensure we don't take more than available
        feeding_option[0] = min(feeding_option[0], player_state['sheep'])
        feeding_option[1] = min(feeding_option[1], player_state['boar'])
        feeding_option[2] = min(feeding_option[2], player_state['cow'])

        # Update livestock
        player_state['sheep'] -= feeding_option[0]
        player_state['boar'] -= feeding_option[1]
        player_state['cow'] -= feeding_option[2]

        player_missing_foods += acquired_food

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
        player_missing_foods = player_required_foods - player_state['food']

        # Deduct food from player's state
        player_state['food'] = max(0, player_state['food'] - player_required_foods)

        # Not enough foods, players have to use either grains or livestocks to feed
        if player_missing_foods > 0:
            #   Feed the farmers using improvements
            player_missing_foods = self.use_improvement_to_feed(player_state, -player_missing_foods,
                                                                player_improvements)

            if player_missing_foods == 0:
                #!!print('Done feeding!')
                pass

            if player_missing_foods > 0:
                player_state['food'] = player_missing_foods
                #!!print('Done feeding!')

            if player_missing_foods < 0:
                #   Feed the farmers using livestock
                player_missing_foods = self.use_livestock_to_feed(player_state, player_missing_foods,
                                                                  player_improvements)

                if player_missing_foods == 0:
                    #!!print('Done feeding!')
                    pass

                if player_missing_foods > 0:
                    player_state['food'] = player_missing_foods
                    #!!print('Done feeding!')

                if player_missing_foods < 0:
                    #   Feed the farmers using grains
                    player_missing_foods = self.use_grain_to_feed(player_state, player_missing_foods)

                    if player_missing_foods == 0:
                        #!!print('Done feeding!')
                        pass

                    if player_missing_foods > 0:
                        player_state['food'] = player_missing_foods
                        #!!print('Done feeding!')

                    if player_missing_foods < 0:
                        #   Still not enough foods, get begging tokens
                        player_state['begging'] += (-1) * player_missing_foods

        ## Offsprings
        # Assigning offsprings
        if min(self.reserve_resource['sheep'], player_state['sheep'] // 2) <= self.reserve_resource['sheep']:
            sheep_offspring = min(self.reserve_resource['sheep'], player_state['sheep'] // 2)
            self.reserve_resource['sheep'] -= sheep_offspring
        else:
            sheep_offspring = self.reserve_resource['sheep']
            self.reserve_resource['sheep'] = 0

        if min(self.reserve_resource['boar'], player_state['boar'] // 2) <= self.reserve_resource['boar']:
            boar_offspring = min(self.reserve_resource['boar'], player_state['boar'] // 2)
            self.reserve_resource['boar'] -= boar_offspring
        else:
            boar_offspring = self.reserve_resource['boar']
            self.reserve_resource['boar'] = 0
        
        if min(self.reserve_resource['cow'], player_state['cow'] // 2) <= self.reserve_resource['cow']:
            cow_offspring = min(self.reserve_resource['cow'], player_state['cow'] // 2)
            self.reserve_resource['cow'] -= cow_offspring
        else:
            cow_offspring = self.reserve_resource['cow']
            self.reserve_resource['cow'] = 0

        # Re-assign livestocks
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

    def generate_obs(self, player1_state, player2_state, player3_state, player4_state, board_resource, reserve_resource,
                     tiles, moves):
        observation = []
        observation.extend(player1_state.values())
        observation.extend(player2_state.values())
        observation.extend(player3_state.values())
        observation.extend(player4_state.values())
        observation.extend(board_resource.values())
        observation.extend(reserve_resource.values())
        observation.extend(tiles.values())
        observation.extend(moves.values())
        obs = np.array(observation, dtype=np.float32)
        return obs

    def check_negative_resource(self, data):
        ignore_indices = [2, 28, 54, 80]  # Indices to be ignored
        for i, value in enumerate(data):
            if i not in ignore_indices and value < 0:
                print(f"Breaking at index {i}, value: {value}")
                print(data)
                sys.exit("Terminating script due to negative value")  # Break the function

    def calculate_reward(self, parameter):

        # Example reward logic
        # print(f'Previous {parameter}: {self.previous_parameter}')
        # print(f'Current {parameter}: {self.player1_state[parameter]}')

        reward = (self.player1_state[parameter] - self.previous_parameter)
        self.previous_parameter = self.player1_state[parameter]

        return reward

    def new_round_action_set(self):

        self.moves = [self.action_a, self.action_b, self.action_c,
                      self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o]


        if self.round >= 1:
            self.moves.append(self.action_1)
        if self.round >= 2:
            self.moves.append(self.action_2)
            # self.moves.append(self.action_2_b)
        if self.round >= 3:
            self.moves.append(self.action_3)
        if self.round >= 4:
            self.moves.append(self.action_4)
            # self.moves.append(self.action_4_b)
        if self.round >= 5:
            self.moves.append(self.action_5)
        if self.round >= 6:
            self.moves.append(self.action_6)
        if self.round >= 7:
            self.moves.append(self.action_7)
        if self.round >= 8:
            self.moves.append(self.action_8)
        if self.round >= 9:
            self.moves.append(self.action_9)
        if self.round >= 10:
            self.moves.append(self.action_10)
        if self.round >= 11:
            self.moves.append(self.action_11)
        if self.round >= 12:
            self.moves.append(self.action_12)
        if self.round >= 13:
            self.moves.append(self.action_13)
            # self.moves.append(self.action_13_b)
        if self.round >= 14:
            self.moves.append(self.action_14)

    def determine_order(self, player1_state, player2_state, player3_state, player4_state):
        self.player1_number_actions = player1_state['farmer']
        self.player2_number_actions = player2_state['farmer']
        self.player3_number_actions = player3_state['farmer']
        self.player4_number_actions = player4_state['farmer']
        self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

        self.order_list = [1, 2, 3, 4]

        if player1_state['rooster'] == 1:
            self.order_list[0] = 1
        if player2_state['rooster'] == 1:
            self.order_list[0] = 2
        if player3_state['rooster'] == 1:
            self.order_list[0] = 3
        if player4_state['rooster'] == 1:
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

        self.player_order_numeric = [self.order_list[0], self.order_list[1],
                             self.order_list[2], self.order_list[3]]

    ### Gameplay
    def step(self, action):
        print('=====================================================================================================')
        print(f'Round {self.round}')
        self.player1_state['round'] = self.round
        self.player2_state['round'] = self.round
        self.player3_state['round'] = self.round
        self.player4_state['round'] = self.round
        self.board_resource['round'] = self.round

        #!!print('Here are board resources')
        #!!print(self.board_resource)

        # Players take actions
        if self.remain_actions > 0:
            for order in self.player_order:

                # Player 1 take action
                # #!!print('Actions:')
                # #!!print(self.moves)
                if order == 'player1':
                    if self.player1_number_actions != 0:
                        # print(f"There are {self.board_resource['cow']} cows on board")

                        # Check if action is valid
                        if self.moves_check[self.moves_total_names[action]] == 1:
                            #!!print('-----------------------PLAYER 1-----------------------')
                            #!!print(f'action index is {action[action_index]}')
                            #!!print(f'length of action list is {len(self.moves)}')

                            #!!print('States BEFORE actions')
                            #!!print(self.player1_state)

                            # print(len(self.moves))
                            # print(self.obs[-29:].tolist())
                            # print(action)

                            self.player1_action = self.moves_total[action]  # player 1 takes action from the training agent
                            print(self.moves_total[action])
                            self.player1_state['action'] = action
                            #!!print(f"player 1 take action {self.player1_action}")


                            self.player1_action(self.player1_state, self.player1_field_dict, self.player1_improvements)
                            #!!print('States AFTER actions')
                            #!!print(self.player1_state)
                            # #!!print(len(self.moves))

                            self.action_used.append(self.moves_total_names[action])
                            total_action_used.append(self.moves_total_names[action])

                        if self.moves_check[self.moves_total_names[action]] == 0:
                            print('INVALID ACTION')
                            self.action_used.append('INVALID')
                            total_action_used.append('INVALID')
                            # self.player1_state['invalid_action'] = self.player1_state['invalid_action'] + 1

                        self.player1_number_actions -= 1

                        # print(f"Player 1 has {self.player1_state['cow']} cows")

                # Calculate round reward based on specific parameter
                self.reward = self.calculate_reward('valid_action')

                if self.reward != 0:
                    print('$$$')
                    print(self.reward)

                # Player 2 take action
                if order == 'player2':
                    if self.player2_number_actions != 0:
                        #!!print('-----------------------PLAYER 2-----------------------')
                        #!!print('States BEFORE actions')
                        #!!print(self.player2_state)
                        x = random.randint(0, len(self.moves) - 1)  # randomzzz
                        self.player2_action = self.moves[x]
                        self.player2_state['action'] = x
                        #!!print(f"player 2 take action {self.player2_action}")
                        self.player2_action(self.player2_state, self.player2_field_dict, self.player2_improvements)
                        #!!print('States AFTER actions')
                        #!!print(self.player2_state)
                        # #!!print(len(self.moves))
                        self.player2_number_actions -= 1

                        self.action_used.append(self.action_name_dict[self.player2_action])
                        total_action_used.append(self.action_name_dict[self.player2_action])

                # Player 3 take action
                if order == 'player3':
                    if self.player3_number_actions != 0:
                        #!!print('-----------------------PLAYER 3-----------------------')
                        #!!print('States BEFORE actions')
                        #!!print(self.player3_state)
                        x = random.randint(0, len(self.moves) - 1)  # randomzzz
                        self.player3_action = self.moves[x]
                        self.player3_state['action'] = x
                        #!!print(f"player 3 take action {self.player3_action}")
                        self.player3_action(self.player3_state, self.player3_field_dict, self.player3_improvements)
                        #!!print('States AFTER actions')
                        #!!print(self.player3_state)
                        # #!!print(len(self.moves))
                        self.player3_number_actions -= 1

                        self.action_used.append(self.action_name_dict[self.player3_action])
                        total_action_used.append(self.action_name_dict[self.player3_action])

                # Player 4 take action
                if order == 'player4':
                    if self.player4_number_actions != 0:
                        #!!print('-----------------------PLAYER 4-----------------------')
                        #!!print('States BEFORE actions')
                        #!!print(self.player4_state)
                        x = random.randint(0, len(self.moves) - 1)  # randomzzz
                        self.player4_action = self.moves[x]
                        self.player4_state['action'] = x
                        #!!print(f"player 4 take action {self.player4_action}")
                        self.player4_action(self.player4_state, self.player4_field_dict, self.player4_improvements)
                        #!!print('States AFTER actions')
                        #!!print(self.player4_state)
                        # #!!print(len(self.moves))
                        self.player4_number_actions -= 1

                        self.action_used.append(self.action_name_dict[self.player4_action])
                        total_action_used.append(self.action_name_dict[self.player4_action])

            self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

        if self.remain_actions == 0:
            # Harvesting:
            #!!print('=====================================================================================================')
            #!!print('player 1 - harvesting')
            self.harvesting(self.player1_state, self.player1_field_dict, self.player1_improvements)
            #!!print('------------------------------------------------------')
            #!!print('player 2 - harvesting')
            self.harvesting(self.player2_state, self.player2_field_dict, self.player2_improvements)
            #!!print('------------------------------------------------------')
            #!!print('player 3 - harvesting')
            self.harvesting(self.player3_state, self.player3_field_dict, self.player3_improvements)
            #!!print('------------------------------------------------------')
            #!!print('player 4 - harvesting')
            self.harvesting(self.player4_state, self.player4_field_dict, self.player4_improvements)

            # Round points calculate
            self.player1_state['point'] = self.point_cal(self.player1_state)
            self.player2_state['point'] = self.point_cal(self.player2_state)
            self.player3_state['point'] = self.point_cal(self.player3_state)
            self.player4_state['point'] = self.point_cal(self.player4_state)

            #!!print('------------------------------------------------------')
            #!!print('States AFTER HARVESTING')
            #!!print(self.player1_state)
            #!!print(self.player2_state)
            #!!print(self.player3_state)
            #!!print(self.player4_state)

            # Refill board resources after each round
            if self.reserve_resource['clay'] >= 2:
                self.board_resource['2_clay'] = self.board_resource['2_clay'] + 2
                self.reserve_resource['clay'] -= 2
            else:
                self.board_resource['2_clay'] = self.board_resource['2_clay'] + self.reserve_resource['clay']
                self.reserve_resource['clay'] = 0
            
            if self.reserve_resource['clay'] >= 1:
                self.board_resource['1_clay'] = self.board_resource['1_clay'] + 1
                self.reserve_resource['clay'] -= 1
            else:
                self.board_resource['1_clay'] = self.board_resource['1_clay'] + self.reserve_resource['clay']
                self.reserve_resource['clay'] = 0

            if self.reserve_resource['reed'] >= 1:
                self.board_resource['reed'] = self.board_resource['reed'] + 1
                self.reserve_resource['reed'] -= 1
            else:
                self.board_resource['reed'] = self.board_resource['reed'] + self.reserve_resource['reed']
                self.reserve_resource['reed'] = 0

            if self.reserve_resource['wood'] >= 1:
                self.board_resource['1_wood'] = self.board_resource['1_wood'] + 1
                self.reserve_resource['wood'] -= 1
            else:
                self.board_resource['1_wood'] = self.board_resource['1_wood'] + self.reserve_resource['wood']
                self.reserve_resource['wood'] = 0

            if self.reserve_resource['wood'] >= 2:
                self.board_resource['2_wood'] = self.board_resource['2_wood'] + 2
                self.reserve_resource['wood'] -= 2
            else:
                self.board_resource['2_wood'] = self.board_resource['2_wood'] + self.reserve_resource['wood']
                self.reserve_resource['wood'] = 0

            if self.reserve_resource['wood'] >= 3:
                self.board_resource['3_wood'] = self.board_resource['3_wood'] + 3
                self.reserve_resource['wood'] -= 3
            else:
                self.board_resource['3_wood'] = self.board_resource['3_wood'] + self.reserve_resource['wood']
                self.reserve_resource['wood'] = 0

            if self.reserve_resource['food'] >= 1:
                self.board_resource['food'] = self.board_resource['food'] + 1
                self.reserve_resource['food'] -= 1
            else:
                self.board_resource['food'] = self.board_resource['food'] + self.reserve_resource['food']
                self.reserve_resource['food'] = 0

            if self.reserve_resource['sheep'] >= 1:
                self.board_resource['sheep'] = self.board_resource['sheep'] + 1
                self.reserve_resource['sheep'] -= 1
            else:
                self.board_resource['sheep'] = self.board_resource['sheep'] + self.reserve_resource['sheep']
                self.reserve_resource['sheep'] = 0
                
            if self.round >= 5:
                if self.reserve_resource['boar'] >= 1:
                    self.board_resource['boar'] = self.board_resource['boar'] + 1
                    self.reserve_resource['boar'] -= 1
                else:
                    self.board_resource['boar'] = self.board_resource['boar'] + self.reserve_resource['boar']
                    self.reserve_resource['boar'] = 0

            if self.round >= 7:
                if self.reserve_resource['cow'] >= 1:
                    self.board_resource['cow'] = self.board_resource['cow'] + 1
                    self.reserve_resource['cow'] -= 1
                else:
                    self.board_resource['cow'] = self.board_resource['cow'] + self.reserve_resource['cow']
                    self.reserve_resource['cow'] = 0

            # Determine player order for NEXT round
            self.determine_order(self.player1_state, self.player2_state, self.player3_state, self.player4_state)

            # self.player1_state['invalid_action'] = 0

            self.round += 1

            # Reset actions list for new round
            self.new_round_action_set()

        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state,
                                     self.board_resource, self.reserve_resource, self.tiles, self.moves_check)

        # Check if any resource values are negative
        self.check_negative_resource(self.obs)

        info = [self.moves, self.player_order_numeric, self.player1_number_actions, self.player2_number_actions, self.player3_number_actions, self.player4_number_actions]

        # Check if the game is done
        if self.round > 14:
            self.done = True

        return self.obs, self.reward, self.done, info


# TODO: randomimze number of pasteur to take for action c, right now the players only take 1 pasteur
# TODO: harvesting: feeding/begging, field work, offsprings/assigning or converting offsprings to foods.
# TODO: offspring after each harvest and players have to assign livestocks right away
# TODO: when take/offspring livestock and not enough space, choose to keep one and discard another or use stoves to convert to foods
# TODO: make sure to shuffle field list before action_g
# TODO: make sure update field list after action_d
# TODO: calculating points after round 14
# TODO: converting discarded livestock to food if the player has improvements (after every livestock assignment)

# ======================================================================================================================
# TRAINING
training = True
total_action_used = []

class AgricolaEnv(gym.Env):
    def __init__(self):
        super(AgricolaEnv, self).__init__()
        self.game = AgricolaAI()

        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(len(self.game.obs),), dtype=np.float32)

        self.reset()

    def reset(self):
        obs = self.game.reset()
        self.previous_state = obs

        # Define action and observation space
        # self.action_space_list = self.update_action_space([1, 2, 3, 4], 2, 2, 2, 2)

        self.action_space = spaces.Discrete(29)

        return obs

    def step(self, action):
        obs, reward, done, info = self.game.step(action)

        self.action_space = spaces.Discrete(29)

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        pass

    def close(self):
        """Perform any necessary cleanup."""
        pass

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

def chart_occurrences(actions_list):
    # Count occurrences of each action
    occurrences = Counter(actions_list)

    # Sort actions by their occurrences
    sorted_actions = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

    # Split the sorted actions into two lists: actions and counts
    actions, counts = zip(*sorted_actions)

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(actions, counts, color='blue')
    plt.xlabel('Actions')
    plt.ylabel('Occurrences')
    plt.title('Occurrences of Actions')
    plt.xticks(rotation=90)
    plt.tight_layout()

def run_single_game(game, agent_model, parameters_to_show):
    states = {player: {resource: [] for resource in game.player1_state} for player in range(1, 5)}
    points = {player: [] for player in range(1, 5)}

    obs = game.reset()
    while not game.done:
        action, _states = agent_model.predict(obs, deterministic=True)
        obs, reward, done, _ = game.step(action)

        for player, state in enumerate([game.player1_state, game.player2_state, game.player3_state, game.player4_state],
                                       start=1):
            for resource, value in state.items():
                if resource in parameters_to_show:
                    states[player][resource].append(value)

    # Store points at the end of the game
    for i in range(1, 5):
        points[i].append(getattr(game, f'player_{i}_points'))

    return states, points, game.action_used

def run_multiple_iterations(num_iterations, parameters_to_show):
    all_states = []
    total_action_used = []
    all_points = {player: [] for player in range(1, 5)}

    env = AgricolaEnv()
    agent_model = PPO.load("ppo_agricola_valid_action_point", env=env)

    for _ in range(num_iterations):
        game = AgricolaAI()
        states, points, action_used = run_single_game(game, agent_model, parameters_to_show)
        all_states.append(states)
        for player in range(1, 5):
            all_points[player].extend(points[player])

        total_action_used.extend(action_used)

    chart_occurrences(total_action_used)
    plot_results(all_states, all_points, parameters_to_show)

if training == True:
    # def objective(trial):
    #     n_steps = trial.suggest_int("n_steps", 2048, 8192)
    #     gamma = trial.suggest_float("gamma", 0.8, 0.9999)
    #     learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-3)
    #     ent_coef = trial.suggest_loguniform("ent_coef", 1e-8, 1e-2)
    #
    #     env = AgricolaEnv()
    #     model = PPO(
    #         "MlpPolicy",
    #         env,
    #         n_steps=n_steps,
    #         gamma=gamma,
    #         learning_rate=learning_rate,
    #         ent_coef=ent_coef,
    #         verbose=0
    #     )
    #
    #     model.learn(total_timesteps=1000)
    #     mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=10)
    #
    #     return mean_reward
    #
    #
    # study = optuna.create_study(direction="maximize")
    # study.optimize(objective, n_trials=100)
    #
    # print("Best hyperparameters: ", study.best_params)
    #
    # env = AgricolaEnv()
    # model = PPO(
    #     "MlpPolicy",
    #     env,
    #     n_steps=study.best_params["n_steps"],
    #     gamma=study.best_params["gamma"],
    #     learning_rate=study.best_params["learning_rate"],
    #     ent_coef=study.best_params["ent_coef"],
    #     verbose=1
    # )
    #
    # model.learn(total_timesteps=1000)
    # model.save("ppo_agricola_best")

    env = AgricolaEnv()
    model = PPO(
        "MlpPolicy",
        env,
        n_steps=2048,
        batch_size=64,
        gamma=0.901510767006798,
        learning_rate=1.1571376087582738e-05,
        ent_coef=5.467057108921686e-05,
        verbose=1
    )

    # Load the Trained Model and Continue Training
    # model = PPO.load("ppo_agricola_valid_action_food", env=env)

    model.learn(total_timesteps=100)
    model.save("(NEW_1)_ppo_agricola_valid_action")

    # Evaluate the Continued Model (optional)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Mean reward: {mean_reward} +/- {std_reward}")

    chart_occurrences(total_action_used)
    plt.show()

# ======================================================================================================================
# GAME TEST
# Run multiple iterations
parameters_to_show = ['sheep', 'boar', 'wood', 'point']
# run_multiple_iterations(10, parameters_to_show)

plt.show()