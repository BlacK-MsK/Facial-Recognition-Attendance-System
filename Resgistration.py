import os
from tkinter import *
from tkinter import messagebox as mb
import csv

root = Tk()
root.geometry('620x640+650+220')
root.title("Registration Form")
root.configure(background='#262523')

#defining function msg() using messagebox

def login():
    root.destroy()
    os.system('python login.py')


def msg():
    if (e1.index("end") == 0):
        mb.showwarning('Missing details', 'enter your name')
    elif(e2.index("end") == 0):
        mb.showwarning('Missing details', 'enter your email id')
    elif(e8.index("end") == 0):
        mb.showwarning('Missing details', 'enter your UID')
    else:
        mb.showinfo('Success', 'Registration done successfully for the course ')
        root.destroy()
        os.system('python login.py')

#exporting entered data
def save():


    with open('Students Details/Student_details.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader :
            if row[1] == (e8.get()).upper() :
                mb.showinfo("Info", "UID already registered!")
                login()


    # save data in csv file
    with open('Students Details/Student_details.csv', 'a') as fs:
        w = csv.writer(fs, delimiter=',', lineterminator='\r')
        w.writerow([e1.get(), (e8.get()).upper(), e4.get(), e2.get()])
        fs.close()


def saveinfo():
    save()
    msg()

# creating labels and entry widgets


l1 = Label(root, text="Registration form", width=25, font=("Pacifico", 35), bg='#262523', fg='grey')
l1.place(x=-70, y=10)
l2 = Label(root, text="Full Name", width=20, font=("Roboto", 14, "bold"), anchor="w", bg='#262523', fg='white')
l2.place(x=100, y=130)
e1 = Entry(root, width=30, bd=2)
e1.place(x=270, y=130)
l3 = Label(root, text="Email", width=20, font=("Roboto", 14, "bold"), anchor="w", bg='#262523', fg='white')
l3.place(x=100, y=180)
e2 = Entry(root, width=30,bd=2)
e2.place(x=270, y=180)
l8 = Label(root, text="UID", width=20, font=("Roboto", 14, "bold"), anchor="w", bg='#262523', fg='white')
l8.place(x=100, y=230)
e8 = Entry(root, width=30, bd=2)
e8.place(x=270, y=230)

l4 = Label(root, text="Password", width=20, font=("Roboto", 14, "bold"), anchor="w", bg='#262523', fg='white')
l4.place(x=100, y=280)
e4 = Entry(root, show='•', width=30, bd=2)
e4.place(x=270, y=280)

l7 = Label(root, text="Select course", width=20, font=("Roboto", 14, "bold"), anchor="w", bg='#262523', fg='white')
l7.place(x=100, y=330)

# create a dropdown menu with the OptionMenu widget
cvar = StringVar()
cvar.set("Select course")
option = ("CSE", "Mechanical", "Electrical", "Civil")
o = OptionMenu(root, cvar, *option)
o.config(font=("Roboto", 11), bd=3)
o.place(x=270, y=330, width=190)

# submit and cancel buttons
b1 = Button(root, text='Submit', command=saveinfo, width=15, bg='green', fg='white', font=("Roboto", 12, "bold"))
b1.place(x=100, y=450)
b2 = Button(root, text='Cancel', command=root.destroy, width=15, bg='maroon', fg='white', font=("Roboto", 12, "bold"))
b2.place(x=330, y=450)


b3 = Button(root, text='Already Registered, Login?', command=login, width=25, bg='red', fg='white', font=("Roboto",
                                                                                                             6, "bold"))
b3.place(x=480, y=620)

root.mainloop()
