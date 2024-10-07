from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import sqlite3
import os
from datetime import datetime

root = Tk()
root.title("Daily Expense Calculator")
root.iconbitmap('window_icon.ico')
root.resizable(False, False)
root.geometry("335x700")

# Create a database or connect to one
conn = sqlite3.connect("expense.db")

# Create a cursor
cur = conn.cursor()

# Create a table


cur.execute("""CREATE TABLE IF NOT EXISTS expense (
        day integer,
        month integer,
        year integer,
        cost float
    )
""")




# Create a function to update a record
def save_record():
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()
    record_id = select_entry.get()
    cur.execute("""UPDATE expense SET
                day = :day,
                month = :month,
                year = :year,
                cost = :cost
                WHERE oid = :oid""",
                {
                    'day':day_editor.get(),
                    'month':month_editor.get(),
                    'year':year_editor.get(),
                    'cost':cost_editor.get(),
                    'oid':record_id
                }
                )

    # commit changes to database
    conn.commit()
    # close connection
    
   

    conn.close()
    editor.destroy()

def update():
    global editor
    editor = Toplevel()
    editor.title("Update Record Window")
    editor.iconbitmap('window_icon.ico')
    editor.resizable(False, False)
    editor.geometry("335x250")

    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()

    record_id = select_entry.get()
    # Query the database
    cur.execute("SELECT * FROM expense WHERE oid = " + record_id)
    records = cur.fetchall()

    

    # Create editor entries global
    global day_editor
    global month_editor
    global year_editor
    global cost_editor
    
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract day, month, and year
    day_current = current_datetime.day
    month_current = current_datetime.month
    year_current = current_datetime.year

    # Error handling for dates
    if int(day.get())>day_current or int(month.get())>month_current or int(year.get())>year_current:
        return
    elif int(month.get()) == 1 or int(month.get()) == 3 or int(month.get()) == 5 or int(month.get()) == 7 or int(month.get()) == 8 or int(month.get()) == 10 or int(month.get()) == 12: 
        if int(day.get()) > 31 or int(day.get()) < 1:
            return
        
    elif int(month.get()) == 4 or int(month.get()) == 6 or int(month.get()) == 9 or int(month.get()) == 11: 
        if int(day.get()) > 30 or int(day.get()) < 1:
            return

    elif int(year.get())%4==0:
        if int(month.get()) == 2:
            if int(day.get()) > 29 or int(day.get()) < 1:
                return

    elif int(month.get()) == 2:
        if int(day.get()) > 28 or int(day.get()) < 1:
            return

    elif int(month.get()) > 12 or int(month.get()) < 1:
        return

    # Enter the data
    day_editor= Entry(editor, width=30)
    day_editor.grid(row=0, column=1, padx=20, pady=(5, 0))

    month_editor = Entry(editor, width=30)
    month_editor.grid(row=1, column=1, padx=20)

    year_editor = Entry(editor, width=30)
    year_editor.grid(row=2, column=1, padx=20)

    cost_editor = Entry(editor, width=30)
    cost_editor.grid(row=3, column=1, padx=20)


    
    # Create the label for the entries
    Label(editor, text="Enter the day: ").grid(row=0, column=0, pady=(5, 0), sticky=W)
    Label(editor, text="Enter the month: ").grid(row=1, column=0, sticky=W)
    Label(editor, text="Enter the year: ").grid(row=2, column=0, sticky=W)
    Label(editor, text="Enter the expenditure: ").grid(row=3, column=0, sticky=W)
    
    # have the old data in entry box
    for record in records:
        day_editor.insert(0, record[0])
        month_editor.insert(0, record[1])
        year_editor.insert(0, record[2])
        cost_editor.insert(0, record[3])

    
    save_button = Button(editor, text="Save", command=save_record)
    save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=139, sticky=W)

    # commit changes to database
    conn.commit()
    # close connection
    conn.close()

    # Clear existing label content
    record_label_last_ten_days.config(text=" ")
    total_label_last_ten_days.config(text=" ")
    

