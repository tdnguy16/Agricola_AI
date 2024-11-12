import random
from enum import Enum
from collections import namedtuple
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def count_action_levels(moves_total_levels, moves_total_names):
    # Initialize a dictionary to count occurrences for each level
    level_counts = defaultdict(int)

    # Count occurrences of each action's level
    for action in moves_total_names:
        level = moves_total_levels.get(action, None)  # Get level of the action
        if level is not None:
            level_counts[level] += 1  # Increment count for that level

    return dict(level_counts)  # Convert to regular dict for cleaner output

moves_total_levels = {'action_a': 1, 'action_b': 2, 'action_c': 2,
                              'action_d': 1, 'action_e': 1, 'action_f': 1,
                              'action_g': 3, 'action_h': 1, 'action_i': 1, 'action_j': 1, 'action_k': 1, 'action_l': 1,
                              'action_m': 1, 'action_n': 1, 'action_o': 1, 'action_1': 2, 'action_2': 2, 'action_3': 2,
                              'action_4': 3, 'action_5': 3, 'action_6': 1, 'action_7': 2, 'action_8': 1, 'action_9': 2,
                              'action_10': 2, 'action_11': 2, 'action_12': 1, 'action_13': 3, 'action_14': 1}

moves_total_names = ['action_a', 'action_i', 'action_i', 'action_b', 'action_c', 'action_13', 'action_13']

level_occurrences = count_action_levels(moves_total_levels, moves_total_names)
print(level_occurrences)


def plot_level_occurrences(level_occurrences):
    levels = list(level_occurrences.keys())
    occurrences = list(level_occurrences.values())

    plt.figure(figsize=(8, 6))
    plt.bar(levels, occurrences)
    plt.xlabel("Action Level")
    plt.ylabel("Occurrences")
    plt.title("Occurrences of Different Action Levels")
    plt.xticks(levels)  # Set x-ticks to show each level
    plt.show()


plot_level_occurrences(level_occurrences)