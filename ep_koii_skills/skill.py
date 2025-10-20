from .midi_interface import MIDIInterface
from .sample_manager import SampleManager

class EP133Skill:
    """EP-133 K.O. II Skill - MIDI Control & Sample Browser"""
    
    def __init__(self):
        self.midi_interface = MIDIInterface()
        self.sample_manager = SampleManager()
    
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

def create_skill():
    return EP133Skill()