# Create function to delete a record
def delete():
    
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()
    
    record_id = select_entry.get()
    # Query the database
    cur.execute("SELECT * FROM expense WHERE oid = " + record_id)
    records = cur.fetchall()

    

    # Delete a record
    cur.execute("DELETE from expense WHERE oid=" + select_entry.get())

    

    # commit changes to database
    conn.commit()
    # close connection
    conn.close()

    # Clear existing label content
    record_label_last_ten_days.config(text=" ")
    total_label_last_ten_days.config(text=" ")

# Create Submit Function
def Submit():
    
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()
    
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract day, month, and year
    day_current = current_datetime.day
    month_current = current_datetime.month
    year_current = current_datetime.year

    # Error handling for dates
    if int(day.get())>day_current or int(month.get())>month_current or int(year.get())>year_current:
        return
    elif int(month.get()) == 1 or int(month.get()) == 3 or int(month.get()) == 5 or int(month.get()) == 7 or int(month.get()) == 8 or int(month.get()) == 10 or int(month.get()) == 12: 
        if int(day.get()) > 31 or int(day.get()) < 1:
            return
        
    elif int(month.get()) == 4 or int(month.get()) == 6 or int(month.get()) == 9 or int(month.get()) == 11: 
        if int(day.get()) > 30 or int(day.get()) < 1:
            return

    elif int(year.get())%4==0:
        if int(month.get()) == 2:
            if int(day.get()) > 29 or int(day.get()) < 1:
                return

    elif int(month.get()) == 2:
        if int(day.get()) > 28 or int(day.get()) < 1:
            return

    elif int(month.get()) > 12 or int(month.get()) < 1:
        return
    

    cur.execute("SELECT *, oid FROM expense")
    records = cur.fetchall()
    bool_sub = False
    for record in records:
        if record[0] == day.get() and record[1] == month.get() and record[2] == year.get():
            existing_record = float(record[3]) + float(cost.get())
            record_id = record[4]
            cur.execute("""UPDATE expense SET
                day = :day,
                month = :month,
                year = :year,
                cost = :cost
                WHERE oid = :oid""",
                {
                    'day':day.get(),
                    'month':month.get(),
                    'year':year.get(),
                    'cost':existing_record,
                    'oid':record[4]
                }
                )

            bool_sub = True
    # Insert into table
    if(not bool_sub):
        cur.execute("INSERT INTO expense VALUES (:day, :month, :year, :cost)",
                    {
                        'day':day.get(),
                        'month':month.get(),
                        'year':year.get(),
                        'cost':cost.get()
                    }
        )


    # commit changes to database
    conn.commit()
    # close connection
    conn.close()


    # Clear text boxes
    day.delete(0, END)
    month.delete(0, END)
    year.delete(0, END)
    cost.delete(0, END)



# Create Query Function
def Query():
    global record_label
    
    
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT *, oid FROM expense ORDER BY year DESC, month DESC, day DESC")
    records = cur.fetchall()
    # print(records)

    print_record = ''
    for record in records:
        print_record += "ID: " + str(record[4]) + " | " + str(record[0]) + "/" + str(record[1]) + "/" + str(record[2]) + " | expenditure: " + str(record[3]) + " rupees"  + '\n'  

    
    record_label = Label(all_records_window, text=print_record)
    record_label.grid(row=3, column=0, columnspan=2)
    # commit changes to database
    conn.commit()
    # close connection
    conn.close()

total_cost = StringVar


def total(): 
    
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()
    
    cur.execute("SELECT *, oid FROM expense")
    records = cur.fetchall()
    total_cost = 0
    for record in records:
        total_cost+= record[3]
    
    total_label = Label(all_records_window, text="Your total expenditure is: " + str(total_cost) + " rupees")
    total_label.grid(row=1, column=0, columnspan=2)

    # commit changes to database
    conn.commit()
    # close connection
    conn.close()

