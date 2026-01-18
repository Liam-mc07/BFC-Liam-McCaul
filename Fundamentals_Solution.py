#What is needed: 
#
# Modular
# Multiple paradigms
# Input validation/error handling
# Meaningful commenting
# Maintainable


import csv, os # Allows csv file to be used and brings in my local OS
from datetime import datetime
import tkinter as tk # Library to create GUI
from tkinter import messagebox # Required for taking username and password input

CSV_PATH = "improved_inventory.csv"
COLUMNS = ["itemId", "itemName", "quantity"]

root = tk.Tk()
root.title("Inventory Tracker")




def CSVReady():
    # Create csv if doesnt exist or is empty
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0 :
        with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as f:
            csv.writer(f).writerow(COLUMNS)

def AppendRow(row):
    # Adds single row without overwriting file
    CSVReady()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: # opens csv file from end
        writer = csv.DictWriter(f, fieldnames = COLUMNS) # creates a writer to write to csv

def ValidateLogin():
    userId = username.get()
    password = pw.get()

    # input validation here
    if userId == "admin" and password == "4321" :
        messagebox.showinfo("Login Successful", "Admin access approved")
    else :
        messagebox.showerror("Login Failed", "Invalid userID or password")



def StartUp() : 
    # Main window creation
    main = tk.Tk()
    main.title("Login")

    # Creation of username and password box for entry
    usernameLabel = tk.Label(main, text="Enter UserId : ")
    usernameLabel.pack()
    passwordLabel = tk.Label(main, text="Enter Password : ")
    passwordLabel.pack()

    # Creation of button to verify login info
    confirmButton = tk.Button(main, text = "Confirm", command = ValidateLogin)
    confirmButton.pack()

    # Starts the TKinter main loop
    main.mainloop()

StartUp()


