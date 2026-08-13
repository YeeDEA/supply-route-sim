# supply-route-sim

> **Archived personal project (Sep–Oct 2024).** Kept as-is; the notebooks reflect what I knew at the time and are no longer maintained.

Supply route planning experiments: the same problem — getting supplies from a depot to units while avoiding threat zones — attacked three different ways: reinforcement learning on a gridworld, classical optimization with OR-Tools (CVRP), and an interactive GUI/map simulator.

## Motivation

The problem comes from my military service: planning supply runs when parts of the map are effectively off-limits. Everything here is a **synthetic scenario** — the maps use arbitrary points in downtown Seoul as stand-ins, and no real military data, facility locations, or routes appear anywhere.

## Three approaches to one problem

| Approach | Notebook | Idea |
|---|---|---|
| Reinforcement learning | `rl_gridworld_qlearning_ppo.ipynb` | Tabular Q-learning on 5×5 (with a trap cell) and 4×4 grids, then PPO (stable-baselines3, 10,000 timesteps) on a custom `gym.Env` for the same 4×4 grid |
| Classical optimization | `ortools_cvrp_supply_routing.ipynb` | Capacitated vehicle routing: 1 depot + 5 delivery points, 2 vehicles of capacity 3, Euclidean distances |
| Simulation / visualization | `logistics_sim_tkinter_v1.ipynb` → `logistics_sim_tkinter_folium_v2.ipynb` → `folium_route_comparison_map.ipynb` | v1: tkinter GUI managing soldiers' hunger/health/stress/hygiene against supply stocks; v2: adds a folium map of buildings and threats; final: folium map comparing a "low-learning" route (skirts a missile-threat circle) vs a "high-learning" route (fully avoids it) |

The OR-Tools solver produces (from the notebook output):

```
Objective: 50
Vehicle 0: 0 -> 3 -> 4 -> 0  (distance 23)
Vehicle 1: 0 -> 1 -> 5 -> 2 -> 0  (distance 27)
```

The RL notebooks show the learned Q-tables converging toward the goal cell; no quantitative benchmark beyond that was recorded.

## Screenshots

Supply-decision flowchart rendered by `combat_supply_flowchart.ipynb`:

![Supply planning flowchart](docs/images/supply_flowchart.png)

The route-comparison map is interactive folium output — open [`docs/folium_route_comparison.html`](docs/folium_route_comparison.html) in a browser (extracted from the notebook output). It shows three facility markers, two threat circles, and the two routes (blue = early training, green = trained).

## Notebook index

| File | Purpose |
|---|---|
| `rl_gridworld_qlearning_ppo.ipynb` | Q-learning (5×5 and 4×4 grids) + PPO on a custom gym environment |
| `ortools_cvrp_supply_routing.ipynb` | OR-Tools CVRP for supply vehicle routing |
| `combat_supply_flowchart.ipynb` | matplotlib flowchart of the supply-planning decision process |
| `logistics_sim_tkinter_v1.ipynb` | tkinter GUI simulator v1 (soldier stats vs supply stocks) |
| `logistics_sim_tkinter_folium_v2.ipynb` | v2: tkinter GUI + folium map of buildings/threats |
| `folium_route_comparison_map.ipynb` | folium map comparing low- vs high-training routes around threat zones |

## Running

The RL, CVRP, and flowchart notebooks run directly in Colab (`!pip install ortools` / `stable-baselines3` cells included). The tkinter notebooks need a display: v1 includes an `xvfb`/`pyvirtualdisplay` setup for Colab, but the GUI is really meant to be run locally with a desktop Python; `logistics_sim_tkinter_folium_v2.ipynb` also calls `os.startfile`, which is Windows-only — expect it not to work in Colab as-is.

```
pip install -r requirements.txt
```

## What I'd do differently

The three tracks never actually meet: the RL agent lives on an abstract grid, the CVRP solver on abstract coordinates, and the folium "learning comparison" routes are hand-drawn to illustrate the idea rather than produced by the trained agent. Today I would project the gridworld onto the map's coordinate frame so the plotted routes come straight from the Q-table/PPO policy, log a proper training curve instead of eyeballing Q-tables, and encode threat zones as costs in the CVRP distance matrix so the two solvers become directly comparable on one scenario.

## Provenance

These were Colab notebooks organized and renamed later; original names and dates below. Work period: **Sep 15 – Oct 2, 2024**. The original Korean README is preserved at [`docs/README.ko.md`](docs/README.ko.md).

| File | Original name | Date |
|---|---|---|
| `rl_gridworld_qlearning_ppo.ipynb` | A/Untitled0.ipynb | 2024-09-15 |
| `ortools_cvrp_supply_routing.ipynb` | A/Untitled1.ipynb | 2024-09-29 |
| `combat_supply_flowchart.ipynb` | A/Untitled2.ipynb | 2024-09-29 |
| `logistics_sim_tkinter_v1.ipynb` | A/Untitled3.ipynb | 2024-09-29 |
| `logistics_sim_tkinter_folium_v2.ipynb` | A/Untitled4.ipynb | 2024-09-29 |
| `folium_route_comparison_map.ipynb` | A/Untitled5.ipynb | 2024-10-02 |

## License

MIT — see [LICENSE](LICENSE).
