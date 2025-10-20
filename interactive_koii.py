#!/usr/bin/env python3
"""
EP-133 K.O. II Interactive Demo
Interactive interface for controlling the Koii device via USB-C
"""

from ep_koii_skills import EP133Skill
import sys
import time

def connect_device(skill):
    """Connect to the EP-133 K.O. II device"""
    print("\n" + "=" * 60)
    print("Connecting to EP-133 K.O. II...")
    print("=" * 60)

    ports = skill.list_midi_ports()
    if not ports:
        print("ERROR: No MIDI ports found!")
        return False

    print(f"\nFound {len(ports)} MIDI port(s):")
    for idx, port in enumerate(ports):
        print(f"  [{idx}] {port}")

    # Auto-connect to first port
    print("\nConnecting to first available port...")
    if skill.connect_to_device():
        print("Connected successfully!")
        return True
    else:
        print("Failed to connect!")
        return False

def show_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print("EP-133 K.O. II Interactive Control")
    print("=" * 60)
    print()
    print("1. Play a note (MIDI note number)")
    print("2. Play pad (e.g., A1, B5, C9)")
    print("3. List sound categories")
    print("4. List sounds in category")
    print("5. Search sounds")
    print("6. Play drum pattern")
    print("7. Check connection status")
    print("8. Reconnect device")
    print("9. Exit")
    print()

def play_note(skill):
    """Play a MIDI note"""
    try:
        note = int(input("Enter MIDI note number (36-83): "))
        velocity = int(input("Enter velocity (0-127, default 100): ") or "100")
        duration = float(input("Enter duration in seconds (default 0.2): ") or "0.2")

        print(f"Playing note {note}...")
        if skill.play_note(note, velocity, duration):
            print("Note played successfully!")
        else:
            print("Failed to play note!")
    except ValueError:
        print("Invalid input!")

def play_pad(skill):
    """Play a pad using pad notation"""
    pad = input("Enter pad (e.g., A1, B5, C9): ").strip().upper()
    try:
        note = skill.midi_interface.pad_to_note(pad)
        print(f"Playing pad {pad} (MIDI note {note})...")
        if skill.play_note(note, velocity=100, duration=0.2):
            print("Pad played successfully!")
        else:
            print("Failed to play pad!")
    except Exception as e:
        print(f"Error: {e}")

def list_categories(skill):
    """List all sound categories"""
    print("\nSound Categories:")
    print("-" * 40)
    categories = skill.list_sound_categories()
    for idx, cat in enumerate(categories, 1):
        print(f"  {idx}. {cat}")

def list_sounds(skill):
    """List sounds in a category"""
    category = input("Enter category name: ").strip()
    try:
        sounds = skill.list_sounds_in_category(category)
        print(f"\nSounds in '{category}':")
        print("-" * 40)
        for sound_id, sound_name in sounds.items():
            print(f"  [{sound_id}] {sound_name}")
    except Exception as e:
        print(f"Error: {e}")

def search_sounds(skill):
    """Search for sounds"""
    query = input("Enter search query: ").strip()
    results = skill.search_sounds(query)
    print(f"\nSearch results for '{query}':")
    print("-" * 40)
    if results:
        for sound_id, sound_name in results.items():
            print(f"  [{sound_id}] {sound_name}")
    else:
        print("  No sounds found!")

def play_pattern(skill):
    """Play a simple drum pattern"""
    print("\nPlaying demo drum pattern...")
    pattern = [
        (36, 100),  # Kick
        (38, 80),   # Snare
        (42, 60),   # Hi-hat
        (38, 80),   # Snare
    ]

    for _ in range(2):  # Play pattern twice
        for note, velocity in pattern:
            skill.play_note(note, velocity, 0.15)
            time.sleep(0.1)

    print("Pattern completed!")

def main():
    """Main interactive loop"""
    print("\n" + "=" * 60)
    print("EP-133 K.O. II Interactive Interface")
    print("=" * 60)

    skill = EP133Skill()

    # Connect to device
    if not connect_device(skill):
        print("\nCannot continue without device connection.")
        return 1

    # Main loop
    while True:
        show_menu()
        choice = input("Select option (1-9): ").strip()

        if choice == "1":
            play_note(skill)
        elif choice == "2":
            play_pad(skill)
        elif choice == "3":
            list_categories(skill)
        elif choice == "4":
            list_sounds(skill)
        elif choice == "5":
            search_sounds(skill)
        elif choice == "6":
            play_pattern(skill)
        elif choice == "7":
            status = "Connected" if skill.is_connected() else "Not connected"
            print(f"\nConnection status: {status}")
        elif choice == "8":
            skill.disconnect_device()
            connect_device(skill)
        elif choice == "9":
            print("\nDisconnecting and exiting...")
            skill.disconnect_device()
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
