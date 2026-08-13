# Proposal-stage code sketches

Every code block from the 2024 Defense AI Ideathon planning document, reproduced
verbatim. The document is summarized in [`../proposal-summary.md`](../proposal-summary.md).

**These are design-stage sketches, not run code.** They were written into a
planning document to show what the system would look like; there is no evidence
any of them was executed, and several cannot be — they reference classes the
document never defines, or return names that were never bound. Nothing in this
directory is imported, tested, or used by `src/` or `notebooks/`. They are here
so the proposal's own code is readable next to the code that was actually built,
and so the gap between the two is visible.

They are **not repaired**. Where a sketch is broken, the file's header comment
says how — the code below the header is left as the author wrote it. The only
edit applied anywhere is decoding the HTML entities (`&lt;` `&gt;` `&quot;`)
that .docx text extraction introduced. Korean comments are the author's.

Every file passes `python -m py_compile` (they parse); that is not a claim that
they run.

## Contents, in document order

| File | What it is | Runnable? |
|---|---|---|
| — | `Soldier` / `Vehicle` / `Building` with `update_stats()` and `apply_supply()` | kept importable at [`../../src/supply_sim/entities.py`](../../src/supply_sim/entities.py) |
| `01_entities_with_positions.py` | second revision: `Entity` base class with x/y and `distance_to()`, the three classes re-declared on it, `Soldier.move_towards()` | parses; drops the stat methods, so it is not a superset of the first revision |
| `02_run_simulation.py` | 100-day driver loop: tick stats, issue supply class 1/3/4 on threshold | needs the first-revision classes in scope (no import line in the document) |
| `03_run_simulation_soldier_ai.py` | same loop over positioned entities, 5 soldiers, 2 buildings, 2 vehicles | no — instantiates `SoldierAI` and calls `decide_action()`, neither ever defined |
| `04_run_simulation_soldier_ai_variant.py` | near-duplicate of 03 appearing a few lines later | no — same undefined `SoldierAI`, plus brackets closed mid-comment, lost indentation, and a `run_simulation()` call that landed inside the loop (infinite recursion) |
| `05_peaceful_logistics_env_ppo.py` | `PeacefulLogisticsEnv(gym.Env)` — 5-dim Box state, 3 actions (paved / unpaved / tunnel), PPO 10,000 timesteps | parses; the transition is random noise and `done` is always `False`, so it learns a constant preference, not a route |
| `06_war_logistics_env_ppo.py` | `WarLogisticsEnv(gym.Env)` — 6-dim Box state, 3 actions (safe / risky / fast), PPO 10,000 timesteps | same shape as 05; continues 05's code block, so it has no imports of its own |
| `07_disaster_environment.py` | `DisasterEnvironment` — the class framing supply-priority learning | no — a skeleton; `regions`/`vehicles` are literally `[...]` and the two private methods return unbound names |
| `08_dqn_keras.py` | `DQN` agent: 2×24 dense net, 2000-entry replay deque, ε-greedy 1.0→0.01 | parses; uses `Adam(lr=...)`, already deprecated then and removed in Keras 3 |
| `09_dqn_training_loop.py` | pairs 07 with 08 — 1000 episodes × 500 steps, `replay(32)` per episode | no — 07 has no `state_size`/`action_size`, and this unpacks `step()` as 3 values while the gym envs return 4 |
| `10_military_env_dqn.py` | `MilitaryEnv` (10×10 grid, 5 actions incl. wait) + `DQNAgent` + `__main__` loop. Fenced ` ```python ` in the document under a heading crediting ChatGPT | no — every movement branch in `step()` is `pass`, and the damage/goal checks read cells `[7][7]`/`[8][8]` that `reset()` never marks, so the agent cannot move and the episode cannot end |

## Relationship to `rl_gridworld_qlearning_ppo.ipynb`

The implemented RL notebook is the *working* version of what 05, 06 and 10 sketch,
scaled down until it actually ran:

- **What carried over.** The gym + stable-baselines3 PPO setup and the
  10,000-timestep budget are identical between the sketches and the notebook's
  `GridEnv`. Q-learning, DQN and PPO are all named as candidates in the proposal;
  the notebook picks tabular Q-learning and PPO.
- **What changed.** The notebook's `GridEnv` is a 4×4 grid with a 2-dim position
  observation and 4 movement actions — real state transitions, a real terminal
  condition (reaching `(3, 3)`), and reward +10 / −1. The sketches' environments
  never move: they redraw a random state vector each step and never terminate, so
  the "route choice" they encode is a one-shot preference among three labels
  (paved/unpaved/tunnel, safe/risky/fast) rather than a path.
- **The threat zone.** `10_military_env_dqn.py` is the sketch closest to the
  notebook's idea — a grid, movement actions, a damage cell and a goal cell — but
  its movement is unimplemented. The notebook's first Q-learning cell is that idea
  finished: a 5×5 grid with a trap cell at `(2, 2)` worth −100 and a goal at
  `(4, 4)` worth +100. That trap cell is the threat zone the whole proposal is about,
  reduced to one square.
- **What was never attempted.** No DQN was implemented anywhere in the repo —
  neither Keras agent in `08` or `10` has a counterpart notebook. Neither does
  `DisasterEnvironment`, i.e. the supply-*priority* learning the document calls
  "the most important thing".
