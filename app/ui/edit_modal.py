# app/ui/edit_modal.py
import tkinter as tk
from tkinter import ttk, messagebox

class EditTransactionModal(tk.Toplevel):
    def __init__(self, parent, transaction, categories, on_save_callback):
        super().__init__(parent)
        self.title("Edit Transaction")
        self.geometry("400x500")
        self.trans_id = transaction["id"]
        self.categories = categories
        self.on_save_callback = on_save_callback
        
        self.columnconfigure(1, weight=1)
        self.create_widgets(transaction)

    def create_widgets(self, t):
        # Item Name
        ttk.Label(self, text="Item Name:").grid(row=0, column=0, sticky="w", pady=6, padx=10)
        self.item_entry = ttk.Entry(self)
        self.item_entry.grid(row=0, column=1, sticky="ew", pady=6, padx=10)
        self.item_entry.insert(0, t["item_name"])
        
        # Price
        ttk.Label(self, text="Price ($):").grid(row=1, column=0, sticky="w", pady=6, padx=10)
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=1, column=1, sticky="ew", pady=6, padx=10)
        self.price_entry.insert(0, str(t["price"]))
        
        # Category Dropdown
        ttk.Label(self, text="Category:").grid(row=2, column=0, sticky="w", pady=6, padx=10)
        category_names = [name for _, name in self.categories]
        self.category_map = {name: cat_id for cat_id, name in self.categories}
        id_to_name = {cat_id: name for cat_id, name in self.categories}
        
        self.category_cb = ttk.Combobox(self, values=category_names, state="readonly")
        self.category_cb.grid(row=2, column=1, sticky="ew", pady=6, padx=10)
        current_cat_name = id_to_name.get(t["category_id"], category_names[0] if category_names else "")
        self.category_cb.set(current_cat_name)
        
        # Necessity Level
        ttk.Label(self, text="Necessity:").grid(row=3, column=0, sticky="w", pady=6, padx=10)
        self.necessity_cb = ttk.Combobox(self, values=["Essential", "Optional", "Luxury"], state="readonly")
        self.necessity_cb.grid(row=3, column=1, sticky="ew", pady=6, padx=10)
        self.necessity_cb.set(t["necessity_level"] or "Optional")
        
        # Intent / Impulse
        ttk.Label(self, text="Intent:").grid(row=4, column=0, sticky="w", pady=6, padx=10)
        self.impulse_cb = ttk.Combobox(self, values=["Planned", "Impulse", "Convenience", "Peer Pressure"], state="readonly")
        self.impulse_cb.grid(row=4, column=1, sticky="ew", pady=6, padx=10)
        self.impulse_cb.set(t["impulse_type"] or "Planned")
        
        # Spend Rating
        ttk.Label(self, text="Spend Rating:").grid(row=5, column=0, sticky="w", pady=6, padx=10)
        self.rating_cb = ttk.Combobox(self, values=[
            "1 - Regret / Waste", "2 - Questionable", "3 - Fair", "4 - Good", "5 - Smart / Worth It"
        ], state="readonly")
        self.rating_cb.grid(row=5, column=1, sticky="ew", pady=6, padx=10)
        rating_val = t["spend_rating"] or 3
        for val in self.rating_cb["values"]:
            if val.startswith(str(rating_val)):
                self.rating_cb.set(val)
                break
                
        # Was Planned Checkbox
        self.was_planned_var = tk.IntVar(value=t["was_planned"])
        self.planned_chk = ttk.Checkbutton(self, text="Was this purchase planned?", variable=self.was_planned_var)
        self.planned_chk.grid(row=6, column=0, columnspan=2, sticky="w", pady=8, padx=10)
        
        # Notes
        ttk.Label(self, text="Notes:").grid(row=7, column=0, sticky="nw", pady=6, padx=10)
        self.notes_text = tk.Text(self, height=4, font=("Arial", 10))
        self.notes_text.grid(row=7, column=1, sticky="ew", pady=6, padx=10)
        if t["notes"]:
            self.notes_text.insert("1.0", t["notes"])
            
        # Save Button
        save_btn = ttk.Button(self, text="Update Transaction", command=self.handle_save)
        save_btn.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(15, 10), padx=10)

    def handle_save(self):
        try:
            item_name = self.item_entry.get().strip()
            price = float(self.price_entry.get().strip())
            category_id = self.category_map.get(self.category_cb.get())
            necessity_level = self.necessity_cb.get()
            impulse_type = self.impulse_cb.get()
            spend_rating = int(self.rating_cb.get().split(" - ")[0])
            was_planned = self.was_planned_var.get()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if not item_name:
                messagebox.showerror("Error", "Item name cannot be empty.")
                return
                
            if self.on_save_callback:
                self.on_save_callback(
                    self.trans_id, item_name, price, necessity_level, 
                    impulse_type, spend_rating, was_planned, notes, category_id
                )
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric price.")
