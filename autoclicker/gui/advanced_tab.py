# # advanced_tab.py
# import ttkbootstrap as ttkb
# from ttkbootstrap.widgets import (Frame, Label, Checkbutton, LabelFrame, Spinbox)
# from ttkbootstrap.scrolled import ScrolledFrame
# from tkinter import BooleanVar, IntVar, DoubleVar

# from .base_tab import BaseTab
# from .card import Card


# class AdvancedTab(BaseTab):
#     """Erweiterte Einstellungen für Click-Optionen"""

#     def __init__(self, parent, manager):
#         self.repeat_var = None
#         self.random_delay_var = None
#         self.hold_click_var = None
#         self.hold_duration_var = None
#         self.sound_enabled_var = None
#         self.notify_complete_var = None
#         super().__init__(parent, manager)

#     def _build_content(self):
#         """Builds content"""

#         scroll_frame = ScrolledFrame(self, autohide=True)
#         scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
#         # Advanced Click Options
#         adv_card = Card.create(scroll_frame, "Advanced Click Options", "warning", geometry="pack", fill="x", pady=15) 
        
#         # Click repetition
#         rep_frame = Frame(adv_card)
#         rep_frame.pack(fill="x", pady=5)
        
#         Label(rep_frame, text="🔁 Repeat clicks:").pack(side="left", padx=5)
#         self.repeat_var = IntVar(value=1)
#         Spinbox(
#             rep_frame,
#             from_=1,
#             to=1000,
#             textvariable=self.repeat_var,
#             width=10,
#             bootstyle="warning"
#         ).pack(side="left", padx=5)
#         Label(rep_frame, text="times per interval").pack(side="left")
        
#         # Random delay
#         self.random_delay_var = BooleanVar(value=False)
#         rand_frame = Frame(adv_card)
#         rand_frame.pack(fill="x", pady=5)
        
#         Checkbutton(
#             rand_frame,
#             text="🎲 Add random delay (±20%)",
#             variable=self.random_delay_var,
#             bootstyle="warning-round-toggle"
#         ).pack(side="left", padx=5)
        
#         # Hold click option
#         self.hold_click_var = BooleanVar(value=False)
#         hold_frame = Frame(adv_card)
#         hold_frame.pack(fill="x", pady=5)
        
#         Checkbutton(
#             hold_frame,
#             text="⏸️ Hold click for",
#             variable=self.hold_click_var,
#             bootstyle="warning-round-toggle"
#         ).pack(side="left", padx=5)
        
#         self.hold_duration_var = DoubleVar(value=0.5)
#         Spinbox(
#             hold_frame,
#             from_=0.1,
#             to=5.0,
#             increment=0.1,
#             textvariable=self.hold_duration_var,
#             width=8,
#             bootstyle="warning"
#         ).pack(side="left", padx=5)
#         Label(hold_frame, text="seconds").pack(side="left")
        
#         # Sound feedback
#         sound_card = Card.create(scroll_frame, "Sound & Notifications", "success", geometry="pack", fill="x", pady=15)
        
#         self.sound_enabled_var = BooleanVar(value=False)
#         Checkbutton(
#             sound_card,
#             text="🔊 Enable click sounds",
#             variable=self.sound_enabled_var,
#             bootstyle="success-round-toggle"
#         ).pack(anchor="w", pady=5)
        
#         self.notify_complete_var = BooleanVar(value=True)
#         Checkbutton(
#             sound_card,
#             text="📢 Notify when complete",
#             variable=self.notify_complete_var,
#             bootstyle="success-round-toggle"
#         ).pack(anchor="w", pady=5)