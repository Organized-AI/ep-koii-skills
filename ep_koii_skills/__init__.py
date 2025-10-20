"""
EP-KOII Skills - Unified skill for EP-133 K.O. II MIDI control and sample management
"""

__version__ = "1.0.0"
__author__ = "Organized-AI"
__license__ = "MIT"

from .skill import EP133Skill
from .midi_interface import MIDIInterface
from .sample_manager import SampleManager

__all__ = ["EP133Skill", "MIDIInterface", "SampleManager"]
