# Sound Compatibility Analyzer

Ensure your beats sound cohesive before exporting them to the sampler! The Sound Compatibility Analyzer uses music theory, sound families, and timbre analysis to predict how well sounds will work together.

## Overview

The analyzer examines compositions and provides:

- **Overall Compatibility Score**: 0-100% rating
- **Sound Family Analysis**: Checks if sounds come from compatible families (NT, 808, S95X, etc.)
- **Category Balance**: Ensures proper mix of kicks, snares, hats, percussion
- **Timbre Compatibility**: Analyzes warmth, brightness, and tonal characteristics
- **Style Kit Matching**: Identifies which pre-defined kit your sounds match

## How It Works

### 1. Sound Families

Sounds are grouped by family based on naming patterns:

- **NT Family**: Natural, acoustic sounds (NT KICK, NT SNARE, NT HH)
- **808 Family**: Classic 808-style sounds
- **909 Family**: Classic 909-style sounds
- **S95X Family**: Modern synthesized sounds
- **MICRO Family**: Tight, crisp sounds
- **TURBO/TUBRO Family**: Heavy, aggressive sounds

**Why it matters**: Sounds from the same family tend to have cohesive timbres and work better together.

### 2. Timbre Analysis

Each sound is classified by timbre:

- **Warm**: Natural, mellow sounds (NT family, WURLI)
- **Bright**: Sharp, clear sounds (CLAP, CLEAN, OPEN hats)
- **Dark**: Deep, bass-heavy sounds (BASS, MICRO KICK)
- **Neutral/Balanced**: Versatile, middle-ground sounds (S95X, BLUE)

**Why it matters**: Complementary timbres create nice contrast; too many different timbres can sound disjointed.

### 3. Category Balance

Good compositions have:
- ✓ Kicks (low-end foundation)
- ✓ Snares (backbeat)
- ✓ Hi-hats or cymbals (rhythm and texture)
- Optional: Percussion, bass, melodic elements

**Why it matters**: Missing essential elements makes beats sound incomplete.

### 4. Sound Characteristics

Sounds are tagged with characteristics inferred from names:

- **acoustic, organic, natural** - Natural-sounding samples
- **electronic, synth, digital** - Synthesized sounds
- **clean, clear, polished** - High-quality, processed sounds
- **punchy, crisp, tight** - Sharp attack, short decay
- **deep, sub, powerful** - Bass-heavy sounds
- **sustained, ringing** - Longer decay times

**Why it matters**: Helps identify if sounds have complementary or clashing characteristics.

## Pre-Defined Sound Kits

The analyzer includes curated kits with excellent compatibility:

### Natural Kit
```python
Description: Organic, natural-sounding drum kit
Style: organic
Timbre: warm
Sounds: NT KICK, NT SNARE, NT HH, NT CLAP variants
Use Case: Acoustic, organic-sounding beats
```

### Electronic Kit
```python
Description: Modern electronic/synth sounds
Style: electronic
Timbre: bright
Sounds: MICRO KICK, S95X sounds, electronic elements
Use Case: EDM, electronic music, modern production
```

### Hybrid Kit
```python
Description: Mix of natural and electronic elements
Style: hybrid
Timbre: balanced
Sounds: Mix of NT, MICRO, S95X families
Use Case: Versatile, contemporary production
```

### Heavy Kit
```python
Description: Aggressive, powerful sounds
Style: aggressive
Timbre: dark
Sounds: Heavy variants, TURBO BASS, aggressive drums
Use Case: Heavy bass music, trap, aggressive styles
```

## Rating System

### EXCELLENT (85-100%)
- Same family OR highly compatible families
- Good category balance
- Cohesive timbres
- **Action**: Export confidently!

### GOOD (70-84%)
- Compatible families with some variety
- Acceptable category balance
- Mixed but complementary timbres
- **Action**: Should work well, minor tweaks optional

### ACCEPTABLE (55-69%)
- Multiple families that can work together
- Some category balance
- Varied timbres
- **Action**: May work, consider refinement

### NEEDS IMPROVEMENT (<55%)
- Too many disparate families
- Poor category balance
- Clashing timbres
- **Action**: Reconsider sound selection

## Usage Examples

### Analyze a Composition

The time-based generator automatically analyzes every composition:

```python
from time_based_generator import TimeBasedGenerator

gen = TimeBasedGenerator()
composition = gen.generate_from_time()

# Compatibility analysis is included in composition['compatibility']
comp = composition['compatibility']
print(f"Score: {comp['overall_score']}")
print(f"Rating: {comp['rating']}")
print(f"Verdict: {comp['verdict']}")
```

### Standalone Analysis

Analyze any set of sound IDs:

