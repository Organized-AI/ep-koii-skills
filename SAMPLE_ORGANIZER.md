# EP-133 K.O. II Sample Pack Auto-Organizer

Automatically organize and manage your sample packs when connecting your EP-133 K.O. II via USB-C.

## Features

- **Automatic USB-C Detection**: Monitors for EP-133 K.O. II connections
- **iCloud Integration**: Fetches samples from your iCloud Drive
- **Smart Categorization**: Automatically categorizes samples by type (Kicks, Snares, Bass, etc.)
- **Local Caching**: Organizes samples in a local cache for quick access
- **Multiple Usage Modes**: Run as standalone script or integrate with your Python code

## Quick Start

### Option 1: Automatic Monitoring (Recommended)

Monitor for USB connections and auto-organize when device is connected:

```bash
python auto_organize.py
```

This will:
1. Monitor for EP-133 K.O. II USB-C connections
2. Automatically fetch samples from `~/Library/Mobile Documents/com~apple~CloudDocs/KO ii`
3. Organize them by category in `~/.ep133_samples/`
4. Keep monitoring for future connections

### Option 2: Organize Once

Organize samples immediately without monitoring:

```bash
python auto_organize.py --organize-now
```

### Option 3: Custom Paths

Specify custom iCloud and cache paths:

```bash
python auto_organize.py --icloud-path "/path/to/samples" --cache-path "/path/to/cache"
```

## Python API Usage

### Basic Usage

```python
from ep_koii_skills import SamplePackOrganizer

# Initialize organizer
organizer = SamplePackOrganizer(
    icloud_path="~/Library/Mobile Documents/com~apple~CloudDocs/KO ii"
)

# Organize samples
result = organizer.auto_organize()

if result['success']:
    print(f"Organized {result['stats']['total_samples']} samples")
    print(f"Categories: {result['stats']['by_category']}")
```

### Integrated with EP133Skill

```python
from ep_koii_skills import EP133Skill

# Create skill with auto-organization
skill = EP133Skill(
    icloud_path="~/Library/Mobile Documents/com~apple~CloudDocs/KO ii",
    enable_auto_organize=True
)

# Manually trigger organization
result = skill.organize_sample_packs()

# Or start automatic monitoring
skill.start_auto_organize_monitoring()
```

### USB Connection Monitoring

```python
from ep_koii_skills import USBConnectionMonitor, SamplePackOrganizer

def on_connect(port_name):
    print(f"EP-133 connected on {port_name}!")
    organizer.auto_organize()

def on_disconnect(port_name):
    print(f"EP-133 disconnected from {port_name}")

# Set up organizer
organizer = SamplePackOrganizer("~/Library/Mobile Documents/com~apple~CloudDocs/KO ii")

# Create monitor with callbacks
monitor = USBConnectionMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect
)

# Start monitoring
monitor.monitor_loop(check_interval=2.0)
```

## Sample Organization

### Categories

Samples are automatically categorized into:

- **Kicks**: Bass drums, kick sounds
- **Snares**: Snare drums, claps
- **Cymbals and Hats**: Hi-hats, cymbals, crashes
- **Percussion**: Toms, congas, shakers, tambourines
- **Bass**: Bass synths, 808s, sub bass
- **Melodic & Synth**: Leads, pads, chords, melodies

### Categorization Logic

The organizer uses intelligent keyword matching:

- `kick`, `bd`, `bass drum` → Kicks
- `snare`, `sd`, `clap` → Snares
- `hat`, `hh`, `cymbal`, `crash` → Cymbals and Hats
- `perc`, `tom`, `conga`, `shaker` → Percussion
- `bass`, `808`, `303`, `sub` → Bass
- `synth`, `lead`, `pad`, `chord` → Melodic & Synth

Files that don't match any category go into "Uncategorized".

## Directory Structure

After organization, your cache will look like:

```
~/.ep133_samples/
├── Kicks/
│   ├── kick_01.wav
│   ├── 808_kick.wav
│   └── ...
├── Snares/
│   ├── snare_acoustic.wav
│   └── ...
├── Cymbals and Hats/
├── Percussion/
├── Bass/
├── Melodic & Synth/
└── Uncategorized/
```

## Supported Formats

- WAV (.wav)
- AIFF (.aiff, .aif)
- MP3 (.mp3)
- FLAC (.flac)

## Command Line Options

```bash
auto_organize.py [OPTIONS]

Options:
  --icloud-path PATH      Path to iCloud samples folder
                          (default: ~/Library/Mobile Documents/com~apple~CloudDocs/KO ii)

  --cache-path PATH       Custom cache path for organized samples
                          (default: ~/.ep133_samples)

  --organize-now          Organize samples once without monitoring

  --check-interval SECS   Seconds between USB checks (default: 2.0)

  -h, --help              Show help message
```

## Requirements

- Python 3.7+
- `mido` library for MIDI/USB communication
- macOS (for iCloud Drive integration)
- EP-133 K.O. II connected via USB-C

## Installation

The sample organizer is included with `ep-koii-skills`:

```bash
pip install -e .
```

Or install dependencies separately:

```bash
pip install -r requirements.txt
```

## Troubleshooting

### iCloud Path Not Found

**Problem**: `Warning: iCloud path does not exist`

**Solutions**:
- Verify iCloud Drive is enabled in System Preferences
- Check that the "KO ii" folder exists in iCloud Drive
- Use `--icloud-path` to specify a different location
- Try the full path: `--icloud-path "/Users/YOUR_USERNAME/Library/Mobile Documents/com~apple~CloudDocs/KO ii"`

### No Samples Found

**Problem**: Organization completes but no samples copied

**Solutions**:
- Verify sample files are in supported formats (WAV, AIFF, MP3, FLAC)
- Check that files are not in hidden subdirectories
- Ensure files have proper read permissions

### Device Not Detected

**Problem**: EP-133 K.O. II not detected when connected

**Solutions**:
- Ensure device is powered on
- Check USB-C cable connection
- Verify MIDI driver is installed (see main README)
- Try listing available MIDI ports:
  ```python
  from ep_koii_skills import MIDIInterface
  midi = MIDIInterface()
  print(midi.list_ports())
  ```

## Examples

### Example 1: One-Time Organization

```bash
# Organize all samples from iCloud once
python auto_organize.py --organize-now
```

### Example 2: Background Monitoring

```bash
# Run in background, organize on each connection
python auto_organize.py &
```

### Example 3: Custom Workflow

```python
from ep_koii_skills import SamplePackOrganizer

organizer = SamplePackOrganizer("~/Music/Samples")

# Scan samples
samples = organizer.scan_sample_packs()
print(f"Found {len(samples)} samples")

# Organize by category
organized = organizer.organize_samples(samples)

# Get statistics
stats = organizer.get_stats(organized)
print(f"Total size: {stats['total_size_mb']:.2f} MB")

# Copy to cache
organizer.copy_to_cache(samples, organize_by_category=True)
```

## Tips

- **First Run**: The first organization may take a few minutes for large sample libraries
- **Incremental Updates**: Subsequent runs only copy new or changed files
- **Storage**: Monitor disk space - organized samples are cached locally
- **Performance**: Adjust `--check-interval` based on your needs (lower = more responsive, higher = less CPU)

## Integration with Workflow

The sample organizer integrates seamlessly with the existing EP-133 K.O. II workflow:

1. Connect device via USB-C
2. Samples auto-organize from iCloud
3. MIDI connection establishes automatically
4. Browse organized samples via `interactive_koii.py`
5. Load samples to device using EP-133 interface

## License

MIT License - See LICENSE file for details
