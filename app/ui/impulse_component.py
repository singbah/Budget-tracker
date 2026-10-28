# app/ui/impulse_component.py
import tkinter as tk
from tkinter import ttk

class ImpulseInsights(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text=" Psychological & Habit Insights ", padding="10")
        
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # Impulse Ratio Metric Label
        self.ratio_label = ttk.Label(self, text="Impulse Ratio: 0.0% of total spend", font=("Arial", 10, "bold"))
        self.ratio_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        # Driver Breakdown Container
        self.driver_frame = ttk.Frame(self)
        self.driver_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    def update_insights(self, impulse_ratio, impulse_data):
        """Update the impulse ratio metric and driver breakdown chips."""
        # Color code the ratio based on financial health thresholds
        color_tag = "#27ae60" if impulse_ratio < 20 else ("#f39c12" if impulse_ratio < 50 else "#c0392b")
        self.ratio_label.config(text=f"Unplanned Spend Ratio: {impulse_ratio:.1f}%")
        
        # Clear existing driver chips
        for widget in self.driver_frame.winfo_children():
            widget.destroy()
            
        if not impulse_data:
            ttk.Label(self.driver_frame, text="No emotional driver data this month", font=("Arial", 9, "italic")).pack(side=tk.LEFT)
            return
            
        for item in impulse_data:
            driver = item["impulse_type"] or "Unknown"
            amount = item["total"]
            count = item["count"]
            
            chip = ttk.Label(
                self.driver_frame,
                text=f"{driver}: ${amount:.2f} ({count}x)",
                padding=(6, 3),
                background="#edf2f7"
            )
            chip.pack(side=tk.LEFT, padx=3)
