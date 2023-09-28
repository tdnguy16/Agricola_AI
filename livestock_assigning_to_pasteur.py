import numpy as np
import random

def distribute_sum(total_sum, num_variables):
    # Generate random integers for each variable except the last one
    values = [random.randint(0, total_sum) for _ in range(num_variables - 1)]

    # Sort the values in ascending order
    values.sort()

    # Calculate the differences between consecutive values to get the allocated amounts
    allocated_amounts = [values[0]] + [values[i] - values[i - 1] for i in range(1, num_variables - 1)] + [
        total_sum - values[-1]]

    return allocated_amounts

player1_state = {'grain': 3, 'field': 0, 'grain_on_field': 0, 'clay': 0, 'reed': 0, 'wood': 0, 'food': 0, 'sheep': 10, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 0, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1,'farmer': 2, 'livestock_slot': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0}

# Default capacity of the pasteurs
pasteur_capacity_arrays = np.array([2, 4, 6, 8])

pasteur_arrays = np.array([[1], [1], [1],])

# Pasteurs that players have
# [pasteur2_number, pasteur4_number, pasteur6_number, pasteur8_number]
player1_pasteur_list = [1, 2, 1, 0]

# Show the available spaces that players have
player1_available_space_arrays = pasteur_capacity_arrays * player1_pasteur_list * pasteur_arrays
print('Here is the available spaces')
print(player1_available_space_arrays)
print('-------------------------------------------------------------')

#-----------------------------------------------------------------------------------------------
#   Player's livestocks count
sheep_list = distribute_sum(player1_state['sheep'], 4)
print(sheep_list)

boar_list = [0, 0, 8, 0]

cow_list = [0, 0, 0, 0]

for sheep in sheep_list:
    if sheep > 0:
        print(f'{sheep} sheeps added to the pasteurs')

for boar in boar_list:
    if boar > 0:
        print(f'{boar} boars added to the pasteurs')

for cow in cow_list:
    if cow > 0:
        print(f'{cow} cows added to the pasteurs')

player1_livestock_arrays = np.array([
    sheep_list,
    boar_list,
    cow_list,
])

#   Where the player choose to put their livestocks
player1_available_space_arrays = player1_available_space_arrays - player1_livestock_arrays
print('Here is the available spaces after adding the livestocks')
print(player1_available_space_arrays)



stable_arrays = np.array([
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
])



# Total sum to distribute
total_sum = 100

# Number of variables to distribute the sum to
num_variables = 5

allocated_amounts = distribute_sum(total_sum, num_variables)
print(allocated_amounts)