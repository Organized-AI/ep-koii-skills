#!/usr/bin/env python3
"""
Automatic Sample Pack Organizer for EP-133 K.O. II

This script monitors for USB-C connections to the EP-133 K.O. II
and automatically organizes sample packs from iCloud.

Usage:
    python auto_organize.py                    # Use default iCloud path
    python auto_organize.py --icloud-path PATH # Use custom iCloud path
    python auto_organize.py --cache-path PATH  # Use custom cache path
    python auto_organize.py --organize-now     # Organize once without monitoring
"""

import argparse
import os
from ep_koii_skills.usb_monitor import USBConnectionMonitor
from ep_koii_skills.sample_pack_organizer import SamplePackOrganizer


# Default iCloud path for KO II samples
DEFAULT_ICLOUD_PATH = "~/Library/Mobile Documents/com~apple~CloudDocs/KO ii"


def on_device_connect(port_name: str, organizer: SamplePackOrganizer):
    """
    Callback function executed when EP-133 K.O. II connects

    Args:
        port_name: Name of the MIDI port the device connected to
        organizer: SamplePackOrganizer instance
    """
    print(f"\n{'='*60}")
    print(f"EP-133 K.O. II CONNECTED!")
    print(f"Port: {port_name}")
    print(f"{'='*60}\n")

    print("Starting automatic sample pack organization...\n")

    result = organizer.auto_organize()

    if result['success']:
        print(f"\n{'='*60}")
        print("✓ SAMPLE ORGANIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"\n{result['message']}")

        if result['stats']:
            stats = result['stats']
            print(f"\nTotal samples: {stats['total_samples']}")
            print(f"Total size: {stats['total_size_mb']:.2f} MB")
            print(f"Cache location: {stats['cache_path']}\n")

            print("Samples by category:")
            for category, count in stats['by_category'].items():
                if count > 0:
                    print(f"  • {category}: {count}")
    else:
        print(f"\n⚠ {result['message']}\n")


def on_device_disconnect(port_name: str):
    """
    Callback function executed when EP-133 K.O. II disconnects

    Args:
        port_name: Name of the MIDI port the device disconnected from
    """
    print(f"\n{'='*60}")
    print(f"EP-133 K.O. II DISCONNECTED")
    print(f"Previous port: {port_name}")
    print(f"{'='*60}\n")
    print("Waiting for device to reconnect...\n")


def organize_once(icloud_path: str, cache_path: str = None):
    """
    Organize samples once without monitoring

    Args:
        icloud_path: Path to iCloud samples directory
        cache_path: Optional custom cache path
    """
    print("Organizing samples from iCloud...")
    print(f"Source: {icloud_path}\n")

    organizer = SamplePackOrganizer(icloud_path, cache_path)
    result = organizer.auto_organize()

    if result['success']:
        print(f"\n{'='*60}")
        print("✓ ORGANIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"\n{result['message']}")

        if result['stats']:
            stats = result['stats']
            print(f"\nTotal samples: {stats['total_samples']}")
            print(f"Total size: {stats['total_size_mb']:.2f} MB")
            print(f"Cache location: {stats['cache_path']}\n")
    else:
        print(f"\n⚠ {result['message']}\n")


def main():
    """Main entry point for the auto-organizer"""

    parser = argparse.ArgumentParser(
        description="Automatic sample pack organizer for EP-133 K.O. II"
    )
    parser.add_argument(
        '--icloud-path',
        type=str,
        default=DEFAULT_ICLOUD_PATH,
        help=f'Path to iCloud samples folder (default: {DEFAULT_ICLOUD_PATH})'
    )
    parser.add_argument(
        '--cache-path',
        type=str,
        default=None,
        help='Custom cache path for organized samples (default: ~/.ep133_samples)'
    )
    parser.add_argument(
        '--organize-now',
        action='store_true',
        help='Organize samples once without monitoring for USB connections'
    )
    parser.add_argument(
        '--check-interval',
        type=float,
        default=2.0,
        help='Seconds between USB connection checks (default: 2.0)'
    )

    args = parser.parse_args()

    # Expand user path
    icloud_path = os.path.expanduser(args.icloud_path)

    print(f"\n{'='*60}")
    print("EP-133 K.O. II Sample Pack Auto-Organizer")
    print(f"{'='*60}\n")

    # Check if iCloud path exists
    if not os.path.exists(icloud_path):
        print(f"⚠ Warning: iCloud path does not exist: {icloud_path}")
        print("Please check the path and try again.\n")
        print("Tips:")
        print("  • Make sure iCloud Drive is enabled")
        print("  • Check that the 'KO ii' folder exists in iCloud")
        print("  • Use --icloud-path to specify a different location\n")
        return

    if args.organize_now:
        # Organize once and exit
        organize_once(icloud_path, args.cache_path)
    else:
        # Set up automatic monitoring
        organizer = SamplePackOrganizer(icloud_path, args.cache_path)

        # Create connection monitor with callbacks
        monitor = USBConnectionMonitor(
            on_connect=lambda port: on_device_connect(port, organizer),
            on_disconnect=on_device_disconnect
        )

        print(f"iCloud source: {icloud_path}")
        print(f"Cache location: {organizer.cache_path}")
        print(f"\nMonitoring for EP-133 K.O. II connections...")
        print("Connect your device via USB-C to trigger automatic organization\n")

        # Check if device is already connected
        if monitor.check_connection():
            print("Device is already connected. Organization will start now.\n")

        # Start monitoring loop
        try:
            monitor.monitor_loop(check_interval=args.check_interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user. Goodbye!\n")


if __name__ == "__main__":
    main()
