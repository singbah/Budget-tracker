# app/ui/summary_component.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class SummaryBanner(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text=f" Current Month  Overview ", padding="10")
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        self.create_widgets()

    def create_widgets(self):
        # Total Monthly Spend Label
        self.total_label = ttk.Label(self, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Category Breakdown Container
        self.breakdown_frame = ttk.Frame(self)
        self.breakdown_frame.grid(row=0, column=1, sticky="e", padx=5, pady=5)

    def update_summary(self, total_spend, breakdown_data):
        """Refresh summary numbers and dynamic category breakdown tags."""
        # Update total
        self.total_label.config(text=f"Total Spend: ${total_spend:.2f}")
        
        # Clear existing breakdown widgets
        for widget in self.breakdown_frame.winfo_children():
            widget.destroy()
            
        # Rebuild breakdown chips/labels
        if not breakdown_data:
            lbl = ttk.Label(self.breakdown_frame, text="No spending this month", font=("Arial", 9, "italic"))
            lbl.pack(side=tk.RIGHT, padx=5)
        else:
            for item in breakdown_data:
                cat_name = item["category_name"] or "Uncategorized"
                cat_total = item["total"]
                
                # Create a small tag-like label for each category
                chip = ttk.Label(
                    self.breakdown_frame, 
                    text=f"{cat_name}: ${cat_total:.2f}", 
                    padding=(6, 3),
                    background="#e2e8f0"
                )
                chip.pack(side=tk.LEFT, padx=3)
