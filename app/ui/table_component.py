# app/ui/table_component.py
import tkinter as tk
from tkinter import ttk

class TransactionTable(ttk.Frame):
    def __init__(self, parent, on_edit_callback=None):
        super().__init__(parent, padding="10")
        self.on_edit_callback = on_edit_callback
        
        self.create_widgets()
        
        self.tree.bind("<Double-1>", self.handle_double_click)

    def handle_double_click(self, event):
        """Trigger the edit callback with the ID of the double-clicked row."""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item, "values")
        trans_id = int(row_values[0])
        
        if self.on_edit_callback:
            self.on_edit_callback(trans_id)
            
    def create_widgets(self):
        # Define table columns matching your database fields
        self.columns = (
            "id", "item_name", "price", "category_name", 
            "necessity_level", "spend_rating", "was_planned", "date"
        )
        
        # Create Treeview widget
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", selectmode="browse")
        
        # Configure column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("price", text="Price")
        self.tree.heading("category_name", text="Category")
        self.tree.heading("necessity_level", text="Necessity")
        self.tree.heading("spend_rating", text="Rating")
        self.tree.heading("was_planned", text="Planned?")
        self.tree.heading("date", text="Date")
        
        # Configure column widths and text alignment
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("item_name", width=130, anchor="w")
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("category_name", width=110, anchor="center")
        self.tree.column("necessity_level", width=90, anchor="center")
        self.tree.column("spend_rating", width=60, anchor="center")
        self.tree.column("was_planned", width=70, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        
        # --- ZEBRA STRIPE TAG CONFIGURATIONS ---
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#a8c4d2")  # Soft light-gray tint
        
        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar into the frame layout
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

    def load_data(self, transactions):
        """Clear existing rows and load fresh transaction dictionaries with zebra striping."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for index, t in enumerate(transactions):
            planned_text = "Yes" if t["was_planned"] == 1 else "No"
            
            # Alternate rows between even and odd tags
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"
            
            self.tree.insert("", tk.END, values=(
                t["id"],
                t["item_name"],
                f"${t['price']:.2f}",
                t["category_name"] or "Uncategorized",
                t["necessity_level"] or "N/A",
                t["spend_rating"],
                planned_text,
                t["date"]
            ), tags=(row_tag,))

    def get_selected_transaction_id(self):
        """Return the ID of the currently selected row in the table."""
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        
        # Get the values of the selected row (column 0 is 'id')
        row_values = self.tree.item(selected_item, "values")
        return int(row_values[0]) if row_values else None
