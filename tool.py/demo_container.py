#!/usr/bin/env python3
"""
Demonstration of container at coordinates (5,5) to (15,10)
This script shows how the container works with various text placements.
"""

import sys
import os
import time
import types

# Add the tool.py directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import Display

def demo_container():
    """Demonstrate the container at (5,5) to (15,10)"""
    # Mock terminal size for demo purposes (in case running without a terminal)
    try:
        # Try to get real terminal size
        os.get_terminal_size()
    except OSError:
        # If no terminal, use a mock size
        os.get_terminal_size = lambda: types.SimpleNamespace(columns=80, lines=24)
    
    d = Display()
    
    print("\n=== Container Demo at (5,5) to (15,10) ===\n")
    
    # Create the container
    # Container spans from (5,5) to (15,10), giving us 11x6 character space
    d.container(5, 5, 15, 10, "demo_box")
    
    # Add border visualization (fits within 11-char width)
    # Top border (11 chars total)
    d.text("+---------+", 0, 0, container=["demo_box"])
    
    # Side borders and content area
    for i in range(1, 5):
        d.text("|", 0, i, container=["demo_box"])
        d.text("|", 9, i, container=["demo_box"])
    
    # Bottom border
    d.text("+---------+", 0, 5, container=["demo_box"])
    
    # Add text inside the container (within the border area)
    d.text("Test Box", 1, 1, container=["demo_box"])
    d.text("(5,5) to", 1, 2, container=["demo_box"])
    d.text("(15,10)", 1, 3, container=["demo_box"])
    
    # Add legend outside container
    d.text("Legend:", 0, 0)
    d.text("- Container boundaries: (5,5) to (15,10)", 0, 1)
    d.text("- Container size: 11 cols x 6 rows", 0, 2)
    d.text("- Text is positioned relative to container origin", 0, 3)
    
    # Render the display
    d.freeze()
    d.render()
    d.unfreeze()
    
    print("\nContainer demonstration complete!")
    print("The container has been rendered at coordinates (5,5) to (15,10)")
    print("Text inside is positioned relative to the container's origin.")

if __name__ == "__main__":
    demo_container()
