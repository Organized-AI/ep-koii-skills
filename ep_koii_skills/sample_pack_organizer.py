"""
Sample Pack Organizer for EP-133 K.O. II

This module handles automatic organization of sample packs when
the EP-133 K.O. II is connected via USB-C.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class SamplePackOrganizer:
    """Organizes and manages sample packs from iCloud for EP-133 K.O. II"""

    # Supported audio file formats for EP-133
    SUPPORTED_FORMATS = ['.wav', '.aiff', '.aif', '.mp3', '.flac']

    # Sample categories matching EP-133 sound library structure
    CATEGORIES = [
        "Kicks",
        "Snares",
        "Cymbals and Hats",
        "Percussion",
        "Bass",
        "Melodic & Synth"
    ]

    def __init__(self, icloud_path: str, cache_path: Optional[str] = None):
        """
        Initialize the sample pack organizer

        Args:
            icloud_path: Path to iCloud folder containing sample packs
            cache_path: Optional local cache path for organized samples
        """
        self.icloud_path = Path(os.path.expanduser(icloud_path))

        if cache_path:
            self.cache_path = Path(os.path.expanduser(cache_path))
        else:
            # Default cache in user's home directory
            self.cache_path = Path.home() / '.ep133_samples'

        # Create cache directory if it doesn't exist
        self.cache_path.mkdir(parents=True, exist_ok=True)

    def scan_sample_packs(self) -> List[Dict[str, any]]:
        """
        Scan iCloud directory for sample packs

        Returns:
            List of dictionaries containing sample pack information
        """
        sample_packs = []

        if not self.icloud_path.exists():
            print(f"Warning: iCloud path not found: {self.icloud_path}")
            return sample_packs

        # Scan for folders and audio files
        for item in self.icloud_path.rglob('*'):
            if item.is_file() and item.suffix.lower() in self.SUPPORTED_FORMATS:
                pack_info = {
                    'name': item.stem,
                    'path': str(item),
                    'format': item.suffix.lower(),
                    'size': item.stat().st_size,
                    'parent_folder': item.parent.name,
                    'category': self._categorize_sample(item.stem)
                }
                sample_packs.append(pack_info)

        return sample_packs

    def _categorize_sample(self, filename: str) -> str:
        """
        Attempt to categorize a sample based on its filename

        Args:
            filename: Name of the sample file

        Returns:
            Category name or "Uncategorized"
        """
        filename_lower = filename.lower()

        # Simple keyword-based categorization
        categorization_rules = {
            "Kicks": ['kick', 'bd', 'bass drum', 'bassdrum'],
            "Snares": ['snare', 'sd', 'clap'],
            "Cymbals and Hats": ['hat', 'hh', 'hihat', 'cymbal', 'crash', 'ride', 'oh', 'ch'],
            "Percussion": ['perc', 'tom', 'conga', 'bongo', 'shaker', 'tamb'],
            "Bass": ['bass', '808', '303', 'sub'],
            "Melodic & Synth": ['synth', 'lead', 'pad', 'chord', 'melody', 'pluck', 'keys']
        }

        for category, keywords in categorization_rules.items():
            if any(keyword in filename_lower for keyword in keywords):
                return category

        return "Uncategorized"

    def organize_samples(self, samples: List[Dict[str, any]]) -> Dict[str, List[Dict]]:
        """
        Organize samples by category

        Args:
            samples: List of sample dictionaries

        Returns:
            Dictionary with categories as keys and lists of samples as values
        """
        organized = {category: [] for category in self.CATEGORIES}
        organized["Uncategorized"] = []

        for sample in samples:
            category = sample['category']
            if category in organized:
                organized[category].append(sample)
            else:
                organized["Uncategorized"].append(sample)

        return organized

    def copy_to_cache(self, samples: List[Dict[str, any]], organize_by_category: bool = True):
        """
        Copy samples to local cache, optionally organized by category

        Args:
            samples: List of sample dictionaries to copy
            organize_by_category: If True, organize into category subdirectories
        """
        copied_count = 0

        for sample in samples:
            source = Path(sample['path'])

            if organize_by_category:
                # Create category subdirectory
                category_dir = self.cache_path / sample['category']
                category_dir.mkdir(exist_ok=True)
                destination = category_dir / source.name
            else:
                destination = self.cache_path / source.name

            try:
                # Only copy if file doesn't exist or is different
                if not destination.exists() or destination.stat().st_size != source.stat().st_size:
                    shutil.copy2(source, destination)
                    copied_count += 1
                    print(f"Copied: {source.name} -> {sample['category']}")
            except Exception as e:
                print(f"Error copying {source.name}: {e}")

        return copied_count

    def get_stats(self, organized_samples: Dict[str, List[Dict]]) -> Dict[str, any]:
        """
        Get statistics about organized samples

        Args:
            organized_samples: Dictionary of organized samples

        Returns:
            Dictionary containing statistics
        """
        stats = {
            'total_samples': sum(len(samples) for samples in organized_samples.values()),
            'by_category': {cat: len(samples) for cat, samples in organized_samples.items()},
            'total_size_mb': sum(
                sum(s['size'] for s in samples)
                for samples in organized_samples.values()
            ) / (1024 * 1024),
            'cache_path': str(self.cache_path),
            'timestamp': datetime.now().isoformat()
        }

        return stats

    def auto_organize(self) -> Dict[str, any]:
        """
        Automatically scan, organize, and cache samples

        Returns:
            Dictionary containing operation results and statistics
        """
        print(f"Scanning sample packs from: {self.icloud_path}")
        samples = self.scan_sample_packs()

        if not samples:
            return {
                'success': False,
                'message': 'No samples found in iCloud directory',
                'stats': None
            }

        print(f"Found {len(samples)} samples")

        organized = self.organize_samples(samples)
        stats = self.get_stats(organized)

        print("\nSample distribution:")
        for category, count in stats['by_category'].items():
            if count > 0:
                print(f"  {category}: {count} samples")

        print(f"\nCopying samples to cache: {self.cache_path}")
        copied = self.copy_to_cache(samples, organize_by_category=True)

        return {
            'success': True,
            'message': f'Successfully organized {len(samples)} samples ({copied} copied)',
            'stats': stats,
            'organized_samples': organized
        }
