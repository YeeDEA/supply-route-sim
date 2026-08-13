# -*- coding: utf-8 -*-
"""Folium map comparing a low-training vs high-training supply route.

Extracted from notebooks/folium_route_comparison_map.ipynb (code cell 0).
The notebook was a top-level script building and saving one map; here it is
wrapped in build_route_comparison_map() with the save path as a parameter.
All coordinates and data are the notebook's synthetic Seoul scenario, verbatim.
"""

import folium
from folium.features import DivIcon  # noqa: F401  (imported in the notebook, unused there too)
from folium.map import Popup  # noqa: F401

# 군사 시설 좌표 (Barracks, Supply Depot, Command HQ)
military_facilities = {
    "Barracks (옥인동)": [37.5826, 126.9667],
    "Supply Depot (신문로1가)": [37.5697, 126.9696],
    "Command HQ (소격동)": [37.5838, 126.9811],
}

# 위협 지역 (미사일 위협과 스나이퍼 존, 운니동)
threats = {
    "Missile Threat (미사일 위협)": {"location": [37.5742, 126.9706], "radius": 300, "damage": "High", "type": "Explosive"},
    "Sniper Zone (스나이퍼 존)": {"location": [37.574, 126.992], "radius": 200, "damage": "Medium", "type": "Ballistic"},
}

# 경로 1: 학습이 덜 된 경로 (미사일 위협을 아슬아슬하게 피함)
route_low_learning = [
    [37.5826, 126.9667],  # Barracks
    [37.581, 126.970],    # 경유지 1
    [37.581, 126.970],    # 경유지 1

    [37.579, 126.972],    # 경유지 2
    [37.577, 126.974],    # 경유지 3 (Missile Threat 근처)
    [37.575, 126.975],    # Missile Threat 근처
    [37.573, 126.973],    # 경유지 4
    [37.570, 126.971],    # Supply Depot 근처
    [37.5697, 126.9696],  # Supply Depot
    [37.572, 126.976],    # 경유지 5
    [37.575, 126.977],    # 경유지 6 (Missile Threat 근처)
    [37.578, 126.979],    # 경유지 7
    [37.5838, 126.9811]   # Command HQ
]

# 경로 2: 학습이 많이 된 경로 (미사일 위협을 완전히 회피)
route_high_learning = [
    [37.5826, 126.9667],  # Barracks
    [37.581, 126.968],    # 경유지 1
    [37.579393,126.968517],    # 경유지 2
    [37.578, 126.968],    # 경유지 3
    [37.576, 126.967],    # 경유지 4 (Missile Threat 완전 회피)
    [37.574, 126.965],    # 경유지 5
    [37.572, 126.965],    # 경유지 6 (Supply Depot 근처)
    [37.5697, 126.9696],  # Supply Depot
    [37.571, 126.974],    # 경유지 7
    [37.573, 126.976],    # 경유지 8
    [37.575, 126.978],    # 경유지 9
    [37.5838, 126.9811]   # Command HQ
]


def build_route_comparison_map(output_path="military_route_learning_comparison_with_popups.html"):
    """Build the comparison map and save it to output_path. Returns the map."""
    # 지도 생성 (서울 중심 좌표)
    m = folium.Map(location=[37.58, 126.98], zoom_start=14)

    # 군사 시설 마커 추가 (팝업 자동 표시 설정)
    for base, loc in military_facilities.items():
        folium.Marker(
            location=loc,
            popup=folium.Popup(f"<b>{base}</b><br>Coordinates: {loc}", show=True),
            icon=folium.Icon(color="blue")
        ).add_to(m)

    # 위협 지역 표시 (위협의 종류, 범위, 피해량 기본 표시)
    for threat, info in threats.items():
        folium.Circle(
            location=info["location"],
            radius=info["radius"],
            color='red',
            fill=True,
            fill_opacity=0.4,
            popup=folium.Popup(f"<b>Threat: {threat}</b><br>Type: {info['type']}<br>Range: {info['radius']}m<br>Damage: {info['damage']}", show=True)
        ).add_to(m)

    # 경로 표시 (학습이 덜 된 경로)
    folium.PolyLine(
        locations=route_low_learning,
        color="blue",
        weight=5,
        opacity=0.6,
        popup=folium.Popup("Low AI Learning - Near Missile Threat", show=True)
    ).add_to(m)

    # 경로 표시 (학습이 많이 된 경로)
    folium.PolyLine(
        locations=route_high_learning,
        color="green",
        weight=5,
        opacity=0.6,
        popup=folium.Popup("High AI Learning - Avoiding Missile Threat", show=True)
    ).add_to(m)

    # 지도 저장 및 출력
    m.save(output_path)
    return m
