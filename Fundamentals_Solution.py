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
from tkinter import * # Imports all required packages from tkinter
from tkinter import messagebox

CSV_PATH = "improved_inventory.csv"
LOG_PATH = "userlog.csv"
ICOLUMNS = ["itemId", "itemName", "quantity"]
LCOLUMNS = ["Username", "Date accessed"]



class FileManagement:

    @staticmethod
    def AddUserLog(username):
        # Adds username and date accessed to logbook csv
        CSVChecker.LogCSVReady()
        with open(LOG_PATH, "a", newline ="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames = LCOLUMNS)
            row = {
                "Username"      : username,
                "Date accessed" : datetime.now()
                }
            writer.writerow(row)

    @staticmethod
    def AddItemToCSV(row):
        # Adds single row without overwriting file
        CSVChecker.ItemsCSVReady()
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: # opens csv file from end
            writer = csv.DictWriter(f, fieldnames = ICOLUMNS) # creates a writer to write to csv
            writer.writerow(row)




class CSVChecker():

    @staticmethod
    def LogCSVReady():
        # Create csv if doesnt exist or is empty
        if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0 :
            with open(LOG_PATH, "w", newline = "", encoding = "utf-8") as f:
                csv.writer(f).writerow(LCOLUMNS)

    @staticmethod
    def ItemsCSVReady():
        # Create csv if doesnt exist or is empty
        if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0 :
            with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as f:
                csv.writer(f).writerow(ICOLUMNS)





class MainWindow():

    @staticmethod
    def ValidateLogin(username, pw, frame, root):
        userId = username.get()
        password = pw.get()

        # input validation here
        if userId.lower() == "admin" and password == "4321" :
            messagebox.showinfo("Login Successful", "Admin access approved")
            CSVChecker.LogCSVReady()
            FileManagement.AddUserLog(username=userId) # Logs user and when they accessed
            frame.destroy() # Destroys login input stage when valid input entered
            
        else :
            messagebox.showerror("Login Failed", "Invalid userID or password")
            frame.destroy()
            MainWindow.Login(root)

    @staticmethod
    def AddItem():
        print("Hello World")

    @staticmethod
    def InvManagement(root):
            menubar = tk.Menu(root) # Creates a menu bar to navigate actions

            root.config(menu=menubar)
            addButton = tk.Button(menubar, text="ADD", command= lambda: MainWindow.AddItem())
            addButton.pack()
            
    @staticmethod        
    def Login(root):
        
        frame = tk.Frame(root)
        frame.pack()

        # Creation of username and password box for entry
        usernameLabel = tk.Label(frame, text="Enter UserId : ")
        usernameLabel.pack()
        username = tk.Entry(frame)
        username.pack()

        passwordLabel = tk.Label(frame, text="Enter Password : ")
        passwordLabel.pack()
        pw = tk.Entry(frame, show = "*")
        pw.pack()

        # Creation of button to verify login info
        confirmButton = tk.Button(frame, text = "Confirm", command = lambda:  MainWindow.ValidateLogin(username, pw, frame, root))
        confirmButton.pack()
        
        



        
    @staticmethod
    def StartUp() : 
        # Creation of main window
        root = tk.Tk()
        root.title("Inventory")
        root.geometry("700x400") # Resizes window

        MainWindow.Login(root) # Prompts user to log in
        MainWindow.InvManagement(root) # Continues into the main portion of the program
        root.mainloop() # Starts the TKinter main loop

        print("Finished")
        
    
    





MainWindow.StartUp()


