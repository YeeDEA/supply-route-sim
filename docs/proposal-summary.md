# Proposal summary — "Supply Optimization Under Multiple Conditions"

*Source: my team's planning document for the 2024 1st Defense AI Ideathon (제1회 국방 AI 아이디어톤). Summarized in English; the document itself is not in this repo. Names removed.*

## How to read the document

The file is two things stacked. The **first part is a raw brainstorming log** — a list of candidate topics with a "tech needed" line under each, written before anything was decided. The **second part is the actual proposal**, restarting under the heading *"주제: 여러 조건 속 군수품 보급 최적화 시스템"* ("Supply optimization system under multiple conditions"), with the standard proposal sections (background, core idea, detail, differentiation, applicability, expected effect) plus an appendix of design notes and Python code blocks. The code is extracted into the repo — see [Code written into the document](#code-written-into-the-document) below.

I'm keeping the brainstorming part in this summary because the narrowing is the interesting bit: eight or so unrelated defense-AI ideas collapse into one, and the one that survives is the only one where a simulator could stand in for data we didn't have.

## Candidate ideas that were considered

From the brainstorming section, roughly in order:

- **DELLIS integration** — simplify vehicle-logbook and administrative paperwork, and additionally predict which consumables are due for replacement and warn about emerging vehicle/equipment risks before they cause accidents.
- **AI on military equipment** — EOD / mine-clearing vehicles for jobs humans shouldn't do; partial automation of high-fatigue duties such as military police work.
- **More realistic training** (e.g. KCTC exercises).
- **Battlefield medical triage** and **cybersecurity** (listed as one-liners).
- **Friend-or-foe weapon interlock** — a detachable IFF unit gating a rifle, plus marking friendly/hostile in CCTV footage. Explicitly annotated as *not AI*.
- **CBRN contamination mapping** — assess contamination severity and predict the plume's path on a map.
- **Compromised-countersign detection** during base defense, auto-broadcasting the backup countersign.
- **Wartime transport-support prioritization** — list what transport is needed and rank it.

A note in the middle asks whether any single AI technique spans several of these. The answer the team converges on: a map + weather + situation simulator, into which you enter units and supply constraints and get back an optimal allocation. That becomes the chosen topic.

## Chosen topic

**여러 조건 속 군수품 보급 최적화 시스템** — a supply-distribution optimization system covering both peacetime and wartime.

Stated goal: efficient military supply distribution in both peacetime and wartime conditions.

### Framing / motivation (from the background section)

The argument is budgetary, not tactical. Declining birth rates shrink the conscript intake while spending rises on pay and facilities; the team's read is that the underlying waste is **inefficient resource use** — some items over-ordered while items actually needed for training or combat arrive late, and short-term tasks (snow clearing is the example given) soaking up manpower that's needed elsewhere. The claim is that better allocation frees budget, and that current logistics is largely manual and so degrades exactly when the situation becomes unpredictable.

A second thread runs through the differentiation section: commercial logistics AI (UPS, DHL are named) optimizes for customer satisfaction, whereas this system has to prioritize soldier survival — so supply priority is driven by soldier condition, not delivery SLAs.

## Proposed system

### Two modes

1. **Peacetime (비전시)** — demand forecasting and stock management.
2. **Wartime (전시)** — threat entry, dynamic re-routing, dynamic priority.

### The six components the proposal enumerates

1. **Interactive UI.** An authorized reporter drops a pin on the map with a short description of an incident; keyword input places a color-coded icon by incident type (blast, collapse, CBRN, fire), with time / type / severity readable on click. Users zoom and filter; incidents refresh live or periodically. Each incident icon becomes an **obstacle** for routing. Map layer built on commercial map services (Google/Naver are named).
2. **Reinforcement-learning route model.** Inputs: terrain, weather, travel time, troops, CBRN contamination. Military maps are simplified into layers — terrain (cover large/small, movement-impeding areas like marsh, no-go areas, contours), transport network (unpaved / paved / tunnel), a CBRN layer in wartime mode, buildings (non-military by height band; military simplified from standard map symbols), and a wartime weather layer giving temperature, wind speed and direction to estimate visibility and contamination spread. Loop: incident entered in (1) → map weights updated → RL rerun → route updated.
3. **Supervised demand forecasting.** Learn annual peacetime consumption per item, forecast, and pre-stock. Random Forest is the named model. Preprocessing explicitly removes outliers from training periods and events. Downstream: reorder points, minimum stock levels, and a supply priority ranking factoring importance, urgency (gap between forecast demand and minimum stock), and distance.
4. **Situation-dependent priority weighting (RL).** Wartime → class V (ammunition) and weapons first; peacetime → class I and II (food, clothing); after a strike or CBRN event → class VIII, medical and rescue first. Q-learning, DQN and PPO are all named as candidates, rewarded by how much the supply run mitigates damage.
5. **Soldier behavior model.** Soldiers carry stats (hunger, health, stress, hygiene, all 1–100), vehicles carry durability / load capacity / fuel, buildings carry durability. Stats decay over time and with random events; each supply class restores specific stats (I food → hunger; II bedding/clothing → stress and hygiene; III fuel and lubricants → vehicles; IV construction materials → buildings; V ammunition consumed by training and combat; VI PX goods → stress; VIII medical → health; IX repair parts → vehicle durability). Class VII is equipment rather than issued supply, and class X is out of scope. The objective stated: find the supply plan minimizing total consumption, discarding any run in which a soldier dies or a vehicle/building is destroyed. This is where per-day demand comes from.
6. **Vehicle and driver assignment.** Enumerate available vehicle types (1t / 5t / 25t, small / medium / large bus), match cargo weight or passenger count to vehicle class, enumerate drivers and which classes each may drive, and prefer assigning the *lowest adequate* class so that special-license drivers aren't consumed by jobs anyone can do. Driver count is a hard constraint, so the plan is time-staggered — one item type now, another later.

### The algorithmic flow the proposal describes

Static data (fixed routes) is cached so it isn't recomputed. When an incident is entered, only the affected segment is recomputed via a **dynamic shortest path** approach, evaluating each candidate route's travel time against its risk (enemy positions, road condition, weather). In peacetime the Random Forest forecast drives stocking; in wartime the incident feed drives a PPO policy that re-ranks supply priority, with the soldier as the agent. The re-ranked quantities and the recomputed route are combined into a final plan that tells each driver which vehicle to take on which route.

### Data the team thought they'd need

- Vehicle repair-case records, to train the consumable-replacement/risk prediction.
- Consumption and delivery-time records — placeholder/synthetic at first, with DELLIS as the eventual real source.
- A dataset of where damage actually occurred and of what kind — with an open question flagged in the document about *how* damage gets reported to the system at all (voice? typed reports over the network?), resolved as "through the UI: user adds elements as input, predicted result shown visually as output."
- A dataset of where personnel and supplies were delivered.
- Supply-class definitions (the document links a public wiki page on 보급품 classes).

### Wartime damage model (appendix)

Damage types the appendix defines for the RL environment: chemical / biological / radiological contamination, graded 1st–3rd degree by epicenter, size, wind speed and direction; and kinetic damage split into close-range (~1m radius), ranged (~10m radius), and area weapons such as missiles, where an area threat can be entered either as a *predicted* location (wide area, large damage) or a *confirmed* location (narrower area, very large damage), with routes recomputed accordingly.

### Code written into the document

The document is not only prose: roughly the second half carries eleven Python code blocks, interleaved with the design discussion. **All of them are now extracted into this repo** — the entity model at [`../src/supply_sim/entities.py`](../src/supply_sim/entities.py), everything else under [`proposal-code/`](proposal-code/) with a per-file header and an index in [`proposal-code/README.md`](proposal-code/README.md). They are design-stage sketches, not run code; several cannot run at all, and they are preserved unrepaired.

In document order:

1. **The entity model** — `Soldier` (hunger / health / stress / hygiene), `Vehicle` (durability / capacity / fuel), `Building` (durability), each with `update_stats()` for one tick of decay and `apply_supply(supply_type)` dispatching on the supply class number. This is the concrete form of component 5 above: it is where the per-day demand numbers were supposed to come from. Kept importable at `src/supply_sim/entities.py`.
2. **A positional revision** — an `Entity` base class holding x/y with `distance_to()`, the same three classes re-declared on top of it, and `Soldier.move_towards()` walking one step per call. It drops the stat methods; the document never merges the two revisions.
3. **Three driver loops** — a 100-day loop ticking one soldier, one vehicle and one building and issuing supply class 1, 3 or 4 when hunger, fuel or durability crosses a threshold; then two near-identical rewrites placing five soldiers against two buildings and two vehicles. Both rewrites instantiate a `SoldierAI` class and call `decide_action()` — **neither is ever defined anywhere in the document**. The prose right after says this is where Q-learning, DQN, a behaviour tree or a decision network would go, so `SoldierAI` marks intent rather than work done. The last copy is also physically damaged (brackets closed mid-comment, lost indentation, and the top-level call pulled inside the loop, making it infinitely recursive).
4. **Two `gym.Env` route sketches with PPO** — `PeacefulLogisticsEnv` (5-dim Box state; actions paved / unpaved / tunnel) and `WarLogisticsEnv` (6-dim Box state; actions safe / risky / fast), each trained by stable-baselines3 PPO for 10,000 timesteps. In both, the state transition is fresh random noise and `done` is always `False` — so despite the framing they encode a one-shot preference among three labels, not a path through a map.
5. **`DisasterEnvironment`** — the class meant to carry the supply-*priority* problem the document calls "the most important thing". It is a skeleton: `regions` and `vehicles` are literally `[...]`, and both private methods return names that were never bound.
6. **A Keras `DQN` agent and its training loop** — 2×24 dense net, 2000-entry replay deque, ε-greedy 1.0 → 0.01, paired with `DisasterEnvironment` for 1000 episodes. It cannot run against that skeleton, and it unpacks `step()` as three values where the gym sketches return four.
7. **`MilitaryEnv` + `DQNAgent`** — the longest block, fenced as ```` ```python ```` under a heading that credits ChatGPT. A 10×10 grid, five actions (four directions plus wait), −100 for a damage cell, +100 for the goal. Every movement branch in `step()` is `pass`, and the damage and goal checks read fixed cells that `reset()` never marks — so the agent cannot move and the episode cannot end.

A note between the blocks observes that training everything jointly is too much, so the soldier model should be trained separately and loaded as a fixed input to later training.

The shape of the whole appendix is worth stating plainly: the parts that are complete are the ones that needed no environment (the stat model, the textbook DQN agent), and every block that had to represent the actual map, the actual soldier decision, or the actual priority ranking is a stub.

## Stated intended impact

- Budget freed by better allocation, redirected to equipment or to pay and living conditions.
- Reduced paperwork for supply and transport clerks via DELLIS (supplies) and DTIS (vehicle mileage) integration, plus fewer accidents from advance warning of due consumables and emerging risks.
- Simulation used to size unit manning, easing pressure on conscription numbers.
- Wartime mode giving commanders a live threat picture for faster decisions, and the same tooling feeding more realistic training (KCTC, damage control, emergency rescue, base defense are named).
- Transfer beyond the military: disaster relief and civilian evacuation under unpredictable threat (earthquakes, and the Ukraine–Russia war are cited as motivating cases), and commercial logistics/delivery dispatch.

## Illustrations the document references

The document embeds screenshots described in captions (the images are not reproduced here): the base UI where buildings, threats, troops, vehicles and drivers are placed on a map and a simulation period is set; a before/after threat pair showing a two-vehicle transport plan re-routing around a new red threat marker; a peacetime screen with per-vehicle color-coded routes, a daily transport table, and a week-ahead per-facility material requirement graph; and a route map contrasting an under-trained policy (blue, clipping a missile threat zone) with a trained one (green, fully avoiding it).
