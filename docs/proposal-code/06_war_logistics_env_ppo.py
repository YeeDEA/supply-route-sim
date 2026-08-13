# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# Wartime counterpart to 05.  Continues the same code block in the document and
# so has no imports of its own - it reuses numpy / gym / PPO from that file.
#
# 6-dim Box observation (CBRN contamination, enemy position, weather, terrain,
# troop condition) and 3 discrete actions (0 safe route, 1 risky route, 2 fast
# route).  Preceding prose describes the intent: explore the safe route then
# look for a faster one, explore the risky route then look for a safer one, and
# settle between the two.  As with 05 the transition is random noise, done is
# always False, and PPO trains for 10,000 timesteps at module level.

class WarLogisticsEnv(gym.Env):
    def __init__(self):
        super(WarLogisticsEnv, self).__init__()

        # 상태 공간: 화생방 오염도, 적군 위치, 날씨, 지형, 병력 상태
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(6,), dtype=np.float32)
        
        # 행동 공간: 경로 선택 (0: 안전 경로, 1: 위험 경로, 2: 신속 경로)
        self.action_space = gym.spaces.Discrete(3)
        
        self.state = np.zeros(6)
    
    def reset(self):
        # 초기 상태 설정
        self.state = np.random.uniform(0, 1, size=(6,))
        return self.state

    def step(self, action):
        # 화생방 위험 지역을 우회할 경우
        if action == 0:  # 안전 경로
            reward = 15 - np.random.uniform(0, 3)  # 높은 보상 (안전)
            time_penalty = np.random.uniform(0, 2)  # 시간 소모
        elif action == 1:  # 위험 경로
            reward = 5 - np.random.uniform(3, 6)  # 페널티 (위험)
            time_penalty = np.random.uniform(2, 5)
        else:  # 신속 경로
            reward = 10 - np.random.uniform(1, 3)  # 중간 보상
            time_penalty = np.random.uniform(0, 1)

        # 상태 전이
        self.state = np.random.uniform(0, 1, size=(6,))
        
        done = False

        return self.state, reward - time_penalty, done, {}

# PPO로 학습
env = WarLogisticsEnv()
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)