def QueryLastTenDays():
    global record_label_last_ten_days
     # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT *, oid FROM expense ORDER BY year DESC, month DESC, day DESC")
    records = cur.fetchall()
    # print(records)

    print_record = ''
    for record in records[-10:]:
        print_record += "ID: " + str(record[4]) + " | " + str(record[0]) + "/" + str(record[1]) + "/" + str(record[2]) + " | expenditure: " + str(record[3]) + " rupees"  + '\n'  

    record_label_last_ten_days = Label(root, text=print_record)
    record_label_last_ten_days.grid(row=11, column=0, columnspan=2)

    # commit changes to database
    conn.commit()
    # close connection
    conn.close()

def AllRecords():
    global all_records_window

    all_records_window = Toplevel()
    all_records_window.title("All Records")
    all_records_window.iconbitmap('window_icon.ico')
    all_records_window.resizable(False, False)
    all_records_window.geometry("335x400")

    query_button = Button(all_records_window, text="Show records", command=Query)
    query_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=115, sticky=W)

    total_cost_button = Button(all_records_window, text="Total Expenditure", command=total)
    total_cost_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, ipadx=105, sticky=W)

def TotalLastTenDays():
    global total_label_last_ten_days
    # Create a database or connect to one
    conn = sqlite3.connect("expense.db")
    # Create a cursor
    cur = conn.cursor()
    
    cur.execute("SELECT *, oid FROM expense ORDER BY year DESC, month DESC, day DESC")
    records = cur.fetchall()
    total_cost = 0
    for record in records[-10:]:
        total_cost+= record[3]
    
    total_label_last_ten_days = Label(root, text="You spent " + str(total_cost) + " rupees in the last ten days!")
    total_label_last_ten_days.grid(row=9, column=0, columnspan=2)

    # commit changes to database
    conn.commit()
    # close connection
    conn.close()



# Enter the data
day = Entry(root, width=30)
day.grid(row=0, column=1, padx=20, pady=(5, 0))

month = Entry(root, width=30)
month.grid(row=1, column=1, padx=20)

year = Entry(root, width=30)
year.grid(row=2, column=1, padx=20)

cost = Entry(root, width=30)
cost.grid(row=3, column=1, padx=20)


select_entry = Entry(root, width=30)
select_entry.grid(row=5, column=1, padx=20)

# Create the label for the entries
Label(root, text="Enter the day: ").grid(row=0, column=0, pady=(5, 0), sticky=W)
Label(root, text="Enter the month: ").grid(row=1, column=0, sticky=W)
Label(root, text="Enter the year: ").grid(row=2, column=0, sticky=W)
Label(root, text="Enter the expenditure: ").grid(row=3, column=0, sticky=W)

Label(root, text="Select ID: ").grid(row=5, column=0, sticky=W)

# Create Submit button  
submit_button = Button(root, text="Add record to Database", command=Submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=90, sticky=W)

# Create a Delete button
delete_button = Button(root, text="Delete a record", command=delete)
delete_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=113, sticky=W)

# Create an Update button
edit_button = Button(root, text="Update a record", command=update)
edit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=111, sticky=W)

# Create a button for displaying total cost of last ten days
total_cost_last_ten_days = Button(root, text="Total Expenditure in last ten  days", command=TotalLastTenDays)
total_cost_last_ten_days.grid(row=8, column=0, columnspan=2, padx=10, pady=10, ipadx=65, sticky=W)

# Create a Query button for last 10 days
query_button = Button(root, text="Show records of the last Ten Days", command=QueryLastTenDays)
query_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=65, sticky=W)

# Create a button to show all records
all_records_button = Button(root, text="Show all records", command=AllRecords)
all_records_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=110, sticky=W)

exit_button = Button(root, text="Exit Application", command=root.quit)
exit_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10, ipadx=112, sticky=W)

# commit changes to database
conn.commit()

# close connection
conn.close()

root.mainloop()