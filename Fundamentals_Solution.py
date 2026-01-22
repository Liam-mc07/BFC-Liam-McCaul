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
from tkinter import messagebox # Import needed to output approved/error window
from tkinter import ttk # Import needed to use data tree to display data

CSV_PATH  = "improved_inventory.csv"
LOG_PATH  = "userlog.csv"
USER_PATH = "usernames.csv"
ICOLUMNS  = ["itemId", "itemName", "quantity"]
LCOLUMNS  = ["Username", "Date accessed"]
UCOLUMNS  = ["Username", "Password"]

################################################################################################################

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
    def AddUsername(username, pw):

        CSVChecker.UsersCSVReady()

        with open(USER_PATH, "a", newline ="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames = UCOLUMNS)
            row = {
                "Username" : username,
                "Password" : pw
                }
            writer.writerow(row)


    @staticmethod
    def AddItemToCSV(row):
        # Adds single row without overwriting file
        CSVChecker.ItemsCSVReady()
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: # opens csv file from end
            writer = csv.DictWriter(f, fieldnames = ICOLUMNS) # creates a writer to write to csv
            writer.writerow(row)

    @staticmethod
    def RemoveItemFromCSV(itemId):
        CSVChecker.ItemsCSVReady()

        rows = [] # New variable to store all rows excluding that with target itemId

        # Saves all rows in file to rows variable other than target itemId
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["itemId"] != itemId:
                    rows.append(row)
        
        # Writes new rows variable to file
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ICOLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def ClearItemsCSV():
        
        rows = []
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ICOLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def AlterCSVQuantity(itemId, quantity):

        CSVChecker.ItemsCSVReady()

        rows = []
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["itemId"] == itemId: # Only alters item which has chosen id
                    row["quantity"] = quantity
                rows.append(row)

        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ICOLUMNS)
            writer.writeheader()
            writer.writerows(rows)
    
    @staticmethod
    def IsInPwCSV(username, pw):
        
        users = FileManagement.LoadUsernames_Pw()
        isCorrect = False
        isPresent = False

        for row in users:
            if row["Username"] == username:
                isPresent = True
                return row["Password"] == pw   
        FileManagement.AddUsername(username, pw)
        return True
            

            
        




    @staticmethod
    def LoadItems(): # Returns all items stored in csv file

        CSVChecker.ItemsCSVReady()

        items = []
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
        return items
    
    @staticmethod
    def LoadUsernames_Pw():

        CSVChecker.UsersCSVReady()

        users = []
        with open(USER_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
        return users
    
    
######################################################################################################################


class CSVChecker():

    @staticmethod
    def UsersCSVReady():
        if not os.path.exists(USER_PATH) or os.path.getsize(USER_PATH) == 0 :
            with open(USER_PATH, "w", newline = "", encoding = "utf-8") as f:
                csv.writer(f).writerow(UCOLUMNS)



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
    
##############################################################################################################

class Operations():
    
    table      = None # Shared reference so all methods can access
    root       = None
    tableFrame = None

    @staticmethod
    def AddItem():
        if Operations.tableFrame:
            Operations.tableFrame.place_forget()  # Hides the table frame before add frame created
        
        addFrame = tk.Frame(Operations.root)
        addFrame.place(relx=0, rely= 1/6, relwidth=1, relheight=5/6)

        tk.Label(addFrame, text="ItemID : ").pack(pady=5) # Creates input label for each field needed to be inputted
        itemIdin = tk.Entry(addFrame)
        itemIdin.pack()

        tk.Label(addFrame, text="Item Name").pack(pady=5)
        itemNamein = tk.Entry(addFrame)
        itemNamein.pack()

        tk.Label(addFrame, text="Quantity").pack(pady=5)
        quantityin = tk.Entry(addFrame)
        quantityin.pack()

        def Confirm():
            itemId   = itemIdin.get()
            itemName = itemNamein.get()
            quantity = quantityin.get()

            if not itemId or not itemName or not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Please enter valid integer values.")
                return
            if int(quantity) < 5:
                messagebox.showerror("Warning", "Item stock low, order more soon.")

            FileManagement.AddItemToCSV({
                "itemId"  : itemId,
                "itemName": itemName,
                "quantity": quantity
            }) # Adds item to csv, passing in each of the fields

            Operations.table.insert("", "end", values=[itemId, itemName, quantity])
            addFrame.destroy()
            Operations.tableFrame.place(relx=0, rely=1/6, relwidth=1, relheight=5/6)

        tk.Button(addFrame, text="Enter", command=Confirm).pack(pady=20)

    @staticmethod
    def RemoveItem():
        
        table = Operations.table

        selectedItem = table.selection()
        if not selectedItem: # Errors if user doesnt select an item
            messagebox.showerror("Error", "No item selected to remove")
            return
        item = table.item(selectedItem[0], "values") # Stores selected item from table and it's associated values
        itemId = item[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Do you want to remove item '{itemId}'?") # Asks user a yes or no question to remove selected item
        if not confirm: # Does nothing if the user says no
            return
        
        table.delete(selectedItem[0]) # Deletes item from table

        FileManagement.RemoveItemFromCSV(itemId) # Removes selected item from csv


    @staticmethod
    def AlterQuantity():
        
        table = Operations.table

        selectedItem = table.selection()
        if not selectedItem:
            messagebox.showerror("Error", "No item selected to remove")
            return
        row  = selectedItem[0]
        item = table.item(row, "values")

        itemId   = item[0]
        itemName = item[1]
        quantity = item[2]

        alterFrame = tk.Toplevel(Operations.root)
        alterFrame.title("Alter Quantity")
        alterFrame.geometry("300x300")

        tk.Label(alterFrame, text=f"Item : {itemName}").pack(pady=5)
        tk.Label(alterFrame, text="New Quantity : ").pack()

        quantityin = tk.Entry(alterFrame)
        quantityin.insert(0, quantity)
        quantityin.pack()

        def Confirm():
            newQuantity = quantityin.get()
            if not newQuantity.isdigit() or int(newQuantity) <= 0:
                messagebox.showerror("Error", "Enter a valid integer input")
                return
            if int(newQuantity) < 5:
                messagebox.showerror("Warning", "Item stock low, order more soon.")
            
            table.item(row, values=[itemId, itemName, newQuantity])

            FileManagement.AlterCSVQuantity(itemId, newQuantity)

            alterFrame.destroy()

        tk.Button(alterFrame, text="Enter", command=Confirm).pack(pady=10)




    @staticmethod
    def ClearTable():
        
        for row_id in Operations.table.get_children(): # Iterates through each item in table
            Operations.table.delete(row_id)

        FileManagement.ClearItemsCSV()
        

   

    @staticmethod
    def InvSetup(root):
            bottomFrame = tk.Frame(root, bg = "white")
            bottomFrame.place(relx=0, rely=1/6, relwidth=1, relheight=5/6) # Formats the frame to take up 5/6 of the root window
            
            Operations.tableFrame = bottomFrame # Makes variable accessible to Operations class
            Operations.root       = root
            Operations.table      = MainWindow.ItemTable(root, bottomFrame, ICOLUMNS) # Creates the table inside frame
            
            items = FileManagement.LoadItems()
            for row in items:
                Operations.table.insert("", "end", values=[
                    row["itemId"],
                    row["itemName"],
                    row["quantity"]
                ])

################################################################################################################


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

            Operations.InvSetup(root) # Sets up main body of the program
            MainWindow.NavBarSetup(root) # Creates the navigation bar
        
        elif FileManagement.IsInPwCSV(userId.lower(), password): # Checks if username and pw are correct or if new, creates new account
            messagebox.showinfo("Login Successful", "Access approved")
            CSVChecker.LogCSVReady()
            FileManagement.AddUserLog(username=userId)

            frame.destroy()

            Operations.InvSetup(root) # Sets up main body of the program
            MainWindow.NavBarSetup(root) # Creates the navigation bar

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
    def NavBarSetup(root):

            topFrame = tk.Frame(root, bg = "gray")
            topFrame.place(relx=0, rely=0, relwidth=1, relheight=1/6)
            
            addButton      = tk.Button(topFrame, text="ADD", command=Operations.AddItem) # Creates button and passes function without calling it
            removeButton   = tk.Button(topFrame, text="REMOVE", command=Operations.RemoveItem)
            clearButton    = tk.Button(topFrame, text="CLEAR", command=Operations.ClearTable)
            quantityButton = tk.Button(topFrame, text="CHANGE QUANTITY", command=Operations.AlterQuantity)

            addButton.pack     (side="left", padx=10, pady=10) # Makes the buttons sit next to eachother from the left
            removeButton.pack  (side="left", padx=10, pady=10)
            clearButton.pack   (side="left", padx=10, pady=10)
            quantityButton.pack(side="left", padx=10, pady=10)
            



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


