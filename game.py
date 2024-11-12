import random
from enum import Enum
from collections import namedtuple
import numpy as np


### improvement tiles
#   improvement_2, improvement_3a (no livestocks), improvement_3b, improvement_4a (no livestocks), improvement_4b, improvement_5
#   improvement_7, improvement_9, improvement_10, improvement_11, improvement_14
#   price [clay, reed, wood]

# pasteur price[clay,reed,wood]
pasteur_2 = {'price': [0,0,3], 'capacity': 2}
pasteur_4 = {'price': [0,0,5], 'capacity': 4}
pasteur_6 = {'price': [0,0,6], 'capacity': 6}
pasteur_8 = {'price': [0,0,7], 'capacity': 8}
pasteur_list = [pasteur_2, pasteur_4, pasteur_6, pasteur_8]

# actions
# action_a    = {'price': [0,0,0], 'clay': 1, 'reed': 1, 'wood': 1, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'rooster': 0, 'clay_house': 0, 'farmer': 0, 'extra_room': 0, 'pasteur': 0, 'stable': 0, 'field': 0, 'sow': 0}
# action_b_1  = {'price': [0,0,0], 'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'rooster': 0, 'clay_house': 0, 'farmer': 0, 'extra_room': 0, 'pasteur': 1, 'stable': 0, 'field': 0, 'sow': 0}

