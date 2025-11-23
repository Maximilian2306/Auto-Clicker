# autoclicker/utils/translation.py
"""Translation/Localization Utility - Multi-language support"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional


class TranslationManager:
    """Manages translations and multi-language support"""

    def __init__(self):
        self.current_language = "en"
        self.translations: Dict[str, Dict[str, str]] = {}
        self._load_all_translations()

    def _load_all_translations(self) -> None:
        """Load all translation files from translations directory"""
        # PyInstaller compatibility: use _MEIPASS for bundled app
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
            translations_dir = base_path / "autoclicker" / "translations"
        else:
            translations_dir = Path(__file__).parent.parent / "translations"

        if not translations_dir.exists():
            print(f"[WARN] Translations directory not found: {translations_dir}")
            return

        for json_file in translations_dir.glob("*.json"):
            lang_code = json_file.stem  # e.g., "en" from "en.json"
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to load translation {json_file}: {e}")

    def set_language(self, language_code: str) -> bool:
        """Set current language. Returns True if supported."""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False

    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """Get translated text or key if not found"""
        lang = language or self.current_language
        if lang in self.translations:
            return self.translations[lang].get(key, key)
        return key

    def get_all_languages(self) -> list[str]:
        """Get list of supported languages"""
        return list(self.translations.keys())

    def add_translation(self, language_code: str, key: str, text: str):
        """Add or update a translation"""
        if language_code not in self.translations:
            self.translations[language_code] = {}
        self.translations[language_code][key] = text

    def add_language(self, language_code: str, translations_dict: Dict[str, str]):
        """Add a new language with its translations"""
        self.translations[language_code] = translations_dict

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