```python
from sound_compatibility import SoundCompatibilityAnalyzer

analyzer = SoundCompatibilityAnalyzer()

# Example: All NT sounds (should score highly)
nt_sounds = [2, 100, 200, 300]  # NT KICK, NT SNARE, NT HH, NT CLAP
analysis = analyzer.analyze_composition(nt_sounds)

print(f"Overall Score: {analysis['overall_score']}")
print(f"Rating: {analysis['rating']}")
print(f"Verdict: {analysis['verdict']}")

# Show detailed analysis
print("\nFamily Analysis:")
print(f"  {analysis['family_analysis']['reason']}")

print("\nBalance Analysis:")
print(f"  {analysis['balance_analysis']['reason']}")

print("\nTimbre Analysis:")
print(f"  {analysis['timbre_analysis']['reason']}")
```

### Get Sound Profile

```python
analyzer = SoundCompatibilityAnalyzer()

# Get detailed profile
profile = analyzer.get_sound_profile(2)  # NT KICK
print(f"Name: {profile.name}")
print(f"Family: {profile.family}")
print(f"Timbre: {profile.timbre}")
print(f"Characteristics: {profile.characteristics}")
```

### Find Matching Kit

```python
analyzer = SoundCompatibilityAnalyzer()

# Which kit do these sounds match?
sound_ids = [2, 100, 200]  # NT sounds
kit_name = analyzer.find_matching_kit(sound_ids)
print(f"Matches: {kit_name}")  # Output: "Natural Kit"

# Get kit details
kit = analyzer.get_recommended_kit(kit_name)
print(f"Description: {kit['description']}")
print(f"Style: {kit['style']}")
```

## Integration with Time-Based Generator

The compatibility analyzer is automatically integrated into the time-based generator:

```bash
# Generate composition (analysis included)
python time_based_generator.py

# Choose option 1 or 2 to generate
# Compatibility analysis displays automatically:

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

## Understanding the Analysis

### Example 1: Excellent Compatibility

```
Sounds: NT KICK, NT SNARE, NT HH CLOSED
Score: 99%
Reason: All from NT family, uniform warm timbre, perfect balance
```

**Why excellent**: Same family, cohesive timbre, essential drum elements present.

### Example 2: Good Compatibility

```
Sounds: MICRO KICK, NT SNARE, S95X ROUND, NT HH OPEN
Score: 85%
Reason: NT sounds are versatile and work with MICRO/S95X families
```

**Why good**: Multiple families, but NT acts as glue; complementary timbres.

### Example 3: Needs Improvement

```
Sounds: Only kicks, no snares or hats
Score: 50%
Reason: Missing essential drum elements
```

**Why poor**: Unbalanced - needs snares and hats for complete drum pattern.

## Tips for Best Results

### 1. Stick to Families
Use sounds from the same family (all NT, all S95X) for maximum cohesion.

### 2. Use NT as Glue
NT sounds work well with most other families - use them to bridge different styles.

### 3. Balance Your Elements
Always include:
- 1-2 kick variants
- 1-2 snare variants
- 2-3 hi-hat variants (closed + open)
- Optional: percussion for flavor

### 4. Match Timbres
- All warm OR all bright = cohesive
- Warm + bright = nice contrast
- Too many different timbres = disjointed

### 5. Start with Kits
Use pre-defined kits (Natural, Electronic, Hybrid, Heavy) as starting points.

## Technical Details

### Scoring Algorithm

```python
overall_score = (
    family_score * 0.40 +      # Family compatibility (40%)
    balance_score * 0.35 +     # Category balance (35%)
    timbre_score * 0.25        # Timbre compatibility (25%)
)
```

### Family Compatibility Scoring

- All same family: 100%
- NT + 1 other: 85%
- 2-3 families: 70%
- 4+ families: 40%

### Balance Scoring

- Has kicks + snares + hats: 100%
- Has kicks + snares: 80%
- Has kicks only: 50%
- No essential elements: 30%

### Timbre Scoring

- All same timbre: 95%
- Includes balanced/neutral: 90%
- Complementary mix: 85%
- Mixed (≤2 types): 75%
- Too varied (3+ types): 50%

## Limitations

The analyzer works with:
- ✓ Sound names and categories
- ✓ Naming pattern inference
- ✓ Music theory rules

It does NOT have access to:
- ✗ Actual audio files
- ✗ Frequency/spectrum analysis
- ✗ Pitch detection
- ✗ Actual timbre measurement

**Result**: The analysis is predictive and theory-based, not based on audio analysis. It provides strong guidance but isn't perfect. Always trust your ears!

## Future Enhancements

Potential improvements:
- Audio file analysis (if WAV files are available)
- Pitch/key detection for melodic sounds
- Frequency spectrum compatibility
- Machine learning-based compatibility prediction
- User feedback to improve predictions

---

**Created for the EP-133 K.O. II Skills project**
