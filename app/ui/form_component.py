# app/ui/form_component.py
import tkinter as tk
from tkinter import ttk

class TransactionForm(ttk.LabelFrame):
    def __init__(self, parent, categories, on_submit_callback):
        super().__init__(parent, text=" Add New Transaction ", padding="15")
        self.categories = categories  # Expected list of (id, name) tuples
        self.on_submit_callback = on_submit_callback
        
        self.columnconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        # 1. Item Name
        ttk.Label(self, text="Item Name:").grid(row=0, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.item_entry = ttk.Entry(self)
        self.item_entry.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        
        # 2. Price
        ttk.Label(self, text="Price ($):").grid(row=1, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=1, column=1, sticky="ew", pady=(0, 8))
        
        # 3. Category Dropdown
        ttk.Label(self, text="Category:").grid(row=2, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        cat_names = [name for _, name in self.categories]
        self.category_map = {name: cat_id for cat_id, name in self.categories}
        
        self.category_cb = ttk.Combobox(self, values=cat_names, state="readonly")
        self.category_cb.grid(row=2, column=1, sticky="ew", pady=(0, 8))
        if cat_names:
            self.category_cb.current(0)
            
        # 4. Necessity Level
        ttk.Label(self, text="Necessity:").grid(row=3, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.necessity_cb = ttk.Combobox(self, values=["Essential", "Optional", "Luxury"], state="readonly")
        self.necessity_cb.grid(row=3, column=1, sticky="ew", pady=(0, 8))
        self.necessity_cb.current(1)  # Default to Optional
        
        # 5. Intent / Impulse Driver
        ttk.Label(self, text="Intent:").grid(row=4, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.impulse_cb = ttk.Combobox(self, values=["Planned", "Impulse", "Convenience", "Peer Pressure"], state="readonly")
        self.impulse_cb.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        self.impulse_cb.current(0)  # Default to Planned
        
        # 6. Spend Rating
        ttk.Label(self, text="Spend Rating:").grid(row=5, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.rating_cb = ttk.Combobox(self, values=[
            "1 - Regret / Waste", "2 - Questionable", "3 - Fair", "4 - Good", "5 - Smart / Worth It"
        ], state="readonly")
        self.rating_cb.grid(row=5, column=1, sticky="ew", pady=(0, 8))
        self.rating_cb.current(2)  # Default to 3 - Fair
        
        # 7. Was Planned Checkbox
        # Use standard tk.Checkbutton for better visibility, font scaling, and styling control
        self.was_planned_var = tk.IntVar(value=1)
        self.planned_chk = tk.Checkbutton(
            self, 
            text=" Was this purchase planned?", 
            variable=self.was_planned_var,
            font=("Segoe UI", 10),
            bg="#ffffff",          # Matches your white card background
            activebackground="#ffffff",
            selectcolor="#ffffff", # Background of the check box itself when checked
            anchor="w"
        )
        self.planned_chk.grid(row=6, column=0, columnspan=2, sticky="w", pady=(4, 12))
        
        # 8. Notes Text Area
        ttk.Label(self, text="Notes:").grid(row=7, column=0, sticky="nw", pady=(0, 8), padx=(0, 10))
        self.notes_text = tk.Text(self, height=4, font=("Segoe UI", 9), relief="solid", borderwidth=1)
        self.notes_text.grid(row=7, column=1, sticky="ew", pady=(0, 12))
        
        # 9. Submit Button (Using Primary style)
        submit_btn = ttk.Button(self, text="Add Transaction", style="Primary.TButton", command=self.submit_data)
        submit_btn.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(5, 0))

    def submit_data(self):
        """Extract form values and pass them to the main controller callback."""
        item_name = self.item_entry.get().strip()
        price_str = self.price_entry.get().strip()
        category_name = self.category_cb.get()
        category_id = self.category_map.get(category_name)
        
        necessity_level = self.necessity_cb.get()
        impulse_type = self.impulse_cb.get()
        
        # Extract numeric rating from start of string (e.g., '3 - Fair' -> 3)
        rating_selection = self.rating_cb.get()
        spend_rating = int(rating_selection.split(" - ")[0]) if rating_selection else 3
        
        was_planned = self.was_planned_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        data = {
            "item_name": item_name,
            "price": price_str,
            "category_id": category_id,
            "necessity_level": necessity_level,
            "impulse_type": impulse_type,
            "spend_rating": spend_rating,
            "was_planned": was_planned,
            "notes": notes
        }
        
        if self.on_submit_callback:
            self.on_submit_callback(data)

    def clear_form(self):
        """Reset all input fields back to their defaults."""
        self.item_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        if self.categories:
            self.category_cb.current(0)
        self.necessity_cb.current(1)
        self.impulse_cb.current(0)
        self.rating_cb.current(2)
        self.was_planned_var.set(1)
        self.notes_text.delete("1.0", tk.END)
