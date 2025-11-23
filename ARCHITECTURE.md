# Architecture

ClickMAX uses an MVC architecture with clear separation between GUI, logic, and data.

## Overview

```
autoclicker.py (Entry Point)
    |
    v
ApplicationModel (Controller) <---> GUIManager (View)
    |
    v
Logic Components (Model)
```

## Project Structure

```
autoclicker/
├── model.py              # Central controller (facade pattern)
├── events.py             # Event codes for status system
│
├── gui/                  # View Layer
│   ├── gui_manager.py    # Main coordinator
│   ├── handlers/         # Status and profile handlers
│   ├── components/       # UI components (tabs, buttons, cards)
│   └── utils.py          # UI helper functions
│
├── logic/                # Model Layer
│   ├── clicker.py        # Auto-click engine
│   ├── macro_recording.py# Macro recording/playback
│   ├── profiles.py       # Profile management
│   ├── setup_hotkeys.py  # Global hotkeys
│   ├── stats.py          # Statistics tracking
│   └── capture_coordinates.py
│
└── utils/                # Utilities
    ├── constants.py      # Centralized constants
    ├── validators.py     # Input validation
    ├── translation.py    # Multi-language support
    ├── theme.py          # Theme management
    └── toast_notification.py
```

## Communication Flow

### User Action to Logic

```
User clicks button
    -> GUIManager handles event
    -> ApplicationModel method
    -> Logic component executes
```

### Logic to GUI Update

```
Logic component sends event
    -> ApplicationModel receives callback
    -> GUIManager.update_status()
    -> root.after() for thread-safe UI update
```

## Key Concepts

### Event System

Status changes are communicated via event codes defined in `events.py`. This keeps logic components independent of GUI implementation.

```python
# Logic sends:
on_status(CLICKER_STARTED)

# GUIManager receives and translates:
StatusHandler.handle(CLICKER_STARTED)
```

### Thread Safety

All GUI updates from background threads use `root.after()`:

```python
self.gm.root.after(0, lambda: self._update_ui(event_code))
```

This applies to:
- Stats updater thread
- Hotkey callbacks
- Clicker thread
- Macro player thread

### Callback Pattern

The model registers callbacks for loose coupling:

```python
# GUIManager registers:
self.model.set_status_callback(self.update_status)

# Model calls:
if self.on_status_changed:
    self.on_status_changed(CLICKER_STARTED)
```

## Configuration Storage

| File | Location | Content |
|------|----------|---------|
| Profiles | `~/.autoclicker_profiles.json` | User profiles |
| Last Profile | `~/.autoclicker_last_profile.json` | Auto-load on startup |
| Macros | `~/.autoclicker_macros/*.json` | Saved macros |

## Threading

| Thread | Purpose | Communication |
|--------|---------|---------------|
| Main (Tkinter) | UI events, rendering | - |
| Stats Updater | Statistics every 1s | `root.after()` |
| Clicker | Execute clicks | Callbacks + `root.after()` |
| Hotkey Listener | Global hotkeys | `root.after()` |
| Macro Player | Macro playback | Callbacks + `root.after()` |

## Dependencies

- **ttkbootstrap** - Modern Tkinter UI
- **pyautogui** - Mouse/keyboard automation
- **keyboard** - Global hotkeys
- **mouse** - Mouse event hooks
- **pillow** - Image processing

## Design Rules

- GUI -> Model -> Logic (never GUI -> Logic directly)
- Use callbacks for all feedback
- Use `root.after()` for GUI updates from other threads
- Use event codes instead of strings
- Keep constants in `constants.py`
- Don't update Tkinter widgets from background threads

