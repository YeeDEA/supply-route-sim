# -*- coding: utf-8 -*-
"""CLI for the OR-Tools CVRP supply-routing scenario (notebooks/ortools_cvrp_supply_routing.ipynb)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supply_sim.cvrp import main as solve


def main():
    argparse.ArgumentParser(
        description="Solve the fixed CVRP scenario: 1 depot + 5 delivery points, 2 vehicles of capacity 3."
    ).parse_args()
    solve()


if __name__ == "__main__":
    main()
