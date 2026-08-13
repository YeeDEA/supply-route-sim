# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# Document heading: "병사, 차량, 건물의 위치 클래스 추가"
#   ("add position classes for soldiers, vehicles and buildings")
#
# Second revision of the entity model: an Entity base class holding x/y with
# distance_to(), and Soldier/Vehicle/Building re-declared on top of it.  This
# revision drops update_stats() and apply_supply() - the document never merges
# the two revisions into one class set.  The stat-carrying first revision is
# the one kept importable, at src/supply_sim/entities.py.

import random
import math

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, target):
        """목표까지의 거리를 계산"""
        return math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)

class Soldier(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hunger = 100
        self.health = 100
        self.stress = 0
        self.hygiene = 100
    
    def move_towards(self, target):
        """목표 건물이나 차량으로 이동"""
        step_size = 1  # 한 번에 이동하는 거리
        if self.distance_to(target) > step_size:
            angle = math.atan2(target.y - self.y, target.x - self.x)
            self.x += step_size * math.cos(angle)
            self.y += step_size * math.sin(angle)
        else:
            self.x, self.y = target.x, target.y  # 목표에 도착

class Vehicle(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.durability = 100
        self.capacity = 100
        self.fuel = 100

class Building(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.durability = 100
