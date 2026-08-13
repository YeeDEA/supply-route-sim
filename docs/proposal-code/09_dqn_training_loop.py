# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# Document heading: "학습 진행 과정" ("training procedure")
#
# Driver loop pairing 07's DisasterEnvironment with 08's DQN: 1000 episodes of
# up to 500 steps, replay(32) once per episode.  Cannot run - DisasterEnvironment
# has no state_size / action_size attributes and its methods return undefined
# names.  Note env.step() is unpacked as 3 values here, while the gym
# environments in 05/06/10 return 4.

env = DisasterEnvironment()
agent = DQN(state_size=env.state_size, action_size=env.action_size)

for episode in range(1000):
    state = env.reset()
    state = np.reshape(state, [1, env.state_size])
    
    for time in range(500):
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1, env.state_size])
        
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        
        if done:
            print(f"Episode {episode}/{1000}, Score: {time}")
            break
        
    agent.replay(32)  # 경험 리플레이로 학습
