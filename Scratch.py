import matplotlib.pyplot as plt
import random

# Sample data for 14 rounds
rounds = list(range(1, 15))

# Initialize player states
player1_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1, 'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
player2_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1, 'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
player3_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1, 'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}
player4_state = {'clay': 0, 'reed': 0, 'wood': 0, 'grain': 0, 'food': 0, 'sheep': 0, 'boar': 0, 'cow': 0, 'begging': 0, 'rooster': 1, 'clay_conversion': 0, 'clay_room': 0, 'wood_room': 0, 'room_space': 2, 'livestock_space': 1, 'farmer': 2, 'livestock_slot': 0, 'grain_on_field': 0, 'pasteur_2': 0, 'pasteur_4': 0, 'pasteur_6': 0, 'pasteur_8': 0, 'stable': 0, 'field': 0}

# Initialize empty lists to store the values for each player and resource
player_states = [player1_state, player2_state, player3_state, player4_state]
resources = ['clay', 'reed', 'wood', 'grain', 'food', 'sheep', 'boar', 'cow', 'begging', 'rooster', 'clay_conversion', 'clay_room', 'wood_room', 'room_space', 'livestock_space', 'farmer', 'livestock_slot', 'grain_on_field', 'pasteur_2', 'pasteur_4', 'pasteur_6', 'pasteur_8', 'stable', 'field']

# Randomly generate data for each resource over 14 rounds for simplicity
data = {player: {resource: [random.randint(0, 10) for _ in rounds] for resource in resources} for player in range(1, 5)}

# Plotting the data
fig, axes = plt.subplots(len(resources), 1, figsize=(12, len(resources) * 3), sharex=True)

for idx, resource in enumerate(resources):
    for player in range(1, 5):
        axes[idx].plot(rounds, data[player][resource], label=f'Player {player}')
    axes[idx].set_ylabel(resource)
    axes[idx].legend(loc='upper right')

axes[-1].set_xlabel('Rounds')
plt.tight_layout()
plt.show()
