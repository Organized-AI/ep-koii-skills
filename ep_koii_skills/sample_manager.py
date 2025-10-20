from typing import Dict, List, Optional, Any
from .midi_interface import SOUND_LIBRARY, SOUND_CATEGORIES, DEFAULT_PAD_CONFIG

class SampleManager:
    def __init__(self):
        self.sound_library = SOUND_LIBRARY
        self.categories = SOUND_CATEGORIES
        self.default_config = DEFAULT_PAD_CONFIG
    
    def list_sound_categories(self):
        return self.categories
    
    def list_sounds_in_category(self, category):
        if category not in self.sound_library:
            raise ValueError(f"Category not found: {category}")
        return [{"id": sid, "name": sname, "category": category} 
                for sid, sname in self.sound_library[category].items()]
    
    def search_sounds(self, query):
        query_u = query.upper()
        results = []
        for cat, sounds in self.sound_library.items():
            for sid, sname in sounds.items():
                if query_u in sname:
                    results.append({"id": sid, "name": sname, "category": cat})
        return results
    
    def get_sound_by_id(self, sound_id):
        for cat, sounds in self.sound_library.items():
            if sound_id in sounds:
                return {"id": sound_id, "name": sounds[sound_id], "category": cat}
        return None
    
    def get_default_pad_configuration(self):
        return self.default_config
