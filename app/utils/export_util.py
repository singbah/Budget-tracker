# app/utils/export_util.py
import csv
from tkinter import filedialog, messagebox

def export_transactions_to_csv(transactions):
    """Prompt the user for a save location and export transaction records to CSV."""
    if not transactions:
        messagebox.showwarning("No Data", "There are no transactions to export.")
        return
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Export Transactions to CSV"
    )
    
    if not file_path:
        return  # User canceled dialog
        
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write header row
            writer.writerow([
                "ID", "Item Name", "Price", "Category", 
                "Necessity", "Spend Rating", "Was Planned", "Date", "Notes"
            ])
            
            # Write data rows
            for t in transactions:
                writer.writerow([
                    t["id"],
                    t["item_name"],
                    t["price"],
                    t["category_name"] or "Uncategorized",
                    t["necessity_level"] or "N/A",
                    t["spend_rating"],
                    "Yes" if t["was_planned"] == 1 else "No",
                    t["date"],
                    t["notes"] or ""
                ])
                
        messagebox.showinfo("Export Successful", f"Successfully exported records to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to save CSV file: {e}")
