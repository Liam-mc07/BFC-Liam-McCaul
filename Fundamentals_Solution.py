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
from tkinter import messagebox # Import needed to output approved/error window
from tkinter import ttk # Import needed to use data tree to display data

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

class Operations():
    
    @staticmethod
    def AddItem():
        print()

    @staticmethod
    def RemoveItem():
        print()

    @staticmethod
    def IncrementItem():
        print()

    @staticmethod
    def DecrementItem():
        print()

    @staticmethod
    def ClearTable():
        print()



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

            MainWindow.InvSetup(root) # Continues into the main portion of the program
            
        else :
            messagebox.showerror("Login Failed", "Invalid userID or password")
            frame.destroy()
            MainWindow.Login(root)



    @staticmethod
    def ItemTable(root, parent, columns):
        
        table = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col.upper()) # Displays each column header for table
            table.column(col, width=150, anchor="center") # Formats the columns for table

        table.pack(fill="both", expand=True)
        return table
    

    @staticmethod
    def InvSetup(root):
            bottomFrame = tk.Frame(root, bg = "white")
            bottomFrame.place(relx=0, rely=1/6, relwidth=1, relheight=5/6) # Formats the frame to take up 5/6 of the root window

            table = MainWindow.ItemTable(root, bottomFrame, ICOLUMNS) # Creates the table inside frame
            
            # EXAMPLE TO INSERT ROW
            table.insert("", "end", values=["id1", "item1", "1"])


    @staticmethod
    def NavBarSetup(root):

            topFrame = tk.Frame(root, bg = "gray")
            topFrame.place(relx=0, rely=5/6, relwidth=1, relheight=1/6)
            
            addButton    = tk.Button(topFrame, text="ADD", command=Operations.AddItem())
            removeButton = tk.Button(topFrame, text="REMOVE", command=Operations.RemoveItem())

            
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

        root.mainloop() # Starts the TKinter main loop

        print("Finished")
        
    
    





MainWindow.StartUp()


