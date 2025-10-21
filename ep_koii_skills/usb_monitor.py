"""
USB Connection Monitor for EP-133 K.O. II

This module monitors for USB-C connections to the EP-133 K.O. II
and triggers sample pack organization.
"""

import time
import mido
from typing import Callable, Optional, List


class USBConnectionMonitor:
    """Monitors USB-C connections for EP-133 K.O. II devices"""

    # Device identifiers for EP-133 K.O. II
    DEVICE_IDENTIFIERS = ["EP-133", "KO II", "Teenage"]

    def __init__(self, on_connect: Optional[Callable] = None, on_disconnect: Optional[Callable] = None):
        """
        Initialize the USB connection monitor

        Args:
            on_connect: Callback function to execute when device connects
            on_disconnect: Callback function to execute when device disconnects
        """
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.is_connected = False
        self.connected_port = None
        self.monitoring = False

    def _find_device_port(self) -> Optional[str]:
        """
        Search for EP-133 K.O. II in available MIDI ports

        Returns:
            Port name if device found, None otherwise
        """
        try:
            ports = mido.get_output_names()

            for port in ports:
                if any(identifier in port for identifier in self.DEVICE_IDENTIFIERS):
                    return port
        except Exception as e:
            print(f"Error scanning MIDI ports: {e}")

        return None

    def check_connection(self) -> bool:
        """
        Check current connection status

        Returns:
            True if device is connected, False otherwise
        """
        port = self._find_device_port()
        was_connected = self.is_connected

        if port and not was_connected:
            # Device just connected
            self.is_connected = True
            self.connected_port = port
            print(f"\n[USB Monitor] EP-133 K.O. II connected on port: {port}")

            if self.on_connect:
                try:
                    self.on_connect(port)
                except Exception as e:
                    print(f"[USB Monitor] Error in on_connect callback: {e}")

            return True

        elif not port and was_connected:
            # Device just disconnected
            self.is_connected = False
            previous_port = self.connected_port
            self.connected_port = None
            print(f"\n[USB Monitor] EP-133 K.O. II disconnected from port: {previous_port}")

            if self.on_disconnect:
                try:
                    self.on_disconnect(previous_port)
                except Exception as e:
                    print(f"[USB Monitor] Error in on_disconnect callback: {e}")

            return False

        return self.is_connected

    def monitor_loop(self, check_interval: float = 2.0):
        """
        Continuously monitor for USB connection changes

        Args:
            check_interval: Seconds between connection checks (default: 2.0)
        """
        self.monitoring = True
        print("[USB Monitor] Started monitoring for EP-133 K.O. II connections...")
        print("[USB Monitor] Press Ctrl+C to stop")

        try:
            while self.monitoring:
                self.check_connection()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\n[USB Monitor] Monitoring stopped by user")
            self.monitoring = False

    def stop_monitoring(self):
        """Stop the monitoring loop"""
        self.monitoring = False

    def get_available_ports(self) -> List[str]:
        """
        Get list of all available MIDI ports

        Returns:
            List of MIDI port names
        """
        try:
            return mido.get_output_names()
        except Exception as e:
            print(f"Error getting MIDI ports: {e}")
            return []

    def is_device_connected(self) -> bool:
        """
        Check if device is currently connected

        Returns:
            True if connected, False otherwise
        """
        return self.is_connected and self.connected_port is not None
