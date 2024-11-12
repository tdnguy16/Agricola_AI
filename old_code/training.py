import numpy as np
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
import logging
import optuna

from game_AI import AgricolaAI  # Assuming your environment is defined in agricola_env.py


def optimize_ppo(trial):
    # Define the hyperparameter search space
    learning_rate = trial.suggest_loguniform('learning_rate', 1e-5, 1e-4)
    ent_coef = trial.suggest_loguniform('ent_coef', 0.0001, 0.005)
    n_epochs = trial.suggest_int('n_epochs', 1, 2)

    # Create the environment
    env = AgricolaAI()

    # Create the model with the current hyperparameters
    model = PPO('MlpPolicy', env, learning_rate=learning_rate, ent_coef=ent_coef, n_epochs=n_epochs, verbose=0)

    # Train the model
    model.learn(total_timesteps=500)

    # Evaluate the model
    mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=10)

    return mean_reward


# Optimize hyperparameters
study = optuna.create_study(direction='maximize')
study.optimize(optimize_ppo, n_trials=1)

# Log the best hyperparameters
print('Best trial:')
trial = study.best_trial
print(f'  Value: {trial.value}')
print('  Params: ')
for key, value in trial.params.items():
    print(f'    {key}: {value}')

# Train the final model with the best hyperparameters
best_params = study.best_params

num_iterations = 2  # Specify the number of iterations

for iteration in range(num_iterations):
    print(f"Starting iteration {iteration + 1}")

    # Re-create the environment for each iteration
    env = AgricolaEnv()

    # Create the model with the best hyperparameters
    model = PPO('MlpPolicy', env, **best_params, verbose=1)

    # Train the model
    model.learn(total_timesteps=500)

    # Get the final resources of each player after training
    final_resources = env.get_player_resources()

    # Print and log the final resources of each player
    logging.basicConfig(filename='training_log.txt', level=logging.INFO, format='%(message)s')
    logging.info(f"Final resources after training iteration {iteration + 1}:")
    print(f"Final resources after training iteration {iteration + 1}:")
    for player, resources in final_resources.items():
        logging.info(f"{player}: {resources}")
        print(f"{player}: {resources}")

    print(f"Ending iteration {iteration + 1}")
    print("##########################################################\n")

# Save the model if needed
model.save("ppo_agricola")

# Print and log the best hyperparameters
logging.info("Best hyperparameters:")
print("Best hyperparameters:")
for key, value in best_params.items():
    logging.info(f"{key}: {value}")
    print(f"{key}: {value}")