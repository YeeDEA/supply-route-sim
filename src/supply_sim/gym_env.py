# -*- coding: utf-8 -*-
"""Custom gym environment + PPO training on a 4x4 grid.

Extracted from notebooks/rl_gridworld_qlearning_ppo.ipynb (code cell 2).
Requires gym and stable-baselines3 (the notebook ran on Colab's preinstalled
versions; written against the old gym API — reset() returns obs only and
step() returns 4 values, so recent gymnasium-based stable-baselines3 releases
may reject this env).
"""

import gym
import numpy as np


# 간단한 그리드 환경 만들기
class GridEnv(gym.Env):
    def __init__(self):
        super(GridEnv, self).__init__()
        self.grid_size = 4
        self.action_space = gym.spaces.Discrete(4)  # 상, 하, 좌, 우
        self.observation_space = gym.spaces.Box(low=0, high=self.grid_size-1, shape=(2,), dtype=np.int32)
        self.state = np.array([0, 0])  # 시작 지점
        self.goal_state = np.array([3, 3])

    def reset(self):
        self.state = np.array([0, 0])
        return self.state

    def step(self, action):
        row, col = self.state
        if action == 0 and row > 0:
            row -= 1
        elif action == 1 and row < self.grid_size - 1:
            row += 1
        elif action == 2 and col > 0:
            col -= 1
        elif action == 3 and col < self.grid_size - 1:
            col += 1
        self.state = np.array([row, col])

        # 보상 계산
        done = np.array_equal(self.state, self.goal_state)
        reward = 10 if done else -1

        return self.state, reward, done, {}

    def render(self, mode='human'):
        grid = np.zeros((self.grid_size, self.grid_size))
        grid[tuple(self.state)] = 1
        grid[tuple(self.goal_state)] = 2
        print(grid)


def train_ppo(total_timesteps=10000):
    """Train PPO on GridEnv and roll out the learned policy (notebook cell 2).

    Returns (model, path).
    """
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv

    # 환경 만들기
    env = DummyVecEnv([lambda: GridEnv()])

    # PPO 에이전트 학습
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=total_timesteps)

    # 최적 경로 출력
    obs = env.reset()
    done = False
    path = [obs]

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        path.append(obs)

    return model, path
