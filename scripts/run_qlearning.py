# -*- coding: utf-8 -*-
"""CLI for the tabular Q-learning experiments (notebooks/rl_gridworld_qlearning_ppo.ipynb)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supply_sim.gridworld_qlearning import run_q_learning_5x5, run_q_learning_4x4


def main():
    parser = argparse.ArgumentParser(description="Tabular Q-learning on a gridworld.")
    parser.add_argument("--variant", choices=["5x5", "4x4"], default="5x5",
                        help="5x5: goal+trap grid (500 episodes default); 4x4: goal-only grid (1000 episodes default)")
    parser.add_argument("--episodes", type=int, default=None, help="Override number of episodes")
    args = parser.parse_args()

    if args.variant == "5x5":
        q = run_q_learning_5x5(args.episodes if args.episodes is not None else 500)
        print("Q-table:")
        print(q)
    else:
        q, path = run_q_learning_4x4(args.episodes if args.episodes is not None else 1000)
        print("최종 Q 테이블:")
        print(q)
        print("학습된 최적 경로: ", path)


if __name__ == "__main__":
    main()
