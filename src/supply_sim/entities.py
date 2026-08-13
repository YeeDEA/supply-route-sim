"""Simulation entity model from the ideathon planning document.

Unlike the rest of ``supply_sim``, this module does **not** come from a
notebook.  It is the entity code written directly into the 2024 Defense AI
Ideathon planning document (summarized in ``docs/proposal-summary.md``),
under the heading "병사와 차량, 건물과 재고량을 정의하는 클래스 구현"
("implement the classes defining soldiers, vehicles, buildings and stock").
It is reproduced verbatim below, changed only by decoding the HTML entities
(``&lt;``, ``&gt;``, ``&quot;``) that the .docx text extraction introduced.
Comments are the author's and are left in Korean.

What it encodes: a soldier carries hunger / health / stress / hygiene, a
vehicle carries durability / capacity / fuel, a building carries durability.
``update_stats()`` is one tick of decay (plus a 1% chance of a large
durability drop for vehicles and buildings); ``apply_supply(supply_type)``
applies the effect of one Korean military supply class (1 food, 2
bedding/clothing, 3 fuel, 4 construction materials, 5 ammunition, 8 medical,
9 repair parts).  Nothing clamps the stats to 1-100 even though the proposal
text describes them that way, and death/destruction only print a message
rather than removing the entity - both are as written.

Relationship to the notebooks
-----------------------------
``notebooks/logistics_sim_tkinter_v1.ipynb`` (and the ``_folium_v2`` follow-up,
which carries an identical copy) implements a *reduced* version of this model,
not this code.  Its ``Soldier`` uses the same four stat names - hunger, health,
stress, hygiene - but takes them as constructor arguments alongside a ``name``,
and its only supply behaviour is ``consume_supply(supply)``, which adds a food
``Supply``'s ``effect_on_stats["hunger"]`` while hunger is below 100.  The
notebook has no per-tick decay, no supply-class dispatch, and no ``Vehicle`` or
``Building`` class at all (buildings there are ``(x, y)`` tuples drawn on a
tkinter canvas).  So the stat vocabulary carried over into the simulator; the
decay-and-resupply mechanics below never did.

A later revision in the same document re-declares these three classes with x/y
coordinates and a ``move_towards()`` method, and the driver loops that use them
are preserved separately - see ``docs/proposal-code/``.  None of that code was
ever run; this module is kept importable so the stat model can be read and
exercised, but it too was never part of a working system.
"""

import random

class Soldier:
    def __init__(self):
        self.hunger = 100  # 배고픔: 0이 되면 체력 감소
        self.health = 100  # 체력: 0이 되면 사망
        self.stress = 0    # 스트레스: 높아지면 체력 감소
        self.hygiene = 100 # 위생: 낮아지면 체력 감소
    
    def update_stats(self):
        # 시간에 따른 자연스러운 스탯 감소
        self.hunger -= random.uniform(0.1, 0.5)
        self.hygiene -= random.uniform(0.1, 0.5)
        
        # 배고픔과 위생이 0이 되면 체력이 급격히 감소
        if self.hunger <= 0 or self.hygiene <= 0:
            self.health -= random.uniform(1, 5)
        
        # 스트레스가 높아지면 체력이 감소
        if self.stress > 80:
            self.health -= random.uniform(0.1, 0.5)
        
        # 체력이 0이 되면 사망 처리
        if self.health <= 0:
            print("병사가 사망했습니다.")
    
    def apply_supply(self, supply_type):
        if supply_type == 1:  # 1종 보급품
            self.hunger += random.uniform(20, 40)
            self.stress -= random.uniform(5, 10)
            self.health += random.uniform(10, 20)
            self.hygiene += random.uniform(5, 10)
        elif supply_type == 2:  # 2종 보급품
            self.stress -= random.uniform(10, 20)
            self.health += random.uniform(5, 10)
            self.hygiene += random.uniform(10, 30)
        elif supply_type == 5:  # 5종 보급품 (탄약 훈련 시)
            self.stress += random.uniform(5, 15)
        elif supply_type == 8:  # 8종 보급품 (의무대대)
            self.health += random.uniform(50, 100)

class Vehicle:
    def __init__(self):
        self.durability = 100  # 내구성: 0이 되면 차량 파괴
        self.capacity = 100    # 적재용량: 물품이 실릴수록 감소
        self.fuel = 100        # 연료 지수: 0이 되면 차량 이동 불가
    
    def update_stats(self):
        # 시간 경과에 따른 내구성 감소 및 확률적 큰 감소
        self.durability -= random.uniform(0.1, 0.5)
        if random.uniform(0, 1) < 0.01:  # 1% 확률로 큰 감소
            self.durability -= random.uniform(5, 10)
        
        # 적재량이 90% 이상일 때 내구성 비례 감소
        if self.capacity > 90:
            self.durability -= (self.capacity - 90) * 0.1
        
        # 연료가 부족하면 경고 출력
        if self.fuel <= 0:
            print("연료가 부족하여 차량이 멈췄습니다.")
    
    def apply_supply(self, supply_type):
        if supply_type == 3:  # 3종 보급품 (연료 보급)
            self.fuel += random.uniform(30, 70)
        elif supply_type == 9:  # 9종 보급품 (정비 보급)
            self.durability += random.uniform(30, 70)

class Building:
    def __init__(self):
        self.durability = 100  # 내구도: 0이 되면 건물 파괴
    
    def update_stats(self):
        # 시간에 따른 내구도 감소 및 확률적 큰 감소
        self.durability -= random.uniform(0.1, 0.5)
        if random.uniform(0, 1) < 0.01:  # 1% 확률로 큰 감소
            self.durability -= random.uniform(5, 10)
        
        # 내구도가 0이 되면 건물이 파괴됨
        if self.durability <= 0:
            print("건물이 파괴되었습니다.")
    
    def apply_supply(self, supply_type):
        if supply_type == 4:  # 4종 보급품 (수리 보급)
            self.durability += random.uniform(50, 100)
