# autoclicker/utils/validators.py
"""Shared Validation Logic - Security and input validation functions"""

from typing import Tuple, Union


def validate_safe_filename(name: str, max_length: int = 100, allow_default: bool = False) -> Tuple[bool, str]:
    """Validate filename to prevent path traversal. Returns (is_valid, error_message)."""
    if not name:
        return False, "Name cannot be empty"

    # "Default" is always valid for profiles
    if allow_default and name == "Default":
        return True, ""

    # No path separators or parent directory references
    forbidden = ['/', '\\', '..', '\0', ':']
    for char in forbidden:
        if char in name:
            return False, f"Invalid character: {char}"

    # Only alphanumeric characters, underscores, hyphens, spaces
    if not all(c.isalnum() or c in ('-', '_', ' ') for c in name):
        return False, "Only letters, numbers, -, _ and spaces allowed"

    # Not too long
    if len(name) > max_length:
        return False, f"Name too long (max {max_length} characters)"

    return True, ""


def validate_profile_name(name: str) -> bool:
    """Validate profile name for security"""
    is_valid, _ = validate_safe_filename(name, max_length=100, allow_default=True)
    return is_valid


def validate_macro_name(name: str) -> bool:
    """Validate macro name for security"""
    is_valid, _ = validate_safe_filename(name, max_length=100, allow_default=False)
    return is_valid


# ============================================
# === NUMERIC INPUT VALIDATION ===
# ============================================

def validate_number(
    value: Union[int, float, str],
    min_val: float = None,
    max_val: float = None,
    allow_float: bool = True,
    name: str = "Value"
) -> Tuple[bool, str, Union[int, float, None]]:
    """Validate numeric input, returns (is_valid, error_message, parsed_value)"""
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return False, f"{name} cannot be empty", None
        try:
            parsed = float(value) if allow_float else int(value)
        except ValueError:
            return False, f"{name} must be {'a number' if allow_float else 'an integer'}", None
    else:
        parsed = float(value) if allow_float else int(value)

    if min_val is not None and parsed < min_val:
        return False, f"{name} must be at least {min_val}", None

    if max_val is not None and parsed > max_val:
        return False, f"{name} must be at most {max_val}", None

    return True, "", parsed


def validate_delay(value: Union[float, str]) -> Tuple[bool, str, float]:
    """Validate click delay (0 - 60 seconds)"""
    return validate_number(value, min_val=0, max_val=60, allow_float=True, name="Delay")


def validate_duration(value: Union[int, str]) -> Tuple[bool, str, int]:
    """Validate duration (0 = unlimited, max 86400 seconds = 24h)"""
    is_valid, error, parsed = validate_number(value, min_val=0, max_val=86400, allow_float=False, name="Duration")
    return is_valid, error, int(parsed) if parsed is not None else None


def validate_repeat(value: Union[int, str]) -> Tuple[bool, str, int]:
    """Validate repeat count (1-1000)"""
    is_valid, error, parsed = validate_number(value, min_val=1, max_val=1000, allow_float=False, name="Repeat")
    return is_valid, error, int(parsed) if parsed is not None else None


def validate_pattern_size(value: Union[int, str]) -> Tuple[bool, str, int]:
    """Validate pattern size (10-1000 pixels)"""
    is_valid, error, parsed = validate_number(value, min_val=10, max_val=1000, allow_float=False, name="Pattern Size")
    return is_valid, error, int(parsed) if parsed is not None else None


def validate_coordinates(x: Union[int, str], y: Union[int, str]) -> Tuple[bool, str, Tuple[int, int]]:
    """Validate screen coordinates"""
    is_valid_x, error_x, parsed_x = validate_number(x, min_val=0, max_val=10000, allow_float=False, name="X")
    if not is_valid_x:
        return False, error_x, (0, 0)

    is_valid_y, error_y, parsed_y = validate_number(y, min_val=0, max_val=10000, allow_float=False, name="Y")
    if not is_valid_y:
        return False, error_y, (0, 0)

    return True, "", (int(parsed_x), int(parsed_y))


# ============================================
# === HOTKEY VALIDATION ===
# ============================================

# Valid hotkey keys
VALID_HOTKEYS = {
    # Function keys
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    # Special keys
    'esc', 'escape', 'tab', 'space', 'enter', 'return', 'backspace', 'delete', 'insert',
    'home', 'end', 'pageup', 'pagedown', 'up', 'down', 'left', 'right',
    # Letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    # Numbers
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # Modifiers 
    'ctrl', 'alt', 'shift', 'win',
}


def validate_hotkey(key: str) -> Tuple[bool, str]:
    """Validate hotkey string, supports single keys (f6, esc) and combinations (ctrl+shift+a)"""
    if not key:
        return False, "Hotkey cannot be empty"

    key = key.strip().lower()
    parts = [p.strip() for p in key.split('+')]

    for part in parts:
        if part not in VALID_HOTKEYS:
            return False, f"Invalid key: '{part}'"

    # Check for duplicate modifiers
    modifiers = [p for p in parts if p in ('ctrl', 'alt', 'shift', 'win')]
    if len(modifiers) != len(set(modifiers)):
        return False, "Duplicate modifiers not allowed"

    return True, ""
