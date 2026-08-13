# UNRUN DESIGN SKETCH - reproduced verbatim from the 2024 Defense AI Ideathon
# planning document (see docs/proposal-summary.md). Not run code: it was never
# executed, and it is not imported or tested by anything in this repository.
# The only change is decoding the HTML entities that .docx text extraction
# introduced (&lt; &gt; &quot;). Korean comments are the author's.
#
# A second copy of the same loop appearing a few lines later in the document,
# after the note about the soldier AI mechanism.  It differs only by damage
# picked up in the document itself: the list brackets are closed mid-comment,
# the section comments lost their indentation, and the final run_simulation()
# call ended up *inside* the day loop, making the function infinitely
# recursive.  Kept because it is what the document contains; do not repair it.
# It carries the same undefined SoldierAI / decide_action as the previous file.

def run_simulation():
    # 건물과 차량을 좌표에 배치
    buildings = [
        Building(10, 10),  # 식당 위치 (1종 보급)
        Building(50, 50), ] # 의무대대 위치 (8종 보급) 
    vehicles = [
        Vehicle(20, 20),  # 차량 1 위치
        Vehicle(30, 30),  ]# 차량 2 위치
    
    # 병사들을 초기 위치에 배치
    soldiers = [SoldierAI(0, 0) for _ in range(5)]  # 5명의 병사
    
    for day in range(1, 101):  # 100일 동안의 시뮬레이션
        print(f"\nDay {day}")
                # 병사들의 행동 결정 및 실행
        for soldier in soldiers:
            soldier.decide_action(buildings, vehicles)
            soldier.update_stats()
                # 현재 상태 출력
        for i, soldier in enumerate(soldiers):
            print(f"Soldier {i+1} - Location: ({soldier.x:.2f}, {soldier.y:.2f}) Hunger: {soldier.hunger:.2f}, Health: {soldier.health:.2f}")
        run_simulation()
