# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# Document heading: "시뮬레이션 예시" ("simulation example")
#
# 100-day driver loop over one soldier, one vehicle and one building: tick the
# stats, then issue supply class 1 / 3 / 4 whenever hunger, fuel or building
# durability crosses a threshold.  Expects the *first* revision of the entity
# classes (no-argument constructors) - i.e. src/supply_sim/entities.py - which
# is not imported here because the document's block had no import line.

def run_simulation():
    soldier = Soldier()
    vehicle = Vehicle()
    building = Building()
    
    for day in range(1, 101):  # 100일 동안의 시뮬레이션
        print(f"\nDay {day}")
        
        # 병사, 차량, 건물의 스탯 업데이트
        soldier.update_stats()
        vehicle.update_stats()
        building.update_stats()
        
        # 특정 조건에서 보급품 제공
        if soldier.hunger < 30:
            soldier.apply_supply(1)  # 1종 보급품 제공
        if vehicle.fuel < 20:
            vehicle.apply_supply(3)  # 3종 보급품 제공
        if building.durability < 50:
            building.apply_supply(4)  # 4종 보급품 제공
        
        # 현재 스탯 출력
        print(f"Soldier - Hunger: {soldier.hunger:.2f}, Health: {soldier.health:.2f}, Stress: {soldier.stress:.2f}, Hygiene: {soldier.hygiene:.2f}")
        print(f"Vehicle - Durability: {vehicle.durability:.2f}, Fuel: {vehicle.fuel:.2f}")
        print(f"Building - Durability: {building.durability:.2f}")
    
run_simulation()
