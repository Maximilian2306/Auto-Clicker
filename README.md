# Auto-Clicker

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
- **Profile Management** - Save and load different configurations
- **Global Hotkeys** - Control the app from anywhere
- **Multi-Language** - English, German, Spanish, French
- **Themes** - Multiple visual themes via ttkbootstrap

## Installation

### For Users (No Python Required)

1. Go to [Releases](https://github.com/Maximilian2306/Auto-Clicker/releases)
2. Download `AutoClicker.exe` or `AutoClicker-Windows.zip`
3. Run `AutoClicker.exe` - no installation needed

**Note:** Windows Defender may show a warning for unsigned executables. Add an exception if needed.

### For Developers

```bash
# Clone the repository
git clone https://github.com/Maximilian2306/Auto-Clicker
cd Auto-Clicker

# Install dependencies with safe venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run
python autoclicker.py
```

## Hotkeys

| Key | Action |
|-----|--------|
| F6 | Start/Stop Auto-Clicker |
| F7 | Capture Coordinates |
| F3 | Start Macro Recording |
| F4 | Stop Macro Recording |
| F5 | Play Macro |
| ESC | Exit Application |

## System Requirements

- Windows 10/11
- Python 3.8+ (for running from source)

## Building from Source

### Local Build

```bash
pip install pyinstaller
python build.py
```

### Manual Build (alternative)

```bash
pyinstaller autoclicker.spec --clean
```

Output:
- `dist/AutoClicker.exe` - Standalone executable
- `dist/AutoClicker-Windows.zip` - Release package

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for details on the codebase structure.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
