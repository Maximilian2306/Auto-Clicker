# autoclicker/events.py
"""
Event Codes for Status System

This module defines all event codes used for communication between
Logic → Model → GUI layers. Event codes are simple strings that
represent state changes without any UI-specific formatting.

The GUI layer (GUIManager) is responsible for translating these
event codes into user-friendly, localized status messages.
"""


# ============================================
# === CLICKER EVENTS ===
# ============================================

CLICKER_STARTED = "CLICKER_STARTED"
CLICKER_STOPPED = "CLICKER_STOPPED"
CLICKER_COMPLETED = "CLICKER_COMPLETED"
CLICKER_PAUSED = "CLICKER_PAUSED"
CLICKER_RESUMED = "CLICKER_RESUMED"
CLICKER_WAITING = "CLICKER_WAITING"


# ============================================
# === COORDINATE CAPTURE EVENTS ===
# ============================================

CAPTURE_READY = "CAPTURE_READY"
CAPTURE_LISTENING = "CAPTURE_LISTENING"
CAPTURE_SUCCESS = "CAPTURE_SUCCESS"
CAPTURE_ERROR = "CAPTURE_ERROR"


# ============================================
# === MACRO EVENTS ===
# ============================================

MACRO_RECORDING_STARTED = "MACRO_RECORDING_STARTED"
MACRO_RECORDING_STOPPED = "MACRO_RECORDING_STOPPED"
MACRO_ALREADY_RECORDING = "MACRO_ALREADY_RECORDING"
MACRO_NOT_RECORDING = "MACRO_NOT_RECORDING"
MACRO_SAVED = "MACRO_SAVED"
MACRO_SAVE_ERROR = "MACRO_SAVE_ERROR"
MACRO_LOADED = "MACRO_LOADED"
MACRO_LOAD_ERROR = "MACRO_LOAD_ERROR"
MACRO_PLAYING = "MACRO_PLAYING"
MACRO_PLAY_COMPLETED = "MACRO_PLAY_COMPLETED"
MACRO_PLAY_ERROR = "MACRO_PLAY_ERROR"
MACRO_DELETED = "MACRO_DELETED"
MACRO_DELETE_ERROR = "MACRO_DELETE_ERROR"
MACRO_NO_EVENTS = "MACRO_NO_EVENTS"
MACRO_INVALID_NAME = "MACRO_INVALID_NAME"
MACRO_NOT_FOUND = "MACRO_NOT_FOUND"
MACRO_LIBS_UNAVAILABLE = "MACRO_LIBS_UNAVAILABLE"


# ============================================
# === PROFILE EVENTS ===
# ============================================

PROFILE_SAVED = "PROFILE_SAVED"
PROFILE_SAVE_ERROR = "PROFILE_SAVE_ERROR"
PROFILE_LOADED = "PROFILE_LOADED"
PROFILE_LOAD_ERROR = "PROFILE_LOAD_ERROR"
PROFILE_DELETED = "PROFILE_DELETED"
PROFILE_DELETE_ERROR = "PROFILE_DELETE_ERROR"
PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"


# ============================================
# === THEME EVENTS ===
# ============================================

THEME_APPLIED = "THEME_APPLIED"
THEME_APPLY_ERROR = "THEME_APPLY_ERROR"


# ============================================
# === HOTKEY EVENTS ===
# ============================================

HOTKEY_REGISTERED = "HOTKEY_REGISTERED"
HOTKEY_REGISTER_ERROR = "HOTKEY_REGISTER_ERROR"
HOTKEY_UNKNOWN = "HOTKEY_UNKNOWN"
HOTKEY_NO_CALLBACK = "HOTKEY_NO_CALLBACK"


# ============================================
# === STATISTICS EVENTS ===
# ============================================

STATS_EXPORTED = "STATS_EXPORTED"
STATS_EXPORT_ERROR = "STATS_EXPORT_ERROR"
STATS_RESET = "STATS_RESET"


# ============================================
# === GENERAL EVENTS ===
# ============================================

READY = "READY"
ERROR = "ERROR"
SUCCESS = "SUCCESS"
