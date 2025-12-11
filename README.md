# ClickMAX

A Python-based mouse automation tool with a modern GUI.

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/Maximilian2306/Auto-Clicker?style=flat&logo=git&logoColor=white&color=0080ff)
![Downloads](https://img.shields.io/github/downloads/Maximilian2306/Auto-Clicker/total?style=flat&logo=github&color=0080ff)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Hotkeys](#hotkeys)
- [System Requirements](#system-requirements)
- [Building from Source](#building-from-source)
- [License](#license)

## Features

- **Click Automation** - Configurable click delay, duration, and button
- **Click Patterns** - Circle, Square, Star, Spiral, Zigzag, Random, Figure-8, Line
- **Macro Recording** - Record and replay mouse/keyboard sequences
- **Stats Management** - Live statistics about your click session
- **Profile Management** - Save and load different configurations
- **Global Hotkeys** - Control the app from anywhere
- **Multi-Language** - English, German, Spanish, French
- **Themes** - Multiple visual themes via ttkbootstrap

## Installation

### Windows (Standalone Executable)

1. Go to [Releases](https://github.com/Maximilian2306/Auto-Clicker/releases)
2. Download `ClickMAX.exe` or `ClickMAX-Windows.zip`
3. Run `ClickMAX.exe` - no installation needed

**Note:** Warning: When starting ClickMAX.exe a Blue/Red Window (Smartscreen) Will Probably Popup.
To Run The Application You Have To Press More Info And Then Run Anyways.

### macOS / Linux / From Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Maximilian2306/Auto-Clicker
   cd Auto-Clicker
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   # venv\Scripts\activate       # Windows (if not using .exe)
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python autoclicker.py
   ```

4. **macOS only - Grant permissions:**
   - System will prompt for Accessibility permissions
   - Go to: System Settings → Privacy & Security → Accessibility
   - Add Terminal (or Python) to allowed apps

5. **Optional - Build standalone app:**
   ```bash
   python build.py
   ```
   - **Windows:** Creates `dist/ClickMAX.exe`
   - **macOS:** Creates `dist/ClickMAX.app` (move to Applications folder)
   - **Linux:** Creates `dist/ClickMAX`

## Hotkeys

| Key | Action |
|-----|--------|
| F6 | Start/Stop ClickMAX |
| F7 | Capture Coordinates |
| F3 | Start Macro Recording |
| F4 | Stop Macro Recording |
| F5 | Play Macro |
| ESC | Exit Application |

## System Requirements

- **Windows:** Windows 10/11
- **macOS:** macOS 10.13 High Sierra or newer (requires Accessibility permissions)
- **Linux:** Most modern distributions (untested but should work)
- **Python:** 3.8+ (for running from source)

## Building from Source

### Windows Build

```bash
pip install pyinstaller
python build.py
```

Output:
- `dist/ClickMAX.exe` - Standalone executable
- `dist/ClickMAX-Windows.zip` - Release package

### macOS Build

```bash
pip install pyinstaller
python build.py
```

Output:
- `dist/ClickMAX.app` - macOS application bundle
- `dist/ClickMAX-macOS.zip` - Release package

**Note:** On macOS, you may need to grant Accessibility permissions to the built app.

### Manual Build (alternative)

```bash
pyinstaller autoclicker.spec --clean
```

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for details on the codebase structure.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
