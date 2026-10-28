# app/ui/action_bar_component.py
import tkinter as tk
from tkinter import ttk

class ActionBar(ttk.Frame):
    def __init__(self, parent, on_export_callback, on_delete_callback):
        super().__init__(parent)
        self.on_export_callback = on_export_callback
        self.on_delete_callback = on_delete_callback
        
        self.create_widgets()

    def create_widgets(self):
        # Export CSV Button
        export_btn = ttk.Button(
            self, 
            text="Export to CSV", 
            style="Primary.TButton",
            command=self.on_export_callback
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delete Selected Button
        delete_btn = ttk.Button(
            self, 
            text="Delete", 
            style="Danger.TButton",
            command=self.on_delete_callback
        )
        delete_btn.pack(side=tk.LEFT)
