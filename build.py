#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Auto-Clicker application.
Creates a standalone executable using PyInstaller.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def clean_build_directories():
    """Remove old build artifacts."""
    print("[*] Cleaning build directories...")

    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

    print("[OK] Cleanup complete\n")


def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    print("[*] Checking PyInstaller...")

    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} found\n")
    except ImportError:
        print("   Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed\n")


def build_executable():
    """Build the executable using PyInstaller."""
    print("[*] Building executable...")

    # Run PyInstaller with the spec file
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "autoclicker.spec", "--clean"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ERROR] Build failed!")
        print(result.stderr)
        sys.exit(1)

    print("[OK] Build complete\n")


def verify_build():
    """Verify the build was successful."""
    print("[*] Verifying build...")

    exe_path = Path("dist/AutoClicker.exe")

    if not exe_path.exists():
        print("[ERROR] AutoClicker.exe not found in dist/")
        sys.exit(1)

    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"[OK] AutoClicker.exe created ({size_mb:.2f} MB)")
    print(f"   Location: {exe_path.absolute()}\n")


def create_zip_release():
    """Create a ZIP file for release."""
    print("[*] Creating release ZIP...")

    zip_name = "AutoClicker-Windows"

    # Create a temporary directory with release contents
    release_dir = Path("dist/release_temp")
    release_dir.mkdir(exist_ok=True)

    # Copy executable
    shutil.copy("dist/AutoClicker.exe", release_dir / "AutoClicker.exe")

    # Copy README if it exists
    if Path("README.md").exists():
        shutil.copy("README.md", release_dir / "README.md")

    # Create ZIP
    shutil.make_archive(f"dist/{zip_name}", 'zip', release_dir)

    # Cleanup temp directory
    shutil.rmtree(release_dir)

    print(f"[OK] Created {zip_name}.zip\n")


def main():
    """Main build process."""
    print("=" * 60)
    print("Auto-Clicker Build Script")
    print("=" * 60 + "\n")

    try:
        clean_build_directories()
        install_pyinstaller()
        build_executable()
        verify_build()
        create_zip_release()

        print("=" * 60)
        print("Build successful!")
        print("=" * 60)
        print("\nRelease files:")
        print("  - dist/AutoClicker.exe")
        print("  - dist/AutoClicker-Windows.zip")
        print("\nYou can now upload these to GitHub Releases.")

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
