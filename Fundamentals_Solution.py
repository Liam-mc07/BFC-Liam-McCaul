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
LOG_PATH = "userlog.csv"
ICOLUMNS = ["itemId", "itemName", "quantity"]
LCOLUMNS = ["Username", "Date accessed"]



class CSVChecker():
    def LogCSVReady():
        # Create csv if doesnt exist or is empty
        if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0 :
            with open(LOG_PATH, "w", newline = "", encoding = "utf-8") as f:
                csv.writer(f).writerow(LCOLUMNS)


    def ItemsCSVReady():
        # Create csv if doesnt exist or is empty
        if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0 :
            with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as f:
                csv.writer(f).writerow(ICOLUMNS)



class LoginPage():

    def ValidateLogin(username, pw):
        userId = username.get()
        password = pw.get()

        # input validation here
        if userId.lower() == "admin" and password == "4321" :
            messagebox.showinfo("Login Successful", "Admin access approved")
            CSVChecker.LogCSVReady()
            AddUserLog(username=userId)
            
        else :
            messagebox.showerror("Login Failed", "Invalid userID or password")
            #exit() # Exits program
            
    def Login():
        # Main window creation
        main = tk.Tk()
        main.title("Login")
        main.geometry("700x400")

        # Creation of username and password box for entry
        usernameLabel = tk.Label(main, text="Enter UserId : ")
        usernameLabel.pack()
        username = tk.Entry(main)
        username.pack()

        passwordLabel = tk.Label(main, text="Enter Password : ")
        passwordLabel.pack()
        pw = tk.Entry(main, show = "*")
        pw.pack()

        # Creation of button to verify login info
        confirmButton = tk.Button(main, text = "Confirm", command = lambda:  LoginPage.ValidateLogin(username, pw))
        confirmButton.pack()

        # Starts the TKinter main loop
        main.mainloop()
        
    
def AddUserLog(username):
    # Adds username and date accessed to logbook csv
    CSVChecker.LogCSVReady()
    with open(LOG_PATH, "a", newline ="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames = LCOLUMNS)
        print("username")
        writer.writerow(username, datetime.now())

def AddItem(row):
    # Adds single row without overwriting file
    CSVChecker.ItemsCSVReady()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: # opens csv file from end
        writer = csv.DictWriter(f, fieldnames = ICOLUMNS) # creates a writer to write to csv
        writer.writerow(row)    

def StartUp() : 
    LoginPage.Login()
    print("Finished")



StartUp()