class AgricolaAI:

    def __init__(self):
        self.reset()

    def reset(self):
        # improvement = {'price': [0,0,0], 'grain_wood_food': , 'sheep_food': , 'boar_food': , 'cow_food': , 'clay_food': , 'reed_food': , 'wood_food': , 'grain_food': , 'clay_point': , 'reed_point': , 'wood_point': , 'grain_point': , '3_random_point': }
        self.improvement_2 = {'price': [2, 0, 0], 'grain_wood_food': 2, 'sheep_food': 2, 'boar_food': 2, 'cow_food': 3,
                         'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                         'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_3a = {'price': [3, 0, 0], 'grain_wood_food': 5, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                          'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                          'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_3 = {'price': [3, 0, 0], 'grain_wood_food': 2, 'sheep_food': 2, 'boar_food': 2, 'cow_food': 3,
                         'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                         'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_4a = {'price': [4, 0, 0], 'grain_wood_food': 5, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                          'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                          'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_4 = {'price': [4, 0, 0], 'grain_wood_food': 3, 'sheep_food': 2, 'boar_food': 3, 'cow_food': 4,
                         'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                         'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_5 = {'price': [5, 0, 0], 'grain_wood_food': 3, 'sheep_food': 2, 'boar_food': 3, 'cow_food': 4,
                         'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                         'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_7 = {'price': [3, 0, 1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                         'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 3, 'clay_point': 0,
                         'reed_point': 0, 'wood_point': 0, 'grain_point': 1, '3_random_point': 0}
        self.improvement_9 = {'price': [0, 1, 2], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                         'clay_food': 0, 'reed_food': 3, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                         'reed_point': 1, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_10 = {'price': [1, 2, 0], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                          'clay_food': 2, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 1,
                          'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 0}
        self.improvement_11 = {'price': [2, 0, 1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                          'clay_food': 0, 'reed_food': 0, 'wood_food': 2, 'grain_food': 0, 'clay_point': 0,
                          'reed_point': 0, 'wood_point': 1, 'grain_point': 0, '3_random_point': 0}
        self.improvement_14 = {'price': [1, 1, 1], 'grain_wood_food': 0, 'sheep_food': 0, 'boar_food': 0, 'cow_food': 0,
                          'clay_food': 0, 'reed_food': 0, 'wood_food': 0, 'grain_food': 0, 'clay_point': 0,
                          'reed_point': 0, 'wood_point': 0, 'grain_point': 0, '3_random_point': 1}

        # init game state
        self.round = 1
        # self.moves = [self.action_a,self.action_b_1,self.action_b_2,self.action_c,self.action_d,self.action_e,self.action_f,self.action_g,self.action_h,self.action_i,self.action_j,self.action_k,self.action_l,self.action_m,self.action_n,self.action_o]
        # initial game resouces
        self.board_resouce   = {'2_clay': 2, '1_clay': 1, 'reed': 1, '1_wood': 1, '2_wood': 2, '3_wood': 3, 'food': 1, 'sheep': 1, 'boar': 0, 'cow': 0, 'round': 1}
        self.reserve_resouce = {'clay': 27, 'reed': 19, 'wood': 34, 'grain': 31, 'food': 71, 'sheep': 25, 'boar': 19, 'cow': 17, 'begging': 5}

        self.improvements = [self.improvement_2, self.improvement_3a, self.improvement_3, self.improvement_4a, self.improvement_4, self.improvement_5]
        self.tiles = {'pasteur_2': 20, 'pasteur_4': 13, 'pasteur_6': 2, 'pasteur_8': 1, 'field': 20, 'stable': 10, 'room': 12}

        # initial player resouces
        self.player1_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
        self.player1_improvements = []
        self.player1_field_dict = {}
        self.player1_field_list = list(self.player1_field_dict.keys())

        self.player2_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
        self.player2_improvements = []
        self.player2_field_dict = {}
        self.player2_field_list = list(self.player2_field_dict.keys())

        self.player3_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
        self.player3_improvements = []
        self.player3_field_dict = {}
        self.player3_field_list = list(self.player3_field_dict.keys())

        self.player4_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
        self.player4_improvements = []
        self.player4_field_dict = {}
        self.player4_field_list = list(self.player4_field_dict.keys())


        self.player_state_list = [self.player1_state, self.player2_state, self.player3_state, self.player4_state]

    #--------------------------------------------------------------------------------------------------------------------------------------------------#
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
        # Pick a random integer between 1 and 10 (inclusive)
        stables_tobe_assigned = random.randint(0, player_state['stable'])  # randomzzz

        a = distribute_sum_stable(stables_tobe_assigned, len(player_expanded_pasteur_list))

        stable_arrays = 2 * np.array([a, a, a, ])

        return stable_arrays

    def assign_livestock(self, player_state, acquired_sheeps, acquired_boars, acquired_cows):
        pasteur_arrays = np.array([[1], [1], [1], ])

        player_pasteur_list = [player_state['pasteur_2'], player_state['pasteur_4'], player_state['pasteur_6'],
                                player_state['pasteur_8']]

        player_expanded_pasteur_list = []
        for x in range(player_pasteur_list[0]):
            player_expanded_pasteur_list.append(2)
        for x in range(player_pasteur_list[1]):
            player_expanded_pasteur_list.append(4)
        for x in range(player_pasteur_list[2]):
            player_expanded_pasteur_list.append(6)
        for x in range(player_pasteur_list[3]):
            player_expanded_pasteur_list.append(8)

        player_pasteur_capacity_arrays = np.array(player_expanded_pasteur_list)

        # Assign stables
        stable_arrays = assign_stables(player_state, player_expanded_pasteur_list)

        # Pasteurs that players have
        # [pasteur2_number, pasteur4_number, pasteur6_number, pasteur8_number]

        # Show the available spaces that players have
        player_available_space_arrays = player_pasteur_capacity_arrays * pasteur_arrays + stable_arrays
        print('Here is the available spaces')
        print(player_available_space_arrays)
        print('-------------------------------------------------------------')

        #-----------------------------------------------------------------------------------------------
        #   Player's livestocks count
        sheeps_tobe_assigned = acquired_sheeps + player_state['sheep']
        sheep_list = distribute_sum_livestocks(sheeps_tobe_assigned, len(player_expanded_pasteur_list))

        boars_tobe_assigned = acquired_boars + player_state['boar']
        boar_list = distribute_sum_livestocks(boars_tobe_assigned, len(player_expanded_pasteur_list))

        cows_tobe_assigned = acquired_cows + player_state['cow']
        cow_list = distribute_sum_livestocks(cows_tobe_assigned, len(player_expanded_pasteur_list))

        x1 = 0
        for sheep in sheep_list:
            if sheep > 0:
                x1 = x1 + sheep
        print(f'{x1} sheeps to be assigned')

        x2 = 0
        for boar in boar_list:
            if boar > 0:
                x2 = x2 + boar
        print(f'{x2} boars to be assigned')

        x3 = 0
        for cow in cow_list:
            if cow > 0:
                x3 = x3 + cow
        print(f'{x3} cows to be assigned')

        # TODO: randomize livestock priority
        # Create a list of integers representing each while loop
        loop_order = ['sheeps', 'boars', 'cows']

        # Shuffle the list to randomize the order
        random.shuffle(loop_order)

        # Iterate through the shuffled list
        no_joined_array = np.full(len(player_pasteur_capacity_arrays), 0)
        for loop_num in loop_order:
            if loop_num == 'sheeps':
                while True:
                    player_livestock_arrays = np.array([
                        sheep_list,
                        sheep_list,
                        sheep_list,
                    ])

                    original_array = player_available_space_arrays.copy()

                    # Where the player choose to put their livestocks
                    player_available_space_arrays = player_available_space_arrays - player_livestock_arrays

                    # Change all negative values of the arrays to 0
                    player_available_space_arrays[player_available_space_arrays < 0] = 0

                    player_on_hand_sheeps_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
                    no_joined_array = player_on_hand_sheeps_array.copy()
                    no_joined_array[no_joined_array != 0] = -99
                    player_on_hand_sheeps_array[player_on_hand_sheeps_array < 0] = 0


                    # print('Here is the the sheeps on hand')
                    # print(player_on_hand_sheeps_array)
                    #
                    # print('Here is the available spaces after adding the sheeps')
                    # print(player_available_space_arrays)

                    break

            if loop_num == 'boars':
                while True:
                    player_livestock_arrays = np.array([
                        boar_list,
                        boar_list,
                        boar_list,
                    ])

                    original_array = player_available_space_arrays.copy()

                    # Where the player choose to put their livestocks
                    player_available_space_arrays = player_available_space_arrays - player_livestock_arrays

                    # Change all negative values of the arrays to 0
                    player_available_space_arrays[player_available_space_arrays < 0] = 0

                    player_on_hand_boars_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
                    no_joined_array = player_on_hand_boars_array.copy()
                    no_joined_array[no_joined_array != 0] = -99
                    player_on_hand_boars_array[player_on_hand_boars_array < 0] = 0

                    # print('Here is the the boars on hand')
                    # print(player_on_hand_boars_array)
                    #
                    # print('Here is the available spaces after adding the boars')
                    # print(player_available_space_arrays)

                    break

            if loop_num == 'cows':
                while True:
                    player_livestock_arrays = np.array([
                        cow_list,
                        cow_list,
                        cow_list,
                    ])

                    original_array = player_available_space_arrays.copy()

                    # Where the player choose to put their livestocks
                    player_available_space_arrays = player_available_space_arrays - player_livestock_arrays

                    # Change all negative values of the arrays to 0
                    player_available_space_arrays[player_available_space_arrays < 0] = 0

                    player_on_hand_cows_array = original_array[0] - player_available_space_arrays[0] + no_joined_array
                    no_joined_array = player_on_hand_cows_array.copy()
                    no_joined_array[no_joined_array != 0] = -99
                    player_on_hand_cows_array[player_on_hand_cows_array < 0] = 0

                    # print('Here is the the cows on hand')
                    # print(player_on_hand_cows_array)
                    #
                    # print('Here is the available spaces after adding the cows')
                    # print(player_available_space_arrays)

                    break

        player_on_hand_livestock_arrays = np.array([
            player_on_hand_sheeps_array,
            player_on_hand_boars_array,
            player_on_hand_cows_array,
        ])

        discarded_sheeps = sheeps_tobe_assigned - sum(player_on_hand_sheeps_array)
        discarded_boars = boars_tobe_assigned - sum(player_on_hand_boars_array)
        discarded_cows = cows_tobe_assigned - sum(player_on_hand_cows_array)
        print(f'{discarded_sheeps} sheeps discarded')
        print(f'{discarded_boars} boars discarded')
        print(f'{discarded_cows} cows discarded')

        # update inventory with new livestocks arrangement
        player_state['sheep'] = sum(player_on_hand_sheeps_array)
        player_state['boar'] = sum(player_on_hand_boars_array)
        player_state['cow'] = sum(player_on_hand_cows_array)

        print('Here is all the livestocks on hand')
        print(player_on_hand_livestock_arrays)

    def action_a(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.reserve_resouce['wood'] > 0:
            # Player gain
            player_state['wood'] = player_state['wood'] + 1
            # Deduct from global resources
            self.reserve_resouce['wood'] = self.reserve_resouce['wood'] - 1
        else: print('out of woods')

        if self.reserve_resouce['clay'] > 0:
            # Player gain
            player_state['clay'] = player_state['clay'] + 1
            # Deduct from global resources
            self.reserve_resouce['clay'] = self.reserve_resouce['clay'] - 1
        else:
            print('out of clays')

        if self.reserve_resouce['reed'] > 0:
            # Player gain
            player_state['reed'] = player_state['reed'] + 1
            # Deduct from global resources
            self.reserve_resouce['reed'] = self.reserve_resouce['reed'] - 1
        else:
            print('out of reeds')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_a']

    def action_b(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resource type
        if pasteur_type == 'pasteur_2':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_2["price"][0] & player_state['reed'] >= pasteur_2["price"][1] & player_state['wood'] >= pasteur_2["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_2["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_2["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_2["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_2["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_2["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_2["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1
                    self.tiles['field'] = tiles['field'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_4':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_4["price"][0] & player_state['reed'] >= pasteur_4["price"][1] & player_state['wood'] >= pasteur_4["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_4["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_4["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_4["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_4["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_4["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_6':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_6["price"][0] & player_state['reed'] >= pasteur_6["price"][1] & player_state['wood'] >= pasteur_6["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_6["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_6["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_6["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_6["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_6["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_6["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_8':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_8["price"][0] & player_state['reed'] >= pasteur_8["price"][1] & player_state['wood'] >= pasteur_8["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_8["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_8["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_8["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_8["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_8["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_8["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')


        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('our of stables')


    def action_b_2(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('our of stables')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_b_2']

    def action_c(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resource type
        if pasteur_type == 'pasteur_2':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_2["price"][0] & player_state['reed'] >= pasteur_2["price"][1] & player_state['wood'] >= pasteur_2["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_2["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_2["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_2["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_2["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_2["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_2["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1
                    self.tiles['field'] = self.tiles['field'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_4':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_4["price"][0] & player_state['reed'] >= pasteur_4["price"][1] & player_state['wood'] >= pasteur_4["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_4["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_4["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_4["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_4["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_4["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_4["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_6':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_6["price"][0] & player_state['reed'] >= pasteur_6["price"][1] & player_state['wood'] >= pasteur_6["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_6["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_6["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_6["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_6["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_6["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_6["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        if pasteur_type == 'pasteur_8':
            # Check resouce availability
            if self.tiles[f'{pasteur_type}'] > 0:
                # Check player's payment
                if player_state['clay'] >= pasteur_8["price"][0] & player_state['reed'] >= pasteur_8["price"][1] & player_state['wood'] >= pasteur_8["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - pasteur_8["price"][0]
                    player_state['reed'] = player_state['reed'] - pasteur_8["price"][1]
                    player_state['wood'] = player_state['wood'] - pasteur_8["price"][2]
                    # Player gain
                    player_state[f'{pasteur_type}'] = player_state[f'{pasteur_type}'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + pasteur_8["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + pasteur_8["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + pasteur_8["price"][2]

                    # Deduct from global resources
                    self.tiles[f'{pasteur_type}'] = self.tiles[f'{pasteur_type}'] - 1

                else: print('you cannot afford it')

            else: print('out of tiles')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_c']

    def action_d(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                for x in range(len(player_field_dict)):
                    player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            print('out of fields')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_d']

    def action_e(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['clay'] = player_state['clay']+ self.board_resouce['2_clay']
        # Deduct from global resources
        self.board_resouce['2_clay'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_e']

    def action_f(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['clay'] = player_state['clay']+ self.board_resouce['1_clay']
        # Deduct from global resources
        self.board_resouce['1_clay'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_f']

    #TODO: randomize player_field_list order before taking action_g using random.shuffle(list)
    #TODO: randomize number of grains to be sowed, it has to be less than what the players have in their inventory
    def action_g(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        if grains <= player_state['grain']:
            y = 0
            for x in range(min(grains, len(player_field_list))):
                if len(player_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        else:
            y = 0
            for x in range(min(player_state['grain'], len(player_field_list))):
                if len(player1_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_g']

    def action_h(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.reserve_resouce['grain'] > 0:
            # Player gain
            player_state['grain'] = player_state['grain'] + 1
            # Deduct from global resources
            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 1
        else: print('out of grains')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_h']

    def action_i(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['reed'] = player_state['reed']+ self.board_resouce['reed']
        # Deduct from global resources
        self.board_resouce['reed'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_i']

    def action_j(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['wood'] = player_state['wood']+ self.board_resouce['1_wood']
        # Deduct from global resources
        self.board_resouce['1_wood'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_j']

    def action_k(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Deduct from global resources
        self.board_resouce['sheep'] = 0
        # Player gain
        player_state['sheep'] = player_state['sheep']+ self.board_resouce['sheep']

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_k']

    def action_l(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['wood'] = player_state['wood']+ self.board_resouce['2_wood']
        # Deduct from global resources
        self.board_resouce['2_wood'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_l']

    def action_m(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['wood'] = player_state['wood']+ self.board_resouce['3_wood']
        # Deduct from global resources
        self.board_resouce['3_wood'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_m']

    def action_n(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['food'] = player_state['food']+ self.board_resouce['food']
        # Deduct from global resources
        self.board_resouce['food'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_n']

    def action_o(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.reserve_resouce['food'] > 0:
            # Player gain
            player_state['food'] = player_state['food'] + 1
            # Deduct from global resources
            self.reserve_resouce['food'] = self.reserve_resouce['food'] - 1
        else: print('out of foods')

        # Take rooster from all players
        for player in self.player_state_list:
            player['rooster'] = 0

        # Give rooster to new player
        player_state['rooster'] = 1

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_o']

    def action_1(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        try:
            chosen_improvement = self.improvements[random.randint(0,len(self.improvements) - 1)]

            if chosen_improvement in self.improvements:
                # Check player's payment
                if player_state['clay'] >= chosen_improvement["price"][0] & player_state['reed'] >= \
                        chosen_improvement["price"][1] & player_state['wood'] >= chosen_improvement["price"][2]:
                    # Player pays
                    player_state['clay'] = player_state['clay'] - chosen_improvement["price"][0]
                    player_state['reed'] = player_state['reed'] - chosen_improvement["price"][1]
                    player_state['wood'] = player_state['wood'] - chosen_improvement["price"][2]

                    # Add to reserved resources
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + chosen_improvement["price"][0]
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + chosen_improvement["price"][1]
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + chosen_improvement["price"][2]

                    # Deduct from global resources
                    element_to_remove = chosen_improvement
                    self.improvements = [x for x in self.improvements if x != element_to_remove]

                    # Player gain
                    player_improvements.append(chosen_improvement)

        except:
            print('out of improvements')


        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_1']

    def action_2(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 0:

            # Check resouce availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 2 & player_state['wood'] >= 5:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 2
                    player_state['wood'] = player_state['wood'] - 5
                    # Player gain
                    player_state['wood_room'] = player_state['wood_room'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + 2
                    self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 5

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1

                else: print('you cannot afford it')

            else: print('out of rooms')

        else:
            print('player has already coverted to clay, cannot take this action')

        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('out of stables')

    def action_2_b(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('our of stables')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_2_b']

    def action_3(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 0:
            # Check resouce availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 1 & player_state['clay'] >= 3:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 1
                    player_state['clay'] = player_state['clay'] - 3
                    # Player gain
                    player_state['clay_conversion'] = 1

                    # Add to reserved resources
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + 1
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + 3

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1
                else: print('you cannot afford it')
            else: print('out of rooms')
        else:
            print('player has already coverted to clay, cannot take this action')

        if self.tiles['stable'] > 0:
            # Player gain
            player_state['stable'] = player_state['stable'] + 1
            # Deduct from global resources
            self.tiles['stable'] = self.tiles['stable'] - 1
        else: print('out of stables')


    def action_4(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check if player hasn't coverted to clay
        if player_state['clay_conversion'] == 1:
            # Check resouce availability
            if self.tiles['room'] > 0:
                # Check player's payment
                if player_state['reed'] >= 1 & player_state['clay'] >= 3:
                    # Player pays
                    player_state['reed'] = player_state['reed'] - 1
                    player_state['clay'] = player_state['clay'] - 3
                    # Player gain
                    player_state['clay_room'] = player_state['clay_room'] + 1

                    # Add to reserved resources
                    self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + 1
                    self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + 3

                    # Deduct from global resources
                    self.tiles['room'] = self.tiles['room'] - 1

                else: print('you cannot afford it')

            else: print('out of rooms')
        else:
            print('convert to clay first before take this action')

        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('our of stables')

    def action_4_b(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.tiles['stable'] > 0:
            # Check player's payment
            if player_state['wood'] >= 2:
                # Player pays
                player_state['wood'] = player_state['wood'] - 2
                # Player gain
                player_state['stable'] = player_state['stable'] + 1

                # Add to reserved resources
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + 2
                # Deduct from global resources
                self.tiles['stable'] = self.tiles['stable'] - 1

        else:
            print('our of stables')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_4_b']

    def action_5(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if player_state['farmer'] < 5:
            if player_state['room_space'] > player_state['farmer']:
                player_state['farmer'] = player_state['farmer'] + 1
            else: print('not enough rooms')
        else: print('no more farmers')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_5']

    def action_6(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['boar'] = player_state['boar']+ self.board_resouce['boar']
        # Deduct from global resources
        self.board_resouce['boar'] = 0

        #(self, player_state, acquired_sheeps, acquired_boars, acquired_cows)
        acquired_sheeps = 0
        # acquired_boars =

        self.assign_livestock(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvement)

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_6']

    def action_7(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if self.improvement_7 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_7["price"][0] & player_state['reed'] >= self.improvement_7["price"][1] & player_state['wood'] >= self.improvement_7["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_7["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_7["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_7["price"][2]

                # Add to reserved resources
                self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + self.improvement_7["price"][0]
                self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + self.improvement_7["price"][1]
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + self.improvement_7["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_7
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_7)

            else: print('you cannot afford it')

        else: print(f'improvement_7 is not available')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_7']

    def action_8(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Player gain
        player_state['cow'] = player_state['cow']+ self.board_resouce['cow']
        # Deduct from global resources
        self.board_resouce['cow'] = 0

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_8']

    def action_9(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if self.improvement_9 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_9["price"][0] & player_state['reed'] >= self.improvement_9["price"][1] & player_state['wood'] >= self.improvement_9["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_9["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_9["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_9["price"][2]

                # Add to reserved resources
                self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + self.improvement_9["price"][0]
                self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + self.improvement_9["price"][1]
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + self.improvement_9["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_9
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(improvement_9)

            else: print('you cannot afford it')

        else: print(f'improvement_9 is not available')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_9']

    def action_10(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if self.improvement_10 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_10["price"][0] & player_state['reed'] >= self.improvement_10["price"][1] & player_state['wood'] >= self.improvement_10["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_10["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_10["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_10["price"][2]

                # Add to reserved resources
                self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + self.improvement_10["price"][0]
                self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + self.improvement_10["price"][1]
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + self.improvement_10["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_10
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_10)

            else: print('you cannot afford it')

        else: print(f'improvement_10 is not available')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_10']

    def action_11(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if self.improvement_11 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_11["price"][0] & player_state['reed'] >= self.improvement_11["price"][1] & player_state['wood'] >= self.improvement_11["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_11["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_11["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_11["price"][2]

                # Add to reserved resources
                self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + self.improvement_11["price"][0]
                self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + self.improvement_11["price"][1]
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + self.improvement_11["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_11
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_11)

            else: print('you cannot afford it')

        else: print(f'improvement_11 is not available')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_11']

    def action_12(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if player_state['farmer'] < 5:
            player_state['farmer'] = player_state['farmer'] + 1
        else: print('no more farmers')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_12']

    def action_13(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Check resouce availability
        if self.tiles['field'] > 0:
            # Player gain
            player_state['field'] = player_state['field'] + 1

            # Deduct from global resources
            self.tiles['field'] = self.tiles['field'] - 1

            # Add the field to the sowing dict
            if len(player_field_dict) > 0:
                for x in range(len(player_field_dict)):
                    player_field_dict[f'field_{len(player_field_dict) + 1}'] = 0
            else:
                player_field_dict['field_1'] = 0

        else:
            print('out of fields')

        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        if grains <= player_state['grain']:
            y = 0
            for x in range(min(grains, len(player_field_list))):
                if len(player_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[
                                                                               f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[
                                                                           f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        else:
            y = 0
            for x in range(min(player_state['grain'], len(player_field_list))):
                if len(player_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[
                                                                               f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[
                                                                           f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

    def action_13_b(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        # Random number of grains to be sowed
        grains = random.randint(0, player_state['grain'])

        if grains <= player_state['grain']:
            y = 0
            for x in range(min(grains, len(player_field_list))):
                if len(player_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        else:
            y = 0
            for x in range(min(player_state['grain'], len(player_field_list))):
                if len(player_field_list) > 0:
                    # take 1 grain from player's inventory
                    player_state['grain'] = player_state['grain'] - 1
                    # check if there is enough grains in global inventory
                    if self.reserve_resouce['grain'] >= 2:
                        try:
                            # sow grains on field
                            player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 3
                            # take grain from global inventory
                            self.reserve_resouce['grain'] = self.reserve_resouce['grain'] - 2
                            y = y + 1
                        except:
                            print('plow more fields')

                    else:
                        # sow grains on field
                        player_field_dict[f'{player_field_list[y]}'] = player_field_dict[f'{player_field_list[y]}'] + 1 + \
                                                                       self.reserve_resouce['grain']
                        # take grain from global inventory
                        self.reserve_resouce['grain'] = 0
                        y = y + 1
                else:
                    print('plow a field first')
                    break

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_13_b']

    def action_14(self, player_state, player_field_dict, player_field_list, pasteur_type, player_improvements):
        if self.improvement_14 in self.improvements:
            # Check player's payment
            if player_state['clay'] >= self.improvement_14["price"][0] & player_state['reed'] >= self.improvement_14["price"][1] & player_state['wood'] >= self.improvement_14["price"][2]:
                # Player pays
                player_state['clay'] = player_state['clay'] - self.improvement_14["price"][0]
                player_state['reed'] = player_state['reed'] - self.improvement_14["price"][1]
                player_state['wood'] = player_state['wood'] - self.improvement_14["price"][2]

                # Add to reserved resources
                self.reserve_resouce['clay'] = self.reserve_resouce['clay'] + self.improvement_14["price"][0]
                self.reserve_resouce['reed'] = self.reserve_resouce['reed'] + self.improvement_14["price"][1]
                self.reserve_resouce['wood'] = self.reserve_resouce['wood'] + self.improvement_14["price"][2]

                # Deduct from global resources
                element_to_remove = self.improvement_14
                self.improvements = [x for x in my_list if x != element_to_remove]

                # Player gain
                player_improvements.append(self.improvement_14)

            else: print('you cannot afford it')

        else: print(f'improvement_14 is not available')

        # Remove this action from the current round
        self.moves = [x for x in self.moves if x != 'action_14']

    ### Gameplay
    def round_play(self):

        # Unlock round actions
        self.moves = [self.action_a,self.action_b,self.action_c,self.action_d,self.action_e,self.action_f,self.action_g,self.action_h,self.action_i,self.action_j,self.action_k,self.action_l,self.action_m,self.action_n,self.action_o]

        if self.round >= 1:
            self.moves.append(self.action_1)
        if self.round >= 2:
            self.moves.append(self.action_2)
        if self.round >= 3:
            self.moves.append(self.action_3)
        if self.round >= 4:
            self.moves.append(self.action_4)
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
        if self.round >= 14:
            self.moves.append(self.action_14)

        self.player1_number_actions = self.player1_state['farmer']
        self.player2_number_actions = self.player2_state['farmer']
        self.player3_number_actions = self.player3_state['farmer']
        self.player4_number_actions = self.player4_state['farmer']
        self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions

        # Assign order in which player take actions based on rooster assignment
        print(self.player1_state['rooster'])
        print(self.player2_state['rooster'])
        print(self.player3_state['rooster'])
        print(self.player4_state['rooster'])

        self.order_list = [1,2,3,4]

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
        print(self.player_order)

        # Players take actions
        while self.remain_actions > 0:
            for order in self.player_order:
                # Player 1 take action
                if order == 'player1':
                    if self.player1_number_actions != 0:
                        self.player1_action = self.moves[random.randint(0, len(self.moves)-1)] #randomzzz
                        # print(f"player 1 before states {self.player1_state}")
                        print(f"player 1 take action {self.player1_action}")
                        self.player1_action(self.player1_state, self.player1_field_dict, self.player_state_list, pasteur_list[random.randint(0,3)], self.player1_improvements)
                        # print(f"player 1 after states {self.player1_state}")
                        self.moves.remove(self.player1_action)
                        print(len(self.moves))
                        self.player1_number_actions -= 1


                # Player 2 take action
                if order == 'player2':
                    if self.player2_number_actions != 0:
                        self.player2_action = self.moves[random.randint(0, len(self.moves)-1)] #randomzzz
                        print(f"player 2 take action {self.player2_action}")
                        self.player2_action(self.player2_state, self.player2_field_dict, self.player_state_list, pasteur_list[random.randint(0,3)], self.player2_improvements)
                        self.moves.remove(self.player2_action)
                        print(len(self.moves))
                        self.player2_number_actions -= 1

                # Player 3 take action
                if order == 'player3':
                    if self.player3_number_actions != 0:
                        self.player3_action = self.moves[random.randint(0, len(self.moves)-1)] #randomzzz
                        print(f"player 3 take action {self.player3_action}")
                        self.player3_action(self.player3_state, self.player3_field_dict, self.player_state_list, pasteur_list[random.randint(0,3)], self.player3_improvements)
                        self.moves.remove(self.player3_action)
                        print(len(self.moves))
                        self.player3_number_actions -= 1


                # Player 4 take action
                if order == 'player4':
                    if self.player4_number_actions != 0:
                        self.player4_action = self.moves[random.randint(0, len(self.moves)-1)] #randomzzz
                        print(f"player 4 take action {self.player4_action}")
                        self.player4_action(self.player4_state, self.player4_field_dict, self.player_state_list, pasteur_list[random.randint(0,3)], self.player4_improvements)
                        self.moves.remove(self.player4_action)
                        print(len(self.moves))
                        self.player4_number_actions -= 1

            self.remain_actions = self.player1_number_actions + self.player2_number_actions + self.player3_number_actions + self.player4_number_actions



        # Refill board resouces after each round
        self.board_resouce['2_clay'] = self.board_resouce['2_clay'] + 2
        self.board_resouce['1_clay'] = self.board_resouce['1_clay'] + 1
        self.board_resouce['reed'] = self.board_resouce['reed'] + 1
        self.board_resouce['1_wood'] = self.board_resouce['1_wood'] + 1
        self.board_resouce['2_wood'] = self.board_resouce['2_wood'] + 2
        self.board_resouce['3_wood'] = self.board_resouce['3_wood'] + 3
        self.board_resouce['food'] = self.board_resouce['food'] + 1
        self.board_resouce['sheep'] = self.board_resouce['sheep'] + 1
        if self.round >= 6:
            self.board_resouce['boar'] = self.board_resouce['boar'] + 1
        if self.round >= 8:
            self.board_resouce['cow'] = self.board_resouce['cow'] + 1

#TODO: can only take 1 pasteur for action b_1
#TODO: randomimze number of pasteur to take for action c
#TODO: harvesting: feeding/begging, field work, offsprings/assigning or converting offsprings to foods.
#TODO: offspring after each harvest and players have to assign livestocks right away
#TODO: when take/offspring livestock and not enough space, choose to keep one and discard another
#TODO: make sure to shuffle field list before action_g
#TODO: make sure update field list after action_d
#TODO: calculating points after round 14

### Agent
player1_acquired_sheeps = 10
player1_acquired_boars = 4
player1_acquired_cows = 3

game = AgricolaAI()
while game.round < 15:
    print(f'This is round {game.round}')
    game.round_play()
    # print(len(game.moves))
    print('================================================================================================')
    game.round += 1


