import tkinter as tk
from tkinter import messagebox



town_hall_level = input("Enter Townhall level : ")
coc_title = input("Enter COC title : ")
coc_description = input("Enter COC description : ")
coc_media_title = input("Enter COC media title : ")
coc_media_url = input("Enter COC media URL : ")



def on_submit():
    user_input = entry.get()
    if user_input:
        messagebox.showinfo("Input Received", f"You entered: {user_input}")
        entry.delete(0, tk.END)  # Clear the entry field
    else:
        messagebox.showwarning("Empty Input", "Please enter some text!")

# Create the main window
root = tk.Tk()
root.title("Input Field Example")
root.geometry("400x150")

# Create and place the label
label = tk.Label(root, text="Enter your text:")
label.pack(pady=10)

# Create and place the entry field
entry = tk.Entry(root, width=40)
entry.pack(pady=5)
entry.focus()  # Set focus to the entry field

# Create and place the submit button
submit_btn = tk.Button(root, text="Submit", command=on_submit)
submit_btn.pack(pady=10)

# Start the application
root.mainloop()
