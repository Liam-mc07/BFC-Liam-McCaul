import tkinter as tk

def button_click() :
    print("Button Clicked")

root = tk.Tk()
root.title("Sample Tkinter App")

button = tk.Button(root, text="click me", command = button_click)
button.pack(pady=10)

root.mainloop()