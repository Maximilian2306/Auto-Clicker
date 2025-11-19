# autoclicker/utils/translation.py
"""
Translation/Localization Utility
Handles multi-language support
"""

from typing import Dict, Optional


class TranslationManager:
    """Manages translations and multi-language support"""

    def __init__(self):
        self.current_language = "en"
        self.translations: Dict[str, Dict[str, str]] = {
            "en": {
                # === App & Tabs ===
                "app_title": "ClickMAX",
                "main_controls": "Main Controls",
                "advanced": "Advanced Settings",
                "patterns": "Patterns & Macros",
                "statistics": "Statistics",
                "settings": "Settings",

                # === Main Tab ===
                "click_delay": "Click Delay",
                "duration": "Duration",
                "seconds": "seconds",
                "seconds_zero_infinite": "seconds (0 = ∞)",
                "infinite": "∞",
                "repeat_clicks": "Repeat clicks",
                "times_per_interval": "times per interval",
                "add_random_delay": "Add random delay (±20%)",
                "notify_when_done": "Notify when done",
                "click_type": "Click Type",
                "left_click": "Left Click",
                "right_click": "Right Click",
                "middle_click": "Middle Click",
                "double_click": "Double Click",
                "fixed_position": "Fixed Position",
                "x_label": "X:",
                "y_label": "Y:",
                "capture": "Capture",
                "start_clicking": "START CLICKING",
                "stop_clicking": "STOP CLICKING",
                "ready": "READY",
                "running": "RUNNING",
                "stopped": "STOPPED",
                "completed": "COMPLETED",

                # === Patterns Tab ===
                "pattern_interaction": "Choose how the mouse interacts with the pattern:",
                "pattern_size": "Pattern Size",
                "pattern_size_px": "px",
                "pause_on_move": "Pause pattern when mouse is moved",
                "macro_record": "Record",
                "macro_stop": "Stop",
                "macro_play": "Play",
                "no_macro_recorded": "No macro recorded",

                # === Statistics Tab ===
                "total_clicks": "Total Clicks",
                "session_time": "Session Time",
                "click_rate": "Click Rate",
                "export_statistics": "Export Statistics",
                "reset_statistics": "Reset Statistics",
                "ready_to_start": "Ready to start",

                # === Settings Tab ===
                "language": "Language",
                "select_theme": "Select Theme",
                "set_hotkey": "Set",
                "save": "Save",
                "load": "Load",
                "delete": "Delete",
                "profile": "Profile",
                "theme": "Theme",
                "hotkeys": "Hotkeys",

                # === Status Messages ===
                "theme_changed": "Theme changed to",
                "profile_saved": "Profile saved",
                "profile_loaded": "Profile loaded",
                "profile_deleted": "Profile deleted",
                "hotkey_set": "Hotkey set to",
                "error_setting_hotkey": "Error setting hotkey",
                "statistics_exported": "Statistics exported to",
                "error_exporting_statistics": "Error exporting statistics",
                "statistics_reset": "Statistics reset",
                "error_saving_profile": "Error saving profile",
                "profile_not_found": "Profile not found",
                "error_deleting_profile": "Error deleting profile",

                # === New Event-Based Status Messages ===
                "paused": "PAUSED",
                "waiting": "WAITING",
                "listening": "LISTENING",
                "recording": "RECORDING",
                "playing": "PLAYING",

                # Clicker Events
                "clicker_started": "Clicker started",
                "clicker_stopped": "Clicker stopped",
                "clicker_completed": "Click session completed",
                "clicker_paused": "Paused (manual mouse movement)",
                "clicker_resumed": "Resumed",
                "clicker_waiting": "Waiting for mouse to leave button",

                # Capture Events
                "capture_ready": "Ready to capture",
                "capture_listening": "Press F7 to capture mouse position",
                "capture_success": "Position captured",
                "capture_error": "Error capturing position",

                # Macro Events
                "macro_recording_started": "Recording macro (Press F4 to stop)",
                "macro_recording_stopped": "Macro recording stopped - events recorded",
                "macro_already_recording": "Already recording",
                "macro_not_recording": "Not currently recording",
                "macro_saved": "Macro saved",
                "macro_save_error": "Error saving macro",
                "macro_loaded": "Macro loaded",
                "macro_load_error": "Error loading macro",
                "macro_playing": "Playing macro",
                "macro_play_completed": "Macro playback completed",
                "macro_play_error": "No macro loaded",
                "macro_deleted": "Macro deleted",
                "macro_delete_error": "Error deleting macro",
                "macro_no_events": "No macro recorded",
                "macro_invalid_name": "Invalid macro name",
                "macro_not_found": "Macro not found",
                "macro_libs_unavailable": "Mouse/Keyboard libraries not available",

                # Profile Events
                "profile_save_error": "Error saving profile",
                "profile_load_error": "Error loading profile",
                "profile_delete_error": "Error deleting profile",

                # Theme Events
                "theme_applied": "Theme applied",
                "theme_apply_error": "Error applying theme",

                # Hotkey Events
                "hotkey_registered": "Hotkey set",
                "hotkey_register_error": "Error setting hotkey",
                "hotkey_unknown": "Unknown hotkey",
                "hotkey_no_callback": "No callback for hotkey",

                # Stats Events
                "stats_exported": "Statistics exported",
                "stats_export_error": "Error exporting statistics",
                "stats_reset": "Statistics reset",

                # === General ===
                "error": "Error",
                "success": "Success",
                "confirm": "Confirm",
                "cancel": "Cancel",
                "connected": "Connected",
                "version": "v1.0.0 Pro",

                # === Card Titles ===
                "click_configuration": "Click Configuration",
                "advanced_click_options": "Advanced Click Options",
                "position_settings": "Position Settings",
                "click_patterns": "Click Patterns",
                "pattern_behavior": "Pattern Behavior",
                "pattern_settings": "Pattern Settings",
                "macro_recording": "Macro Recording",
                "live_statistics": "Live Statistics",
                "session_progress": "Session Progress",
                "session_history": "Session History",
                "language_region": "Language & Region",
                "appearance": "Appearance",
                "hotkey_configuration": "Hotkey Configuration",
                "profile_management": "Profile Management",

                # === Pattern Names ===
                "pattern_none": "None",
                "pattern_none_desc": "No pattern",
                "pattern_circle": "Circle",
                "pattern_circle_desc": "Moves in circular pattern",
                "pattern_figure8": "Figure 8",
                "pattern_figure8_desc": "Classic figure-8 pattern",
                "pattern_square": "Square",
                "pattern_square_desc": "Square pattern",
                "pattern_star": "Star",
                "pattern_star_desc": "5-point star",
                "pattern_zigzag": "Zigzag",
                "pattern_zigzag_desc": "Zigzag pattern",
                "pattern_random": "Random",
                "pattern_random_desc": "Random positions in area",
                "pattern_spiral": "Spiral",
                "pattern_spiral_desc": "Spiral outward pattern",
                "pattern_line": "Line",
                "pattern_line_desc": "Back and forth line",

                # === Pattern Behavior ===
                "only_move": "Only Move",
                "only_move_desc": "Mouse follows pattern, no clicking",
                "click_and_move": "Click & Move",
                "click_and_move_desc": "Click at each pattern point",

                # === Hotkey Labels ===
                "hotkey_record_macro": "Record Macro",
                "hotkey_stop_macro": "Stop Macro",
                "hotkey_play_macro": "Play Macro",
                "hotkey_start_stop": "Start/Stop",
                "hotkey_exit_program": "Exit Program",
                "hotkey_capture_position": "Capture Position",

                # === Dialog Text ===
                "save_profile_dialog_title": "Save Profile",
                "save_profile_prompt": "Enter profile name:",
                "load_profile_dialog_title": "Load Profile",
                "load_profile_prompt": "Enter profile name:",
                "available_profiles": "Available profiles:",
                "delete_profile_dialog_title": "Delete Profile",
                "delete_profile_prompt": "Enter profile name:",
                "no_deletable_profiles": "No deletable profiles (Default is protected)",

                # === Status/Error Messages ===
                "auto_clicker_statistics_header": "Auto-Clicker Statistics",
                "export_dialog_title": "Export Statistics",
                "text_files": "Text files",
                "csv_files": "CSV files",
            },
            "de": {
                # === App & Tabs ===
                "app_title": "ClickMAX",
                "main_controls": "Hauptsteuerung",
                "advanced": "Erweiterte Einstellungen",
                "patterns": "Muster & Makros",
                "statistics": "Statistiken",
                "settings": "Einstellungen",

                # === Main Tab ===
                "click_delay": "Klick-Verzögerung",
                "duration": "Dauer",
                "seconds": "Sekunden",
                "seconds_zero_infinite": "Sekunden (0 = ∞)",
                "infinite": "∞",
                "repeat_clicks": "Klicks wiederholen",
                "times_per_interval": "mal pro Intervall",
                "add_random_delay": "Zufällige Verzögerung (±20%)",
                "notify_when_done": "Benachrichtigen wenn fertig",
                "click_type": "Klick-Typ",
                "left_click": "Linksklick",
                "right_click": "Rechtsklick",
                "middle_click": "Mittelklick",
                "double_click": "Doppelklick",
                "fixed_position": "Feste Position",
                "x_label": "X:",
                "y_label": "Y:",
                "capture": "Erfassen",
                "start_clicking": "KLICKEN STARTEN",
                "stop_clicking": "KLICKEN STOPPEN",
                "ready": "BEREIT",
                "running": "LÄUFT",
                "stopped": "GESTOPPT",
                "completed": "ABGESCHLOSSEN",

                # === Patterns Tab ===
                "pattern_interaction": "Wähle wie die Maus mit dem Muster interagiert:",
                "pattern_size": "Mustergröße",
                "pattern_size_px": "px",
                "pause_on_move": "Muster pausieren bei Mausbewegung",
                "macro_record": "Aufnahme",
                "macro_stop": "Stopp",
                "macro_play": "Abspielen",
                "no_macro_recorded": "Kein Makro aufgenommen",

                # === Statistics Tab ===
                "total_clicks": "Gesamtklicks",
                "session_time": "Sitzungszeit",
                "click_rate": "Klick-Geschwindigkeit",
                "export_statistics": "Statistiken exportieren",
                "reset_statistics": "Statistiken zurücksetzen",
                "ready_to_start": "Bereit zum Starten",

                # === Settings Tab ===
                "language": "Sprache",
                "select_theme": "Design auswählen",
                "set_hotkey": "Setzen",
                "save": "Speichern",
                "load": "Laden",
                "delete": "Löschen",
                "profile": "Profil",
                "theme": "Design",
                "hotkeys": "Tastenkürzel",

                # === Status Messages ===
                "theme_changed": "Design geändert zu",
                "profile_saved": "Profil gespeichert",
                "profile_loaded": "Profil geladen",
                "profile_deleted": "Profil gelöscht",
                "hotkey_set": "Tastenkürzel gesetzt auf",
                "error_setting_hotkey": "Fehler beim Setzen des Tastenkürzels",
                "statistics_exported": "Statistiken exportiert nach",
                "error_exporting_statistics": "Fehler beim Exportieren der Statistiken",
                "statistics_reset": "Statistiken zurückgesetzt",
                "error_saving_profile": "Fehler beim Speichern des Profils",
                "profile_not_found": "Profil nicht gefunden",
                "error_deleting_profile": "Fehler beim Löschen des Profils",

                # === New Event-Based Status Messages ===
                "paused": "PAUSIERT",
                "waiting": "WARTET",
                "listening": "HÖRT ZU",
                "recording": "NIMMT AUF",
                "playing": "SPIELT AB",

                # Clicker Events
                "clicker_started": "Clicker gestartet",
                "clicker_stopped": "Clicker gestoppt",
                "clicker_completed": "Klick-Sitzung abgeschlossen",
                "clicker_paused": "Pausiert (manuelle Mausbewegung)",
                "clicker_resumed": "Fortgesetzt",
                "clicker_waiting": "Wartet bis Maus den Button verlässt",

                # Capture Events
                "capture_ready": "Bereit zum Erfassen",
                "capture_listening": "Drücke F7 um Mausposition zu erfassen",
                "capture_success": "Position erfasst",
                "capture_error": "Fehler beim Erfassen der Position",

                # Macro Events
                "macro_recording_started": "Makro wird aufgenommen (Drücke F4 zum Stoppen)",
                "macro_recording_stopped": "Makroaufnahme gestoppt - Ereignisse aufgezeichnet",
                "macro_already_recording": "Nimmt bereits auf",
                "macro_not_recording": "Nimmt derzeit nicht auf",
                "macro_saved": "Makro gespeichert",
                "macro_save_error": "Fehler beim Speichern des Makros",
                "macro_loaded": "Makro geladen",
                "macro_load_error": "Fehler beim Laden des Makros",
                "macro_playing": "Makro wird abgespielt",
                "macro_play_completed": "Makro-Wiedergabe abgeschlossen",
                "macro_play_error": "Kein Makro geladen",
                "macro_deleted": "Makro gelöscht",
                "macro_delete_error": "Fehler beim Löschen des Makros",
                "macro_no_events": "Kein Makro aufgenommen",
                "macro_invalid_name": "Ungültiger Makroname",
                "macro_not_found": "Makro nicht gefunden",
                "macro_libs_unavailable": "Maus-/Tastatur-Bibliotheken nicht verfügbar",

                # Profile Events
                "profile_save_error": "Fehler beim Speichern des Profils",
                "profile_load_error": "Fehler beim Laden des Profils",
                "profile_delete_error": "Fehler beim Löschen des Profils",

                # Theme Events
                "theme_applied": "Design angewendet",
                "theme_apply_error": "Fehler beim Anwenden des Designs",

                # Hotkey Events
                "hotkey_registered": "Tastenkürzel gesetzt",
                "hotkey_register_error": "Fehler beim Setzen des Tastenkürzels",
                "hotkey_unknown": "Unbekanntes Tastenkürzel",
                "hotkey_no_callback": "Keine Funktion für Tastenkürzel",

                # Stats Events
                "stats_exported": "Statistiken exportiert",
                "stats_export_error": "Fehler beim Exportieren der Statistiken",
                "stats_reset": "Statistiken zurückgesetzt",

                # === General ===
                "error": "Fehler",
                "success": "Erfolg",
                "confirm": "Bestätigen",
                "cancel": "Abbrechen",
                "connected": "Verbunden",
                "version": "v1.0.0 Pro",

                # === Card Titles ===
                "click_configuration": "Klick-Konfiguration",
                "advanced_click_options": "Erweiterte Klick-Optionen",
                "position_settings": "Positions-Einstellungen",
                "click_patterns": "Klick-Muster",
                "pattern_behavior": "Muster-Verhalten",
                "pattern_settings": "Muster-Einstellungen",
                "macro_recording": "Makro-Aufzeichnung",
                "live_statistics": "Live-Statistiken",
                "session_progress": "Sitzungsfortschritt",
                "session_history": "Sitzungsverlauf",
                "language_region": "Sprache & Region",
                "appearance": "Erscheinungsbild",
                "hotkey_configuration": "Tastenkürzel-Konfiguration",
                "profile_management": "Profilverwaltung",

                # === Pattern Names ===
                "pattern_none": "Keins",
                "pattern_none_desc": "Kein Muster",
                "pattern_circle": "Kreis",
                "pattern_circle_desc": "Bewegt sich in kreisförmigem Muster",
                "pattern_figure8": "Figur 8",
                "pattern_figure8_desc": "Klassisches Achter-Muster",
                "pattern_square": "Quadrat",
                "pattern_square_desc": "Quadratisches Muster",
                "pattern_star": "Stern",
                "pattern_star_desc": "5-zackiger Stern",
                "pattern_zigzag": "Zickzack",
                "pattern_zigzag_desc": "Zickzack-Muster",
                "pattern_random": "Zufällig",
                "pattern_random_desc": "Zufällige Positionen im Bereich",
                "pattern_spiral": "Spirale",
                "pattern_spiral_desc": "Spiralmuster nach außen",
                "pattern_line": "Linie",
                "pattern_line_desc": "Linie hin und her",

                # === Pattern Behavior ===
                "only_move": "Nur Bewegen",
                "only_move_desc": "Maus folgt dem Muster, kein Klicken",
                "click_and_move": "Klicken & Bewegen",
                "click_and_move_desc": "An jedem Musterpunkt klicken",

                # === Hotkey Labels ===
                "hotkey_record_macro": "Makro aufnehmen",
                "hotkey_stop_macro": "Makro stoppen",
                "hotkey_play_macro": "Makro abspielen",
                "hotkey_start_stop": "Start/Stopp",
                "hotkey_exit_program": "Programm beenden",
                "hotkey_capture_position": "Position erfassen",

                # === Dialog Text ===
                "save_profile_dialog_title": "Profil speichern",
                "save_profile_prompt": "Profilname eingeben:",
                "load_profile_dialog_title": "Profil laden",
                "load_profile_prompt": "Profilname eingeben:",
                "available_profiles": "Verfügbare Profile:",
                "delete_profile_dialog_title": "Profil löschen",
                "delete_profile_prompt": "Profilname eingeben:",
                "no_deletable_profiles": "Keine löschbaren Profile (Default ist geschützt)",

                # === Status/Error Messages ===
                "auto_clicker_statistics_header": "Auto-Clicker Statistiken",
                "export_dialog_title": "Statistiken exportieren",
                "text_files": "Textdateien",
                "csv_files": "CSV-Dateien",
            },
            # === SPANISH TRANSLATIONS ===
            "es": {
                # === App & Tabs ===
                "app_title": "ClickMAX",
                "main_controls": "Controles Principales",
                "advanced": "Configuración Avanzada",
                "patterns": "Patrones y Macros",
                "statistics": "Estadísticas",
                "settings": "Configuración",

                # === Main Tab ===
                "click_delay": "Retraso de Clic",
                "duration": "Duración",
                "seconds": "segundos",
                "seconds_zero_infinite": "segundos (0 = ∞)",
                "infinite": "∞",
                "repeat_clicks": "Repetir clics",
                "times_per_interval": "veces por intervalo",
                "add_random_delay": "Añadir retraso aleatorio (±20%)",
                "notify_when_done": "Notificar al terminar",
                "click_type": "Tipo de Clic",
                "left_click": "Clic Izquierdo",
                "right_click": "Clic Derecho",
                "middle_click": "Clic Medio",
                "double_click": "Doble Clic",
                "fixed_position": "Posición Fija",
                "x_label": "X:",
                "y_label": "Y:",
                "capture": "Capturar",
                "start_clicking": "INICIAR CLIC",
                "stop_clicking": "DETENER CLIC",
                "ready": "LISTO",
                "running": "EJECUTANDO",
                "stopped": "DETENIDO",
                "completed": "COMPLETADO",

                # === Patterns Tab ===
                "pattern_interaction": "Elige cómo el ratón interactúa con el patrón:",
                "pattern_size": "Tamaño del Patrón",
                "pattern_size_px": "px",
                "pause_on_move": "Pausar patrón cuando se mueve el ratón",
                "macro_record": "Grabar",
                "macro_stop": "Detener",
                "macro_play": "Reproducir",
                "no_macro_recorded": "No hay macro grabada",

                # === Statistics Tab ===
                "total_clicks": "Clics Totales",
                "session_time": "Tiempo de Sesión",
                "click_rate": "Velocidad de Clic",
                "export_statistics": "Exportar Estadísticas",
                "reset_statistics": "Reiniciar Estadísticas",
                "ready_to_start": "Listo para comenzar",

                # === Settings Tab ===
                "language": "Idioma",
                "select_theme": "Seleccionar Tema",
                "set_hotkey": "Establecer",
                "save": "Guardar",
                "load": "Cargar",
                "delete": "Eliminar",
                "profile": "Perfil",
                "theme": "Tema",
                "hotkeys": "Atajos de Teclado",

                # === Status Messages ===
                "theme_changed": "Tema cambiado a",
                "profile_saved": "Perfil guardado",
                "profile_loaded": "Perfil cargado",
                "profile_deleted": "Perfil eliminado",
                "hotkey_set": "Atajo de teclado establecido en",
                "error_setting_hotkey": "Error al establecer atajo de teclado",
                "statistics_exported": "Estadísticas exportadas a",
                "error_exporting_statistics": "Error al exportar estadísticas",
                "statistics_reset": "Estadísticas reiniciadas",
                "error_saving_profile": "Error al guardar perfil",
                "profile_not_found": "Perfil no encontrado",
                "error_deleting_profile": "Error al eliminar perfil",

                # === New Event-Based Status Messages ===
                "paused": "PAUSADO",
                "waiting": "ESPERANDO",
                "listening": "ESCUCHANDO",
                "recording": "GRABANDO",
                "playing": "REPRODUCIENDO",

                # Clicker Events
                "clicker_started": "Clicker iniciado",
                "clicker_stopped": "Clicker detenido",
                "clicker_completed": "Sesión de clics completada",
                "clicker_paused": "Pausado (movimiento manual del ratón)",
                "clicker_resumed": "Reanudado",
                "clicker_waiting": "Esperando que el ratón salga del botón",

                # Capture Events
                "capture_ready": "Listo para capturar",
                "capture_listening": "Presiona F7 para capturar posición del ratón",
                "capture_success": "Posición capturada",
                "capture_error": "Error al capturar posición",

                # Macro Events
                "macro_recording_started": "Grabando macro (Presiona F4 para detener)",
                "macro_recording_stopped": "Grabación de macro detenida - eventos grabados",
                "macro_already_recording": "Ya está grabando",
                "macro_not_recording": "No está grabando actualmente",
                "macro_saved": "Macro guardada",
                "macro_save_error": "Error al guardar macro",
                "macro_loaded": "Macro cargada",
                "macro_load_error": "Error al cargar macro",
                "macro_playing": "Reproduciendo macro",
                "macro_play_completed": "Reproducción de macro completada",
                "macro_play_error": "No hay macro cargada",
                "macro_deleted": "Macro eliminada",
                "macro_delete_error": "Error al eliminar macro",
                "macro_no_events": "No hay macro grabada",
                "macro_invalid_name": "Nombre de macro inválido",
                "macro_not_found": "Macro no encontrada",
                "macro_libs_unavailable": "Librerías de ratón/teclado no disponibles",

                # Profile Events
                "profile_save_error": "Error al guardar perfil",
                "profile_load_error": "Error al cargar perfil",
                "profile_delete_error": "Error al eliminar perfil",

                # Theme Events
                "theme_applied": "Tema aplicado",
                "theme_apply_error": "Error al aplicar tema",

                # Hotkey Events
                "hotkey_registered": "Atajo establecido",
                "hotkey_register_error": "Error al establecer atajo",
                "hotkey_unknown": "Atajo desconocido",
                "hotkey_no_callback": "Sin función para atajo",

                # Stats Events
                "stats_exported": "Estadísticas exportadas",
                "stats_export_error": "Error al exportar estadísticas",
                "stats_reset": "Estadísticas reiniciadas",

                # === General ===
                "error": "Error",
                "success": "Éxito",
                "confirm": "Confirmar",
                "cancel": "Cancelar",
                "connected": "Conectado",
                "version": "v1.0.0 Pro",

                # === Card Titles ===
                "click_configuration": "Configuración de Clics",
                "advanced_click_options": "Opciones Avanzadas de Clic",
                "position_settings": "Configuración de Posición",
                "click_patterns": "Patrones de Clic",
                "pattern_behavior": "Comportamiento del Patrón",
                "pattern_settings": "Configuración del Patrón",
                "macro_recording": "Grabación de Macros",
                "live_statistics": "Estadísticas en Vivo",
                "session_progress": "Progreso de Sesión",
                "session_history": "Historial de Sesión",
                "language_region": "Idioma y Región",
                "appearance": "Apariencia",
                "hotkey_configuration": "Configuración de Atajos",
                "profile_management": "Gestión de Perfiles",

                # === Pattern Names ===
                "pattern_none": "Ninguno",
                "pattern_none_desc": "Sin patrón",
                "pattern_circle": "Círculo",
                "pattern_circle_desc": "Se mueve en patrón circular",
                "pattern_figure8": "Figura 8",
                "pattern_figure8_desc": "Patrón clásico de figura 8",
                "pattern_square": "Cuadrado",
                "pattern_square_desc": "Patrón cuadrado",
                "pattern_star": "Estrella",
                "pattern_star_desc": "Estrella de 5 puntas",
                "pattern_zigzag": "Zigzag",
                "pattern_zigzag_desc": "Patrón en zigzag",
                "pattern_random": "Aleatorio",
                "pattern_random_desc": "Posiciones aleatorias en área",
                "pattern_spiral": "Espiral",
                "pattern_spiral_desc": "Patrón espiral hacia afuera",
                "pattern_line": "Línea",
                "pattern_line_desc": "Línea de ida y vuelta",

                # === Pattern Behavior ===
                "only_move": "Solo Mover",
                "only_move_desc": "El ratón sigue el patrón, sin hacer clic",
                "click_and_move": "Clic y Mover",
                "click_and_move_desc": "Hacer clic en cada punto del patrón",

                # === Hotkey Labels ===
                "hotkey_record_macro": "Grabar Macro",
                "hotkey_stop_macro": "Detener Macro",
                "hotkey_play_macro": "Reproducir Macro",
                "hotkey_start_stop": "Iniciar/Detener",
                "hotkey_exit_program": "Salir del Programa",
                "hotkey_capture_position": "Capturar Posición",

                # === Dialog Text ===
                "save_profile_dialog_title": "Guardar Perfil",
                "save_profile_prompt": "Ingrese el nombre del perfil:",
                "load_profile_dialog_title": "Cargar Perfil",
                "load_profile_prompt": "Ingrese el nombre del perfil:",
                "available_profiles": "Perfiles disponibles:",
                "delete_profile_dialog_title": "Eliminar Perfil",
                "delete_profile_prompt": "Ingrese el nombre del perfil:",
                "no_deletable_profiles": "Sin perfiles eliminables (Default está protegido)",

                # === Status/Error Messages ===
                "auto_clicker_statistics_header": "Estadísticas de Auto-Clicker",
                "export_dialog_title": "Exportar Estadísticas",
                "text_files": "Archivos de texto",
                "csv_files": "Archivos CSV",
            },
            # === FRENCH TRANSLATIONS ===
            "fr": {
                # === App & Tabs ===
                "app_title": "ClickMAX",
                "main_controls": "Contrôles Principaux",
                "advanced": "Paramètres Avancés",
                "patterns": "Motifs et Macros",
                "statistics": "Statistiques",
                "settings": "Paramètres",

                # === Main Tab ===
                "click_delay": "Délai de Clic",
                "duration": "Durée",
                "seconds": "secondes",
                "seconds_zero_infinite": "secondes (0 = ∞)",
                "infinite": "∞",
                "repeat_clicks": "Répéter les clics",
                "times_per_interval": "fois par intervalle",
                "add_random_delay": "Ajouter un délai aléatoire (±20%)",
                "notify_when_done": "Notifier lorsque terminé",
                "click_type": "Type de Clic",
                "left_click": "Clic Gauche",
                "right_click": "Clic Droit",
                "middle_click": "Clic Milieu",
                "double_click": "Double Clic",
                "fixed_position": "Position Fixe",
                "x_label": "X:",
                "y_label": "Y:",
                "capture": "Capturer",
                "start_clicking": "DÉMARRER CLIC",
                "stop_clicking": "ARRÊTER CLIC",
                "ready": "PRÊT",
                "running": "EN COURS",
                "stopped": "ARRÊTÉ",
                "completed": "TERMINÉ",

                # === Patterns Tab ===
                "pattern_interaction": "Choisissez comment la souris interagit avec le motif:",
                "pattern_size": "Taille du Motif",
                "pattern_size_px": "px",
                "pause_on_move": "Mettre en pause le motif lorsque la souris bouge",
                "macro_record": "Enregistrer",
                "macro_stop": "Arrêter",
                "macro_play": "Lire",
                "no_macro_recorded": "Aucune macro enregistrée",

                # === Statistics Tab ===
                "total_clicks": "Clics Totaux",
                "session_time": "Temps de Session",
                "click_rate": "Vitesse de Clic",
                "export_statistics": "Exporter les Statistiques",
                "reset_statistics": "Réinitialiser les Statistiques",
                "ready_to_start": "Prêt à démarrer",

                # === Settings Tab ===
                "language": "Langue",
                "select_theme": "Sélectionner le Thème",
                "set_hotkey": "Définir",
                "save": "Sauvegarder",
                "load": "Charger",
                "delete": "Supprimer",
                "profile": "Profil",
                "theme": "Thème",
                "hotkeys": "Raccourcis Clavier",

                # === Status Messages ===
                "theme_changed": "Thème changé en",
                "profile_saved": "Profil sauvegardé",
                "profile_loaded": "Profil chargé",
                "profile_deleted": "Profil supprimé",
                "hotkey_set": "Raccourci clavier défini sur",
                "error_setting_hotkey": "Erreur lors de la définition du raccourci clavier",
                "statistics_exported": "Statistiques exportées vers",
                "error_exporting_statistics": "Erreur lors de l'exportation des statistiques",
                "statistics_reset": "Statistiques réinitialisées",
                "error_saving_profile": "Erreur lors de la sauvegarde du profil",
                "profile_not_found": "Profil non trouvé",
                "error_deleting_profile": "Erreur lors de la suppression du profil",

                # === New Event-Based Status Messages ===
                "paused": "EN PAUSE",
                "waiting": "EN ATTENTE",
                "listening": "ÉCOUTE",
                "recording": "ENREGISTREMENT",
                "playing": "LECTURE",

                # Clicker Events
                "clicker_started": "Clicker démarré",
                "clicker_stopped": "Clicker arrêté",
                "clicker_completed": "Session de clics terminée",
                "clicker_paused": "En pause (mouvement manuel de la souris)",
                "clicker_resumed": "Repris",
                "clicker_waiting": "En attente que la souris quitte le bouton",

                # Capture Events
                "capture_ready": "Prêt à capturer",
                "capture_listening": "Appuyez sur F7 pour capturer la position de la souris",
                "capture_success": "Position capturée",
                "capture_error": "Erreur lors de la capture de position",

                # Macro Events
                "macro_recording_started": "Enregistrement de macro (Appuyez sur F4 pour arrêter)",
                "macro_recording_stopped": "Enregistrement de macro arrêté - événements enregistrés",
                "macro_already_recording": "Enregistrement déjà en cours",
                "macro_not_recording": "Pas d'enregistrement en cours",
                "macro_saved": "Macro sauvegardée",
                "macro_save_error": "Erreur lors de la sauvegarde de la macro",
                "macro_loaded": "Macro chargée",
                "macro_load_error": "Erreur lors du chargement de la macro",
                "macro_playing": "Lecture de macro",
                "macro_play_completed": "Lecture de macro terminée",
                "macro_play_error": "Aucune macro chargée",
                "macro_deleted": "Macro supprimée",
                "macro_delete_error": "Erreur lors de la suppression de la macro",
                "macro_no_events": "Aucune macro enregistrée",
                "macro_invalid_name": "Nom de macro invalide",
                "macro_not_found": "Macro non trouvée",
                "macro_libs_unavailable": "Bibliothèques souris/clavier non disponibles",

                # Profile Events
                "profile_save_error": "Erreur lors de la sauvegarde du profil",
                "profile_load_error": "Erreur lors du chargement du profil",
                "profile_delete_error": "Erreur lors de la suppression du profil",

                # Theme Events
                "theme_applied": "Thème appliqué",
                "theme_apply_error": "Erreur lors de l'application du thème",

                # Hotkey Events
                "hotkey_registered": "Raccourci défini",
                "hotkey_register_error": "Erreur lors de la définition du raccourci",
                "hotkey_unknown": "Raccourci inconnu",
                "hotkey_no_callback": "Aucune fonction pour le raccourci",

                # Stats Events
                "stats_exported": "Statistiques exportées",
                "stats_export_error": "Erreur lors de l'exportation des statistiques",
                "stats_reset": "Statistiques réinitialisées",

                # === General ===
                "error": "Erreur",
                "success": "Succès",
                "confirm": "Confirmer",
                "cancel": "Annuler",
                "connected": "Connecté",
                "version": "v1.0.0 Pro",

                # === Card Titles ===
                "click_configuration": "Configuration des Clics",
                "advanced_click_options": "Options Avancées de Clic",
                "position_settings": "Paramètres de Position",
                "click_patterns": "Motifs de Clic",
                "pattern_behavior": "Comportement du Motif",
                "pattern_settings": "Paramètres du Motif",
                "macro_recording": "Enregistrement de Macros",
                "live_statistics": "Statistiques en Direct",
                "session_progress": "Progrès de Session",
                "session_history": "Historique de Session",
                "language_region": "Langue et Région",
                "appearance": "Apparence",
                "hotkey_configuration": "Configuration des Raccourcis",
                "profile_management": "Gestion des Profils",

                # === Pattern Names ===
                "pattern_none": "Aucun",
                "pattern_none_desc": "Aucun motif",
                "pattern_circle": "Cercle",
                "pattern_circle_desc": "Se déplace en motif circulaire",
                "pattern_figure8": "Figure 8",
                "pattern_figure8_desc": "Motif classique en figure 8",
                "pattern_square": "Carré",
                "pattern_square_desc": "Motif carré",
                "pattern_star": "Étoile",
                "pattern_star_desc": "Étoile à 5 branches",
                "pattern_zigzag": "Zigzag",
                "pattern_zigzag_desc": "Motif en zigzag",
                "pattern_random": "Aléatoire",
                "pattern_random_desc": "Positions aléatoires dans la zone",
                "pattern_spiral": "Spirale",
                "pattern_spiral_desc": "Motif en spirale vers l'extérieur",
                "pattern_line": "Ligne",
                "pattern_line_desc": "Ligne aller-retour",

                # === Pattern Behavior ===
                "only_move": "Seulement Bouger",
                "only_move_desc": "La souris suit le motif, sans cliquer",
                "click_and_move": "Cliquer et Bouger",
                "click_and_move_desc": "Cliquer à chaque point du motif",

                # === Hotkey Labels ===
                "hotkey_record_macro": "Enregistrer Macro",
                "hotkey_stop_macro": "Arrêter Macro",
                "hotkey_play_macro": "Lire Macro",
                "hotkey_start_stop": "Démarrer/Arrêter",
                "hotkey_exit_program": "Quitter le Programme",
                "hotkey_capture_position": "Capturer Position",

                # === Dialog Text ===
                "save_profile_dialog_title": "Sauvegarder le Profil",
                "save_profile_prompt": "Entrez le nom du profil:",
                "load_profile_dialog_title": "Charger le Profil",
                "load_profile_prompt": "Entrez le nom du profil:",
                "available_profiles": "Profils disponibles:",
                "delete_profile_dialog_title": "Supprimer le Profil",
                "delete_profile_prompt": "Entrez le nom du profil:",
                "no_deletable_profiles": "Aucun profil supprimable (Default est protégé)",

                # === Status/Error Messages ===
                "auto_clicker_statistics_header": "Statistiques Auto-Clicker",
                "export_dialog_title": "Exporter les Statistiques",
                "text_files": "Fichiers texte",
                "csv_files": "Fichiers CSV",
            },
        }

    def set_language(self, language_code: str) -> bool:
        """
        Set current language

        Args:
            language_code: Language code (e.g., "en", "de", "es", "fr")

        Returns:
            True if language is supported
        """
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False

    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """
        Get translated text

        Args:
            key: Translation key
            language: Optional language code (uses current if not specified)

        Returns:
            Translated text or key if not found
        """
        lang = language or self.current_language
        if lang in self.translations:
            return self.translations[lang].get(key, key)
        return key

    def get_all_languages(self) -> list[str]:
        """Get list of supported languages"""
        return list(self.translations.keys())

    def add_translation(self, language_code: str, key: str, text: str):
        """
        Add or update a translation

        Args:
            language_code: Language code
            key: Translation key
            text: Translated text
        """
        if language_code not in self.translations:
            self.translations[language_code] = {}
        self.translations[language_code][key] = text

    def add_language(self, language_code: str, translations_dict: Dict[str, str]):
        """
        Add a new language with its translations

        Args:
            language_code: Language code
            translations_dict: Dictionary of translations
        """
        self.translations[language_code] = translations_dict

    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
