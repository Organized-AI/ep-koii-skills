# Quick Start Guide: Connect to Koii via USB-C

This guide will help you load the interface and connect to your EP-133 K.O. II (Koii) device via USB-C.

## Prerequisites

1. **EP-133 K.O. II device** powered on
2. **USB-C cable** connected between computer and device
3. **Python 3.8+** installed

## Setup

### 1. Install the Package

```bash
# Install in development mode
pip install -e .
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mido` - MIDI library for USB communication
- `python-dotenv` - Environment configuration
- `pydantic` - Data validation

### 3. Verify MIDI Port Access

On Linux, you may need to add your user to the `audio` group:

```bash
sudo usermod -a -G audio $USER
```

Then log out and log back in.

## Connect to Koii

### Option 1: Simple Connection Script

Run the connection test script:

```bash
python3 connect_koii.py
```

This will:
1. Load the EP-133 interface
2. Scan for available MIDI ports
3. Connect to the Koii device
4. Play a test note
5. Display available sound categories

### Option 2: Interactive Demo

For full interactive control:

```bash
python3 interactive_koii.py
```

Features:
- Play notes by MIDI number
- Play pads using pad notation (A1, B5, etc.)
- Browse sound library (240+ sounds)
- Search sounds by name
- Play drum patterns
- Real-time connection management

### Option 3: Python Code

```python
from ep_koii_skills import EP133Skill

# Load the interface
skill = EP133Skill()

# List available MIDI ports
ports = skill.list_midi_ports()
print(f"Available ports: {ports}")

# Connect to device (auto-selects first port)
if skill.connect_to_device():
    print("Connected!")

    # Play a note
    skill.play_note(60, velocity=100, duration=0.2)

    # Browse sounds
    categories = skill.list_sound_categories()
    kicks = skill.list_sounds_in_category("Kicks")

    # Disconnect
    skill.disconnect_device()
else:
    print("Connection failed!")
```

## Troubleshooting

### No MIDI Ports Found

**Check:**
- Device is powered on
- USB-C cable is properly connected
- Device shows up in system USB devices: `lsusb`

**On Linux:**
```bash
# Check if device is detected
lsusb | grep -i teenage

# Check ALSA MIDI ports
aconnect -l
```

**On macOS:**
```bash
# Check Audio MIDI Setup
open "/Applications/Utilities/Audio MIDI Setup.app"
```

**On Windows:**
- Install MIDI drivers if needed
- Check Device Manager for MIDI devices

### Permission Denied

On Linux, ensure you're in the `audio` group:

```bash
groups | grep audio
```

If not listed, add yourself and restart:

```bash
sudo usermod -a -G audio $USER
```

### Connection Succeeds But No Sound

- Check device volume
- Verify output routing on EP-133
- Try different MIDI channels (default is channel 0)

### Import Errors

Make sure the package is installed:

```bash
pip install -e .
```

## Next Steps

Once connected, explore the full API:

- **MIDI Control**: `play_note()`, `pad_to_note()`
- **Sound Browser**: `list_sound_categories()`, `search_sounds()`
- **Device Management**: `connect_to_device()`, `disconnect_device()`

See the main README for complete documentation.

## Support

For issues:
- Check device connection and power
- Verify MIDI port permissions
- Review error messages in console
- Check EP-133 firmware is up to date

## Examples

### Play a Drum Pattern

```python
skill = EP133Skill()
skill.connect_to_device()

# Kick, snare, hat, snare pattern
pattern = [36, 38, 42, 38]
for note in pattern:
    skill.play_note(note, velocity=100, duration=0.15)
    import time
    time.sleep(0.1)

skill.disconnect_device()
```

### Browse and Search Sounds

```python
skill = EP133Skill()
skill.connect_to_device()

# List all categories
print(skill.list_sound_categories())

# Get kicks
kicks = skill.list_sounds_in_category("Kicks")
print(f"Found {len(kicks)} kicks")

# Search for specific sounds
bass_sounds = skill.search_sounds("bass")
print(bass_sounds)

skill.disconnect_device()
```

Happy music making!
