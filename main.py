# main.py
import tkinter as tk
from tkinter import messagebox, ttk
import os

from app.database.my_database import (
    init_db, 
    insert_transaction, 
    get_all_transactions, 
    get_categories,
    delete_transaction,
    get_current_month_total,
    get_category_breakdown, get_impulse_breakdown, 
    get_impulse_ratio, get_filtered_transactions, 
    get_transaction_by_id, update_transaction
)
from app.ui.styles import apply_global_styles
from app.utils.export_util import export_transactions_to_csv
from app.ui.edit_modal import EditTransactionModal
from app.ui.form_component import TransactionForm
from app.ui.table_component import TransactionTable
from app.ui.summary_component import SummaryBanner
from app.ui.filter_component import FilterBar
from app.ui.action_bar_component import ActionBar
from app.ui.chart_component import SpendingChart
from app.ui.impulse_component import ImpulseInsights



class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Budget & Habit Tracker")
        self.geometry("2500x1500")
        
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
        if os.path.exists(icon_path):
            self.app_icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, self.app_icon)
        
        # 1. Initialize Database & Global Styles
        init_db()
        apply_global_styles()
        
        # 2. Configure Main Window Grid Responsiveness
        self.columnconfigure(1, weight=1)  # Right panel expands horizontally
        self.rowconfigure(0, weight=1)     # Components stretch vertically
        
        # 3. Build UI Layout & Load Initial Data
        self.create_layout()
        self.refresh_ui()

    def create_layout(self):
        """Mount components side-by-side with responsive grid weights."""
        categories = get_categories()
        
        
        self.form_view = TransactionForm(
            parent=self, 
            categories=categories, 
            on_submit_callback=self.handle_form_submission
        )
        self.form_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Right Container for Summary Banner, Table, and Actions
        right_container = ttk.Frame(self)
        right_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_container.rowconfigure(1, weight=1)  # Table row expands
        right_container.columnconfigure(0, weight=1)
        
        # 1. Summary Banner Component (Row 0)
        self.summary_view = SummaryBanner(parent=right_container)
        self.summary_view.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # 2. Filter Bar Component (Row 1)
        self.filter_view = FilterBar(
            parent=right_container,
            categories=categories,
            on_filter_callback=self.handle_filter_transactions
        )
        self.filter_view.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # 3. Table Component with Zebra Striping (Row 2)
        self.table_view = TransactionTable(
                    parent=right_container,
                    on_edit_callback=self.handle_open_edit_modal
                )
        self.table_view.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # 4. Action Bar Component (Row 3)
        self.action_bar = ActionBar(
            parent=right_container,
            on_export_callback=self.handle_export_csv,
            on_delete_callback=self.handle_delete_transaction
        )
        self.action_bar.grid(row=3, column=0, sticky="e", pady=(5, 0))
        
        
        
        # 4. Spending Chart Component
        self.chart_view = SpendingChart(parent=right_container)
        self.chart_view.grid(row=4, column=0, sticky="nsew", pady=(10, 0))
        
        # 5. Impulse Insights Component
        self.impulse_view = ImpulseInsights(parent=right_container)
        self.impulse_view.grid(row=5, column=0, sticky="ew", pady=(10, 0))

        # Adjust row weights for expansion
        right_container.rowconfigure(2, weight=1)  # Table row expands

    def refresh_ui(self):
        transactions = get_all_transactions()
        self.table_view.load_data(transactions)
        
        total = get_current_month_total()
        breakdown = get_category_breakdown()
        impulse_data = get_impulse_breakdown()
        impulse_ratio = get_impulse_ratio()
        
        self.summary_view.update_summary(total, breakdown)
        self.chart_view.update_chart(breakdown)
        self.impulse_view.update_insights(impulse_ratio, impulse_data)

    def handle_form_submission(self, data):
        """Receive dictionary data from form, save to SQLite, and sync UI."""
        try:
            if not data["item_name"]:
                messagebox.showerror("Validation Error", "Item name cannot be empty.")
                return
            
            price = float(data["price"])
            
            insert_transaction(
                item_name=data["item_name"],
                price=price,
                necessity_level=data["necessity_level"],
                impulse_type=data["impulse_type"],
                spend_rating=data["spend_rating"],
                was_planned=data["was_planned"],
                notes=data["notes"],
                category_id=data["category_id"]
            )
            
            self.form_view.clear_form()
            self.refresh_ui()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value for the price.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save transaction: {e}")

    def handle_delete_transaction(self):
        """Handle deleting the selected record from database and UI."""
        trans_id = self.table_view.get_selected_transaction_id()
        
        if not trans_id:
            messagebox.showwarning("Selection Required", "Please select a transaction from the table to delete.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if confirm:
            try:
                delete_transaction(trans_id)
                self.refresh_ui()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to delete transaction: {e}")

    # Inside your BudgetApp class:
    def handle_export_csv(self):
        """Fetch all records and pass them to the export utility."""
        transactions = get_all_transactions()
        export_transactions_to_csv(transactions)
        
    # Import get_filtered_transactions from my_database in main.py

    def handle_filter_transactions(self, keyword, category_name, start_date, end_date):
        """Fetch filtered records from SQLite and load them into the table."""
        transactions = get_filtered_transactions(
            keyword=keyword, 
            category_name=category_name, 
            start_date=start_date if start_date else None, 
            end_date=end_date if end_date else None
        )
        self.table_view.load_data(transactions)
    
    # Add the handler methods inside BudgetApp class:
    def handle_open_edit_modal(self, trans_id):
        """Fetch transaction details and open the edit modal window."""
        transaction = get_transaction_by_id(trans_id)
        if not transaction:
            messagebox.showerror("Error", "Transaction not found.")
            return
            
        categories = get_categories()
        EditTransactionModal(
            parent=self,
            transaction=transaction,
            categories=categories,
            on_save_callback=self.handle_save_edited_transaction
        )

    def handle_save_edited_transaction(self, trans_id, item_name, price, necessity_level, impulse_type, spend_rating, was_planned, notes, category_id):
        """Save updated transaction data to SQLite and refresh UI."""
        try:
            update_transaction(
                trans_id=trans_id,
                item_name=item_name,
                price=price,
                necessity_level=necessity_level,
                impulse_type=impulse_type,
                spend_rating=spend_rating,
                was_planned=was_planned,
                notes=notes,
                category_id=category_id
            )
            self.refresh_ui()
            messagebox.showinfo("Success", "Transaction updated successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update transaction: {e}")
    
if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
