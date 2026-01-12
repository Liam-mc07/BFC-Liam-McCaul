#What is needed: 
#
# Modular
# Multiple paradigms
# Input validation/error handling
# Meaningful commenting
# Maintainable


import csv, os
from datetime import datetime
import tkinter as tk

CSV_PATH = "improved_inventory.csv"
COLUMNS = ["itemId", "itemName", "quantity"]

root = tk.Tk()
root.title("Inventory Tracker")




def CSVReady():
    #Create csv if doesnt exist or is empty
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0 :
        with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as f:
            csv.writer(f).writerow(COLUMNS)

def AppendRow(row):
    #Adds single row without overwriting file
    CSVReady()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: #opens csv file from end
        writer = csv.DictWriter(f, fieldnames = COLUMNS) #creates a writer to write to csv

def StartUp() : 
    print("Hello World!")


StartUp()
