# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# Peacetime routing environment.  Preceding prose states the peacetime goals:
# minimize travel time/cost over the terrain, avoid danger zones, and prefer
# paved roads by pricing unpaved roads higher.
#
# A gym.Env with a 5-dim Box observation (current position, destination, road
# condition, terrain) and 3 discrete actions (0 paved, 1 unpaved, 2 tunnel).
# Reward is a hand-set constant per road type minus noise minus a time penalty
# proportional to the action index; the state transition is pure random noise
# and done is always False, so nothing is actually being learned about routing.
# Trained with stable-baselines3 PPO for 10,000 timesteps at module level.

import numpy as np
import gym
from stable_baselines3 import PPO

# 평시 상황 환경 정의
class PeacefulLogisticsEnv(gym.Env):
    def __init__(self):
        super(PeacefulLogisticsEnv, self).__init__()

        # 상태 공간: 현재 위치, 목적지, 도로 상태, 지형
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        
        # 행동 공간: 경로 선택 (0: 포장도로, 1: 비포장도로, 2: 터널)
        self.action_space = gym.spaces.Discrete(3)
        
        # 초기 상태 설정
        self.state = np.zeros(5)
    
    def reset(self):
        # 경로 및 초기 상태 리셋
        self.state = np.random.uniform(0, 1, size=(5,))
        return self.state

    def step(self, action):
        # 액션에 따른 비용 및 보상 계산
        if action == 0:  # 포장 도로 선택
            reward = 10 - np.random.uniform(0, 2)  # 낮은 비용
        elif action == 1:  # 비포장 도로 선택
            reward = 5 - np.random.uniform(2, 5)  # 높은 비용
        else:  # 터널 선택
            reward = 8 - np.random.uniform(1, 3)  # 중간 비용
        
        # 시간 소모 계산
        time_penalty = np.random.uniform(0, 1) * action
        
        # 다음 상태 전이
        self.state = np.random.uniform(0, 1, size=(5,))
        
        done = False  # 끝나는 조건 없음

        return self.state, reward - time_penalty, done, {}

# PPO 알고리즘을 사용해 학습
env = PeacefulLogisticsEnv()
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)
