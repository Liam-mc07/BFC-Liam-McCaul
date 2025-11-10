import csv, os 
from datetime import datetime
CSV_PATH = "inventory.csv"
COLUMNS = ["itemId", "itemName", "quantity"]





def CSVReady():
    #Create csv if doesnt exist or is empty
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0 :
        with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as f:
            csv.writer(f).writerow(COLUMNS)





def ReadAll(): # reads row headers from csv
    #Read all items as a list of dictionaries
    CSVReady()
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f: #opens csv file from start
        return list(csv.DictReader(f))

    

def NextId():
    #Find the next numeric item_id by scanning the file
    rows = ReadAll() # reads row headers from csv
    maxId = 0
    for r in rows:
        try: #exception handling
            maxId = max(maxId, int(r.get("itemId", "0")or "0"))
        except ValueError:
            pass
    return str(maxId + 1) #increments maxId to search next row





def AppendRow(row):
    #Adds single row without overwriting file
    CSVReady()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f: #opens csv file from end
        writer = csv.DictWriter(f, fieldnames = COLUMNS) #creates a writer to write to csv




        writer.writerow(row) #writes 'row' variable passed into function

def AddItem():
    print("\n--- ADD ITEM ---")
    name = input("Item name : ").strip() #.strip to remove white space from user input
    inQuantity = input("Quanity (whole num) : ").strip()
    try : #exception handling for if user tries to add 0 of something
        quantity = int(inQuantity) #casts inputted string to an integer
        if quantity <= 0 : 
            print("Quantity must be greater than 0\n")
            return
    except ValueError:
        print("Quantity must be a whole number \n")
        return

    row = {
        "itemId"   : NextId(),
        "itemName" : name,
        "quantity" : inQuantity
    }
    AppendRow(row) #adds the row just created to the csv
    print("Item added \n")


    
def ListItems():
    print("\n --- ALL ITEMS ---")
    rows = ReadAll()
    if not rows :
        print("(no items)\n")
        return
    print(f"{'ID':>3} {'Name':<20} {'Quantity':>4}") #gives titles to sections
    for r in rows:
        print(f"{r.get('itemId',''):>3} {r.get('itemName',''):<20} "
              f"{r.get('quantity',''):>4}") #retrieves fields and their values



    
def RemoveItem():
    print("\n ---REMOVE ITEM---")
    
    rows = ReadAll()
    if not rows:
        print("No items to remove")
        return
    identifier = input("Enter itemId that you want to remove : ").strip()
    updatedRows = [r for r in rows if r.get("itemId") != identifier] #updates rows by removing item with inputted itemId
    
    if len(updatedRows) == len(rows) : 
        print("No item found with that Id\n ")
        return #exits function if no item found
    
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f: #opens up file in writer mode
        writer = csv.DictWriter(f, fieldnames = COLUMNS) # creates dictionary writer for the csv file
        writer.writeheader() #writes the header row to the csv file
        writer.writerows(updatedRows) #writes all the updated rows to the csv

    print("Item removed\n") #lets the user know item was removed





def DecrementItem() :
    print("\n --- DECREMENT ITEM ---")

    rows = ReadAll()
    
    if not rows : #checks to see if the csv is empty
        print("No items available to decrement \n")
        return
    identifier = input("Enter ID you want to decrement: ").strip() #takes user input for item they want to decrement
    isFound = False
    amount = int(input("How much do you want to decrement by : ").strip())

    for r in rows : #searches through all rows
        if r.get("itemId") == identifier : #if correct item is found...
            currentQuant = int(r.get("quantity", "0")) #gets quantity for chosen item
            if currentQuant > amount : #checks that item wont have 0 left
                r["quantity"] = str(currentQuant - amount) # decreases quantity by givem amount
                isFound = True
            elif currentQuant == amount :
                RemoveItem()
                isFound = True
            else :
                print("Cannot decrement past 0\n")
                return
    if not isFound :
        print(f"Not item found with that Id\n")
        return
    if isFound :
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f: #opens up file in writer mode
            writer = csv.DictWriter(f, fieldnames = COLUMNS) # creates dictionary writer for the csv file
            writer.writeheader() #writes the header row to the csv file
            writer.writerows(rows) #writes all the updated rows to the csv




def IncrementItem() :
    print("\n --- Increment Item --- ")

    rows = ReadAll()
    
    if not rows :
        print("No items available to increment \n")
        return
    
    identifier = input("Enter ID you want to increment : ").strip()
    isFound = False
    amount = int(input("How much do you want to increment by : ").strip())

    for r in rows :
        if r.get("itemId") == identifier :
            currentQuant = int(r.get("quantity","0"))
            r["quantity"] = str(currentQuant + amount)
            isFound = True
            
    if not isFound :
        print(f"No item found with that ID\n")

    if isFound :
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f: #opens up file in writer mode
            writer = csv.DictWriter(f, fieldnames = COLUMNS) # creates dictionary writer for the csv file
            writer.writeheader() #writes the header row to the csv file
            writer.writerows(rows) #writes all the updated rows to the csv
        





def Selection():
    CSVReady()
    while True:
        ListItems()
        print("---Inventory---")
        print("(1) Add Item")
        print("(2) Remove Item")
        print("(3) Increment Item")
        print("(4) Decrement Item")
        print("(5) End Program")
        choice = input("Choose (1/2/3/4/5) : ").strip()

        match choice:
            case "1":
                AddItem()
            case "2":
                RemoveItem()
            case "3":
                IncrementItem()
            case "4":
                DecrementItem()
            case "5":
                print("Goodbye!")
                break #ends program by breaking out of loop
            case _:
                print("Invalid input, try again")
        


def StartUp():

    username = input("Enter Username : ").strip() #takes user input for username
    password = input("Enter Password : ").strip() #takes user input for password
    isValid = False

    while not isValid: #loops through asking user for input until valid
        if password == "1234":
            isValid = True #Alters the isValid variable to end the loop once correct passwordpw entered
        else:
            print("Invalid Password")
    Selection()#links to selection function

StartUp()

