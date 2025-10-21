#!/usr/bin/env python3
"""
Time-Based Idea Generator for EP-133 K.O. II
Composes initial ideas based on clock time or bar segment.
"""

import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import random

from ep_koii_skills import EP133Skill
from sound_compatibility import SoundCompatibilityAnalyzer


class TimeBasedGenerator:
    """Generate musical ideas based on time or bar position."""

    def __init__(self):
        self.skill = EP133Skill()
        self.compatibility_analyzer = SoundCompatibilityAnalyzer()

        # Musical parameters
        self.bpm = 120
        self.bars = 4
        self.beats_per_bar = 4
        self.subdivisions = 4  # 16th notes

        # Composition storage
        self.current_composition: List[Dict] = []

    def get_time_seed(self) -> int:
        """Generate a seed from current time (HH:MM:SS)."""
        now = datetime.now()
        # Create seed from hours, minutes, seconds
        seed = now.hour * 10000 + now.minute * 100 + now.second
        return seed

    def get_bar_seed(self, bar_number: int) -> int:
        """Generate a seed from bar number."""
        return bar_number * 1000

    def generate_from_time(self) -> Dict:
        """Generate composition based on current clock time."""
        now = datetime.now()
        seed = self.get_time_seed()
        random.seed(seed)

        print(f"\n🕐 Generating from time: {now.strftime('%H:%M:%S')}")
        print(f"   Seed: {seed}")

        composition = self._generate_composition(seed, "clock")
        composition['metadata']['time'] = now.strftime('%H:%M:%S')

        return composition

    def generate_from_bar(self, bar_number: int) -> Dict:
        """Generate composition based on bar segment number."""
        seed = self.get_bar_seed(bar_number)
        random.seed(seed)

        print(f"\n📊 Generating from bar: {bar_number}")
        print(f"   Seed: {seed}")

        composition = self._generate_composition(seed, "bar")
        composition['metadata']['bar_number'] = bar_number

        return composition

    def _generate_composition(self, seed: int, mode: str) -> Dict:
        """
        Generate a musical composition using the seed.

        The seed influences:
        - Rhythm density
        - Sound selection
        - Pattern complexity
        - Velocity variations
        """
        random.seed(seed)

        # Determine composition characteristics from seed
        density = (seed % 100) / 100.0  # 0.0 to 1.0
        complexity = (seed % 50) / 50.0

        # Generate patterns
        kick_pattern = self._generate_kick_pattern(density)
        snare_pattern = self._generate_snare_pattern(density)
        hat_pattern = self._generate_hat_pattern(density, complexity)
        perc_pattern = self._generate_percussion_pattern(complexity)

        # Combine into composition
        composition = {
            'metadata': {
                'seed': seed,
                'mode': mode,
                'bpm': self.bpm,
                'bars': self.bars,
                'density': round(density, 2),
                'complexity': round(complexity, 2),
                'generated_at': datetime.now().isoformat()
            },
            'patterns': {
                'kick': kick_pattern,
                'snare': snare_pattern,
                'hat': hat_pattern,
                'perc': perc_pattern
            }
        }

        # Analyze sound compatibility
        compatibility = self._analyze_sound_compatibility(composition)
        composition['compatibility'] = compatibility

        # Store current composition
        self.current_composition = composition

        # Print summary
        self._print_composition_summary(composition)

        return composition

    def _generate_kick_pattern(self, density: float) -> List[Dict]:
        """Generate kick drum pattern (typically on beats 1 and 3)."""
        pattern = []
        steps = self.bars * self.beats_per_bar * self.subdivisions  # 64 steps for 4 bars

        # Standard kick on beats 1 and 3
        for step in range(steps):
            beat_position = step % self.subdivisions
            bar_beat = (step // self.subdivisions) % self.beats_per_bar

            # Kick on beat 1 and 3 (stronger pattern)
            if bar_beat in [0, 2] and beat_position == 0:
                velocity = random.randint(90, 127)
                pattern.append({
                    'step': step,
                    'note': 36,  # Kick (A1)
                    'velocity': velocity,
                    'sound_id': random.choice([1, 2, 3, 4, 5])  # Kick variants
                })
            # Add some variation based on density
            elif random.random() < density * 0.3 and beat_position == 0:
                velocity = random.randint(60, 90)
                pattern.append({
                    'step': step,
                    'note': 36,
                    'velocity': velocity,
                    'sound_id': random.choice([1, 2, 3])
                })

        return pattern

    def _generate_snare_pattern(self, density: float) -> List[Dict]:
        """Generate snare pattern (typically on beats 2 and 4)."""
        pattern = []
        steps = self.bars * self.beats_per_bar * self.subdivisions

        for step in range(steps):
            beat_position = step % self.subdivisions
            bar_beat = (step // self.subdivisions) % self.beats_per_bar

            # Snare on beat 2 and 4
            if bar_beat in [1, 3] and beat_position == 0:
                velocity = random.randint(85, 120)
                pattern.append({
                    'step': step,
                    'note': 38,  # Snare (A3)
                    'velocity': velocity,
                    'sound_id': random.choice([100, 101, 102])  # Snare variants
                })
            # Ghost notes based on density
            elif random.random() < density * 0.4 and beat_position in [2]:
                velocity = random.randint(40, 70)
                pattern.append({
                    'step': step,
                    'note': 38,
                    'velocity': velocity,
                    'sound_id': 100
                })

        return pattern

    def _generate_hat_pattern(self, density: float, complexity: float) -> List[Dict]:
        """Generate hi-hat pattern."""
        pattern = []
        steps = self.bars * self.beats_per_bar * self.subdivisions

        # Determine pattern style based on complexity
        if complexity < 0.33:
            # Simple quarter notes
            interval = self.subdivisions
        elif complexity < 0.66:
            # Eighth notes
            interval = self.subdivisions // 2
        else:
            # Sixteenth notes
            interval = 1

        for step in range(steps):
            if step % interval == 0:
                # Vary between closed and open hats
                is_open = random.random() < 0.2
                velocity = random.randint(70, 100) if not is_open else random.randint(80, 110)

                pattern.append({
                    'step': step,
                    'note': 42 if not is_open else 46,  # Closed vs Open hat
                    'velocity': velocity,
                    'sound_id': random.choice([200, 201]) if not is_open else 218  # HH variants
                })
            # Add occasional accents based on density
            elif random.random() < density * 0.3:
                velocity = random.randint(50, 80)
                pattern.append({
                    'step': step,
                    'note': 42,
                    'velocity': velocity,
                    'sound_id': random.choice([200, 201])
                })

        return pattern

    def _generate_percussion_pattern(self, complexity: float) -> List[Dict]:
        """Generate additional percussion based on complexity."""
        pattern = []

        if complexity < 0.3:
            return pattern  # No extra percussion for simple patterns

        steps = self.bars * self.beats_per_bar * self.subdivisions

        for step in range(steps):
            # Add claps or other percussion sporadically
            if random.random() < complexity * 0.15:
                velocity = random.randint(60, 100)
                pattern.append({
                    'step': step,
                    'note': random.choice([39, 54, 56]),  # Various percussion
                    'velocity': velocity,
                    'sound_id': random.choice([300, 301, 302])  # Perc variants
                })

        return pattern

    def _analyze_sound_compatibility(self, composition: Dict) -> Dict:
        """Analyze the sound compatibility of the composition."""
        # Extract all sound IDs from the composition
        sound_ids = []
        for pattern_name, pattern_events in composition['patterns'].items():
            for event in pattern_events:
                if 'sound_id' in event:
                    sound_ids.append(event['sound_id'])

        # Remove duplicates
        unique_sound_ids = list(set(sound_ids))

        # Analyze compatibility
        if not unique_sound_ids:
            return {
                "analyzed": False,
                "reason": "No sounds in composition"
            }

        analysis = self.compatibility_analyzer.analyze_composition(unique_sound_ids)

        # Add sound details
        analysis['sounds_used'] = []
        for sid in sorted(unique_sound_ids):
            summary = self.compatibility_analyzer.get_sound_summary(sid)
            analysis['sounds_used'].append({
                'id': sid,
                'summary': summary
            })

        # Find matching kit
        matching_kit = self.compatibility_analyzer.find_matching_kit(unique_sound_ids)
        analysis['matching_kit'] = matching_kit

        return analysis

    def _print_composition_summary(self, composition: Dict):
        """Print a readable summary of the composition."""
        meta = composition['metadata']
        patterns = composition['patterns']
        compatibility = composition.get('compatibility', {})

        print(f"\n{'='*60}")
        print(f"  COMPOSITION SUMMARY")
        print(f"{'='*60}")
        print(f"  Mode:       {meta['mode'].upper()}")
        print(f"  Seed:       {meta['seed']}")
        if 'time' in meta:
            print(f"  Time:       {meta['time']}")
        if 'bar_number' in meta:
            print(f"  Bar:        {meta['bar_number']}")
        print(f"  BPM:        {meta['bpm']}")
        print(f"  Bars:       {meta['bars']}")
        print(f"  Density:    {meta['density']:.0%}")
        print(f"  Complexity: {meta['complexity']:.0%}")
        print(f"\n  Pattern Elements:")
        print(f"    • Kicks:      {len(patterns['kick'])} hits")
        print(f"    • Snares:     {len(patterns['snare'])} hits")
        print(f"    • Hi-hats:    {len(patterns['hat'])} hits")
        print(f"    • Percussion: {len(patterns['perc'])} hits")
        print(f"  Total Events: {sum(len(p) for p in patterns.values())}")

        # Print sound compatibility analysis
        if compatibility and 'overall_score' in compatibility:
            print(f"\n  🎵 SOUND COMPATIBILITY ANALYSIS")
            print(f"  {'-'*56}")
            print(f"  Rating:      {compatibility['rating']} ({compatibility['overall_score']:.0%})")
            print(f"  Verdict:     {compatibility['verdict']}")

            if compatibility.get('matching_kit'):
                print(f"  Style Kit:   {compatibility['matching_kit']}")

            print(f"\n  Sound Details:")
            for sound_info in compatibility.get('sounds_used', []):
                print(f"    • {sound_info['summary']}")

            # Show key insights
            family_check = compatibility.get('family_analysis', {})
            if family_check.get('families'):
                families_str = ', '.join(family_check['families'])
                print(f"\n  Families:    {families_str}")

            timbre_check = compatibility.get('timbre_analysis', {})
            if timbre_check.get('timbres'):
                timbres_str = ', '.join(timbre_check['timbres'])
                print(f"  Timbres:     {timbres_str}")

        print(f"{'='*60}\n")

    def export_to_sampler(self, composition: Optional[Dict] = None) -> bool:
        """
        Export composition to EP-133 via USB-C MIDI.

        Args:
            composition: The composition to export. If None, uses current composition.

        Returns:
            True if export successful, False otherwise.
        """
        if composition is None:
            composition = self.current_composition

        if not composition:
            print("❌ No composition to export!")
            return False

        print("\n🔌 Connecting to EP-133 K.O. II...")

        # Connect to device
        ports = self.skill.list_midi_ports()
        if not ports:
            print("❌ No MIDI ports found. Is the EP-133 connected?")
            return False

        print(f"   Found {len(ports)} MIDI port(s)")

        # Try to connect
        try:
            self.skill.connect_to_device(port_index=0)
            print("✓ Connected successfully!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

        # Play the composition
        print("\n▶ Playing composition to sampler...")
        self._play_composition(composition)

        # Disconnect
        self.skill.disconnect_device()
        print("✓ Export complete!\n")

        return True

    def _play_composition(self, composition: Dict):
        """Play the composition to the connected device."""
        patterns = composition['patterns']
        meta = composition['metadata']

        # Calculate timing
        step_duration = (60.0 / meta['bpm']) / self.subdivisions  # Duration of one 16th note

        # Merge all patterns into a timeline
        timeline = []
        for pattern_name, pattern_events in patterns.items():
            for event in pattern_events:
                timeline.append(event)

        # Sort by step
        timeline.sort(key=lambda x: x['step'])

        if not timeline:
            print("   No events to play")
            return

        print(f"   Playing {len(timeline)} events at {meta['bpm']} BPM...")

        # Play the timeline
        current_step = 0
        for event in timeline:
            # Wait until the event's step
            steps_to_wait = event['step'] - current_step
            if steps_to_wait > 0:
                time.sleep(steps_to_wait * step_duration)

            # Play the note
            velocity = event['velocity']
            note = event['note']
            self.skill.play_note(note, velocity=velocity, duration=0.1)

            current_step = event['step']

        print(f"   ✓ Played {len(timeline)} events")


def main():
    """Interactive CLI for the time-based generator."""
    generator = TimeBasedGenerator()

    print("\n" + "="*60)
    print("  EP-133 K.O. II - Time-Based Idea Generator")
    print("="*60)
    print("\nQuickly compose ideas based on time or bar position!")
    print("\nCommands:")
    print("  1 - Generate from current time")
    print("  2 - Generate from bar number")
    print("  3 - Export current composition to sampler")
    print("  4 - Generate & export from time (quick workflow)")
    print("  5 - Generate & export from bar (quick workflow)")
    print("  q - Quit")
    print("="*60)

    while True:
        choice = input("\n> ").strip().lower()

        if choice == '1':
            generator.generate_from_time()

        elif choice == '2':
            try:
                bar_num = int(input("Enter bar number: "))
                generator.generate_from_bar(bar_num)
            except ValueError:
                print("❌ Invalid bar number")

        elif choice == '3':
            generator.export_to_sampler()

        elif choice == '4':
            # Quick workflow: generate and export
            composition = generator.generate_from_time()
            generator.export_to_sampler(composition)

        elif choice == '5':
            # Quick workflow: generate and export
            try:
                bar_num = int(input("Enter bar number: "))
                composition = generator.generate_from_bar(bar_num)
                generator.export_to_sampler(composition)
            except ValueError:
                print("❌ Invalid bar number")

        elif choice == 'q':
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")


if __name__ == '__main__':
    main()
