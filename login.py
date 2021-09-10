import os
import random
from tkinter import *
from tkinter import messagebox as mb
import csv
import smtplib


root = Tk()
root.geometry('620x640+650+220')
root.title("Login Form")
root.configure(background='#262523')


# defining function msg() using messagebox

def registration() :
    root.destroy()
    os.system('python Resgistration.py')


def msg() :
    # course = cvar.get()
    if e1.index("end") == 0 :
        mb.showwarning('Missing details', 'enter your name')
    elif e2.index("end") == 0 :
        mb.showwarning('Missing details', 'enter your email id')
    else :
        mb.showinfo('Success', 'Login done successfully')
        root.destroy()


def changePassword():
    root2 = Tk()
    root2.geometry('500x500')
    root2.title("Change Password")
    root2.configure(background='#262523')

    def changePasswordinCSV() :
        r = csv.reader(open('Students Details/Student_details.csv'))  # Here your csv file
        lines = list(r)
        for row in lines:
            if (f0.get()).upper() == row[1]:
                if f1.get() == f2.get():
                    row[2] = f2.get()
                    mb.showinfo("Info", "Password Successfully Changed!")
                    root2.destroy()
                    break
                    # os.system("python login.py")
                else :
                    mb.showwarning("Warning", "New Password and Confirm Password doesn't match!")
                    # root.f1.clear_text()
            else :
                mb.showwarning("Warning", "No Such UID is Registered!")
                # root.f0.clear_text()

        with open('Students Details/Student_details.csv', 'w', newline='') as f :
            write = csv.writer(f)
            write.writerows(lines)

    z1 = Label(root2, text="Enter UID", width=12, font=("Roboto", 12, "bold"), anchor="w", bg='#262523',
                     fg='white')
    z1.place(x=0, y=100)
    f0 = Entry(root2, width=30, bd=5)
    f0.place(x=160, y=100)

    z2 = Label(root2, text="Enter New Password", width=12, font=("Roboto", 12, "bold"), anchor="w", bg='#262523',
                  fg='white')
    z2.place(x=0, y=200)
    f1 = Entry(root2, width=30, bd=5)
    f1.place(x=160, y=200)

    z3 = Label(root2, text="Confirm New Password", width=12, font=("Roboto", 12, "bold"), anchor="w", bg='#262523',
                  fg='white')
    z3.place(x=0, y=230)
    f2 = Entry(root2, width=30, bd=5)
    f2.place(x=160, y=230)

    bu1 = Button(root2, text='OK', command=changePasswordinCSV, width=10, bg='green', fg='white', font=("Roboto",
                                                                                                          8, "bold"))
    bu1.place(x=60, y=410)




def forgotPassword():
    root.destroy()
    window = Tk()
    window.geometry('300x300')
    window.title("Forgot Password")
    window.configure(background='#262523')

    OTP = random.randint(100000, 999999)


    def sendOTP():
        sender_email_id = "19bcs2732@gmail.com"
        sender_email_id_password = "Sachin123@"
        receiver_email_id = g1.get()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email_id, sender_email_id_password)
        message = "Your 6 digit OTP for changing the password is - {}".format(OTP)
        s.sendmail(sender_email_id, receiver_email_id, message)

        # terminating the session
        s.quit()

        window.destroy()
        createOTPScreen()

    w1 = Label(window, text="E-mail", width=20, font=("Roboto", 24, "bold"), anchor="w", bg='#262523', fg='white')
    w1.place(x=100, y=90)
    g1 = Entry(window, width=30, bd=5)
    g1.place(x=60, y=150)
    z3 = Button(window, text='Next', command=sendOTP, width=15, bg='maroon', fg='white',font=("Roboto", 10, "bold"))
    z3.place(x=92, y=200)




    def createOTPScreen():
        window2 = Tk()
        window2.geometry('300x300')
        window2.title("Forgot Password")
        window2.configure(background='#262523')

        def checkOTP() :
            isDone = False
            if OTP == int(g2.get()):
                mb.showinfo("Info", "Correct OTP!")
                window2.destroy()
                changePassword()
                # os.system("python login.py")
                isDone = True
            else :
                mb.showinfo("Info", "Wrong OTP")

            return isDone

        w2 = Label(window2, text="OTP", width=20, font=("Roboto", 24, "bold"), anchor="w", bg='#262523', fg='white')
        w2.place(x=100, y=90)
        g2 = Entry(window2, width=30, bd=5)
        g2.place(x=60, y=150)
        z4 = Button(window2, text='Next', command=checkOTP, width=15, bg='maroon', fg='white', font=("Roboto", 10, "bold"))
        z4.place(x=92, y=200)
        z5 = Button(window2, text='resend OTP', command=sendOTP, width=15, bg='maroon', fg='white',
                    font=("Roboto", 10, "bold"))
        z5.place(x=92, y=250)

        if checkOTP() :
            os.system("python login.py")



# exporting entered data
def check():
    logIn = False

    csvfile = open('Students Details/Student_details.csv')
    reader = csv.reader(csvfile)
    UID = (e1.get()).upper()
    password = e2.get()

    for row in reader :
        if row[1] == UID :
            if row[2] == password :
                logIn = True
                mb.showinfo('Success', 'Login done successfully')
                root.destroy()
                os.system('python home.py')
                break
            else :
                logIn = False
                mb.showinfo('Info', 'Wrong Password')
    if not logIn:
        os.system('python login.py')


# creating labels and entry widgets


l1 = Label(root, text="Login form", width=25, font=("Pacifico", 35), bg='#262523', fg='grey')
l1.place(x=-70, y=10)
l2 = Label(root, text="UID", width=20, font=("times", 24, "bold"), anchor="w", bg='#262523', fg='white')
l2.place(x=100, y=230)
e1 = Entry(root, width=30, bd=5)
e1.place(x=295, y=235)
l3 = Label(root, text="Password", width=20, font=("times", 24, "bold"), anchor="w", bg='#262523', fg='white')
l3.place(x=100, y=300)
e2 = Entry(root, show='•', width=30, bd=5)
e2.place(x=295, y=305)

# submit and cancel buttons
b1 = Button(root, text='LOGIN', command=check, width=15, bg='green', fg='white', font=("Roboto", 12, "bold"))
b1.place(x=130, y=380)
b2 = Button(root, text='Cancel', command=root.destroy, width=15, bg='maroon', fg='white', font=("Roboto", 12, "bold"))
b2.place(x=330, y=380)

b4 = Button(root, text='Forgot Password?', command=forgotPassword, width=25, bg='orange', fg='white', font=("Roboto",
                                                                                                             8, "bold"))
b4.place(x=215, y=440)

b3 = Button(root, text='New?, Sign Up here.', command=registration, width=25, bg='red', fg='white', font=("Roboto",
                                                                                                             6, "bold"))
b3.place(x=480, y=620)

root.mainloop()
