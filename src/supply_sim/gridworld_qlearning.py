# -*- coding: utf-8 -*-
"""Tabular Q-learning on gridworlds.

Extracted from notebooks/rl_gridworld_qlearning_ppo.ipynb (code cells 0 and 1).
Two independent notebook experiments, each wrapped in a function so both can
coexist in one module; the code inside each function is the notebook cell
verbatim (module-level script code became the function body).
"""

import numpy as np
import random


def run_q_learning_5x5(episodes=500):
    """Cell 0: 5x5 grid with a goal at (4, 4) and a trap at (2, 2).

    Returns the learned Q-table.
    """
    # 환경 설정 (5x5 그리드)
    grid_size = 5
    goal_state = (4, 4)  # 목표 위치
    trap_state = (2, 2)  # 함정 위치
    actions = ['up', 'down', 'left', 'right']
    action_dict = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Q-table 초기화
    Q_table = np.zeros((grid_size, grid_size, len(actions)))

    # 하이퍼파라미터 설정
    alpha = 0.1  # 학습률
    gamma = 0.9  # 감가율 (미래 보상에 대한 할인)
    epsilon = 0.1  # 탐험 비율 (exploration)

    # 보상 함수
    def get_reward(state):
        if state == goal_state:
            return 100  # 목표에 도달하면 보상
        elif state == trap_state:
            return -100  # 함정에 빠지면 큰 패널티
        else:
            return -1  # 나머지 이동에는 작은 패널티

    # 다음 상태를 얻는 함수
    def get_next_state(state, action):
        move = action_dict[action]
        next_state = (state[0] + move[0], state[1] + move[1])

        # 그리드 바깥으로 나가는 움직임은 무시 (벽에 부딪히면 같은 자리 유지)
        if next_state[0] < 0 or next_state[0] >= grid_size or next_state[1] < 0 or next_state[1] >= grid_size:
            next_state = state
        return next_state

    # 행동을 선택하는 함수 (탐험과 활용 중 선택)
    def choose_action(state):
        if random.uniform(0, 1) < epsilon:
            return random.choice(actions)  # 탐험: 무작위 선택
        else:
            state_index = state[0], state[1]
            return actions[np.argmax(Q_table[state_index])]  # 활용: Q-value가 가장 큰 행동 선택

    # Q-learning 알고리즘 실행
    def q_learning(episodes):
        for episode in range(episodes):
            state = (0, 0)  # 시작 위치
            done = False

            while not done:
                action = choose_action(state)
                next_state = get_next_state(state, action)
                reward = get_reward(next_state)

                state_index = state[0], state[1]
                next_state_index = next_state[0], next_state[1]
                action_index = actions.index(action)

                # Q-learning 업데이트 공식
                Q_table[state_index][action_index] = Q_table[state_index][action_index] + \
                    alpha * (reward + gamma * np.max(Q_table[next_state_index]) - Q_table[state_index][action_index])

                # 목표에 도달하면 종료
                if next_state == goal_state or next_state == trap_state:
                    done = True

                state = next_state

    # Q-learning 실행
    q_learning(episodes)

    return Q_table


def run_q_learning_4x4(num_episodes=1000):
    """Cell 1: 4x4 grid with a goal at (3, 3); also prints the learned path.

    Returns (q_table, path).
    """
    # 환경 설정 (4x4 그리드 맵)
    grid_size = 4
    goal_state = (3, 3)  # 목표 지점
    actions = ['up', 'down', 'left', 'right']  # 가능한 행동

    # Q 테이블 초기화
    q_table = np.zeros((grid_size, grid_size, len(actions)))

    # 하이퍼파라미터 설정
    alpha = 0.1   # 학습률
    gamma = 0.9   # 할인율
    epsilon = 0.1  # 탐험-이용 균형을 위한 탐험 확률

    # 환경에서의 보상 함수
    def get_reward(state):
        if state == goal_state:
            return 10  # 목표 지점에 도달하면 보상 10
        else:
            return -1  # 그 외에는 -1의 보상

    # 상태에서 가능한 행동을 실행한 후 새로운 상태 반환
    def take_action(state, action):
        row, col = state
        if action == 'up' and row > 0:
            row -= 1
        elif action == 'down' and row < grid_size - 1:
            row += 1
        elif action == 'left' and col > 0:
            col -= 1
        elif action == 'right' and col < grid_size - 1:
            col += 1
        return (row, col)

    # 탐험-이용 정책 (epsilon-greedy)
    def choose_action(state):
        if random.uniform(0, 1) < epsilon:
            return random.choice(actions)  # 탐험
        else:
            row, col = state
            return actions[np.argmax(q_table[row, col])]  # 이용 (Q-값이 가장 큰 행동 선택)

    # 학습 과정
    for episode in range(num_episodes):
        state = (0, 0)  # 시작 지점
        done = False

        while not done:
            # 현재 상태에서 행동 선택
            action = choose_action(state)

            # 선택한 행동으로 새로운 상태로 이동
            new_state = take_action(state, action)

            # 보상 계산
            reward = get_reward(new_state)

            # Q 테이블 업데이트
            row, col = state
            new_row, new_col = new_state
            action_idx = actions.index(action)

            # Q-값 업데이트 식
            q_table[row, col, action_idx] = q_table[row, col, action_idx] + alpha * (
                reward + gamma * np.max(q_table[new_row, new_col]) - q_table[row, col, action_idx]
            )

            # 상태 업데이트
            state = new_state

            # 목표 상태에 도달했을 때 에피소드 종료
            if state == goal_state:
                done = True

    # 학습된 경로 출력
    def print_optimal_path():
        state = (0, 0)
        path = [state]

        while state != goal_state:
            row, col = state
            action_idx = np.argmax(q_table[row, col])
            action = actions[action_idx]
            state = take_action(state, action)
            path.append(state)

        return path

    path = print_optimal_path()
    return q_table, path
