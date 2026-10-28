# app/ui/chart_component.py
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SpendingChart(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text=" Spending by Category ", padding="10")
        
        # Create Matplotlib Figure
        self.fig = Figure(figsize=(5, 2.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Embed canvas into Tkinter frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_chart(self, breakdown_data):
        """Redraw the pie chart with fresh category spending data."""
        self.ax.clear()
        
        if not breakdown_data:
            self.ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.fig.tight_layout()
            self.canvas.draw()
            return
            
        labels = [item["category_name"] or "Uncategorized" for item in breakdown_data]
        values = [item["total"] for item in breakdown_data]
        
        # Draw a clean pie chart
        self.ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14})
        self.ax.axis('equal')  # Equal aspect ratio ensures pie is circular
        
        self.fig.tight_layout()
        self.canvas.draw()
