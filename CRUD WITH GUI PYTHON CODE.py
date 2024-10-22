import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Create the main window and configure it
root = Tk()
root.title("CRUD Application")
root.geometry("500x500")
root.configure(bg="#f0f8ff")  # Light blue background

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crud"
)

# Functions to handle CRUD operations

def insert_data():
    snm = txtsnm.get().strip()
    nm = txtnm.get().strip()
    age = txtage.get().strip()
    if not snm or not nm or not age:
        messagebox.showerror("CRUD", "All fields are required!")
        return

    mycursor = mydb.cursor()
    sql = "Insert Into person (snm, nm, age) values (%s, %s, %s)"
    val = (snm, nm, age)
    mycursor.execute(sql, val)
    mydb.commit()
    
    count = mycursor.rowcount

    if count == 1:
        messagebox.showinfo("CRUD", "Record Inserted Successfully!")
        clear_fields()
    else:
        messagebox.showerror("CRUD", "Error inserting record.")

def update_data():
    mycursor = mydb.cursor()
    id = txtid.get().strip()
    snm = txtsnm.get().strip()
    nm = txtnm.get().strip()
    age = txtage.get().strip()

    if not id or not snm or not nm or not age:
        messagebox.showerror("CRUD", "All fields are required!")
        return

    sql = "Update person Set snm=%s, nm=%s, age=%s where id=%s"
    val = (snm, nm, age, id)
    mycursor.execute(sql, val)
    mydb.commit()
    
    count = mycursor.rowcount
    if count > 0:
        messagebox.showinfo("CRUD", "Record Updated Successfully!")
        clear_fields()
    else:
        messagebox.showerror("CRUD", "No record found with the given ID.")

def delete_data():
    mycursor = mydb.cursor()
    id = txtid.get().strip()
    
    if not id:
        messagebox.showerror("CRUD", "ID is required!")
        return
    
    sql = "DELETE FROM person WHERE id=%s"
    val = (id,)
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    count = mycursor.rowcount
    if count > 0:
        messagebox.showinfo("CRUD", "Record Deleted Successfully!")
        clear_fields()
    else:
        messagebox.showerror("CRUD", "No record found with the given ID.")

def select_id():
    mycursor = mydb.cursor()
    id = txtid.get().strip()
    if not id:
        messagebox.showerror("CRUD", "ID is required!")
        return
    
    sql = "SELECT * FROM person WHERE id=%s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    
    if len(myresult) == 1:
        for x in myresult:
            txtsnm.delete(0, END)
            txtnm.delete(0, END)
            txtage.delete(0, END)
            txtsnm.insert(0, x[1])
            txtnm.insert(0, x[2])
            txtage.insert(0, x[3])
    else:
        messagebox.showerror("CRUD", "No record found with the given ID.")
        clear_fields()

def view_all():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM person")
    results = mycursor.fetchall()

    if results:
        txt_display.delete(1.0, END)  # Clear any previous data
        txt_display.insert(END, "ID\tSurname\tName\tAge\n")
        txt_display.insert(END, "-"*40 + "\n")

        for row in results:
            txt_display.insert(END, f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\n")
    else:
        messagebox.showinfo("CRUD", "No records found.")

# Function to clear input fields
def clear_fields():
    txtid.delete(0, END)
    txtsnm.delete(0, END)
    txtnm.delete(0, END)
    txtage.delete(0, END)

# Create and style the widgets
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10, 'bold'), foreground='#333')
style.configure('TLabel', font=('Arial', 10), background="#f0f8ff")
style.configure('TEntry', font=('Arial', 10))

title_label = Label(root, text="CRUD Operations", font=('Helvetica', 16, 'bold'), bg="#f0f8ff")
title_label.pack(pady=10)

Label(root, text="Enter ID").pack(pady=5)
txtid = ttk.Entry(root, width=30)
txtid.pack()

Button(root, text="Search", command=select_id).pack(pady=5)

Label(root, text="Enter Surname").pack(pady=5)
txtsnm = ttk.Entry(root, width=30)
txtsnm.pack()

Label(root, text="Enter Name").pack(pady=5)
txtnm = ttk.Entry(root, width=30)
txtnm.pack()

Label(root, text="Enter Age").pack(pady=5)
txtage = ttk.Entry(root, width=30)
txtage.pack()

# Add buttons for CRUD operations
ttk.Button(root, text="Add", command=insert_data).pack(pady=5)
ttk.Button(root, text="Update", command=update_data).pack(pady=5)
ttk.Button(root, text="Delete", command=delete_data).pack(pady=5)

# Add the "View All" button
ttk.Button(root, text="View All", command=view_all).pack(pady=5)

# Text box to display all records
txt_display = Text(root, width=50, height=10, wrap=NONE)
txt_display.pack(pady=10)

# Run the application
root.mainloop()
