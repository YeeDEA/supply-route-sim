# -*- coding: utf-8 -*-
"""Matplotlib flowchart of the supply-planning decision process.

Extracted from notebooks/combat_supply_flowchart.ipynb (code cell 0),
verbatim.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw_flowchart():
    plt.figure(figsize=(14, 10))
    ax = plt.gca()

    # Define positions for the flowchart elements
    positions = {
        'start': (0.5, 0.9),
        'user_input': (0.5, 0.75),
        'attack_info': (0.5, 0.6),
        'environment_data': (0.3, 0.45),
        'threat_detection': (0.7, 0.45),
        'plan_route': (0.5, 0.3),
        'delivery_priority': (0.5, 0.15),
        'optimal_route': (0.2, 0),
        'vehicle_selection': (0.8, 0),
        'end': (0.5, -0.1)
    }

    # Define the shapes and their labels
    shapes = {
        'start': ("start", "Start"),
        'user_input': ("rect", "User Input"),
        'attack_info': ("rect", "Attack Information Input"),
        'environment_data': ("rect", "Environmental Data"),
        'threat_detection': ("rect", "Threat Detection"),
        'plan_route': ("rect", "Route Planning"),
        'delivery_priority': ("rect", "Supply Priority Adjustment"),
        'optimal_route': ("rect", "Optimal Route Proposal"),
        'vehicle_selection': ("rect", "Vehicle and Driver Selection"),
        'end': ("end", "End")
    }

    # Draw the flowchart elements
    for key, (shape_type, label) in shapes.items():
        if shape_type == "rect":
            ax.add_patch(mpatches.Rectangle(positions[key], 0.2, 0.1, fill=True, color='lightblue', edgecolor='black'))
        elif shape_type == "start" or shape_type == "end":
            ax.add_patch(mpatches.Circle(positions[key], 0.1, color='lightgreen' if shape_type == "start" else 'lightcoral', edgecolor='black'))

        ax.text(positions[key][0] + 0.1, positions[key][1] + 0.05, label, ha='center', va='center', fontsize=12)

    # Draw arrows between the elements
    arrows = [
        ('start', 'user_input'),
        ('user_input', 'attack_info'),
        ('user_input', 'environment_data'),
        ('attack_info', 'threat_detection'),
        ('environment_data', 'plan_route'),
        ('threat_detection', 'plan_route'),
        ('plan_route', 'delivery_priority'),
        ('delivery_priority', 'optimal_route'),
        ('optimal_route', 'vehicle_selection'),
        ('vehicle_selection', 'end'),
    ]

    for start_key, end_key in arrows:
        start_pos = positions[start_key]
        end_pos = positions[end_key]
        ax.annotate('', xy=end_pos, xycoords='data', xytext=start_pos, textcoords='data',
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

    # Set limits and hide axes
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.15, 1)
    ax.axis('off')

    # Add title
    plt.title("Supply Route Planning Flowchart in Combat Situation", fontsize=16)

    plt.show()
