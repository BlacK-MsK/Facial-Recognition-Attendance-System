############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import os
import csv
import datetime
import time



############################################# FUNCTIONS ################################################

def updateTreeview():
    with open('Attendance CSV/Attendance {}.csv'.format(date)) as f :
        reader = csv.reader(f, delimiter=',')
        next(reader)
        i = 0
        for row in reader :
            SNo = i + 1
            UID = row[0]
            Date = row[2]
            Time = row[1]
            Attendance = "Present"
            tv.insert("", i, values=(UID, Date, Time, Attendance))
            i += 1
##################################################################################

def tick() :
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)


###################################################################################



###################################################################################

def contact() :
    mess._show(title='Contact us', message="Please contact us on : '+91 9521299925' ")


###################################################################################
def TakeAttendance():
    os.system('python recognize_video.py')
    tv.delete(*tv.get_children())
    updateTreeview()


######################################################################################
def changePassword():
    root = tk.Tk()
    root.geometry('500x500')
    root.title("Change Password")
    root.configure(background='#262523')

    def cancel():
        root.destroy()

    def changePasswordinCSV() :
        r = csv.reader(open('Students Details/Student_details.csv'))  # Here your csv file
        lines = list(r)
        print(lines)
        for row in lines:
            if (f0.get()).upper() == row[1] :
                if f1.get() == row[2] :
                    if f2.get() == f3.get() :
                        row[2] = f3.get()
                        mess.showinfo("Info", "Password Successfully Changed!")
                        root.destroy()
                        break

                    else :
                        mess.showwarning("Warning", "New Password and Confirm Password doesn't match!")
                        # root.f2.clear_text()
                        # root.f3.clear_text()
                else :
                    mess.showwarning("Warning", "Old Password doesn't match!")
                    # root.f1.clear_text()
            else :
                mess.showwarning("Warning", "No Such UID is Registered!")
                # root.f0.clear_text()

        with open('Students Details/Student_details.csv', 'w',newline='') as f :
            write = csv.writer(f)
            write.writerows(lines)

    z1 = tk.Label(root, text="Enter UID", font=("Roboto", 12, "bold"), anchor="w", bg='#262523', fg='white')
    z1.place(x=0, y=100)
    f0 = tk.Entry(root, bd=5)
    f0.place(x=200, y=100)

    z2 = tk.Label(root, text="Enter old Password", font=("Roboto", 12, "bold"), anchor="w", bg='#262523', fg='white')
    z2.place(x=0, y=130)
    f1 = tk.Entry(root, bd=5)
    f1.place(x=200, y=130)

    z3 = tk.Label(root, text="Enter New Password", font=("Roboto", 12, "bold"), anchor="w", bg='#262523',
                  fg='white')
    z3.place(x=0, y=160)
    f2 = tk.Entry(root, bd=5)
    f2.place(x=200, y=160)

    z4 = tk.Label(root, text="Confirm New Password", font=("Roboto", 12, "bold"), anchor="w", bg='#262523',
                  fg='white')
    z4.place(x=0, y=190)
    f3 = tk.Entry(root, bd=5)
    f3.place(x=200, y=190)

    bu1 = tk.Button(root, text='OK', command=changePasswordinCSV, width=10, bg='green', fg='white', font=("Roboto",
                                                                                                          8, "bold"))
    bu1.place(x=100, y=250)

    bu2 = tk.Button(root, text='Cancel', command=cancel, width=10, bg='red', fg='white', font=("Roboto",
                                                                                                          8, "bold"))
    bu2.place(x=200, y=250)




#######################################################################################

def TakeImages() :
    os.system('python takeImages.py')
    mess.showinfo("Info", "Images taken successfully!")


def logOut():
    window.destroy()
    os.system("python login.py")


########################################################################################

def TrainImages() :
    os.system('python extract_embeddings.py')
    os.system('python train_model.py')
    mess.showinfo("Info", "Images Trained Successfully!")

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
today_date = date
day, month, year = date.split("-")

mont = {'01' : 'January',
        '02' : 'February',
        '03' : 'March',
        '04' : 'April',
        '05' : 'May',
        '06' : 'June',
        '07' : 'July',
        '08' : 'August',
        '09' : 'September',
        '10' : 'October',
        '11' : 'November',
        '12' : 'December'
        }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.28, rely=0.17, relwidth=0.4283, relheight=0.80)

# frame2 = tk.Frame(window, bg="#00aeff")
# frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#262523", width=55,
                    height=1, font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#262523", width=55,
                 height=1, font=('times', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="orange", bg="#262523", width=55, height=1, font=('times', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()


head1 = tk.Label(frame1, text="                                  For Attendance                                   ", fg="black",
                 bg="#3ece48", font=('times', 17, ' bold '))
head1.place(x=0, y=0)


lbl3 = tk.Label(frame1, text="Today's Attendance", width=20, fg="black", bg="#00aeff", height=1, font=('times',
                                                                                                       17, ' bold '))
lbl3.place(x=126, y=115)



##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label='Change Password', command=change_pass)
# filemenu.add_command(label='Take New Images', command=TakeImages())
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Log Out', command=logOut)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('times', 29, ' bold '), menu=filemenu)

filemenu2 = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label='Change Password', command=change_pass)
filemenu2.add_command(label='Take New Images', command=TakeImages)
filemenu2.add_command(label='Train Images', command=TrainImages)
menubar.add_cascade(label='Images', font=('times', 29, ' bold '), menu=filemenu2)

filemenu3 = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label='Change Password', command=change_pass)
filemenu3.add_command(label='Change Password', command=changePassword)
menubar.add_cascade(label='Password', font=('times', 29, ' bold '), menu=filemenu3)

################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1, height=13, columns=('UID', 'Date', 'Time','Attendance'))
tv.column('#0',  minwidth=0, width=0)
tv.column('UID', width=130, anchor="center")
tv.column('Date', width=133, anchor="center")
tv.column('Time', width=133, anchor="center")
tv.column('Attendance', width=133, anchor="center")
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
tv.heading('UID', text='UID')
tv.heading('Date', text='DATE')
tv.heading('Time', text='TIME')
tv.heading('Attendance', text='ATTENDANCE')

###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)

if date == today_date :
    pass
else :
    os.system("python makeCSV.py")
    today_date = date

updateTreeview()


###################### BUTTONS ##################################

trackImg = tk.Button(frame1, text="Take Attendance", command=TakeAttendance, fg="black", bg="yellow", width=35, height=1,
                    activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=60, y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy, fg="black", bg="red", width=35, height=1,
                       activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=60, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
