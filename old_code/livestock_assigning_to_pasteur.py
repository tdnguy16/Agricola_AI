import numpy as np
import random

player1_state = {'sheep': 1, 'boar': 2, 'cow': 1, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'pasteur_2': 1, 'pasteur_4': 1, 'pasteur_6': 1, 'pasteur_8': 1, 'stable': 10}

def distribute_sum_livestocks(total_sum, num_variables):
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

def distribute_sum_stable(target_sum, num_variables):
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

def assign_stables(player_state, player_expanded_pasteur_list):
    # Pick a random integer between 1 and 10 (inclusive)
    stables_tobe_assigned = random.randint(0, len(player_expanded_pasteur_list) - 1)  # randomzzz

    # Pick a pasteur to add stable to
    random_pasteur = random.sample(range(0, len(player_expanded_pasteur_list) - 1), stables_tobe_assigned)

    for x in random_pasteur:
        player_expanded_pasteur_list[x] = player_expanded_pasteur_list[x] * 2

    return player_expanded_pasteur_list

def assign_livestock(player_state, acquired_sheeps, acquired_boars, acquired_cows):
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

    # Assign stables
    player_expanded_pasteur_list = assign_stables(player_state, player_expanded_pasteur_list)

    player_pasteur_capacity_arrays = np.array(player_expanded_pasteur_list)
    print(player_pasteur_capacity_arrays)

    # Pasteurs that players have
    # [pasteur2_number, pasteur4_number, pasteur6_number, pasteur8_number]

    # Show the available spaces that players have
    player_available_space_arrays = player_pasteur_capacity_arrays * pasteur_arrays
    print('Here is the available spaces')
    print(player_available_space_arrays)
    print('-------------------------------------------------------------')

    #-----------------------------------------------------------------------------------------------
    #   Player's livestocks count
    try:
        sheeps_tobe_assigned = acquired_sheeps + player_state['sheep']
        sheep_list = distribute_sum_livestocks(sheeps_tobe_assigned, len(player_expanded_pasteur_list))

        boars_tobe_assigned = acquired_boars + player_state['boar']
        boar_list = distribute_sum_livestocks(boars_tobe_assigned, len(player_expanded_pasteur_list))

        cows_tobe_assigned = acquired_cows + player_state['cow']
        cow_list = distribute_sum_livestocks(cows_tobe_assigned, len(player_expanded_pasteur_list))
    except:
        print('no pasteur found')
        return

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


### Execution
player1_acquired_sheeps = 10
player1_acquired_boars = 4
player1_acquired_cows = 3

print(player1_state)

assign_livestock(player1_state, player1_acquired_sheeps, player1_acquired_boars, player1_acquired_cows)

print(player1_state)

