# app/ui/styles.py
import tkinter as tk
from tkinter import ttk

def apply_global_styles():
    """Configure a modern, clean global style theme for the application."""
    style = ttk.Style()
    
    # Use 'clam' as a reliable base theme that allows full color customization
    if 'clam' in style.theme_names():
        style.theme_use('clam')
        
    # Cohesive Color Palette
    BG_COLOR = "#F1F1FF"       # Soft slate background
    SURFACE_COLOR = "#ffffff"  # Pure white cards / panels
    PRIMARY_COLOR = "#1e64fb"  # Modern royal blue
    PRIMARY_HOVER = "#062e9d"  # Darker blue for hover states
    TEXT_COLOR = "#080809"     # Dark slate text for readability
    BORDER_COLOR = "#457098"   # Subtle clean borders
    DANGER_ACTION = "#FF0000"   # Subtle clean BUTTON
    
    # General Defaults
    style.configure(".", 
        background=BG_COLOR,
        foreground=TEXT_COLOR,
        font=("Segoe UI", 10)
    )
    
    # Frames & LabelFrames
    style.configure("TFrame", background=BG_COLOR)
    style.configure("TLabelframe", 
                    background=SURFACE_COLOR, bordercolor=BORDER_COLOR, 
                    relief="solid", borderwidth=1)
    style.configure("TLabelframe.Label", background=SURFACE_COLOR, foreground=PRIMARY_COLOR, font=("Segoe UI", 10, "bold"))
    
    # Standard Buttons
    style.configure("TButton",
        background="#e2e8f0",
        foreground=TEXT_COLOR,
        borderwidth=1,
        focusthickness=0,
        padding=6,
        font=("Segoe UI", 10)
    )
    style.map("TButton",
        background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")]
    )
    
    # Primary Action Buttons (Submit, Update, Export)
    style.configure("Primary.TButton",
        background=PRIMARY_COLOR,
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padding=6
    )
    
    style.configure("Danger.TButton",
        background=DANGER_ACTION,
        foreground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        padding=6
    )
    
    style.map("Primary.TButton",
        background=[("active", PRIMARY_HOVER), ("pressed", "#1e40af")],
        foreground=[("active", "#ffffff"), ("pressed", "#ffffff")]
    )
    
    # Input Fields & Comboboxes
    style.configure("TEntry", padding=5, fieldbackground=SURFACE_COLOR)
    style.configure("TCombobox", padding=5, fieldbackground=SURFACE_COLOR)
    
    # Treeview (Table) Styling
    style.configure("Treeview",
        background=SURFACE_COLOR,
        foreground=TEXT_COLOR,
        rowheight=40,
        fieldbackground=SURFACE_COLOR,
        bordercolor=BORDER_COLOR,
        borderwidth=1
    )
    style.configure("Treeview.Heading",
        background="#f1f5f9",
        foreground=TEXT_COLOR,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padding=6
    )
    style.map("Treeview.Heading",
        background=[("active", "#e2e8f0")]
    )
