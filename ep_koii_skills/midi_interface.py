import time, logging
import mido
from typing import Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

PAD_GROUPS = {"A": range(36,48), "B": range(48,60), "C": range(60,72), "D": range(72,84)}
VELOCITY_HIGH, VELOCITY_LOW = 100, 60

SOUND_CATEGORIES = ["Kicks", "Snares", "Cymbals and Hats", "Percussion", "Bass", "Melodic & Synth"]

SOUND_LIBRARY = {
    "Kicks": {1:"MICRO KICK", 2:"NT KICK", 3:"NT KICK B", 4:"NT KICK C", 5:"NT KICK D"},
    "Snares": {100:"NT SNARE", 101:"NT SNARE B", 102:"NT SNARE C"},
    "Cymbals and Hats": {200:"NT HH CLOSED", 201:"NT HH CLOSED B", 218:"NT HH OPEN"},
    "Percussion": {300:"NT CLAP", 301:"NT CLAP B", 302:"NT CLAP C"},
    "Bass": {400:"NT BASS", 401:"S95X ROUND", 402:"TUBRO BASS"},
    "Melodic & Synth": {500:"BLUE", 501:"PIANO S95X", 502:"WURLI CLEAN"}
}

DEFAULT_PAD_CONFIG = {
    "A": {"pads": [[343,235,247],[317,200,218],[100,114,130],[1,21,300]]},
    "B": {"pads": [[445,450,455],[430,435,440],[415,420,425],[400,405,410]]},
    "C": {"pads": [[545,550,555],[530,353,540],[515,520,525],[500,505,510]]}
}

class MIDIInterface:
    def __init__(self):
        self.port = None
        self.channel = 0
        self.connected = False
    
    def list_ports(self):
        return mido.get_output_names()
    
    def connect(self, port_name=None, port_index=None):
        try:
            ports = mido.get_output_names()
            if not ports: return False
            port = ports[port_index or 0] if port_index is not None else (port_name or ports[0])
            self.port = mido.open_output(port)
            self.connected = True
            logger.info(f"Connected to {port}")
            return True
        except: return False
    
    def disconnect(self):
        if self.port:
            self.port.close()
            self.port = None
            self.connected = False
        return True
    
    def pad_to_note(self, pad_ref):
        ch = pad_ref[0].upper()
        if ch not in PAD_GROUPS: raise ValueError(f"Invalid channel: {ch}")
        base = min(PAD_GROUPS[ch])
        if pad_ref[1:] == ".": return base
        elif pad_ref[1:] == "0": return base + 1
        else:
            num = int(pad_ref[1:])
            return base + 3 + ((num-1)//3)*3 + ((num-1)%3)
    
    def find_sound_by_name(self, name):
        name_u = name.upper()
        for cat, sounds in SOUND_LIBRARY.items():
            for sid, sname in sounds.items():
                if sname == name_u: return sid
        return None
    
    def play_note(self, note, velocity=100, duration=0.1):
        if not self.connected: return False
        try:
            self.port.send(mido.Message("note_on", note=note, velocity=velocity, channel=self.channel))
            time.sleep(duration)
            self.port.send(mido.Message("note_off", note=note, velocity=0, channel=self.channel))
            return True
        except: return False
