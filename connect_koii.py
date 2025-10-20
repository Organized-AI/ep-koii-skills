#!/usr/bin/env python3
"""
EP-133 K.O. II USB-C Connection Example
Connect to the Teenage Engineering EP-133 K.O. II via USB-C
"""

from ep_koii_skills import EP133Skill
import sys

def main():
    print("=" * 60)
    print("EP-133 K.O. II (Koii) - USB-C Connection Interface")
    print("=" * 60)
    print()

    # Step 1: Load the interface
    print("[1/4] Loading EP-133 K.O. II interface...")
    skill = EP133Skill()
    print("      Interface loaded successfully!")
    print()

    # Step 2: List available MIDI ports
    print("[2/4] Scanning for available MIDI ports...")
    ports = skill.list_midi_ports()

    if not ports:
        print("      ERROR: No MIDI ports found!")
        print("      Please ensure:")
        print("      - EP-133 K.O. II is powered on")
        print("      - USB-C cable is connected")
        print("      - Device drivers are installed")
        sys.exit(1)

    print(f"      Found {len(ports)} MIDI port(s):")
    for idx, port in enumerate(ports):
        print(f"      [{idx}] {port}")
    print()

    # Step 3: Connect to the device
    print("[3/4] Connecting to EP-133 K.O. II via USB-C...")

    # Try to auto-detect EP-133 port or use first available port
    ep133_port_idx = None
    for idx, port in enumerate(ports):
        if "EP-133" in port or "KO II" in port or "Teenage" in port:
            ep133_port_idx = idx
            break

    if ep133_port_idx is not None:
        print(f"      Auto-detected EP-133 at port [{ep133_port_idx}]")
        success = skill.connect_to_device(port_index=ep133_port_idx)
    else:
        print(f"      Connecting to first available port...")
        success = skill.connect_to_device()

    if not success:
        print("      ERROR: Failed to connect to device!")
        sys.exit(1)

    print("      Connected successfully!")
    print()

    # Step 4: Verify connection
    print("[4/4] Verifying connection...")
    if skill.is_connected():
        print("      Connection verified!")
        print()
        print("=" * 60)
        print("SUCCESS: EP-133 K.O. II is ready!")
        print("=" * 60)
        print()

        # Show available sound categories
        print("Available Sound Categories:")
        categories = skill.list_sound_categories()
        for cat in categories:
            print(f"  - {cat}")
        print()

        # Demo: Play a test note
        print("Playing test note (MIDI note 60 = Middle C)...")
        skill.play_note(60, velocity=100, duration=0.2)
        print("Test note played!")
        print()

        # Cleanup
        print("Disconnecting...")
        skill.disconnect_device()
        print("Disconnected successfully!")

        return 0
    else:
        print("      ERROR: Connection verification failed!")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
