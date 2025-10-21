#!/usr/bin/env python3
"""
Sound Compatibility Analyzer for EP-133 K.O. II
Analyzes and validates sound combinations for musical coherence.
"""

from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from ep_koii_skills.midi_interface import SOUND_LIBRARY
import re


@dataclass
class SoundProfile:
    """Profile of a sound with its characteristics."""
    sound_id: int
    name: str
    category: str
    family: str  # e.g., "NT", "808", "S95X"
    characteristics: Set[str]  # e.g., {"punchy", "analog", "digital"}
    timbre: str  # e.g., "warm", "bright", "dark"


class SoundCompatibilityAnalyzer:
    """Analyzes sound compatibility based on naming, families, and music theory."""

    def __init__(self):
        self.sound_library = SOUND_LIBRARY
        self.sound_profiles = self._build_sound_profiles()
        self.sound_kits = self._define_sound_kits()

    def _extract_family(self, sound_name: str) -> str:
        """Extract sound family from name (e.g., 'NT KICK' -> 'NT')."""
        # Common patterns
        patterns = [
            r'^(NT)\s',           # NT sounds
            r'^(808)\s',          # 808 sounds
            r'^(909)\s',          # 909 sounds
            r'^(S95X)\s',         # S95X sounds
            r'^(MICRO)\s',        # MICRO sounds
            r'^(TURBO)\s',        # TURBO sounds
            r'^(TUBRO)\s',        # TUBRO (typo variant)
            r'\s(CLEAN)$',        # Clean variants
            r'^(BLUE)',           # BLUE
            r'^(PIANO)',          # PIANO
            r'^(WURLI)',          # WURLI
        ]

        for pattern in patterns:
            match = re.search(pattern, sound_name, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        # No specific family found, use generic
        return "GENERIC"

    def _infer_characteristics(self, sound_name: str, category: str) -> Set[str]:
        """Infer sound characteristics from name and category."""
        characteristics = set()
        name_upper = sound_name.upper()

        # Style characteristics
        if 'NT' in name_upper:
            characteristics.update(['natural', 'acoustic', 'organic'])
        if '808' in name_upper or 'BASS' in name_upper:
            characteristics.update(['deep', 'sub', 'powerful'])
        if '909' in name_upper:
            characteristics.update(['classic', 'punchy', 'electronic'])
        if 'MICRO' in name_upper:
            characteristics.update(['tight', 'short', 'crisp'])
        if 'CLEAN' in name_upper:
            characteristics.update(['clean', 'clear', 'polished'])
        if 'OPEN' in name_upper:
            characteristics.update(['sustained', 'ringing', 'bright'])
        if 'CLOSED' in name_upper:
            characteristics.update(['tight', 'short', 'controlled'])
        if 'CLAP' in name_upper:
            characteristics.update(['percussive', 'sharp', 'bright'])
        if 'S95X' in name_upper:
            characteristics.update(['synth', 'electronic', 'modern'])
        if 'TURBO' in name_upper or 'TUBRO' in name_upper:
            characteristics.update(['aggressive', 'distorted', 'heavy'])
        if 'PIANO' in name_upper:
            characteristics.update(['melodic', 'harmonic', 'acoustic'])
        if 'WURLI' in name_upper:
            characteristics.update(['vintage', 'electric', 'warm'])
        if 'BLUE' in name_upper:
            characteristics.update(['smooth', 'synth', 'pad'])

        # Add category-based characteristics
        if category == "Kicks":
            characteristics.add('low-frequency')
        elif category == "Snares":
            characteristics.add('mid-frequency')
        elif category == "Cymbals and Hats":
            characteristics.add('high-frequency')
        elif category == "Bass":
            characteristics.update(['low-frequency', 'harmonic'])
        elif category == "Melodic & Synth":
            characteristics.update(['harmonic', 'pitched'])

        return characteristics

    def _infer_timbre(self, sound_name: str, characteristics: Set[str]) -> str:
        """Infer timbre from name and characteristics."""
        name_upper = sound_name.upper()

        # Determine warmth/brightness
        if 'WURLI' in name_upper or 'natural' in characteristics:
            return 'warm'
        elif 'CLEAN' in name_upper or 'OPEN' in name_upper or 'CLAP' in name_upper:
            return 'bright'
        elif 'BASS' in name_upper or 'MICRO' in name_upper:
            return 'dark'
        elif 'S95X' in name_upper or 'BLUE' in name_upper:
            return 'neutral'
        else:
            return 'balanced'

    def _build_sound_profiles(self) -> Dict[int, SoundProfile]:
        """Build profiles for all sounds in the library."""
        profiles = {}

        for category, sounds in self.sound_library.items():
            for sound_id, sound_name in sounds.items():
                family = self._extract_family(sound_name)
                characteristics = self._infer_characteristics(sound_name, category)
                timbre = self._infer_timbre(sound_name, characteristics)

                profiles[sound_id] = SoundProfile(
                    sound_id=sound_id,
                    name=sound_name,
                    category=category,
                    family=family,
                    characteristics=characteristics,
                    timbre=timbre
                )

        return profiles

    def _define_sound_kits(self) -> Dict[str, Dict[str, List[int]]]:
        """Define pre-curated sound kits that work well together."""
        return {
            "Natural Kit": {
                "description": "Organic, natural-sounding drum kit",
                "family": "NT",
                "kick": [2, 3, 4, 5],  # NT KICK variants
                "snare": [100, 101, 102],  # NT SNARE variants
                "hat": [200, 201, 218],  # NT HH variants
                "perc": [300, 301, 302],  # NT CLAP variants
                "timbre": "warm",
                "style": "organic"
            },
            "Electronic Kit": {
                "description": "Modern electronic/synth sounds",
                "family": "S95X",
                "kick": [1],  # MICRO KICK (tight, electronic)
                "snare": [100],  # NT SNARE (can work with electronic)
                "hat": [200, 201],  # Closed hats for tight feel
                "perc": [300],  # Clap
                "bass": [401],  # S95X ROUND
                "melodic": [500, 501, 502],  # BLUE, PIANO S95X, WURLI CLEAN
                "timbre": "bright",
                "style": "electronic"
            },
            "Hybrid Kit": {
                "description": "Mix of natural and electronic elements",
                "family": "MIXED",
                "kick": [1, 2, 3],  # MICRO + NT variants
                "snare": [100, 101],  # NT SNARE variants
                "hat": [200, 201, 218],  # Mix of closed and open
                "perc": [300, 301],  # Claps
                "bass": [400, 401],  # NT BASS + S95X
                "melodic": [501, 502],  # PIANO S95X, WURLI CLEAN
                "timbre": "balanced",
                "style": "hybrid"
            },
            "Heavy Kit": {
                "description": "Aggressive, powerful sounds",
                "family": "HEAVY",
                "kick": [5],  # NT KICK D (typically heavier)
                "snare": [102],  # NT SNARE C
                "hat": [218],  # NT HH OPEN (more aggressive)
                "perc": [302],  # NT CLAP C
                "bass": [402],  # TURBO BASS
                "timbre": "dark",
                "style": "aggressive"
            }
        }

    def get_sound_profile(self, sound_id: int) -> Optional[SoundProfile]:
        """Get profile for a specific sound ID."""
        return self.sound_profiles.get(sound_id)

    def check_family_compatibility(self, sound_ids: List[int]) -> Dict[str, any]:
        """Check if sounds are from compatible families."""
        profiles = [self.sound_profiles[sid] for sid in sound_ids if sid in self.sound_profiles]

        if not profiles:
            return {"compatible": False, "reason": "No valid sounds"}

        # Get all families
        families = set(p.family for p in profiles)

        # Check compatibility
        if len(families) == 1:
            # All from same family - highly compatible
            return {
                "compatible": True,
                "score": 1.0,
                "families": list(families),
                "reason": f"All sounds from {families.pop()} family - excellent coherence"
            }
        elif "NT" in families and len(families) <= 2:
            # NT sounds are versatile and work with most others
            return {
                "compatible": True,
                "score": 0.85,
                "families": list(families),
                "reason": "NT sounds with other families - good compatibility"
            }
        elif len(families) <= 3:
            # Mix of 2-3 families can work
            return {
                "compatible": True,
                "score": 0.7,
                "families": list(families),
                "reason": "Multiple families - acceptable mix, watch for coherence"
            }
        else:
            # Too many different families
            return {
                "compatible": False,
                "score": 0.4,
                "families": list(families),
                "reason": "Too many different sound families - may lack coherence"
            }

    def check_category_balance(self, sound_ids: List[int]) -> Dict[str, any]:
        """Check if sound categories are balanced."""
        profiles = [self.sound_profiles[sid] for sid in sound_ids if sid in self.sound_profiles]

        if not profiles:
            return {"balanced": False, "reason": "No valid sounds"}

        # Count categories
        category_counts = {}
        for p in profiles:
            category_counts[p.category] = category_counts.get(p.category, 0) + 1

        # Good balance: has kicks, snares, and hats at minimum
        has_kicks = "Kicks" in category_counts
        has_snares = "Snares" in category_counts
        has_hats = "Cymbals and Hats" in category_counts

        if has_kicks and has_snares and has_hats:
            return {
                "balanced": True,
                "score": 1.0,
                "categories": category_counts,
                "reason": "Good balance: has essential drum elements"
            }
        elif has_kicks and has_snares:
            return {
                "balanced": True,
                "score": 0.8,
                "categories": category_counts,
                "reason": "Acceptable: has kicks and snares, missing hats"
            }
        elif has_kicks:
            return {
                "balanced": False,
                "score": 0.5,
                "categories": category_counts,
                "reason": "Unbalanced: only has kicks, missing snares and hats"
            }
        else:
            return {
                "balanced": False,
                "score": 0.3,
                "categories": category_counts,
                "reason": "Very unbalanced: missing essential drum elements"
            }

    def check_timbre_compatibility(self, sound_ids: List[int]) -> Dict[str, any]:
        """Check if timbres work well together."""
        profiles = [self.sound_profiles[sid] for sid in sound_ids if sid in self.sound_profiles]

        if not profiles:
            return {"compatible": False, "reason": "No valid sounds"}

        # Get all timbres
        timbres = [p.timbre for p in profiles]
        timbre_set = set(timbres)

        # Timbre compatibility rules
        if len(timbre_set) == 1:
            # All same timbre - very coherent
            return {
                "compatible": True,
                "score": 0.95,
                "timbres": list(timbre_set),
                "reason": f"Uniform {timbres[0]} timbre - excellent coherence"
            }
        elif "balanced" in timbre_set or "neutral" in timbre_set:
            # Balanced/neutral timbres work with everything
            return {
                "compatible": True,
                "score": 0.9,
                "timbres": list(timbre_set),
                "reason": "Includes balanced timbres - good compatibility"
            }
        elif timbre_set == {"warm", "bright"} or timbre_set == {"warm", "dark"}:
            # Complementary timbres
            return {
                "compatible": True,
                "score": 0.85,
                "timbres": list(timbre_set),
                "reason": "Complementary timbres - creates nice contrast"
            }
        elif len(timbre_set) <= 2:
            return {
                "compatible": True,
                "score": 0.75,
                "timbres": list(timbre_set),
                "reason": "Mixed timbres - acceptable variety"
            }
        else:
            return {
                "compatible": False,
                "score": 0.5,
                "timbres": list(timbre_set),
                "reason": "Too many different timbres - may sound disjointed"
            }

    def analyze_composition(self, sound_ids: List[int]) -> Dict[str, any]:
        """Comprehensive analysis of sound compatibility."""
        # Run all checks
        family_check = self.check_family_compatibility(sound_ids)
        balance_check = self.check_category_balance(sound_ids)
        timbre_check = self.check_timbre_compatibility(sound_ids)

        # Calculate overall score (weighted average)
        overall_score = (
            family_check['score'] * 0.4 +
            balance_check['score'] * 0.35 +
            timbre_check['score'] * 0.25
        )

        # Determine rating
        if overall_score >= 0.85:
            rating = "EXCELLENT"
            verdict = "These sounds will work very well together!"
        elif overall_score >= 0.7:
            rating = "GOOD"
            verdict = "These sounds should work well together."
        elif overall_score >= 0.55:
            rating = "ACCEPTABLE"
            verdict = "These sounds may work, but could use refinement."
        else:
            rating = "NEEDS IMPROVEMENT"
            verdict = "Consider adjusting sound selection for better coherence."

        return {
            "overall_score": round(overall_score, 2),
            "rating": rating,
            "verdict": verdict,
            "family_analysis": family_check,
            "balance_analysis": balance_check,
            "timbre_analysis": timbre_check,
            "sound_count": len(sound_ids)
        }

    def get_recommended_kit(self, style: Optional[str] = None) -> Dict[str, any]:
        """Get a recommended sound kit by style."""
        if style and style in self.sound_kits:
            return self.sound_kits[style]

        # Return all kits if no style specified
        return self.sound_kits

    def find_matching_kit(self, sound_ids: List[int]) -> Optional[str]:
        """Find which kit best matches the given sound IDs."""
        profiles = [self.sound_profiles[sid] for sid in sound_ids if sid in self.sound_profiles]

        if not profiles:
            return None

        # Check each kit
        best_match = None
        best_score = 0

        for kit_name, kit_data in self.sound_kits.items():
            # Get all sound IDs in this kit
            kit_sounds = []
            for category in ['kick', 'snare', 'hat', 'perc', 'bass', 'melodic']:
                if category in kit_data:
                    kit_sounds.extend(kit_data[category])

            # Calculate overlap
            overlap = len(set(sound_ids) & set(kit_sounds))
            score = overlap / len(sound_ids) if sound_ids else 0

            if score > best_score:
                best_score = score
                best_match = kit_name

        return best_match if best_score > 0.3 else None

    def get_sound_summary(self, sound_id: int) -> str:
        """Get a human-readable summary of a sound."""
        profile = self.sound_profiles.get(sound_id)
        if not profile:
            return f"Unknown sound (ID: {sound_id})"

        char_str = ", ".join(sorted(list(profile.characteristics)[:3]))
        return f"{profile.name} ({profile.family} family, {profile.timbre} timbre: {char_str})"


def demo_compatibility_analysis():
    """Demonstrate the compatibility analyzer."""
    analyzer = SoundCompatibilityAnalyzer()

    print("\n" + "="*70)
    print("  Sound Compatibility Analyzer - Demo")
    print("="*70)

    # Example 1: All NT sounds (should be excellent)
    print("\n--- Example 1: Natural Kit (All NT Family) ---")
    nt_sounds = [2, 100, 200, 300]  # NT KICK, NT SNARE, NT HH CLOSED, NT CLAP
    analysis = analyzer.analyze_composition(nt_sounds)
    print(f"\nSounds tested:")
    for sid in nt_sounds:
        print(f"  • {analyzer.get_sound_summary(sid)}")
    print(f"\nOverall Score: {analysis['overall_score']} ({analysis['rating']})")
    print(f"Verdict: {analysis['verdict']}")
    print(f"  - Family: {analysis['family_analysis']['reason']}")
    print(f"  - Balance: {analysis['balance_analysis']['reason']}")
    print(f"  - Timbre: {analysis['timbre_analysis']['reason']}")

    # Example 2: Mixed sounds (should be good)
    print("\n--- Example 2: Hybrid Mix ---")
    mixed_sounds = [1, 101, 218, 401]  # MICRO KICK, NT SNARE B, NT HH OPEN, S95X ROUND
    analysis = analyzer.analyze_composition(mixed_sounds)
    print(f"\nSounds tested:")
    for sid in mixed_sounds:
        print(f"  • {analyzer.get_sound_summary(sid)}")
    print(f"\nOverall Score: {analysis['overall_score']} ({analysis['rating']})")
    print(f"Verdict: {analysis['verdict']}")

    # Example 3: Show available kits
    print("\n--- Example 3: Pre-Defined Sound Kits ---")
    kits = analyzer.get_recommended_kit()
    for kit_name, kit_data in kits.items():
        print(f"\n{kit_name}:")
        print(f"  Description: {kit_data['description']}")
        print(f"  Style: {kit_data['style']}")
        print(f"  Timbre: {kit_data['timbre']}")

    print("\n" + "="*70)


if __name__ == '__main__':
    demo_compatibility_analysis()
