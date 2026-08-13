# -*- coding: utf-8 -*-
"""Capacitated vehicle routing (CVRP) for supply distribution with OR-Tools.

Extracted from notebooks/ortools_cvrp_supply_routing.ipynb (code cell 1).
Scenario: 1 depot + 5 delivery points, 2 vehicles of capacity 3,
Euclidean distances. Code is the notebook cell verbatim; only the module-level
`distance_matrix` computation was moved inside create_data_model() so the
module has no import-time side effects.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

# 위치 정의: 본부와 각 목적지의 (x, y) 좌표
locations = [
    (0, 0),   # 본부
    (-5, 2),  # 목적지 A
    (7, 3),   # 목적지 B
    (-4, -6), # 목적지 C
    (4, -7),  # 목적지 D
    (1, 8)    # 목적지 E
]


# 거리 계산 함수 (유클리드 거리)
def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = math.sqrt(
                    (from_node[0] - to_node[0]) ** 2 +
                    (from_node[1] - to_node[1]) ** 2
                )
    return distances


# 차량 경로 최적화 문제 정의
def create_data_model():
    # 거리 행렬 생성
    distance_matrix = compute_euclidean_distance_matrix(locations)

    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 2  # 차량 2대 사용
    data['depot'] = 0  # 본부 위치 (index 0)

    # 각 목적지에 필요한 물자량 (여기서는 목적지마다 동일하게 1로 설정)
    data['demands'] = [0, 1, 1, 1, 1, 1]
    # 각 차량의 최대 용량을 3으로 설정
    data['vehicle_capacities'] = [3, 3]

    return data


# 용량 제한을 설정하는 부분 추가
def add_capacity_constraints(routing, manager, data):
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, # 각 경로의 물자량을 계산하는 콜백 함수
        0,  # 용량 초과를 허용하지 않음
        data['vehicle_capacities'],  # 각 차량의 용량
        True,  # 경로 시작 시 용량을 0으로 설정
        'Capacity'
    )


# 결과를 출력하는 함수
def print_solution(manager, routing, solution):
    print('Objective: {} meters'.format(solution.ObjectiveValue()))
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        print('Route for vehicle {}:'.format(vehicle_id))
        route_distance = 0
        while not routing.IsEnd(index):
            print(' {} ->'.format(manager.IndexToNode(index)), end='')
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        print(' {}'.format(manager.IndexToNode(index)))
        print('Distance of the route: {} meters'.format(route_distance))


def main():
    data = create_data_model()

    # 경로 관리 객체 생성
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # 거리 계산을 위한 콜백 함수
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 용량 제한 추가
    add_capacity_constraints(routing, manager, data)

    # 탐색 전략 설정
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # 경로 계산
    solution = routing.SolveWithParameters(search_parameters)

    # 결과 출력
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()
