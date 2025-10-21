# Time-Based Idea Generator

Quickly compose musical ideas based on clock time or bar segments and export them directly to your EP-133 K.O. II sampler via USB-C.

## Overview

The Time-Based Idea Generator helps you get ideas onto the sampler quickly by:
- **Clock Mode**: Generates unique beats based on the current time (HH:MM:SS)
- **Bar Mode**: Generates beats based on musical bar/measure numbers
- **Sound Compatibility Analysis**: Automatically checks if sounds work well together
- **Instant Export**: Send compositions directly to the sampler via USB-C MIDI

Each time or bar number creates a deterministic, reproducible composition, making it easy to iterate and return to ideas. Every composition is automatically analyzed for sound compatibility before export!

## Quick Start

### Using Slash Commands (Fastest!)

```bash
/koii-time   # Generate from current time and export to sampler
/koii-bar    # Generate from bar number and export to sampler
```

### Using the Python Script

```bash
# Interactive mode
python time_based_generator.py

# Or use it programmatically
python -c "from time_based_generator import TimeBasedGenerator; g = TimeBasedGenerator(); g.generate_from_time(); g.export_to_sampler()"
```

## How It Works

### Clock Mode

The current time (HH:MM:SS) is converted into a numeric seed:
- `14:30:45` → seed: `143045`
- This seed determines:
  - **Density**: How many hits/events in the pattern (0-100%)
  - **Complexity**: Pattern intricacy (simple → intricate)
  - **Sound selection**: Which kick/snare/hat variants to use
  - **Velocity variations**: Hit dynamics

**Same time = Same composition** (deterministic)

### Bar Mode

A bar/measure number creates the seed:
- `Bar 1` → seed: `1000`
- `Bar 42` → seed: `42000`

This is useful for:
- Creating a series of related ideas
- Building song sections (Bar 1 = intro, Bar 2 = verse, etc.)
- Collaborative workflows (share bar numbers)

## Composition Elements

Generated compositions include:

### Kick Pattern
- Standard on beats 1 and 3
- Additional hits based on density
- Velocity range: 60-127
- 5 kick sound variants

### Snare Pattern
- Standard on beats 2 and 4
- Ghost notes based on density
- Velocity range: 40-120
- 3 snare sound variants

### Hi-Hat Pattern
- Varies from quarter notes → sixteenth notes (complexity)
- Mix of closed and open hats (20% open)
- Velocity range: 50-110
- Accent variations based on density

### Percussion
- Added for complex patterns (complexity > 30%)
- Claps, toms, and other percussion
- Sporadic placement
- 3 percussion variants

## Sound Compatibility Analysis

Every composition is automatically analyzed to ensure sounds work well together! The analyzer checks:

### What's Analyzed

1. **Sound Families**: Checks if sounds come from compatible families (NT, MICRO, S95X, etc.)
2. **Category Balance**: Ensures proper mix of kicks, snares, hats
3. **Timbre Compatibility**: Analyzes warmth, brightness, and tonal characteristics
4. **Style Kit Matching**: Identifies which pre-defined kit your sounds match

### Compatibility Ratings

- **EXCELLENT (85-100%)**: Sounds work very well together - export confidently!
- **GOOD (70-84%)**: Good compatibility - should sound cohesive
- **ACCEPTABLE (55-69%)**: May work, consider refining sound selection
- **NEEDS IMPROVEMENT (<55%)**: Consider different sound combinations

### Example Output

```
🎵 SOUND COMPATIBILITY ANALYSIS
--------------------------------------------------------
Rating:      EXCELLENT (99%)
Verdict:     These sounds will work very well together!
Style Kit:   Natural Kit

Sound Details:
  • NT KICK (NT family, warm timbre: acoustic, low-frequency, organic)
  • NT SNARE (NT family, warm timbre: acoustic, natural, organic)
  • NT HH CLOSED B (NT family, warm timbre: high-frequency, natural, organic)

Families:    NT
Timbres:     warm
```

### Why This Matters

Before exporting to your sampler, you can:
- **Verify coherence**: Ensure sounds will blend well musically
- **Identify issues**: Catch incompatible sound combinations early
- **Learn patterns**: Understand which sound families work together
- **Save time**: Avoid exporting beats that won't sound good

For detailed information, see [SOUND_COMPATIBILITY.md](SOUND_COMPATIBILITY.md).

## Musical Parameters

Default settings (can be modified in the script):
- **BPM**: 120
- **Bars**: 4
- **Time Signature**: 4/4
- **Resolution**: 16th notes (64 steps per 4 bars)

