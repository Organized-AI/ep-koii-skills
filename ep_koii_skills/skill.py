from .midi_interface import MIDIInterface
from .sample_manager import SampleManager
from .sample_pack_organizer import SamplePackOrganizer
from .usb_monitor import USBConnectionMonitor

class EP133Skill:
    """EP-133 K.O. II Skill - MIDI Control & Sample Browser"""

    def __init__(self, icloud_path=None, enable_auto_organize=False):
        self.midi_interface = MIDIInterface()
        self.sample_manager = SampleManager()

        # Optional sample pack organizer
        self.sample_organizer = None
        if icloud_path:
            self.sample_organizer = SamplePackOrganizer(icloud_path)

        # Optional USB monitoring with auto-organization
        self.usb_monitor = None
        if enable_auto_organize and self.sample_organizer:
            self.usb_monitor = USBConnectionMonitor(
                on_connect=lambda port: self._on_device_connect(port),
                on_disconnect=lambda port: self._on_device_disconnect(port)
            )
    
    # Connection
    def list_midi_ports(self):
        return self.midi_interface.list_ports()
    
    def connect_to_device(self, port_name=None, port_index=None):
        return self.midi_interface.connect(port_name, port_index)
    
    def disconnect_device(self):
        return self.midi_interface.disconnect()
    
    def is_connected(self):
        return self.midi_interface.connected
    
    # MIDI
    def play_note(self, note, velocity=100, duration=0.1):
        return self.midi_interface.play_note(note, velocity, duration)
    
    # Samples
    def list_sound_categories(self):
        return self.sample_manager.list_sound_categories()
    
    def list_sounds_in_category(self, category):
        return self.sample_manager.list_sounds_in_category(category)
    
    def search_sounds(self, query):
        return self.sample_manager.search_sounds(query)
    
    def get_sound_info(self, sound_id):
        return self.sample_manager.get_sound_by_id(sound_id)

    # Sample Pack Organization
    def organize_sample_packs(self):
        """Manually trigger sample pack organization"""
        if not self.sample_organizer:
            return {
                'success': False,
                'message': 'Sample organizer not initialized. Provide icloud_path when creating EP133Skill.'
            }
        return self.sample_organizer.auto_organize()

    def start_auto_organize_monitoring(self):
        """Start monitoring for USB connections with auto-organization"""
        if not self.usb_monitor:
            return {
                'success': False,
                'message': 'USB monitor not enabled. Set enable_auto_organize=True when creating EP133Skill.'
            }

        try:
            self.usb_monitor.monitor_loop()
            return {'success': True, 'message': 'Monitoring started'}
        except Exception as e:
            return {'success': False, 'message': f'Error starting monitor: {e}'}

    def stop_auto_organize_monitoring(self):
        """Stop USB connection monitoring"""
        if self.usb_monitor:
            self.usb_monitor.stop_monitoring()
            return {'success': True, 'message': 'Monitoring stopped'}
        return {'success': False, 'message': 'USB monitor not active'}

    def _on_device_connect(self, port_name):
        """Internal callback for device connection"""
        print(f"\n[EP133Skill] Device connected on {port_name}")

        # Auto-connect MIDI interface
        try:
            self.connect_to_device(port_name=port_name)
            print("[EP133Skill] MIDI interface connected")
        except Exception as e:
            print(f"[EP133Skill] Error connecting MIDI: {e}")

        # Auto-organize samples
        if self.sample_organizer:
            print("[EP133Skill] Starting sample organization...")
            result = self.sample_organizer.auto_organize()
            if result['success']:
                print(f"[EP133Skill] {result['message']}")

    def _on_device_disconnect(self, port_name):
        """Internal callback for device disconnection"""
        print(f"\n[EP133Skill] Device disconnected from {port_name}")
        try:
            self.disconnect_device()
        except Exception:
            pass

def create_skill(icloud_path=None, enable_auto_organize=False):
    return EP133Skill(icloud_path, enable_auto_organize)
