# -*- coding: utf-8 -*-
"""CLI for the supply-planning flowchart (notebooks/combat_supply_flowchart.ipynb)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supply_sim.flowchart import draw_flowchart


def main():
    argparse.ArgumentParser(
        description="Render the supply route planning flowchart (opens a matplotlib window)."
    ).parse_args()
    draw_flowchart()


if __name__ == "__main__":
    main()
