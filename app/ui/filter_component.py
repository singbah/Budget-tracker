import tkinter as tk
from tkinter import ttk

class FilterBar(ttk.LabelFrame):
    def __init__(self, parent, categories, on_filter_callback, total_stuff=0.0):
        super().__init__(parent, text=" Filter & Search ", padding="10")
        self.categories = categories
        self.total_stuff = total_stuff
        self.on_filter_callback = on_filter_callback
        
        self.columnconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # Row 0: Search & Category
        ttk.Label(self, text="Search:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.search_entry.bind("<KeyRelease>", self.trigger_filter)
        
        ttk.Label(self, text="Category:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        cat_names = ["All Categories"] + [name for _, name in self.categories]
        self.category_cb = ttk.Combobox(self, values=cat_names, state="readonly", width=14)
        self.category_cb.grid(row=0, column=3, sticky="ew", padx=5, pady=2)
        self.category_cb.current(0)
        self.category_cb.bind("<<ComboboxSelected>>", self.trigger_filter)
        
        # Row 1: Date Range Pickers (YYYY-MM-DD)
        ttk.Label(self, text="From:").grid(row=1, column=0, sticky="w", padx=5, pady=(5, 2))
        self.start_date_entry = ttk.Entry(self, width=12)
        self.start_date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=(5, 2))
        self.start_date_entry.bind("<KeyRelease>", self.trigger_filter)
        
        ttk.Label(self, text="To:").grid(row=1, column=2, sticky="w", padx=5, pady=(5, 2))
        self.end_date_entry = ttk.Entry(self, width=12)
        self.end_date_entry.grid(row=1, column=3, sticky="w", padx=5, pady=(5, 2))
        self.end_date_entry.bind("<KeyRelease>", self.trigger_filter)
        
        # Total Label
        self.total_label = ttk.Label(self, text=f" Total : \n${self.total_stuff:.2f} ", style="Danger.TButton", justify="center")
        self.total_label.grid(row=0, column=4, rowspan=2, padx=10, sticky="nsew")
        
        # Reset Button
        reset_btn = ttk.Button(self, text="Reset Filters", command=self.reset_filters, style="Primary.TButton")
        reset_btn.grid(row=0, column=5, rowspan=2, padx=10, sticky="nsew")

    def update_total(self, new_total):
        """Dynamically updates the displayed total amount."""
        self.total_label.config(text=f" Total : \n${new_total:.2f} ")

    def trigger_filter(self, event=None):
        keyword = self.search_entry.get().strip().lower()
        selected_cat = self.category_cb.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        
        if self.on_filter_callback:
            self.on_filter_callback(keyword, selected_cat, start_date, end_date)

    def reset_filters(self):
        self.search_entry.delete(0, tk.END)
        self.category_cb.current(0)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.trigger_filter()
