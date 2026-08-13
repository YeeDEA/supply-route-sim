# -*- coding: utf-8 -*-
"""CLI for PPO training on the custom gym GridEnv (notebooks/rl_gridworld_qlearning_ppo.ipynb)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supply_sim.gym_env import train_ppo


def main():
    parser = argparse.ArgumentParser(description="Train PPO on the 4x4 GridEnv and print the learned path.")
    parser.add_argument("--timesteps", type=int, default=10000, help="Total training timesteps (notebook used 10000)")
    args = parser.parse_args()

    model, path = train_ppo(total_timesteps=args.timesteps)
    print("학습된 최적 경로: ", path)


if __name__ == "__main__":
    main()
