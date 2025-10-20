# EP-133 K.O. II Skill

A unified skill for controlling the Teenage Engineering EP-133 K.O. II synthesizer with integrated MIDI control and sample management.

## Features

- **MIDI Control**: Connect to EP-133 K.O. II via USB and play notes
- **Sound Browser**: Browse 240+ sounds organized in 6 categories
- **Pattern Sequencing**: Create and play drum patterns
- **Sound Search**: Search for sounds by name and category
- **Integration**: Works with Claude for natural language control

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from ep_koii_skills import EP133Skill

skill = EP133Skill()
skill.connect_to_device()
skill.play_note("C3", velocity=100, duration=0.5)

# Browse sounds
categories = skill.list_sound_categories()
kicks = skill.list_sounds_in_category("Kicks")
```

## Documentation

- **Full README**: See main documentation
- **Examples**: Check examples.py for 8 working examples
- **API Reference**: See docstrings in skill.py

## Sound Library

6 categories with 240+ unique sounds:
- **Kicks** - 31 variations
- **Snares** - 45 variations
- **Cymbals and Hats** - 53 variations
- **Percussion** - 13 variations
- **Bass** - 31 variations
- **Melodic & Synth** - 60 variations

## Requirements

- Python 3.8+
- mido >= 1.2.10
- EP-133 K.O. II connected via USB

## License

MIT License - See LICENSE file

## Version

1.0.0 - October 2025