## Usage Examples

### Interactive CLI

```bash
python time_based_generator.py
```

```
EP-133 K.O. II - Time-Based Idea Generator
============================================================

Commands:
  1 - Generate from current time
  2 - Generate from bar number
  3 - Export current composition to sampler
  4 - Generate & export from time (quick workflow)
  5 - Generate & export from bar (quick workflow)
  q - Quit
```

### Quick Workflows

**Option 4**: Generate from time and immediately export
```
> 4

🕐 Generating from time: 14:23:17
   Seed: 142317

  COMPOSITION SUMMARY
============================================================
  Mode:       CLOCK
  Seed:       142317
  Time:       14:23:17
  BPM:        120
  Density:    17%
  Complexity: 34%

  Pattern Elements:
    • Kicks:      10 hits
    • Snares:     12 hits
    • Hi-hats:    32 hits
    • Percussion: 5 hits
  Total Events: 59
============================================================

🔌 Connecting to EP-133 K.O. II...
✓ Connected successfully!

▶ Playing composition to sampler...
   ✓ Played 59 events
✓ Export complete!
```

**Option 5**: Generate from bar and immediately export
```
> 5
Enter bar number: 16

📊 Generating from bar: 16
   Seed: 16000

[... composition plays to sampler ...]
```

### Programmatic Usage

```python
from time_based_generator import TimeBasedGenerator

# Create generator
gen = TimeBasedGenerator()

# Generate from current time
composition = gen.generate_from_time()

# Generate from specific bar
composition = gen.generate_from_bar(8)

# Export to sampler
gen.export_to_sampler(composition)

# Access composition data
print(composition['metadata']['density'])
print(composition['patterns']['kick'])
```

## Customization

### Change BPM and Musical Parameters

Edit `time_based_generator.py`:

```python
def __init__(self):
    self.skill = EP133Skill()

    # Customize these!
    self.bpm = 140              # Change tempo
    self.bars = 8               # More bars
    self.beats_per_bar = 3      # 3/4 time signature
    self.subdivisions = 4       # Resolution
```

### Modify Pattern Generation

Each pattern generator can be customized:

```python
def _generate_kick_pattern(self, density: float) -> List[Dict]:
    # Add your custom kick pattern logic
    # Change intervals, velocities, sound selection, etc.
    pass
```

## Composition Data Structure

```python
{
    'metadata': {
        'seed': 142317,
        'mode': 'clock',
        'time': '14:23:17',
        'bpm': 120,
        'bars': 4,
        'density': 0.17,
        'complexity': 0.34,
        'generated_at': '2025-10-21T14:23:17.123456'
    },
    'patterns': {
        'kick': [
            {'step': 0, 'note': 36, 'velocity': 95, 'sound_id': 1},
            {'step': 16, 'note': 36, 'velocity': 102, 'sound_id': 2},
            # ...
        ],
        'snare': [...],
        'hat': [...],
        'percussion': [...]
    }
}
```

## Tips & Tricks

### Morning/Afternoon/Evening Vibes
- **Morning** (6:00-11:59): Lower seeds → simpler, sparser patterns
- **Afternoon** (12:00-17:59): Medium seeds → balanced patterns
- **Evening** (18:00-23:59): Higher seeds → denser, more complex patterns

### Bar Number Strategies
- **1-10**: Intro ideas
- **11-20**: Verse variations
- **21-30**: Chorus ideas
- **31-40**: Bridge/breakdown
- **41-50**: Build-ups

### Quick Iteration
Run the same bar/time multiple times to hear it again, or increment bar numbers to explore variations.

### Combine with Manual Tweaks
Export a time-based idea, then manually adjust on the EP-133 for the best of both worlds!

## Troubleshooting

### No MIDI Ports Found
- Ensure EP-133 is connected via USB-C
- Check that the device is powered on
- On Linux, you may need to install `python3-rtmidi` or `libasound2-dev`

### Composition Sounds Wrong
- Check your BPM setting on the EP-133 matches the generator (default: 120)
- Adjust `self.bpm` in the script to match your sampler's tempo

### Pattern Too Simple/Complex
The seed determines density and complexity. Try:
- Different times of day (clock mode)
- Different bar numbers (bar mode)
- Manually adjust the generation algorithms

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies:
- `mido>=1.2.10` - MIDI library for USB communication
- `python-dotenv>=0.19.0`
- `pydantic>=2.0.0`

## License

MIT License - See LICENSE file for details

---

**Created for the EP-133 K.O. II Skills project**
