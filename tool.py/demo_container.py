#!/usr/bin/env python3
"""
Demonstration of container at coordinates (5,5) to (15,10)
This script shows how the container works with various text placements.
"""

import sys
import os
import time

# Add the tool.py directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import Display

def demo_container():
    """Demonstrate the container at (5,5) to (15,10)"""
    d = Display()
    
    print("\n=== Container Demo at (5,5) to (15,10) ===\n")
    
    # Create the container
    d.container(5, 5, 15, 10, "demo_box")
    
    # Add border visualization
    # Top border
    d.text("+-----------+", 0, 0, container=["demo_box"])
    
    # Side borders and content area
    for i in range(1, 5):
        d.text("|", 0, i, container=["demo_box"])
        d.text("|", 10, i, container=["demo_box"])
    
    # Bottom border
    d.text("+-----------+", 0, 5, container=["demo_box"])
    
    # Add text inside the container
    d.text("Container", 1, 1, container=["demo_box"])
    d.text("at (5,5)", 1, 2, container=["demo_box"])
    d.text("to (15,10)", 1, 3, container=["demo_box"])
    
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
