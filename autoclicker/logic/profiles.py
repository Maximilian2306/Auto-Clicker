# autoclicker/logic/profiles.py
"""Profile Management Logic - Save, load, delete profiles"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("Warning: jsonschema not installed. Profile validation disabled.")

from ..utils.validators import validate_profile_name
from ..utils.constants import PROFILES_FILE, LAST_PROFILE_FILE


class Profiles:
    """Verwaltet Profiles (Speichern, Laden, Löschen)"""

    # Use centralized constants
    PROFILES_FILE = PROFILES_FILE
    LAST_PROFILE_FILE = LAST_PROFILE_FILE

    # JSON Schema for profile validation
    PROFILE_SCHEMA = {
        "type": "object",
        "properties": {
            "delay": {"type": "number", "minimum": 0, "maximum": 60},
            "duration": {"type": "integer", "minimum": 0},
            "click_type": {"type": "string", "enum": ["left", "right", "middle", "double"]},
            "pattern": {"type": "string", "enum": ["none", "circle", "square", "spiral", "zigzag", "star", "eight", "random", "line"]},
            "pattern_size": {"type": "integer", "minimum": 10, "maximum": 1000},
            "repeat": {"type": "integer", "minimum": 1, "maximum": 100},
            "random_delay": {"type": "boolean"},
            "notify_when_done": {"type": "boolean"},
            "click_while_pattern": {"type": "boolean"},
            "interrupt_on_move": {"type": "boolean"},
            "language": {"type": "string"},
            "theme": {"type": "string"},
            "hotkeys": {"type": "object"}
        },
        "additionalProperties": True
    }

    def __init__(self):
        self.profiles = self._load_profiles_from_file()

    def _validate_profile_name(self, name: str) -> bool:
        """Validate profile name to prevent path traversal"""
        return validate_profile_name(name)

    def _validate_profile_data(self, data: Dict[str, Any]) -> bool:
        """Validate profile data against JSON schema"""
        if not JSONSCHEMA_AVAILABLE:
            # If jsonschema is not available, skip validation
            return isinstance(data, dict)

        try:
            validate(instance=data, schema=self.PROFILE_SCHEMA)
            return True
        except ValidationError as e:
            print(f"Invalid profile data: {e.message}")
            return False
        except Exception as e:
            print(f"Error validating profile: {e}")
            return False

    def _load_profiles_from_file(self) -> Dict[str, Dict[str, Any]]:
        """Load all profiles from JSON file"""
        if self.PROFILES_FILE.exists():
            try:
                with open(self.PROFILES_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profiles: {e}")
                return {"Default": {}}
        return {"Default": {}}

    def _save_profiles_to_file(self) -> bool:
        """Save all profiles to JSON file"""
        try:
            with open(self.PROFILES_FILE, "w") as f:
                json.dump(self.profiles, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profiles: {e}")
            return False

    def save_last_profile(self, name: str) -> None:
        """Save last active profile name for auto-loading"""
        try:
            with open(self.LAST_PROFILE_FILE, "w") as f:
                json.dump({"last_profile": name}, f)
        except Exception as e:
            print(f"Error saving last profile: {e}")

    def load_last_profile(self) -> Optional[str]:
        """Load last active profile name"""
        if self.LAST_PROFILE_FILE.exists():
            try:
                with open(self.LAST_PROFILE_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("last_profile")
            except Exception as e:
                print(f"Error loading last profile: {e}")
        return None

    def get_all_profiles(self) -> list[str]:
        """Get list of all profile names"""
        try:
            return list(self.profiles.keys())
        except Exception as e:
            print(f"Error getting profile list: {e}")
            return None
        

    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific profile by name"""
        return self.profiles.get(name)

    def create_profile(self, name: str, settings: Dict[str, Any]) -> bool:
        """Create or update a profile"""
        if not self._validate_profile_name(name):
            return False

        # Merge with defaults to ensure all keys exist
        # Use copy to avoid mutating the original settings dict
        default = self.get_default_profile()
        default.update(settings.copy())
        self.profiles[name] = default

        return self._save_profiles_to_file()

    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        if not self._validate_profile_name(name):
            return False

        if name == "Default":
            print("Cannot delete Default profile")
            return False

        if name in self.profiles:
            del self.profiles[name]
            return self._save_profiles_to_file()

        return False

    def load_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a profile and return its settings"""
        if not self._validate_profile_name(name):
            return None

        profile = self.profiles.get(name)
        if profile is None:
            return None

        if not self._validate_profile_data(profile):
            print(f"Profile '{name}' has invalid data, using defaults")
            return self.get_default_profile()

        return profile

    def import_profiles(self, filename: str) -> bool:
        """Import profiles from JSON file"""
        try:
            file_path = Path(filename)
            if not file_path.exists() or not file_path.is_file():
                print(f"Error: File not found or not accessible: {filename}")
                return False

            with open(filename, "r") as f:
                imported = json.load(f)

            for profile_name, profile_data in imported.items():
                if not self._validate_profile_name(profile_name):
                    print(f"Error: Invalid profile name in import: '{profile_name}'")
                    return False

                if not self._validate_profile_data(profile_data):
                    print(f"Error: Invalid profile data for '{profile_name}'")
                    return False

            self.profiles.update(imported)
            return self._save_profiles_to_file()
        except Exception as e:
            print(f"Error importing profiles: {e}")
            return False

    def export_profiles(self, filename: str) -> bool:
        """Export profiles to JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(self.profiles, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting profiles: {e}")
            return False

    def get_default_profile(self) -> Dict[str, Any]:
        """Get the default profile template"""
        return {
            "delay": 0.01,
            "duration": 0,
            "click_type": "left",
            "pattern": "none",
            "pattern_size": 100,
            "repeat": 1,
            "random_delay": False,
            "notify_when_done": False,
            "click_while_pattern": True,
            "interrupt_on_move": False,
            "language": "English",
            "theme": "cyborg",
            "hotkeys": {
                "toggle_clicker": "f6",
                "capture_coordinates": "f7",
                "exit_program": "esc",
                "start_macro_recording": "f3",
                "stop_macro_recording": "f4",
                "play_macro_recording": "f5",
            },
        }