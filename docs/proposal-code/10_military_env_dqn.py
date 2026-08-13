# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# The document's last and longest code block, introduced under
# "CHATGPT를 활용한 전시상황의 우선순위 파악 및 배차 알고리즘" and fenced as
# ```python - i.e. the author records it as assistant-generated.
#
# MilitaryEnv: a 10x10 grid map, Box(low=0, high=3) observation, 5 discrete
# actions (up, down, left, right, wait), agent starting at [5][5], -1 per step,
# -100 for entering a cell marked 2 (damage zone), +100 and done for reaching a
# cell marked 3 (goal).  INCOMPLETE AS WRITTEN: every movement branch in step()
# is `pass`, so the agent never moves and the damage/goal checks read fixed
# cells [7][7] and [8][8] that reset() never sets - the episode can never end.
# DQNAgent is 08's agent again, on tf.keras instead of tensorflow.keras, with
# replay() renamed train().  The __main__ block flattens the 10x10 grid to a
# 100-dim vector and runs 1000 episodes.  Left unfixed.

import gym
import numpy as np
import tensorflow as tf
from collections import deque
import random

# 환경 초기 설정
class MilitaryEnv(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(5)  # 5개의 이동 방향 (상, 하, 좌, 우, 대기)
        self.observation_space = gym.spaces.Box(low=0, high=3, shape=(10, 10))  # 10x10 크기의 지도
        self.state = np.zeros((10, 10))  # 초기 상태
        self.reset()

    def reset(self):
        self.state = np.zeros((10, 10))
        self.state[5][5] = 1  # 병사/차량의 초기 위치
        return self.state

    def step(self, action):
        # 액션에 따른 이동
        reward = -1  # 기본 패널티
        done = False

        # 각 액션에 따른 이동 로직
        if action == 0:  # 상
            # 이동 로직
            pass
        elif action == 1:  # 하
            # 이동 로직
            pass
        elif action == 2:  # 좌
            # 이동 로직
            pass
        elif action == 3:  # 우
            # 이동 로직
            pass
        elif action == 4:  # 대기
            # 대기 로직
            pass

        # 피해 계산
        if self.state[7][7] == 2:  # 피해 구역에 들어갔을 때
            reward -= 100  # 피해를 받았으므로 큰 패널티

        if self.state[8][8] == 3:  # 목표에 도달
            reward += 100  # 목표에 도달하면 큰 보상
            done = True

        return self.state, reward, done, {}

# DQN 모델 정의
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 할인 계수
        self.epsilon = 1.0  # 탐험율
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # 무작위 액션 선택 (탐험)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # 가장 좋은 액션 선택 (탐욕적 행동)

    def train(self, batch_size=32):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# 강화학습 실행
if __name__ == "__main__":
    env = MilitaryEnv()
    agent = DQNAgent(state_size=100, action_size=5)
    episodes = 1000

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, 100])

        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 100])
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon}")
                break

        if len(agent.memory) > 32:
            agent.train(32)
