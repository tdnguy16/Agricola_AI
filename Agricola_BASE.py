import gym
# import optuna
import random
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.policies import ActorCriticPolicy
# from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from gym import spaces
import sys
import matplotlib.pyplot as plt
from collections import Counter
import copy
import os
from collections import defaultdict


class AgricolaAI:

    def __init__(self, seed=None, agent_model=None, partner_model=None):
        self.agent_model = agent_model
        self.partner_model = partner_model
        self.harvesting_time_player_1 = True
        self.harvesting_time_player_2 = True
        self.harvesting_time_player_3 = True
        self.harvesting_time_player_4 = True

        self.milestones = {
            'resource_goal': False,
            'room_goal': False,
            'family_goal': False,
            'field_goal': False,
        }

        if seed is not None:
            random.seed(seed)

        self.reset()

    def reset(self):

        self.round = 1

        self.reward = 0

        self.agent_action_used = []
        self.partner_action_used = []
        self.action_used = []

        self.moves = [self.action_a, self.action_b, self.action_c,
                      self.action_d, self.action_e, self.action_f,
                      self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                      self.action_m, self.action_n, self.action_o, self.action_1]

        self.moves_total = [self.action_a, self.action_b, self.action_c,
                            self.action_d, self.action_e, self.action_f,
                            self.action_g, self.action_h, self.action_i, self.action_j, self.action_k, self.action_l,
                            self.action_m, self.action_n, self.action_o, self.action_1, self.action_2, self.action_3,
                            self.action_4, self.action_5, self.action_6, self.action_7, self.action_8, self.action_9,
                            self.action_10, self.action_11, self.action_12, self.action_13, self.action_14]

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
        self.previous_round = 0

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
        self.player1_state = {'valid_action': 0, 'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0,
                              'grain': 0, 'food': 2,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player1_improvements = []
        self.player1_field_dict = {}

        self.player1_previous_state = copy.deepcopy(self.player1_state)

        self.player2_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                              'food': 2,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player2_improvements = []
        self.player2_field_dict = {}

        self.player3_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                              'food': 2,
                              'sheep': 0, 'boar': 0,
                              'cow': 0,
                              'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0,
                              'room_space': 2, 'livestock_space': 1, 'farmer': 2,
                              'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0,
                              'stable': 0, 'field': 0}
        self.player3_improvements = []
        self.player3_field_dict = {}

        self.player4_state = {'action': 0, 'point': 0, 'round': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0,
                              'food': 2,
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

        self.player_1_harvesting_check = {4: 1, 7: 1, 9: 1, 11: 1, 13: 1, 14: 1}
        self.player_2_harvesting_check = {4: 1, 7: 1, 9: 1, 11: 1, 13: 1, 14: 1}
        self.player_3_harvesting_check = {4: 1, 7: 1, 9: 1, 11: 1, 13: 1, 14: 1}
        self.player_4_harvesting_check = {4: 1, 7: 1, 9: 1, 11: 1, 13: 1, 14: 1}

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
        total_slot = 1 + player_state['pasteur_2'] * 2 + player_state['pasteur_4'] * 4 + player_state['pasteur_6'] * 6 + \
                     player_state['pasteur_8'] * 8
        current_livestock = player_state['sheep'] + player_state['boar'] + player_state['cow']

        # Determine available slots after accounting for current livestock
        available_slot = total_slot - current_livestock

        print(f'Total slots are {total_slot}')
        print(f'Current livestocls are {current_livestock}')
        print(f'Current available slots are {available_slot}')

        if available_slot > 0:
            for livestock in priority_order:
                if acquired_livestock[livestock] > 0:
                    if available_slot > acquired_livestock[livestock]:
                        # Add the livestock to player's resource
                        player_state[livestock] += acquired_livestock[livestock]
                        available_slot -= acquired_livestock[livestock]
                        acquired_livestock[livestock] = 0
                    else:
                        # Add the livestock to player's resource
                        player_state[livestock] += available_slot

                        self.reserve_resource[livestock] += acquired_livestock[livestock] - available_slot
                        acquired_livestock[livestock] = 0

                        available_slot = 0

                    if available_slot == 0:
                        break

            # No available slots, return unassigned livestock to reserved resource
            for livestock in priority_order:
                self.reserve_resource[livestock] += acquired_livestock[livestock]

        else:
            # No available slots, return unassigned livestock to reserved resource
            for livestock in priority_order:
                self.reserve_resource[livestock] += acquired_livestock[livestock]

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
            # !!print('out of woods')
            pass

        if self.reserve_resource['clay'] > 0:
            # Player gain
            player_state['clay'] = player_state['clay'] + 1
            # Deduct from global resources
            self.reserve_resource['clay'] = self.reserve_resource['clay'] - 1
        else:
            # !!print('out of clays')
            pass

        if self.reserve_resource['reed'] > 0:
            # Player gain
            player_state['reed'] = player_state['reed'] + 1
            # Deduct from global resources
            self.reserve_resource['reed'] = self.reserve_resource['reed'] - 1
        else:
            # !!print('out of reeds')
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
                # !!print(f'The player chose pasteur_2')

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                # !!print('you cannot afford the pasteur 2')
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
                        # !!print('you cannot afford the stable')
                        pass
                else:
                    # !!print('out of stables')
                    pass

        else:
            # !!print('out of pasteur_2')

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
                    # !!print(f'The player chose pasteur_4')

                    # Add to reserved resources
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

                else:
                    # !!print('you cannot afford the pasteur 4')
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
                            # !!print('you cannot afford the stable')
                            pass
                    else:
                        # !!print('out of stables')
                        pass

            else:
                # !!print('out of pasteur_4')

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
                        # !!print(f'The player chose pasteur_6')

                        # Add to reserved resources
                        self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                        self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                        self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                        # Deduct from global resources
                        self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

                    else:
                        # !!print('you cannot afford the pasteur 6')
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
                                # !!print('you cannot afford the stable')
                                pass
                        else:
                            # !!print('out of stables')
                            pass

                else:
                    # !!print('out of pasteur_6')

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
                            # !!print(f'The player chose pasteur_8')

                            # Add to reserved resources
                            self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                            self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                            self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                            # Deduct from global resources
                            self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

                        else:
                            # !!print('you cannot afford the pasteur 8')
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
                                    # !!print('you cannot afford the stable')
                                    pass
                            else:
                                # !!print('out of stables')
                                pass

                    else:
                        # !!print('out of pasteur_8')
                        pass

    def action_b_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        # !!print(f'The player chose pasteur_2')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
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
            # !!print('out stables')
            pass

    def action_b_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        # !!print(f'The player chose pasteur_4')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
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
            # !!print('out stables')
            pass

    def action_b_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        # !!print(f'The player chose pasteur_6')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
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
            # !!print('out stables')
            pass

    def action_b_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_b_1', 'action_b_2', 'action_b_3', 'action_b_4', 'action_b_a'])

        # !!print(f'The player chose pasteur_8')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
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
            # !!print('out stables')
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
            # !!print('out of stables')
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
                # !!print(f'The player chose pasteur_2')

                # Add to reserved resources
                self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_2["price"][0]
                self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_2["price"][1]
                self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_2["price"][2]

                # Deduct from global resources
                self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1
                self.tiles['field'] = self.tiles['field'] - 1

            else:
                # !!print('you cannot afford the pasteur 2')
                pass

        else:
            # !!print('out of pasteur_2')

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
                    # !!print(f'The player chose pasteur_4')

                    # Add to reserved resources
                    self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_4["price"][0]
                    self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_4["price"][1]
                    self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles['pasteur_4'] = self.tiles['pasteur_4'] - 1

                else:
                    # !!print('you cannot afford the pasteur 4')
                    pass

            else:
                # !!print('out of pasteur_4')

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
                        # !!print(f'The player chose pasteur_6')

                        # Add to reserved resources
                        self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_6["price"][0]
                        self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_6["price"][1]
                        self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_6["price"][2]

                        # Deduct from global resources
                        self.tiles['pasteur_6'] = self.tiles['pasteur_6'] - 1

                    else:
                        # !!print('you cannot afford the pasteur 6')
                        pass

                else:
                    # !!print('out of pasteur_6')

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
                            # !!print(f'The player chose pasteur_8')

                            # Add to reserved resources
                            self.reserve_resource['clay'] = self.reserve_resource['clay'] + self.pasteur_8["price"][0]
                            self.reserve_resource['reed'] = self.reserve_resource['reed'] + self.pasteur_8["price"][1]
                            self.reserve_resource['wood'] = self.reserve_resource['wood'] + self.pasteur_8["price"][2]

                            # Deduct from global resources
                            self.tiles['pasteur_8'] = self.tiles['pasteur_8'] - 1

                        else:
                            # !!print('you cannot afford the pasteur 8')
                            pass

                    else:
                        # !!print('out of pasteur_8')
                        pass

    def action_c_1(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        # !!print(f'The player chose pasteur_2')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
            pass

    def action_c_2(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        # !!print(f'The player chose pasteur_4')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
            pass

    def action_c_3(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        # !!print(f'The player chose pasteur_6')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
            pass

    def action_c_4(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_c_1', 'action_c_2', 'action_c_3', 'action_c_4'])

        # !!print(f'The player chose pasteur_8')

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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print('out of tiles')
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
            self.tiles['pasteur_2'] = self.tiles['pasteur_2'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            # !!print('out of fields')
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
            # !!print('Not enough grains')
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
                # !!print('plow a field first')
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
            # !!print('out of grains')
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
            # !!print('out of foods')
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
            # !!print(f"The player chose {chosen_improvement}")

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
            # !!print('out of improvements')
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
                    # !!print('you cannot afford it')
                    pass

            else:
                # !!print('out of rooms')
                pass

        else:
            # !!print('player has already coverted to clay, cannot take this action')
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
            # !!print('out of stables')
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
            # !!print('out of stables')
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

                else:
                    # !!print('you cannot afford it')
                    pass
            else:
                # !!print('out of rooms')
                pass
        else:
            # !!print('player has already coverted to clay, cannot take this action')
            pass

        if self.tiles['stable'] > 0:
            # Player gain
            player_state['stable'] = player_state['stable'] + 1
            # Deduct from global resources
            self.tiles['stable'] = self.tiles['stable'] - 1
        else:
            # !!print('out of stables')
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
                    # !!print('you cannot afford it')
                    pass

            else:
                # !!print('out of rooms')
                pass
        else:
            # !!print('convert to clay first before take this action')
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
            # !!print('out of stables')
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
            # !!print('out of stables')
            pass

    def action_5(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_5'])

        if player_state['farmer'] < 5:
            if (player_state['room_space'] + player_state['clay_room'] + player_state['wood_room']) > player_state[
                'farmer']:
                player_state['farmer'] = player_state['farmer'] + 1
            else:
                # !!print('not enough rooms')
                pass
        else:
            # !!print('no more farmers')
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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print(f'improvement_7 is not available')
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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print(f'improvement_9 is not available')
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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print(f'improvement_10 is not available')
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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print(f'improvement_11 is not available')
            pass

    def action_12(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_12'])

        if player_state['farmer'] < 5:
            player_state['farmer'] = player_state['farmer'] + 1
        else:
            # !!print('no more farmers')
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
            # !!print('out of fields')
            pass

        if player_state['grain'] < 1:
            # !!print('Not enough grains')
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
                # !!print('plow a field first')
                break

    def action_13_b(self, player_state, player_field_dict, player_improvements):
        # Remove this action from the current round
        self.remove_actions(['action_13', 'action_13_b'])

        if player_state['grain'] < 1:
            # !!print('Not enough grains')
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
                            # !!print('plow more fields')
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
                    # !!print('plow a field first')
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
                            # !!print('plow more fields')
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
                    # !!print('plow a field first')
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
                # !!print('you cannot afford it')
                pass

        else:
            # !!print(f'improvement_14 is not available')
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

    def use_improvement_to_feed(self, player_state, missing_foods, player_improvements):
        print('111')
        print(player_improvements)
        # Assumption: only use 1 improvement
        if len(player_improvements) < 1:
            return missing_foods

        usable_improvements = self.find_positive_resource_food(player_improvements)

        if not usable_improvements:
            return missing_foods

        x = random.choice(usable_improvements)

        # Assuming `improvement` is a dictionary already
        improvement = next((imp for imp in player_improvements if imp['name'] == x), None)

        if improvement is None:
            return missing_foods

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
                        if acquired_food - missing_foods >= 0:
                            player_state['food'] += acquired_food - missing_foods
                            self.reserve_resource['food'] -= acquired_food - missing_foods
                            y = i
                            break
                        y = i

                    # Ensure we don't take more than available
                    y = min(y, player_state[res1], player_state[res2])

                    # Take the used resources from player's inventory
                    player_state[res1] -= y
                    player_state[res2] -= y

                    self.reserve_resource[res1] += y
                    self.reserve_resource[res2] += y

            else:
                res, key = resource
                if improvement['resource_food'].get(key, 0) > 0:
                    max_possible_use = player_state[res]
                    y = 0
                    for i in range(1, max_possible_use + 1):
                        acquired_food = i * improvement['resource_food'][key]
                        if acquired_food - missing_foods >= 0:
                            player_state['food'] += acquired_food - missing_foods
                            self.reserve_resource['food'] -= acquired_food - missing_foods
                            y = i
                            break
                        y = i

                    # Ensure we don't take more than available
                    y = min(y, player_state[res])

                    player_state[res] -= y
                    self.reserve_resource[res] += y

        print(f'Use improvement to feed for {acquired_food} foods')

        missing_foods -= acquired_food

        return missing_foods

    def use_grain_to_feed(self, player_state, missing_foods):
        print('222')
        if player_state['grain'] < 1:
            # !!print('Not enough grains')
            return missing_foods

        # Amount of grain to be used
        grains_to_use = min(player_state['grain'], missing_foods)

        if grains_to_use == 0:
            return missing_foods

        # !!print(f"{grains_to_use} grain was used to feed")
        player_state['grain'] -= grains_to_use
        missing_foods -= grains_to_use

        # Return resource to reserved
        self.reserve_resource['grain'] += grains_to_use

        print(f'Use grains to feed for {grains_to_use} foods')

        return missing_foods

    def use_livestock_to_feed(self, player_state, missing_foods, player_improvements):
        print('333')
        # TODO Assumption: prioritize the use of livestock for food in this order: cow, boar, sheep
        if len(player_improvements) < 1:
            return missing_foods

        usable_improvements = self.find_positive_livestock_food(player_improvements)

        if len(usable_improvements) < 1:
            # !!print('No appropriate improvement found!')
            return missing_foods

        x = random.choice(usable_improvements)

        # Assuming `improvement` is a dictionary already
        improvement = next((imp for imp in player_improvements if imp['name'] == x), None)

        if improvement is None:
            return missing_foods

        # TODO trade animals for foods in this order: cow, boar then sheep
        acquired_food = 0
        used_cows = 0
        used_boars = 0
        used_sheeps = 0

        while player_state['cow'] > 0:
            acquired_food = improvement['livestock_food']['cow_food']
            player_state['cow'] -= 1
            self.reserve_resource['cow'] += 1
            used_cows += 1
            missing_foods -= acquired_food
            if missing_foods <= 0:
                player_state['food'] += -missing_foods
                self.reserve_resource['food'] -= -missing_foods
                print(f'{used_sheeps} sheeps, {used_boars} boars, and {used_cows} cows were used for foods.')
                return missing_foods

        while player_state['boar'] > 0:
            acquired_food = improvement['livestock_food']['boar_food']
            player_state['boar'] -= 1
            self.reserve_resource['boar'] += 1
            used_boars += 1
            missing_foods -= acquired_food
            if missing_foods <= 0:
                player_state['food'] += -missing_foods
                self.reserve_resource['food'] -= -missing_foods
                print(f'{used_sheeps} sheeps, {used_boars} boars, and {used_cows} cows were used for foods.')
                return missing_foods

        while player_state['sheep'] > 0:
            acquired_food = improvement['livestock_food']['sheep_food']
            player_state['sheep'] -= 1
            self.reserve_resource['sheep'] += 1
            used_sheeps += 1
            missing_foods -= acquired_food
            if missing_foods <= 0:
                player_state['food'] += -missing_foods
                self.reserve_resource['food'] -= -missing_foods
                print(f'{used_sheeps} sheeps, {used_boars} boars, and {used_cows} cows were used for foods.')
                return missing_foods

        print(f'{used_sheeps} sheeps, {used_boars} boars, and {used_cows} cows were used for foods.')

        return missing_foods

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

        # Added used food to global resources
        if player_missing_foods < 0:
            self.reserve_resource['food'] += player_required_foods
        else:
            self.reserve_resource['food'] += player_state['food']

        # Deduct food from player's state
        player_state['food'] = max(0, player_state['food'] - player_required_foods)

        # Not enough foods, players have to use either grains or livestocks to feed
        if player_missing_foods > 0:

            #   Feed the farmers using improvements
            player_missing_foods = self.use_improvement_to_feed(player_state, player_missing_foods,
                                                                player_improvements)

            if player_missing_foods > 0:
                #   Feed the farmers using livestock
                player_missing_foods = self.use_livestock_to_feed(player_state, player_missing_foods,
                                                                  player_improvements)

                if player_missing_foods > 0:
                    #   Feed the farmers using grains
                    player_missing_foods = self.use_grain_to_feed(player_state, player_missing_foods)

                    if player_missing_foods > 0:
                        #   Still not enough foods, get begging tokens
                        player_state['begging'] += player_missing_foods
                        print('999')

        ## Offsprings
        # Assigning offsprings
        if player_state['sheep'] > 2 and self.reserve_resource['sheep'] > 0:
            sheep_offspring = 1
            self.reserve_resource['sheep'] -= 1
        else:
            sheep_offspring = 0

        if player_state['boar'] > 2 and self.reserve_resource['boar'] > 0:
            boar_offspring = 1
            self.reserve_resource['boar'] -= 1
        else:
            boar_offspring = 0

        if player_state['cow'] > 2 and self.reserve_resource['cow'] > 0:
            cow_offspring = 1
            self.reserve_resource['cow'] -= 1
        else:
            cow_offspring = 0

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

    # def calculate_reward(self, parameter):
    #
    #     # Example reward logic
    #     # print(f'Previous {parameter}: {self.previous_parameter}')
    #     # print(f'Current {parameter}: {self.player1_state[parameter]}')
    #
    #     reward = (self.player1_state[parameter] - self.previous_parameter) * 5
    #     self.previous_parameter = self.player1_state[parameter]
    #
    #     return reward

    def calculate_reward(self, previous_state):
        # Calculate the basic reward
        reward = 0
        reward += self.valid_action_reward(self.player1_state, previous_state)
        reward += self.resource_reward(self.player1_state, previous_state)
        reward += self.development_reward(self.player1_state, previous_state)
        reward += self.wood_room_reward(self.player1_state, previous_state)
        reward += self.clay_room_reward(self.player1_state, previous_state)
        reward += self.animal_reward(self.player1_state, previous_state)
        reward += self.food_reward(self.player1_state, previous_state)
        reward += self.family_reward(self.player1_state, previous_state)
        reward += self.feeding_penalty(self.player1_state, previous_state) * 10
        reward += self.calculate_high_level_reward() * 40

        return reward

    def calculate_high_level_reward(self):
        high_level_reward = 0

        # Resource milestone: Collect 20 of each resource
        if not self.milestones['resource_goal']:
            resources_collected = all(
                self.player1_state[resource] >= 10 for resource in ['wood', 'clay', 'reed', 'food'])
            if resources_collected:
                high_level_reward += 50
                self.milestones['resource_goal'] = True

        # Room milestone: Build 5 rooms
        if not self.milestones['room_goal']:
            if self.player1_state['room_space'] >= 2:
                high_level_reward += 50
                self.milestones['room_goal'] = True

        # Family milestone: Have 4 family members
        if not self.milestones['family_goal']:
            if self.player1_state['farmer'] >= 3:
                high_level_reward += 50
                self.milestones['family_goal'] = True

        print(f'Resource reward = {high_level_reward}')

        return high_level_reward

    def resource_reward(self, state, previous_state):
        resource_reward = 0
        resources = ['wood', 'clay', 'reed', 'food']
        for resource in resources:
            resource_reward += (state[resource] - previous_state[resource])

        if resource_reward < 0:
            resource_reward = 0

        print(f'Resource reward = {resource_reward}')
        return resource_reward

    def development_reward(self, state, previous_state):
        development_reward = 0
        development_reward += (state['room_space'] - previous_state['room_space']) * 10
        development_reward += (state['field'] - previous_state['field']) * 5
        development_reward += (state['pasteur_2'] - previous_state['pasteur_2']) * 5
        development_reward += (state['pasteur_4'] - previous_state['pasteur_4']) * 5
        development_reward += (state['pasteur_6'] - previous_state['pasteur_6']) * 5
        development_reward += (state['pasteur_8'] - previous_state['pasteur_8']) * 5

        print(f'Development reward = {development_reward}')
        return development_reward

    def animal_reward(self, state, previous_state):
        animal_reward = 0
        animals = ['sheep', 'boar', 'cow']
        for animal in animals:
            animal_reward += state[animal] - previous_state[animal]

        if animal_reward < 0:
            animal_reward = 0

        print(f'Animal reward = {animal_reward}')
        return animal_reward

    def valid_action_reward(self, state, previous_state):
        valid_action_reward = state['valid_action'] - previous_state['valid_action']
        print(f'Valid action reward = {valid_action_reward}')
        return valid_action_reward

    def family_reward(self, state, previous_state):
        family_reward = state['farmer'] - previous_state['farmer']
        print(f'Family reward = {family_reward}')
        return family_reward

    def wood_room_reward(self, state, previous_state):
        wood_room_reward = state['wood_room'] - previous_state['wood_room']
        print(f'Wood room reward = {wood_room_reward}')
        return wood_room_reward

    def clay_room_reward(self, state, previous_state):
        clay_room_reward = state['clay_room'] - previous_state['clay_room']
        print(f'clay room reward = {clay_room_reward}')
        return clay_room_reward

    def food_reward(self, state, previous_state):
        food_reward = state['food'] - previous_state['food']

        if food_reward < 0:
            food_reward = 0

        print(f'Food reward = {food_reward}')
        return food_reward

    def feeding_penalty(self, state, previous_state):
        feeding_penalty = (state['begging'] - previous_state['begging']) * (-1)
        print(f'Feeding penalty = {feeding_penalty}')
        return feeding_penalty

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

        order_list = [1, 2, 3, 4]
        # Randomize the order of elements in the list
        random.shuffle(order_list)
        self.order_list = order_list

        self.player_order = [f'player{self.order_list[0]}', f'player{self.order_list[1]}',
                             f'player{self.order_list[2]}', f'player{self.order_list[3]}']

        self.player_order_numeric = [self.order_list[0], self.order_list[1],
                                     self.order_list[2], self.order_list[3]]

    def resrouce_check(self):
        if self.board_resource['2_clay'] + self.board_resource['1_clay'] + self.reserve_resource['clay'] + \
                self.player1_state['clay'] + self.player2_state['clay'] + self.player3_state['clay'] + \
                self.player4_state['clay'] != 30:
            sys.exit("Wrong total of clay exists")
        if self.board_resource['reed'] + self.reserve_resource['reed'] + self.player1_state['reed'] + \
                self.player2_state['reed'] + self.player3_state['reed'] + self.player4_state['reed'] != 20:
            sys.exit("Wrong total of reed exists")
        if self.board_resource['1_wood'] + self.board_resource['2_wood'] + self.board_resource['3_wood'] + \
                self.reserve_resource['wood'] + self.player1_state['wood'] + self.player2_state['wood'] + \
                self.player3_state['wood'] + self.player4_state['wood'] != 40:
            sys.exit("Wrong total of wood exists")
        if self.reserve_resource['grain'] + self.player1_state['grain'] + self.player2_state['grain'] + \
                self.player3_state['grain'] + self.player4_state['grain'] + sum(self.player1_field_dict.values()) + sum(
            self.player2_field_dict.values()) + sum(self.player3_field_dict.values()) + sum(
            self.player4_field_dict.values()) != 31:
            print(self.reserve_resource['grain'])
            print(self.player1_state['grain'])
            print(self.player2_state['grain'])
            print(self.player3_state['grain'])
            print(self.player4_state['grain'])
            sys.exit("Wrong total of grain exists")
        if self.board_resource['food'] + self.reserve_resource['food'] + self.player1_state['food'] + \
                self.player2_state['food'] + self.player3_state['food'] + self.player4_state['food'] != 80:
            print(self.board_resource['food'])
            print(self.reserve_resource['food'])
            print(self.player1_state['food'])
            print(self.player2_state['food'])
            print(self.player3_state['food'])
            print(self.player4_state['food'])
            sys.exit("Wrong total of food exists")
        if self.board_resource['sheep'] + self.reserve_resource['sheep'] + self.player1_state['sheep'] + \
                self.player2_state['sheep'] + self.player3_state['sheep'] + self.player4_state['sheep'] != 26:
            print(self.board_resource['sheep'])
            print(self.reserve_resource['sheep'])
            print(self.player1_state['sheep'])
            print(self.player2_state['sheep'])
            print(self.player3_state['sheep'])
            print(self.player4_state['sheep'])
            sys.exit("Wrong total of sheep exists")
        if self.board_resource['boar'] + self.reserve_resource['boar'] + self.player1_state['boar'] + \
                self.player2_state['boar'] + self.player3_state['boar'] + self.player4_state['boar'] != 19:
            print(self.board_resource['boar'])
            print(self.reserve_resource['boar'])
            print(self.player1_state['boar'])
            print(self.player2_state['boar'])
            print(self.player3_state['boar'])
            print(self.player4_state['boar'])
            sys.exit("Wrong total of boar exists")
        if self.board_resource['cow'] + self.reserve_resource['cow'] + self.player1_state['cow'] + self.player2_state[
            'cow'] + self.player3_state['cow'] + self.player4_state['cow'] != 17:
            print(self.board_resource['cow'])
            print(self.reserve_resource['cow'])
            print(self.player1_state['cow'])
            print(self.player2_state['cow'])
            print(self.player3_state['cow'])
            print(self.player4_state['cow'])
            sys.exit("Wrong total of cow exists")
        # if self.tiles['pasteur_2'] + self.player1_state['pasteur_2'] + self.player2_state['pasteur_2'] + self.player3_state['pasteur_2'] + self.player4_state['pasteur_2'] + self.tiles['field'] + self.player1_state['field'] + self.player2_state['field'] + self.player3_state['field'] + self.player4_state['field'] != 20:
        #     sys.exit("Wrong total of pasteur_2/field exists")
        if self.tiles['pasteur_4'] + self.player1_state['pasteur_4'] + self.player2_state['pasteur_4'] + \
                self.player3_state['pasteur_4'] + self.player4_state['pasteur_4'] != 13:
            sys.exit("Wrong total of pasteur_4 exists")
        if self.tiles['pasteur_6'] + self.player1_state['pasteur_6'] + self.player2_state['pasteur_6'] + \
                self.player3_state['pasteur_6'] + self.player4_state['pasteur_6'] != 2:
            sys.exit("Wrong total of pasteur_6 exists")
        if self.tiles['pasteur_8'] + self.player1_state['pasteur_8'] + self.player2_state['pasteur_8'] + \
                self.player3_state['pasteur_8'] + self.player4_state['pasteur_8'] != 1:
            sys.exit("Wrong total of pasteur_8 exists")
        if self.tiles['stable'] + self.player1_state['stable'] + self.player2_state['stable'] + self.player3_state[
            'stable'] + self.player4_state['stable'] != 10:
            sys.exit("Wrong total of stable exists")
        if self.tiles['room'] + self.player1_state['wood_room'] + self.player2_state['wood_room'] + self.player3_state[
            'wood_room'] + self.player4_state['wood_room'] + self.player1_state['clay_room'] + self.player2_state[
            'clay_room'] + self.player3_state['clay_room'] + self.player4_state['clay_room'] != 12:
            sys.exit("Wrong total of room exists")

    def update_resource_history(self, resource_history, round, resource_name, player_state):
        """
        Updates the resource history for a specific resource with rounds nested inside for a single player.

        Parameters:
        resource_history (defaultdict(dict)): Dictionary to store the resource history for a single player.
        resource_name (str): Name of the resource to track (e.g., 'clay').
        round (int): Current round.
        player_state (dict): The player's state dictionary which contains resource values.

        Returns:
        None: Updates the resource_history dictionary in place.
        """
        # Get the resource value from the player's state
        resource_value = player_state.get(resource_name, 0)

        # Ensure the resource key exists in the dictionary
        if resource_name not in resource_history:
            resource_history[resource_name] = defaultdict(list)

        # Append the resource value to the round in the nested dictionary
        resource_history[resource_name][round].append(resource_value)

    def step_training(self, agent_action):
        print('=====================================================================================================')
        print(f'Round {self.round}')

        self.player1_state['round'] = self.round
        self.player2_state['round'] = self.round
        self.player3_state['round'] = self.round
        self.player4_state['round'] = self.round
        self.board_resource['round'] = self.round

        print('Here are reserve resources')
        print(self.reserve_resource)
        print('Here are board resources')
        print(self.board_resource)

        # Players take actions
        if self.remain_actions > 0:
            for order in self.player_order:

                # Player 1 take action
                # #!!print('Actions:')
                # #!!print(self.moves)
                if order == 'player1':
                    print('===== PLAYER 1 =====')
                    if self.player1_number_actions != 0:
                        # print(f"There are {self.board_resource['cow']} cows on board")

                        # Check if action is valid
                        if self.moves_check[self.moves_total_names[agent_action]] == 1:
                            # !!print('-----------------------PLAYER 1-----------------------')
                            # !!print(f'action index is {action[action_index]}')
                            # !!print(f'length of action list is {len(self.moves)}')

                            # !!print('States BEFORE actions')
                            # !!print(self.player1_state)

                            # print(len(self.moves))
                            # print(self.obs[-29:].tolist())
                            # print(action)

                            self.player1_state['valid_action'] = self.player1_state['valid_action'] + 1

                            self.player1_action = self.moves_total[
                                agent_action]  # player 1 takes action from the training agent
                            # print(f"Player 1's action: {self.moves_total[agent_action]}")
                            self.player1_state['action'] = agent_action
                            print(f"player 1 take action {self.player1_action}")

                            print('States BEFORE actions')
                            print(self.player1_state)
                            self.player1_action(self.player1_state, self.player1_field_dict, self.player1_improvements)
                            print('States AFTER actions')
                            print(self.player1_state)

                            self.action_used.append(self.moves_total_names[agent_action])
                            total_action_used.append(self.moves_total_names[agent_action])
                            agent_action_used.append(self.moves_total_names[agent_action])

                            if self.round == 1:
                                agent_action_round_1.append(self.moves_total_names[agent_action])
                            if self.round == 2:
                                agent_action_round_2.append(self.moves_total_names[agent_action])
                            if self.round == 3:
                                agent_action_round_3.append(self.moves_total_names[agent_action])
                            if self.round == 4:
                                agent_action_round_4.append(self.moves_total_names[agent_action])
                            if self.round == 5:
                                agent_action_round_5.append(self.moves_total_names[agent_action])
                            if self.round == 6:
                                agent_action_round_6.append(self.moves_total_names[agent_action])
                            if self.round == 7:
                                agent_action_round_7.append(self.moves_total_names[agent_action])
                            if self.round == 8:
                                agent_action_round_8.append(self.moves_total_names[agent_action])
                            if self.round == 9:
                                agent_action_round_9.append(self.moves_total_names[agent_action])
                            if self.round == 10:
                                agent_action_round_10.append(self.moves_total_names[agent_action])
                            if self.round == 11:
                                agent_action_round_11.append(self.moves_total_names[agent_action])
                            if self.round == 12:
                                agent_action_round_12.append(self.moves_total_names[agent_action])
                            if self.round == 13:
                                agent_action_round_13.append(self.moves_total_names[agent_action])
                            if self.round == 14:
                                agent_action_round_14.append(self.moves_total_names[agent_action])

                        if self.moves_check[self.moves_total_names[agent_action]] == 0:
                            print("Player 1's action: INVALID")

                            print('States AFTER actions')
                            print(self.player1_state)

                            self.action_used.append('INVALID')
                            total_action_used.append('INVALID')
                            agent_action_used.append('INVALID')

                            if self.round == 1:
                                agent_action_round_1.append('INVALID')
                            if self.round == 2:
                                agent_action_round_2.append('INVALID')
                            if self.round == 3:
                                agent_action_round_3.append('INVALID')
                            if self.round == 4:
                                agent_action_round_4.append('INVALID')
                            if self.round == 5:
                                agent_action_round_5.append('INVALID')
                            if self.round == 6:
                                agent_action_round_6.append('INVALID')
                            if self.round == 7:
                                agent_action_round_7.append('INVALID')
                            if self.round == 8:
                                agent_action_round_8.append('INVALID')
                            if self.round == 9:
                                agent_action_round_9.append('INVALID')
                            if self.round == 10:
                                agent_action_round_10.append('INVALID')
                            if self.round == 11:
                                agent_action_round_11.append('INVALID')
                            if self.round == 12:
                                agent_action_round_12.append('INVALID')
                            if self.round == 13:
                                agent_action_round_13.append('INVALID')
                            if self.round == 14:
                                agent_action_round_14.append('INVALID')

                        self.player1_number_actions -= 1

                        # Check valid number of resources
                        self.resrouce_check()

                        # print(f"Player 1 has {self.player1_state['cow']} cows")

                    if self.round in (4, 7, 9, 11, 13, 14) and self.player1_number_actions == 0 and \
                            self.player_1_harvesting_check[self.round] == 1:
                        # Harvesting:
                        # !!print('=====================================================================================================')
                        print('----------player 1 - harvesting----------')
                        print('States BEFORE harvesting')
                        print(self.player1_state)
                        self.harvesting(self.player1_state, self.player1_field_dict, self.player1_improvements)
                        print('States AFTER harvesting')
                        print(self.player1_state)
                        print('Here are reserve resources')
                        print(self.reserve_resource)
                        print('Here are board resources')
                        print(self.board_resource)
                        print('Here are tile resources')
                        print(self.tiles)

                        # Check valid number of resources
                        self.resrouce_check()

                        self.player_1_harvesting_check[self.round] = 0

                    # Calculate round reward
                    self.reward = self.calculate_reward(self.player1_previous_state)

                # Update previous state for future reward calculation
                self.player1_previous_state = copy.deepcopy(self.player1_state)

                # Player 2 take action
                if order == 'player2':
                    print('===== PLAYER 2 =====')
                    if self.player2_number_actions != 0:
                        # agent get action suggested by model
                        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
                        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
                                                     self.player4_state,
                                                     self.board_resource, self.reserve_resource, self.tiles,
                                                     self.moves_check)

                        # player2_action, _states = self.partner_model.predict(self.obs, deterministic=True)
                        player2_action = random.randrange(len(self.moves))

                        # Check if action is valid
                        if self.moves_check[self.moves_total_names[player2_action]] == 1:
                            # !!print('-----------------------PLAYER 1-----------------------')
                            # !!print(f'action index is {action[action_index]}')
                            # !!print(f'length of action list is {len(self.moves)}')

                            print('States BEFORE actions')
                            print(self.player2_state)

                            # print(len(self.moves))
                            # print(self.obs[-29:].tolist())
                            # print(action)

                            self.player2_action = self.moves_total[
                                player2_action]  # player 1 takes action from the training agent
                            # print(f"Player 2's action: {self.moves_total[player2_action]}")
                            self.player2_state['action'] = player2_action
                            print(f"player 2 take action {self.player2_action}")

                            self.player2_action(self.player2_state, self.player2_field_dict, self.player2_improvements)
                            print('States AFTER actions')
                            print(self.player2_state)
                            # #!!print(len(self.moves))

                            self.action_used.append(self.moves_total_names[player2_action])
                            total_action_used.append(self.moves_total_names[player2_action])
                            partner_action_used.append(self.moves_total_names[player2_action])

                            if self.round == 1:
                                partner_action_round_1.append(self.moves_total_names[player2_action])
                            if self.round == 2:
                                partner_action_round_2.append(self.moves_total_names[player2_action])
                            if self.round == 3:
                                partner_action_round_3.append(self.moves_total_names[player2_action])
                            if self.round == 4:
                                partner_action_round_4.append(self.moves_total_names[player2_action])
                            if self.round == 5:
                                partner_action_round_5.append(self.moves_total_names[player2_action])
                            if self.round == 6:
                                partner_action_round_6.append(self.moves_total_names[player2_action])
                            if self.round == 7:
                                partner_action_round_7.append(self.moves_total_names[player2_action])
                            if self.round == 8:
                                partner_action_round_8.append(self.moves_total_names[player2_action])
                            if self.round == 9:
                                partner_action_round_9.append(self.moves_total_names[player2_action])
                            if self.round == 10:
                                partner_action_round_10.append(self.moves_total_names[player2_action])
                            if self.round == 11:
                                partner_action_round_11.append(self.moves_total_names[player2_action])
                            if self.round == 12:
                                partner_action_round_12.append(self.moves_total_names[player2_action])
                            if self.round == 13:
                                partner_action_round_13.append(self.moves_total_names[player2_action])
                            if self.round == 14:
                                partner_action_round_14.append(self.moves_total_names[player2_action])

                        if self.moves_check[self.moves_total_names[player2_action]] == 0:
                            print("Player 2's action: INVALID")

                            self.action_used.append('INVALID')
                            total_action_used.append('INVALID')
                            partner_action_used.append('INVALID')

                            if self.round == 1:
                                partner_action_round_1.append('INVALID')
                            if self.round == 2:
                                partner_action_round_2.append('INVALID')
                            if self.round == 3:
                                partner_action_round_3.append('INVALID')
                            if self.round == 4:
                                partner_action_round_4.append('INVALID')
                            if self.round == 5:
                                partner_action_round_5.append('INVALID')
                            if self.round == 6:
                                partner_action_round_6.append('INVALID')
                            if self.round == 7:
                                partner_action_round_7.append('INVALID')
                            if self.round == 8:
                                partner_action_round_8.append('INVALID')
                            if self.round == 9:
                                partner_action_round_9.append('INVALID')
                            if self.round == 10:
                                partner_action_round_10.append('INVALID')
                            if self.round == 11:
                                partner_action_round_11.append('INVALID')
                            if self.round == 12:
                                partner_action_round_12.append('INVALID')
                            if self.round == 13:
                                partner_action_round_13.append('INVALID')
                            if self.round == 14:
                                partner_action_round_14.append('INVALID')

                        self.player2_number_actions -= 1

                        # Check valid number of resources
                        self.resrouce_check()

                    if self.round in (4, 7, 9, 11, 13, 14) and self.player2_number_actions == 0 and \
                            self.player_2_harvesting_check[self.round] == 1:
                        # Harvesting:
                        print('----------player 2 - harvesting----------')
                        print('States BEFORE harvesting')
                        print(self.player2_state)
                        self.harvesting(self.player2_state, self.player2_field_dict, self.player2_improvements)
                        print('States AFTER harvesting')
                        print(self.player2_state)
                        print('Here are reserve resources')
                        print(self.reserve_resource)
                        print('Here are board resources')
                        print(self.board_resource)
                        print('Here are tile resources')
                        print(self.tiles)

                        # Check valid number of resources
                        self.resrouce_check()

                        self.player_2_harvesting_check[self.round] = 0

                # Player 3 take action
                if order == 'player3':
                    print('===== PLAYER 3 =====')
                    if self.player3_number_actions != 0:
                        # agent get action suggested by model
                        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
                        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
                                                     self.player4_state,
                                                     self.board_resource, self.reserve_resource, self.tiles,
                                                     self.moves_check)
                        # player3_action, _states = self.partner_model.predict(self.obs, deterministic=True)
                        player3_action = random.randrange(len(self.moves))

                        # Check if action is valid
                        if self.moves_check[self.moves_total_names[player3_action]] == 1:
                            # !!print('-----------------------PLAYER 1-----------------------')
                            # !!print(f'action index is {action[action_index]}')
                            # !!print(f'length of action list is {len(self.moves)}')

                            print('States BEFORE actions')
                            print(self.player3_state)

                            # print(len(self.moves))
                            # print(self.obs[-29:].tolist())
                            # print(action)

                            self.player3_action = self.moves_total[
                                player3_action]  # player 1 takes action from the training agent
                            # print(f"Player 3's action: {self.moves_total[player3_action]}")
                            self.player3_state['action'] = player3_action
                            print(f"player 3 take action {self.player3_action}")

                            self.player3_action(self.player3_state, self.player3_field_dict, self.player3_improvements)
                            print('States AFTER actions')
                            print(self.player3_state)
                            # #!!print(len(self.moves))

                            self.action_used.append(self.moves_total_names[player3_action])
                            total_action_used.append(self.moves_total_names[player3_action])
                            partner_action_used.append(self.moves_total_names[player3_action])

                            if self.round == 1:
                                partner_action_round_1.append(self.moves_total_names[player3_action])
                            if self.round == 2:
                                partner_action_round_2.append(self.moves_total_names[player3_action])
                            if self.round == 3:
                                partner_action_round_3.append(self.moves_total_names[player3_action])
                            if self.round == 4:
                                partner_action_round_4.append(self.moves_total_names[player3_action])
                            if self.round == 5:
                                partner_action_round_5.append(self.moves_total_names[player3_action])
                            if self.round == 6:
                                partner_action_round_6.append(self.moves_total_names[player3_action])
                            if self.round == 7:
                                partner_action_round_7.append(self.moves_total_names[player3_action])
                            if self.round == 8:
                                partner_action_round_8.append(self.moves_total_names[player3_action])
                            if self.round == 9:
                                partner_action_round_9.append(self.moves_total_names[player3_action])
                            if self.round == 10:
                                partner_action_round_10.append(self.moves_total_names[player3_action])
                            if self.round == 11:
                                partner_action_round_11.append(self.moves_total_names[player3_action])
                            if self.round == 12:
                                partner_action_round_12.append(self.moves_total_names[player3_action])
                            if self.round == 13:
                                partner_action_round_13.append(self.moves_total_names[player3_action])
                            if self.round == 14:
                                partner_action_round_14.append(self.moves_total_names[player3_action])

                        if self.moves_check[self.moves_total_names[player3_action]] == 0:
                            print("Player 3's action: INVALID")

                            self.action_used.append('INVALID')
                            total_action_used.append('INVALID')
                            partner_action_used.append('INVALID')

                            if self.round == 1:
                                partner_action_round_1.append('INVALID')
                            if self.round == 2:
                                partner_action_round_2.append('INVALID')
                            if self.round == 3:
                                partner_action_round_3.append('INVALID')
                            if self.round == 4:
                                partner_action_round_4.append('INVALID')
                            if self.round == 5:
                                partner_action_round_5.append('INVALID')
                            if self.round == 6:
                                partner_action_round_6.append('INVALID')
                            if self.round == 7:
                                partner_action_round_7.append('INVALID')
                            if self.round == 8:
                                partner_action_round_8.append('INVALID')
                            if self.round == 9:
                                partner_action_round_9.append('INVALID')
                            if self.round == 10:
                                partner_action_round_10.append('INVALID')
                            if self.round == 11:
                                partner_action_round_11.append('INVALID')
                            if self.round == 12:
                                partner_action_round_12.append('INVALID')
                            if self.round == 13:
                                partner_action_round_13.append('INVALID')
                            if self.round == 14:
                                partner_action_round_14.append('INVALID')

                        self.player3_number_actions -= 1

                        # Check valid number of resources
                        self.resrouce_check()

                    if self.round in (4, 7, 9, 11, 13, 14) and self.player3_number_actions == 0 and \
                            self.player_3_harvesting_check[self.round] == 1:
                        # Harvesting:
                        print('----------player 3 - harvesting----------')
                        print('States BEFORE harvesting')
                        print(self.player3_state)
                        self.harvesting(self.player3_state, self.player3_field_dict, self.player3_improvements)
                        print('States AFTER harvesting')
                        print(self.player3_state)
                        print('Here are reserve resources')
                        print(self.reserve_resource)
                        print('Here are board resources')
                        print(self.board_resource)
                        print('Here are tile resources')
                        print(self.tiles)

                        # Check valid number of resources
                        self.resrouce_check()

                        self.player_3_harvesting_check[self.round] = 0

                # Player 4 take action
                if order == 'player4':
                    print('===== PLAYER 4 =====')
                    if self.player4_number_actions != 0:
                        # agent get action suggested by model
                        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
                        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
                                                     self.player4_state,
                                                     self.board_resource, self.reserve_resource, self.tiles,
                                                     self.moves_check)
                        # player4_action, _states = self.partner_model.predict(self.obs, deterministic=True)
                        player4_action = random.randrange(len(self.moves))

                        # Check if action is valid
                        if self.moves_check[self.moves_total_names[player4_action]] == 1:
                            # !!print('-----------------------PLAYER 1-----------------------')
                            # !!print(f'action index is {action[action_index]}')
                            # !!print(f'length of action list is {len(self.moves)}')

                            print('States BEFORE actions')
                            print(self.player4_state)

                            # print(len(self.moves))
                            # print(self.obs[-29:].tolist())
                            # print(action)

                            self.player4_action = self.moves_total[
                                player4_action]  # player 1 takes action from the training agent
                            # print(f"Player 4's action: {self.moves_total[player4_action]}")
                            self.player4_state['action'] = player4_action
                            print(f"player 4 take action {self.player4_action}")

                            self.player4_action(self.player4_state, self.player4_field_dict, self.player4_improvements)
                            print('States AFTER actions')
                            print(self.player4_state)
                            # #!!print(len(self.moves))

                            self.action_used.append(self.moves_total_names[player4_action])
                            total_action_used.append(self.moves_total_names[player4_action])
                            partner_action_used.append(self.moves_total_names[player4_action])

                            if self.round == 1:
                                partner_action_round_1.append(self.moves_total_names[player4_action])
                            if self.round == 2:
                                partner_action_round_2.append(self.moves_total_names[player4_action])
                            if self.round == 3:
                                partner_action_round_3.append(self.moves_total_names[player4_action])
                            if self.round == 4:
                                partner_action_round_4.append(self.moves_total_names[player4_action])
                            if self.round == 5:
                                partner_action_round_5.append(self.moves_total_names[player4_action])
                            if self.round == 6:
                                partner_action_round_6.append(self.moves_total_names[player4_action])
                            if self.round == 7:
                                partner_action_round_7.append(self.moves_total_names[player4_action])
                            if self.round == 8:
                                partner_action_round_8.append(self.moves_total_names[player4_action])
                            if self.round == 9:
                                partner_action_round_9.append(self.moves_total_names[player4_action])
                            if self.round == 10:
                                partner_action_round_10.append(self.moves_total_names[player4_action])
                            if self.round == 11:
                                partner_action_round_11.append(self.moves_total_names[player4_action])
                            if self.round == 12:
                                partner_action_round_12.append(self.moves_total_names[player4_action])
                            if self.round == 13:
                                partner_action_round_13.append(self.moves_total_names[player4_action])
                            if self.round == 14:
                                partner_action_round_14.append(self.moves_total_names[player4_action])

                        if self.moves_check[self.moves_total_names[player4_action]] == 0:
                            print("Player 4's action: INVALID")

                            self.action_used.append('INVALID')
                            total_action_used.append('INVALID')
                            partner_action_used.append('INVALID')

                            if self.round == 1:
                                partner_action_round_1.append('INVALID')
                            if self.round == 2:
                                partner_action_round_2.append('INVALID')
                            if self.round == 3:
                                partner_action_round_3.append('INVALID')
                            if self.round == 4:
                                partner_action_round_4.append('INVALID')
                            if self.round == 5:
                                partner_action_round_5.append('INVALID')
                            if self.round == 6:
                                partner_action_round_6.append('INVALID')
                            if self.round == 7:
                                partner_action_round_7.append('INVALID')
                            if self.round == 8:
                                partner_action_round_8.append('INVALID')
                            if self.round == 9:
                                partner_action_round_9.append('INVALID')
                            if self.round == 10:
                                partner_action_round_10.append('INVALID')
                            if self.round == 11:
                                partner_action_round_11.append('INVALID')
                            if self.round == 12:
                                partner_action_round_12.append('INVALID')
                            if self.round == 13:
                                partner_action_round_13.append('INVALID')
                            if self.round == 14:
                                partner_action_round_14.append('INVALID')

                        self.player4_number_actions -= 1

                        # Check valid number of resources
                        self.resrouce_check()

                    if self.round in (4, 7, 9, 11, 13, 14) and self.player4_number_actions == 0 and \
                            self.player_4_harvesting_check[self.round] == 1:
                        # Harvesting:
                        print('----------player 4 - harvesting----------')
                        print('States BEFORE harvesting')
                        print(self.player4_state)
                        self.harvesting(self.player4_state, self.player4_field_dict, self.player4_improvements)
                        print('States AFTER harvesting')
                        print(self.player4_state)
                        print('Here are reserve resources')
                        print(self.reserve_resource)
                        print('Here are board resources')
                        print(self.board_resource)
                        print('Here are tile resources')
                        print(self.tiles)

                        # Check valid number of resources
                        self.resrouce_check()

                        self.player_4_harvesting_check[self.round] = 0

            self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

            if self.remain_actions == 0:
                # Round points calculate
                self.player1_state['point'] = self.point_cal(self.player1_state)
                self.player2_state['point'] = self.point_cal(self.player2_state)
                self.player3_state['point'] = self.point_cal(self.player3_state)
                self.player4_state['point'] = self.point_cal(self.player4_state)

                # !!print('------------------------------------------------------')
                # !!print('States AFTER HARVESTING')
                # !!print(self.player1_state)
                # !!print(self.player2_state)
                # !!print(self.player3_state)
                # !!print(self.player4_state)

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
                    self.board_resource['sheep'] += 1
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

                self.round += 1

                # Reset actions list for new round
                self.new_round_action_set()

                print('Here are reserve resources')
                print(self.reserve_resource)
                print('Here are board resources')
                print(self.board_resource)
                print('Here are tile resources')
                print(self.tiles)

                # Check valid number of resources
                self.resrouce_check()

        self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
        self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state,
                                     self.board_resource, self.reserve_resource, self.tiles, self.moves_check)

        # Check if any resource values are negative
        self.check_negative_resource(self.obs)

        info = [self.moves, self.player_order_numeric, self.player1_number_actions, self.player2_number_actions,
                self.player3_number_actions, self.player4_number_actions]

        print('Here are reserve resources')
        print(self.reserve_resource)
        print('Here are board resources')
        print(self.board_resource)

        self.update_resource_history(resource_player1, self.round, 'clay', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'reed', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'wood', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'grain', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'food', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'sheep', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'boar', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'cow', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'begging', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'rooster', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'clay_room', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'wood_room', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'farmer', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'field', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'pasteur_2', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'pasteur_4', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'pasteur_6', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'pasteur_8', self.player1_state)
        self.update_resource_history(resource_player1, self.round, 'stable', self.player1_state)

        self.update_resource_history(resource_player2, self.round, 'clay', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'reed', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'wood', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'grain', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'food', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'sheep', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'boar', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'cow', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'begging', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'rooster', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'clay_room', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'wood_room', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'farmer', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'field', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'pasteur_2', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'pasteur_4', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'pasteur_6', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'pasteur_8', self.player2_state)
        self.update_resource_history(resource_player2, self.round, 'stable', self.player2_state)

        self.update_resource_history(resource_player3, self.round, 'clay', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'reed', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'wood', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'grain', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'food', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'sheep', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'boar', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'cow', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'begging', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'rooster', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'clay_room', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'wood_room', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'farmer', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'field', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'pasteur_2', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'pasteur_4', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'pasteur_6', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'pasteur_8', self.player3_state)
        self.update_resource_history(resource_player3, self.round, 'stable', self.player3_state)

        self.update_resource_history(resource_player4, self.round, 'clay', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'reed', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'wood', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'grain', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'food', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'sheep', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'boar', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'cow', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'begging', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'rooster', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'clay_room', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'wood_room', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'farmer', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'field', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'pasteur_2', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'pasteur_4', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'pasteur_6', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'pasteur_8', self.player4_state)
        self.update_resource_history(resource_player4, self.round, 'stable', self.player4_state)

        # Check if the game is done
        if self.round > 14:
            final_points_player1.append(self.player1_state['point'])
            final_points_player2.append(self.player2_state['point'])
            final_points_player3.append(self.player3_state['point'])
            final_points_player4.append(self.player4_state['point'])

            for improvement in self.player1_improvements:
                improvement_player1.append(improvement['name'])
            for improvement in self.player2_improvements:
                improvement_player2.append(improvement['name'])
            for improvement in self.player3_improvements:
                improvement_player3.append(improvement['name'])
            for improvement in self.player4_improvements:
                improvement_player4.append(improvement['name'])

            self.done = True

        return self.obs, self.reward, self.done, info

    ### Gameplay
    # def step(self):
    #     sys.exit()
    #
    #     print('=====================================================================================================')
    #     print(f'Round {self.round}')
    #
    #     self.resrouce_check()
    #
    #     self.player1_state['round'] = self.round
    #     self.player2_state['round'] = self.round
    #     self.player3_state['round'] = self.round
    #     self.player4_state['round'] = self.round
    #     self.board_resource['round'] = self.round
    #
    #     # !!print('Here are board resources')
    #     # !!print(self.board_resource)
    #
    #     # Players take actions
    #     if self.remain_actions > 0:
    #         for order in self.player_order:
    #
    #             # Player 1 take action
    #             # #!!print('Actions:')
    #             # #!!print(self.moves)
    #             if order == 'player1':
    #                 if self.player1_number_actions != 0:
    #                     # agent get action suggested by model
    #                     self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
    #                     self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
    #                                                  self.player4_state,
    #                                                  self.board_resource, self.reserve_resource, self.tiles,
    #                                                  self.moves_check)
    #
    #                     action, _states = self.agent_model.predict(self.obs, deterministic=True)
    #
    #                     # Check if action is valid
    #                     if self.moves_check[self.moves_total_names[action]] == 1:
    #                         # !!print('-----------------------PLAYER 1-----------------------')
    #                         # !!print(f'action index is {action[action_index]}')
    #                         # !!print(f'length of action list is {len(self.moves)}')
    #
    #                         # !!print('States BEFORE actions')
    #                         # !!print(self.player1_state)
    #
    #                         # print(len(self.moves))
    #                         # print(self.obs[-29:].tolist())
    #                         # print(action)
    #
    #                         self.player1_action = self.moves_total[
    #                             action]  # player 1 takes action from the training agent
    #                         print(self.moves_total[action])
    #                         self.player1_state['action'] = action
    #                         # !!print(f"player 1 take action {self.player1_action}")
    #
    #                         self.player1_action(self.player1_state, self.player1_field_dict, self.player1_improvements)
    #                         # !!print('States AFTER actions')
    #                         # !!print(self.player1_state)
    #                         # #!!print(len(self.moves))
    #
    #                         self.action_used.append(self.moves_total_names[action])
    #                         self.agent_action_used.append(self.moves_total_names[action])
    #
    #                     if self.moves_check[self.moves_total_names[action]] == 0:
    #                         print('INVALID ACTION')
    #
    #                         self.action_used.append('INVALID')
    #                         self.agent_action_used.append('INVALID')
    #
    #                     self.player1_number_actions -= 1
    #
    #                     # print(f"Player 1 has {self.player1_state['cow']} cows")
    #
    #             # Calculate round reward based on specific parameter
    #             # self.reward = self.calculate_reward(self.player1_previous_state)
    #
    #             # Player 2 take action
    #             if order == 'player2':
    #                 if self.player2_number_actions != 0:
    #                     # agent get action suggested by model
    #                     self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
    #                     self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
    #                                                  self.player4_state,
    #                                                  self.board_resource, self.reserve_resource, self.tiles,
    #                                                  self.moves_check)
    #
    #                     action, _states = self.partner_model.predict(self.obs, deterministic=True)
    #
    #                     # Check if action is valid
    #                     if self.moves_check[self.moves_total_names[action]] == 1:
    #                         # !!print('-----------------------PLAYER 1-----------------------')
    #                         # !!print(f'action index is {action[action_index]}')
    #                         # !!print(f'length of action list is {len(self.moves)}')
    #
    #                         # !!print('States BEFORE actions')
    #                         # !!print(self.player2_state)
    #
    #                         # print(len(self.moves))
    #                         # print(self.obs[-29:].tolist())
    #                         # print(action)
    #
    #                         self.player2_action = self.moves_total[
    #                             action]  # player 1 takes action from the training agent
    #                         print(self.moves_total[action])
    #                         self.player2_state['action'] = action
    #                         # !!print(f"player 1 take action {self.player2_action}")
    #
    #                         self.player2_action(self.player2_state, self.player2_field_dict, self.player2_improvements)
    #                         # !!print('States AFTER actions')
    #                         # !!print(self.player2_state)
    #                         # #!!print(len(self.moves))
    #
    #                         self.action_used.append(self.moves_total_names[action])
    #                         self.partner_action_used.append(self.moves_total_names[action])
    #
    #                     if self.moves_check[self.moves_total_names[action]] == 0:
    #                         self.action_used.append('INVALID')
    #                         self.partner_action_used.append('INVALID')
    #
    #                     self.player2_number_actions -= 1
    #
    #             # Player 3 take action
    #             if order == 'player3':
    #                 if self.player3_number_actions != 0:
    #                     # agent get action suggested by model
    #                     self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
    #                     self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
    #                                                  self.player4_state,
    #                                                  self.board_resource, self.reserve_resource, self.tiles,
    #                                                  self.moves_check)
    #                     action, _states = self.partner_model.predict(self.obs, deterministic=True)
    #
    #                     # Check if action is valid
    #                     if self.moves_check[self.moves_total_names[action]] == 1:
    #                         # !!print('-----------------------PLAYER 1-----------------------')
    #                         # !!print(f'action index is {action[action_index]}')
    #                         # !!print(f'length of action list is {len(self.moves)}')
    #
    #                         # !!print('States BEFORE actions')
    #                         # !!print(self.player3_state)
    #
    #                         # print(len(self.moves))
    #                         # print(self.obs[-29:].tolist())
    #                         # print(action)
    #
    #                         self.player3_action = self.moves_total[
    #                             action]  # player 1 takes action from the training agent
    #                         print(self.moves_total[action])
    #                         self.player3_state['action'] = action
    #                         # !!print(f"player 1 take action {self.player3_action}")
    #
    #                         self.player3_action(self.player3_state, self.player3_field_dict, self.player3_improvements)
    #                         # !!print('States AFTER actions')
    #                         # !!print(self.player3_state)
    #                         # #!!print(len(self.moves))
    #
    #                         self.action_used.append(self.moves_total_names[action])
    #                         self.partner_action_used.append(self.moves_total_names[action])
    #
    #                     if self.moves_check[self.moves_total_names[action]] == 0:
    #                         self.action_used.append('INVALID')
    #                         self.partner_action_used.append('INVALID')
    #
    #                     self.player3_number_actions -= 1
    #
    #             # Player 4 take action
    #             if order == 'player4':
    #                 if self.player4_number_actions != 0:
    #                     # agent get action suggested by model
    #                     self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
    #                     self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state,
    #                                                  self.player4_state,
    #                                                  self.board_resource, self.reserve_resource, self.tiles,
    #                                                  self.moves_check)
    #                     action, _states = self.partner_model.predict(self.obs, deterministic=True)
    #
    #                     # Check if action is valid
    #                     if self.moves_check[self.moves_total_names[action]] == 1:
    #                         # !!print('-----------------------PLAYER 1-----------------------')
    #                         # !!print(f'action index is {action[action_index]}')
    #                         # !!print(f'length of action list is {len(self.moves)}')
    #
    #                         # !!print('States BEFORE actions')
    #                         # !!print(self.player4_state)
    #
    #                         # print(len(self.moves))
    #                         # print(self.obs[-29:].tolist())
    #                         # print(action)
    #
    #                         self.player4_action = self.moves_total[
    #                             action]  # player 1 takes action from the training agent
    #                         print(self.moves_total[action])
    #                         self.player4_state['action'] = action
    #                         # !!print(f"player 1 take action {self.player4_action}")
    #
    #                         self.player4_action(self.player4_state, self.player4_field_dict, self.player4_improvements)
    #                         # !!print('States AFTER actions')
    #                         # !!print(self.player4_state)
    #                         # #!!print(len(self.moves))
    #
    #                         self.action_used.append(self.moves_total_names[action])
    #                         self.partner_action_used.append(self.moves_total_names[action])
    #
    #                     if self.moves_check[self.moves_total_names[action]] == 0:
    #                         self.action_used.append('INVALID')
    #                         self.partner_action_used.append('INVALID')
    #
    #                     self.player4_number_actions -= 1
    #
    #         self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions
    #
    #     if self.remain_actions == 0:
    #         # Harvesting:
    #         # !!print('=====================================================================================================')
    #         # !!print('player 1 - harvesting')
    #         self.harvesting(self.player1_state, self.player1_field_dict, self.player1_improvements)
    #         # !!print('------------------------------------------------------')
    #         # !!print('player 2 - harvesting')
    #         self.harvesting(self.player2_state, self.player2_field_dict, self.player2_improvements)
    #         # !!print('------------------------------------------------------')
    #         # !!print('player 3 - harvesting')
    #         self.harvesting(self.player3_state, self.player3_field_dict, self.player3_improvements)
    #         # !!print('------------------------------------------------------')
    #         # !!print('player 4 - harvesting')
    #         self.harvesting(self.player4_state, self.player4_field_dict, self.player4_improvements)
    #
    #         # Round points calculate
    #         self.player1_state['point'] = self.point_cal(self.player1_state)
    #         self.player2_state['point'] = self.point_cal(self.player2_state)
    #         self.player3_state['point'] = self.point_cal(self.player3_state)
    #         self.player4_state['point'] = self.point_cal(self.player4_state)
    #
    #         # !!print('------------------------------------------------------')
    #         # !!print('States AFTER HARVESTING')
    #         # !!print(self.player1_state)
    #         # !!print(self.player2_state)
    #         # !!print(self.player3_state)
    #         # !!print(self.player4_state)
    #
    #         # Refill board resources after each round
    #         if self.reserve_resource['clay'] >= 2:
    #             self.board_resource['2_clay'] = self.board_resource['2_clay'] + 2
    #             self.reserve_resource['clay'] -= 2
    #         else:
    #             self.board_resource['2_clay'] = self.board_resource['2_clay'] + self.reserve_resource['clay']
    #             self.reserve_resource['clay'] = 0
    #
    #         if self.reserve_resource['clay'] >= 1:
    #             self.board_resource['1_clay'] = self.board_resource['1_clay'] + 1
    #             self.reserve_resource['clay'] -= 1
    #         else:
    #             self.board_resource['1_clay'] = self.board_resource['1_clay'] + self.reserve_resource['clay']
    #             self.reserve_resource['clay'] = 0
    #
    #         if self.reserve_resource['reed'] >= 1:
    #             self.board_resource['reed'] = self.board_resource['reed'] + 1
    #             self.reserve_resource['reed'] -= 1
    #         else:
    #             self.board_resource['reed'] = self.board_resource['reed'] + self.reserve_resource['reed']
    #             self.reserve_resource['reed'] = 0
    #
    #         if self.reserve_resource['wood'] >= 1:
    #             self.board_resource['1_wood'] = self.board_resource['1_wood'] + 1
    #             self.reserve_resource['wood'] -= 1
    #         else:
    #             self.board_resource['1_wood'] = self.board_resource['1_wood'] + self.reserve_resource['wood']
    #             self.reserve_resource['wood'] = 0
    #
    #         if self.reserve_resource['wood'] >= 2:
    #             self.board_resource['2_wood'] = self.board_resource['2_wood'] + 2
    #             self.reserve_resource['wood'] -= 2
    #         else:
    #             self.board_resource['2_wood'] = self.board_resource['2_wood'] + self.reserve_resource['wood']
    #             self.reserve_resource['wood'] = 0
    #
    #         if self.reserve_resource['wood'] >= 3:
    #             self.board_resource['3_wood'] = self.board_resource['3_wood'] + 3
    #             self.reserve_resource['wood'] -= 3
    #         else:
    #             self.board_resource['3_wood'] = self.board_resource['3_wood'] + self.reserve_resource['wood']
    #             self.reserve_resource['wood'] = 0
    #
    #         if self.reserve_resource['food'] >= 1:
    #             self.board_resource['food'] = self.board_resource['food'] + 1
    #             self.reserve_resource['food'] -= 1
    #         else:
    #             self.board_resource['food'] = self.board_resource['food'] + self.reserve_resource['food']
    #             self.reserve_resource['food'] = 0
    #
    #         if self.reserve_resource['sheep'] >= 1:
    #             self.board_resource['sheep'] = self.board_resource['sheep'] + 1
    #             self.reserve_resource['sheep'] -= 1
    #         else:
    #             self.board_resource['sheep'] = self.board_resource['sheep'] + self.reserve_resource['sheep']
    #             self.reserve_resource['sheep'] = 0
    #
    #         if self.round >= 5:
    #             if self.reserve_resource['boar'] >= 1:
    #                 self.board_resource['boar'] = self.board_resource['boar'] + 1
    #                 self.reserve_resource['boar'] -= 1
    #             else:
    #                 self.board_resource['boar'] = self.board_resource['boar'] + self.reserve_resource['boar']
    #                 self.reserve_resource['boar'] = 0
    #
    #         if self.round >= 7:
    #             if self.reserve_resource['cow'] >= 1:
    #                 self.board_resource['cow'] = self.board_resource['cow'] + 1
    #                 self.reserve_resource['cow'] -= 1
    #             else:
    #                 self.board_resource['cow'] = self.board_resource['cow'] + self.reserve_resource['cow']
    #                 self.reserve_resource['cow'] = 0
    #
    #         # Determine player order for NEXT round
    #         self.determine_order(self.player1_state, self.player2_state, self.player3_state, self.player4_state)
    #
    #         # self.player1_state['invalid_action'] = 0
    #
    #         self.round += 1
    #
    #         # Reset actions list for new round
    #         self.new_round_action_set()
    #
    #     self.moves_check = self.generate_moves_check_dict(self.moves, self.moves_total)
    #     self.obs = self.generate_obs(self.player1_state, self.player2_state, self.player3_state, self.player4_state,
    #                                  self.board_resource, self.reserve_resource, self.tiles, self.moves_check)
    #
    #     # Check if any resource values are negative
    #     self.check_negative_resource(self.obs)
    #
    #     info = [self.moves, self.player_order_numeric, self.player1_number_actions, self.player2_number_actions,
    #             self.player3_number_actions, self.player4_number_actions]
    #
    #     # Check if the game is done
    #     if self.round > 14:
    #         self.done = True
    #
    #     return self.obs, self.reward, self.done, info


# TODO: randomimze number of pasteur to take for action c, right now the players only take 1 pasteur
# TODO: harvesting: feeding/begging, field work, offsprings/assigning or converting offsprings to foods.
# TODO: offspring after each harvest and players have to assign livestocks right away
# TODO: when take/offspring livestock and not enough space, choose to keep one and discard another or use stoves to convert to foods
# TODO: make sure to shuffle field list before action_g
# TODO: make sure update field list after action_d
# TODO: calculating points after round 14
# TODO: converting discarded livestock to food if the player has improvements (after every livestock assignment)

# ======================================================================================================================
class AgricolaEnv(gym.Env):
    def __init__(self, partner_model=None):
        self.partner_model = partner_model
        super(AgricolaEnv, self).__init__()
        self.game = AgricolaAI(partner_model=self.partner_model)

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
        obs, reward, done, info = self.game.step_training(action)

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
    plt.close()


def chart_occurrences(actions_list, name, save_path):
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
    plt.title(f"{name}")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Create the save path directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Save the chart as an image file with the specified path
    file_name = os.path.join(save_path, f"{name}")
    plt.savefig(file_name)  # Save as PNG file

    plt.close()


def chart_occurrences_with_levels(actions_list, moves_total_levels, name, save_path):
    # Define a color mapping for each level using a colormap
    unique_levels = set(moves_total_levels.values())
    color_map = {level: plt.cm.Set3(i / len(unique_levels)) for i, level in enumerate(unique_levels)}

    # Count occurrences of each action
    occurrences = Counter(actions_list)

    # Sort actions by their occurrences
    sorted_actions = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

    # Split the sorted actions into two lists: actions and counts
    actions, counts = zip(*sorted_actions)

    # Create a list of colors for the bars based on action levels
    bar_colors = [color_map[moves_total_levels.get(action, "default")] for action in actions]

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(actions, counts, color=bar_colors)
    plt.xlabel('Actions')
    plt.ylabel('Occurrences')
    plt.title(f"{name}")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Create a legend for the action levels
    legend_labels = {level: color_map[level] for level in unique_levels}
    legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_labels.values()]
    plt.legend(legend_handles, [f'Level {lvl}' for lvl in legend_labels.keys()], title="Action Levels")

    # Create the save path directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Save the chart as an image file with the specified path
    file_name = os.path.join(save_path, f"{name}.png")
    plt.savefig(file_name)  # Save as PNG file

    # Close the figure to free memory
    plt.close()


def count_action_levels(moves_total_levels, moves_total_names):
    # Initialize a dictionary to count occurrences for each level
    level_counts = defaultdict(int)

    # Count occurrences of each action's level
    for action in moves_total_names:
        level = moves_total_levels.get(action, None)  # Get level of the action
        if level is not None:
            level_counts[level] += 1  # Increment count for that level

    return dict(level_counts)  # Convert to regular dict for cleaner output


def plot_level_occurrences(level_occurrences, name, save_path):
    levels = list(level_occurrences.keys())
    occurrences = list(level_occurrences.values())

    plt.figure(figsize=(8, 6))
    plt.bar(levels, occurrences)
    plt.xlabel("Action Level")
    plt.ylabel("Occurrences")
    plt.title(f"{name}")
    plt.xticks(levels)  # Set x-ticks to show each level

    # Save the chart as an image file with the specified path
    file_name = os.path.join(save_path, f"{name}")
    plt.savefig(file_name)  # Save as PNG file

    plt.close()


def plot_points_trend(*players_points, name, save_path):
    rounds = range(1, len(players_points[0]) + 1)  # Assuming each list has the same length

    plt.figure(figsize=(10, 6))

    for i, points in enumerate(players_points, start=1):
        plt.plot(rounds, points, label=f"Player {i}", marker='o')

    # Add labels and title
    plt.xlabel("Rounds")
    plt.ylabel("Average Points")
    plt.title("Players' Points Over Training Rounds")
    plt.legend()

    file_name = os.path.join(save_path, f"{name}_Points Over Training Rounds")
    plt.savefig(file_name)  # Save as PNG file

    plt.close()


def plot_average_resource_over_rounds(resource_histories, resource_name, name, save_path):
    plt.figure(figsize=(10, 6))

    # Loop through each player's resource history
    for player, history in resource_histories.items():
        rounds = sorted(history.get(resource_name, {}).keys())  # Get all the rounds for the resource
        averages = [sum(history[resource_name][rnd]) / len(history[resource_name][rnd]) for rnd in
                    rounds]  # Compute averages

        # Plot the player's average resource values over the rounds
        plt.plot(rounds, averages, marker='o', label=player)

    # Add labels and title
    plt.xlabel('Rounds')
    plt.ylabel(f'Average {resource_name.capitalize()}')
    plt.title(f'Average {resource_name.capitalize()} Over Rounds')
    plt.legend(title="Players")
    plt.grid(True)

    file_name = os.path.join(save_path, f"{name}_{resource_name.capitalize()} Over Training Rounds")
    plt.savefig(file_name)  # Save as PNG file

    plt.close()


def plot_improvement_occurrences(player_lists, name, save_path):
    # Count occurrences of each improvement for each player
    counters = [Counter(player) for player in player_lists]

    # List of all unique improvements across all players
    all_improvements = sorted(set([imp for player in player_lists for imp in player]))

    # Prepare data for plotting
    improvement_counts = [
        [counter.get(imp, 0) for imp in all_improvements]
        for counter in counters
    ]

    # Number of players
    num_players = len(player_lists)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.8 / num_players  # Adjust bar width based on the number of players

    # Positions for bars
    x = range(len(all_improvements))

    # Plot bars for each player
    for i in range(num_players):
        ax.bar([p + (i - num_players / 2) * width for p in x],
               improvement_counts[i], width=width, label=f'Player {i + 1}')

    # Labeling
    ax.set_xlabel('Improvements')
    ax.set_ylabel('Occurrences')
    ax.set_title('Occurrences of Each Improvement by Player')
    ax.set_xticks(x)
    ax.set_xticklabels(all_improvements)
    ax.legend()

    plt.tight_layout()

    file_name = os.path.join(save_path, f"{name}_Occurrences of Each Improvement by Player")
    plt.savefig(file_name)  # Save as PNG file

    plt.close()


def plot_action_occurrences_per_round(*agent_actions, player=None, name, save_path):
    rounds = len(agent_actions)

    for i, actions in enumerate(agent_actions):
        # Count the occurrences of each action in the current round
        counter = Counter(actions)
        sorted_counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

        keys = list(sorted_counter.keys())
        values = list(sorted_counter.values())

        # Create a new figure for each round
        plt.figure(figsize=(8, 6))
        plt.bar(keys, values)
        plt.title(f'{name}_{player}_Occurrences of Each Action_Round {i + 1}')
        plt.xlabel('Action')
        plt.ylabel('Occurrences')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Adjust layout to prevent labels from overlapping
        plt.tight_layout()

        file_name = os.path.join(save_path, f"{name}_{player}_Occurrences of Each Action_Round {i + 1}")
        plt.savefig(file_name)  # Save as PNG file

        plt.close()


def plot_action_occurrences_per_round_colored(
        moves_total_levels, *agent_actions, player=None, name, save_path):
    # Define a color mapping for each level using a colormap
    unique_levels = set(moves_total_levels.values())
    color_map = {level: plt.cm.Set3(i / len(unique_levels)) for i, level in enumerate(unique_levels)}

    for i, actions in enumerate(agent_actions):
        if len(actions) == 0:
            continue  # Skip if a round has no data

        # Count the occurrences of each action in the current round
        counter = Counter(actions)
        sorted_counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

        keys = list(sorted_counter.keys())
        values = list(sorted_counter.values())

        # Create a color list for the bars based on action levels
        bar_colors = [color_map[moves_total_levels.get(action, "default")] for action in keys]

        # Create a new figure for each round
        plt.figure(figsize=(8, 6))
        bars = plt.bar(keys, values, color=bar_colors)
        plt.title(f'{name}_{player}_Occurrences of Each Action_Round {i + 1}')
        plt.xlabel('Action')
        plt.ylabel('Occurrences')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Create a legend for the action levels
        legend_labels = {level: color_map[level] for level in unique_levels}
        legend_handles = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_labels.values()]
        plt.legend(legend_handles, [f'Level {lvl}' for lvl in legend_labels.keys()], title="Action Levels")

        # Adjust layout to prevent labels from overlapping
        plt.tight_layout()

        # Save the chart as a PNG file
        file_name = os.path.join(save_path, f"{name}_{player}_Occurrences_Round_{i + 1}.png")
        plt.savefig(file_name)

        # Close the figure to free memory
        plt.close()


def run_single_game(game, parameters_to_show):
    states = {player: {resource: [] for resource in game.player1_state} for player in range(1, 5)}
    points = {player: [] for player in range(1, 5)}

    while not game.done:
        obs, reward, done, _ = game.step()

        for player, state in enumerate([game.player1_state, game.player2_state, game.player3_state, game.player4_state],
                                       start=1):
            for resource, value in state.items():
                if resource in parameters_to_show:
                    states[player][resource].append(value)

    # Store points at the end of the game
    for i in range(1, 5):
        points[i].append(getattr(game, f'player_{i}_points'))

    return states, points, game.action_used, game.agent_action_used, game.partner_action_used


def run_multiple_iterations(num_iterations, parameters_to_show, agent_model_name, partner_model_name):
    all_states = []
    total_action_used = []
    total_agent_action_used = []
    total_partner_action_used = []
    all_points = {player: [] for player in range(1, 5)}

    env = AgricolaEnv()
    agent_model = PPO.load(agent_model_name, env=env)
    partner_model = PPO.load(partner_model_name, env=env)

    for _ in range(num_iterations):
        game = AgricolaAI(agent_model=agent_model, partner_model=partner_model)
        states, points, action_used, agent_action_used, partner_action_used = run_single_game(game, parameters_to_show)
        all_states.append(states)
        for player in range(1, 5):
            all_points[player].extend(points[player])

        total_action_used.extend(action_used)
        total_agent_action_used.extend(agent_action_used)
        total_partner_action_used.extend(partner_action_used)

    chart_occurrences(total_action_used, 'total_action')
    chart_occurrences(total_agent_action_used, 'agent_action')
    chart_occurrences(total_partner_action_used, 'partner_action')

    plot_results(all_states, all_points, parameters_to_show)


# ======================================================================================================================
# TRAINING
training = True

if training == True:
    total_action_used = []
    agent_action_used = []
    partner_action_used = []
    final_points_player1 = []
    final_points_player2 = []
    final_points_player3 = []
    final_points_player4 = []
    improvement_player1 = []
    improvement_player2 = []
    improvement_player3 = []
    improvement_player4 = []

    agent_action_round_1 = []
    agent_action_round_2 = []
    agent_action_round_3 = []
    agent_action_round_4 = []
    agent_action_round_5 = []
    agent_action_round_6 = []
    agent_action_round_7 = []
    agent_action_round_8 = []
    agent_action_round_9 = []
    agent_action_round_10 = []
    agent_action_round_11 = []
    agent_action_round_12 = []
    agent_action_round_13 = []
    agent_action_round_14 = []

    partner_action_round_1 = []
    partner_action_round_2 = []
    partner_action_round_3 = []
    partner_action_round_4 = []
    partner_action_round_5 = []
    partner_action_round_6 = []
    partner_action_round_7 = []
    partner_action_round_8 = []
    partner_action_round_9 = []
    partner_action_round_10 = []
    partner_action_round_11 = []
    partner_action_round_12 = []
    partner_action_round_13 = []
    partner_action_round_14 = []

    resource_player1 = defaultdict(dict)
    resource_player2 = defaultdict(dict)
    resource_player3 = defaultdict(dict)
    resource_player4 = defaultdict(dict)

    # Training parameters
    model_name = "BASE"
    times_steps = 10000
    agent_entropy = 5.467057108921686e-05
    agent_learning_rate = 1.1571376087582738e-05
    custom_arch = [dict(pi=[64, 64, 64, 64], vf=[64, 64, 64, 64])]

    # Define a custom policy that uses the specified architecture
    class CustomActorCriticPolicy(ActorCriticPolicy):
        def __init__(self, *args, **kwargs):
            super(CustomActorCriticPolicy, self).__init__(
                *args, **kwargs,
                net_arch=custom_arch  # Apply the custom architecture
            )

    env = AgricolaEnv()
    model = PPO(
        CustomActorCriticPolicy,
        env,
        n_steps=2048,
        batch_size=64,
        gamma=0.901510767006798,
        ent_coef=agent_entropy,
        learning_rate=agent_learning_rate,
        verbose=1
    )

    model.learn(total_timesteps=times_steps)
    model.save(f"E:\\Agricola\\{model_name}")

# ======================================================================================================================
### Training procedures
# Partners' actions are RANDOM for base model

