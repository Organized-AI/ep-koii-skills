#!/usr/bin/env python3
"""
Example: Time-Based Idea Generator
Demonstrates quick composition generation without device connection.
"""

from time_based_generator import TimeBasedGenerator


def demo_without_export():
    """Demo composition generation without exporting to device."""
    print("\n" + "="*60)
    print("  Time-Based Generator - Demo Mode")
    print("  (No device connection required)")
    print("="*60)

    generator = TimeBasedGenerator()

    # Example 1: Generate from current time
    print("\n--- Example 1: Generate from Current Time ---")
    composition1 = generator.generate_from_time()
    print(f"\nGenerated {len(composition1['patterns']['kick']) + len(composition1['patterns']['snare'])} drum hits")

    # Example 2: Generate from bar number
    print("\n--- Example 2: Generate from Bar Number ---")
    composition2 = generator.generate_from_bar(16)
    total_events = sum(len(p) for p in composition2['patterns'].values())
    print(f"\nGenerated {total_events} total events")

    # Example 3: Compare different bar numbers
    print("\n--- Example 3: Compare Different Bars ---")
    for bar_num in [1, 10, 25, 50]:
        comp = generator.generate_from_bar(bar_num)
        meta = comp['metadata']
        print(f"Bar {bar_num:2d}: Density={meta['density']:.0%}, "
              f"Complexity={meta['complexity']:.0%}, "
              f"Events={sum(len(p) for p in comp['patterns'].values())}")

    # Example 4: Examine composition structure
    print("\n--- Example 4: Composition Data Structure ---")
    composition = generator.generate_from_bar(42)
    print("\nMetadata keys:", list(composition['metadata'].keys()))
    print("Pattern keys:", list(composition['patterns'].keys()))
    print("\nFirst kick event:", composition['patterns']['kick'][0] if composition['patterns']['kick'] else "None")

    print("\n" + "="*60)
    print("  Demo Complete!")
    print("  To export to device, use: generator.export_to_sampler()")
    print("="*60 + "\n")


if __name__ == '__main__':
    demo_without_export()
