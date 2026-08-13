# -*- coding: utf-8 -*-
"""CLI for the folium route-comparison map (notebooks/folium_route_comparison_map.ipynb)."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from supply_sim.route_map import build_route_comparison_map


def main():
    parser = argparse.ArgumentParser(description="Build the low- vs high-training route comparison map (folium).")
    parser.add_argument("-o", "--output", default="military_route_learning_comparison_with_popups.html",
                        help="Output HTML path (notebook default name)")
    args = parser.parse_args()

    build_route_comparison_map(args.output)
    print(f"Saved map to {args.output}")


if __name__ == "__main__":
    main()
