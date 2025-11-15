# autoclicker/autoclicker.py
"""
ClickMax Pro 
MVC Architecture: GUI ← GUIManager ← Model ← Logic

"""

from autoclicker.gui.gui_manager import GUIManager
from autoclicker.model import ApplicationModel

def main():
    """
    Main application entry point
    
    """
    
    # === Initialize Model ===
    model = ApplicationModel()
    print("[OK] ApplicationModel initialized")

    # === Initialize GUI Manager ===
    gui = GUIManager(model)
    print("[OK] GUIManager initialized")

    # === Start stats updater ===
    model.start_stats_updater()
    print("[OK] Stats updater started")

    # === Start Application ===
    print("[OK] Starting Application...")
    gui.run()


if __name__ == "__main__":
    main()