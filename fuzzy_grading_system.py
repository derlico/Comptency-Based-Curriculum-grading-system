#Importing libraries
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
#Importing the fuzzy system module with set rules
from fuzzySystem import fuzzy_logics

#Creating System User Database
def database():
    global conn, cursor
    conn = sqlite3.connect("userDetails.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'userInfo' (teacher_id TEXT NOT NULL PRIMARY KEY, username TEXT, password TEXT)")

#Creating Student Marks database
def marksdatabase():
    global conn1, cursor1
    conn1 = sqlite3.connect("studentMarks.db")
    cursor1 = conn1.cursor()
    cursor1.execute("CREATE TABLE IF NOT EXISTS 'studentMark' (student_id TEXT NOT NULL PRIMARY KEY, teacher_id TEXT, student_name TEXT, ca TEXT, attendance TEXT, halfTerm TEXT, finalTerm TEXT, gpa TEXT)")

#Login window
def login():
    global imglabel, regnologin, password, student_name, student_id, img, gpa
    
    imglabel = Tk()
    imglabel.title("CBC Grading System")
    imglabel.configure(background='light blue')
    bg_image = Image.open("bgimg.jpg")
    image = ImageTk.PhotoImage(bg_image)
    img = Label(imglabel, image = image)
    img.image = image
    img.pack(fill='both', expand=True)
    imglabel.geometry("800x600")
    large_font = ('Verdana', 20)

    regnologin = StringVar()
    password = StringVar()

    Label(img, text="Enter Your Teacher Registration Number and Password below", fg="black", font="Arial_Bold").grid(row=1, column=2, columnspan=5)
    Label(img, text="Reg Num. ", font="Arial_Bold",bg="light blue", relief="sunken", padx=10, pady=10).grid(row=3, column=3)
    e1 = Entry(img, textvariable=regnologin,font=large_font).grid(row=3, column=5)
    Label(img, text="Password ", font="Arial_Bold", bg="light blue", relief="sunken", padx=10, pady=10).grid(row=6, column=3)
    e2 = Entry(img, textvariable=password, show='*',font=large_font).grid(row=6, column=5)
    Button(img, text="Login", font="Arial_Bold", bg="light green", command=verify, width=10, height=1, padx=5, pady=5).grid(row=9, column=5)
    Label(img, text="Don't have an account?", fg="black", font="Arial_Bold").grid(row=12, column=3)
    Button(img, text="Register", font="Arial_Bold", bg="light green", command=register, width=10, height=1, padx=5, pady=5).grid(row=14, column=3)

    img.rowconfigure(0, minsize=30)
    img.rowconfigure(2, minsize=30)
    img.rowconfigure(5, minsize=30)
    img.rowconfigure(7, minsize=30)
    img.rowconfigure(13, minsize=30)

    imglabel.mainloop()

#Verifying login credentials for login
def verify():
    database()
    loginparams = (str(regnologin.get()), str(password.get()))
    cursor.execute("SELECT * from userInfo")
    rows = cursor.fetchall()
    regdb = [row[0] for row in rows]
    passdb = [row[2] for row in rows]
    conn.commit()
    
    if (loginparams[0] in regdb) and (loginparams[1] in passdb):
        imglabel.destroy()
        dashboard()
    else:
        messagebox.showinfo("Invalid Credentials", "Wrong Registration No. or Password")

#Logout function
def logout():
    home.destroy()
    login()

def Back():
    regt.destroy()
    login()

#Registeration window
def register():
    
    global newname
    global newpass
    global regt
    global regno
   
    imglabel.destroy()
    regt = Tk()
    regt.title("Sign Up")
    regt.geometry("800x600")

    bg_reg = Image.open("bgimg.jpg")
    image = ImageTk.PhotoImage(bg_reg)
    imgreg = Label(regt, image = image)
    imgreg.image = image
    imgreg.pack(fill='both', expand=True)

    newname = StringVar()
    newpass = StringVar()
    regno = StringVar()
    
    lbl_title = Label(imgreg, text = " Login Application", font=('arial', 15)).place(y=50, x=50)
    lbl_username = Label(imgreg, text = "Username:", font=('arial', 14), padx=10, pady=10).place(y=90,x=40)
    user1 = Entry(imgreg, textvariable=newname, font=('arial', 14)).place(y=90,x=200)
    lbl_regno = Label(imgreg, text = "Reg No:", font=('arial', 14), padx=10, pady=10).place(y=180,x=40)
    regno1 = Entry(imgreg, textvariable=regno, font=('arial', 14)).place(y=180,x=200)
    lbl_password = Label(imgreg, text = "Password:", font=('arial', 14), padx=10, pady=10).place(y=270,x=40)
    passw1 = Entry(imgreg, textvariable=newpass, show="*", font=('arial', 14)).place(y=270,x=200)

    Button(imgreg, text="Back", width=10, command=Back, padx=5, pady=5).place(y=340,x=120)
    Button(imgreg, text="Register", width=10, command=regback, padx=5, pady=5).place(y=340,x=280)
    lbl_text = Label(imgreg).place(y=300, x=150)
    regt.mainloop()

#Registration fucntion to User database
def regback():
    database()
    params = (str(regno.get()), str(newname.get()), str(newpass.get()))
    cursor.execute("INSERT OR REPLACE INTO 'userInfo' (teacher_id, username, password) VALUES(?,?,?)", params)
    conn.commit()
    conn.close()
    regt.destroy()
    login()

#Displaying Student Report fucntion
def report():
    global conn, cursor
    conn = sqlite3.connect("studentMarks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, student_name, gpa FROM 'studentMark'")
    rept = tkinter.Tk()
    rept.title("Overall Student Report")
    tree = ttk.Treeview(rept, column=("c1", "c2", "c3"), show='headings')
    tree.column('#1', anchor=tkinter.CENTER)
    tree.heading('#1', text="Student_ID")
    tree.column('#2', anchor=tkinter.CENTER)
    tree.heading('#2', text="Student_Name")
    tree.column('#3', anchor=tkinter.CENTER)
    tree.heading('#3', text="GPA")
    tree.pack()

    rows = cursor.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tkinter.END, values=row)
    

def dashboard():
    global home
    home = Tk()
    database()
    cursor.execute("SELECT * FROM userInfo WHERE teacher_id=?", (str(regnologin.get()),))
    det = cursor.fetchone()

    bg1 = Image.open("bgimg.jpg")
    image = ImageTk.PhotoImage(bg1)
    cbc1 = Label(home, image = image)
    cbc1.image = image
    cbc1.pack(fill='both', expand=True)

    home.title("System Dashboard")
    home.geometry("800x600")

    student_name = StringVar()
    student_id = StringVar()

    Label(cbc1, text = f"Hello Teacher., {det[1]}",fg="black", font=('arial', 14)).place(y=50, x=100)
    Label(cbc1, text = "Academic Performance reports",fg="black", font=('arial', 14)).place(y=70, x=490)
    Label(cbc1, text="Fill the Student details", fg="black", font=('arial', 14)).place(y=100, x=100)
    Label(cbc1, text="Student Reg No. ", bg="light blue", padx=5, pady=5).place(y=150, x=100)
    Label(cbc1, text="Student Name ", bg="light blue", padx=5, pady=5).place(y=200, x=100)
    Label(cbc1, text = "Fill all the subject marks",fg="black", font=('arial', 14)).place(y=250, x=100)

    b1 = Entry(cbc1, textvariable=student_id, font=('arial', 14)).place(y=150, x=250)
    b2 = Entry(cbc1, textvariable=student_name, font=('arial', 14)).place(y=200, x=250)

    Button(cbc1, text="Overall Performance Report", bg="light green", relief="sunken", command=report, width=25, height=2).place(y=110, x=530)
    #Button(cbc1, text="Individual Performance Report", bg="light green", relief="sunken", command=report, width=25, height=2).place(y=170, x=530)
    Button(cbc1, text="Mathematics",command=lambda: inputmarks("Mathematics"), bg="yellow", width=15, height=1, padx=5, pady=5).place(y=300,x=100)
    Button(cbc1, text="English Activities",command=lambda: inputmarks("English Activities"), bg="yellow", width=15, height=1, padx=5, pady=5).place(y=300,x=340)
    Button(cbc1, text="Kiswahili Activities",command=lambda: inputmarks("Kiswahili Activities"), bg="yellow",  width=15, height=1, padx=5, pady=5).place(y=350,x=100)
    Button(cbc1, text="Environment Studies",command=lambda: inputmarks("Environmental Studies"), bg="yellow", width=15, height=1, padx=5, pady=5).place(y=350,x=340)
    Button(cbc1, text="Religious Studies",command=lambda: inputmarks("Religious Studies"), bg="yellow", width=15, height=1, padx=5, pady=5).place(y=400,x=340)
    Button(cbc1, text="Hygiene and Nurtition",command=lambda: inputmarks("Hygiene and Nutrition"), bg="yellow" ,width=15, height=1, padx=5, pady=5).place(y=400,x=100)
    Button(cbc1, text="Determine Grade", bg="light green", relief="sunken", command=result, width=20, height=2).place(y=450,x=200)
    Button(cbc1, text="Logout", bg="pink", relief="sunken", command=logout, width=20, height=2).place(y=450, x=530)
    home.mainloop()

def result():
    student_id = StringVar()
    student_name = StringVar()
    marksdatabase()
    rubric()

    param = (str(student_id),str(regnologin.get()),str(student_name.get()), str((mat[0]+eng[0]+kis[0]+env[0]+rst[0]+hng[0])//6), str((mat[1]+eng[1]+kis[1]+env[1]+rst[1]+hng[1])//6), str((mat[2]+eng[2]+kis[2]+env[2]+rst[2]+hng[2])//6), str((mat[3]+eng[3]+kis[3]+env[3]+rst[3]+hng[3])//6), str(0))
    gradn = str(fuzzy_logics(int(param[3]), int(param[4]), int(param[5]), int(param[6])))
    gradng = str(gradn)
    param1 = (str(student_id), str(regnologin.get()), str(student_name.get()),
             str((mat[0] + eng[0] + kis[0] + env[0] + rst[0] + hng[0]) // 6),
             str((mat[1] + eng[1] + kis[1] + env[1] + rst[1] + hng[1]) // 6),
             str((mat[2] + eng[2] + kis[2] + env[2] + rst[2] + hng[2]) // 6),
             str((mat[3] + eng[3] + kis[3] + env[3] + rst[3] + hng[3]) // 6), str(gradng))

    cursor1.execute("INSERT INTO 'studentMark' (student_id, teacher_id, student_name, ca, attendance, halfTerm, finalTerm, gpa) VALUES(?,?,?,?,?,?,?,?)", param1)
    conn1.commit()
    conn1.close()

    cbc2 = Tk()
    cbc2.title("Cummulative Marks")
    cbc2.geometry("800x600")
    #print(param)

    grad = str(fuzzy_logics(int(param[3]), int(param[4]), int(param[5]), int(param[6])))
    grade = float(grad)
    if (grade >= 9):
        comment = "Excellent"
    elif (grade >= 7.5 and grade<=8.99):
        comment = "Good"
    elif (grade >= 6 and grade<=7.49):
        comment = "Average"
    elif (grade >= 5 and grade <= 5.99):
        comment = "Needs Improvement"
    elif (grade<=4.99):
        comment = "Fail"

    Label(cbc2, text = "Cumulative GPA grade : " + grad,fg="black", font=('arial', 15)).grid(row=2, column=2)
    Label(cbc2, text = "System Remarks: " + comment).grid(row=3, column=2)

    Label(cbc2, text="Subject assesments ", fg="black", font=('arial', 15)).grid(row=4, column=2)
    Label(cbc2, text=" ").grid(row=5, column=2)
    Label(cbc2, text=" ").grid(row=6, column=2)
    Label(cbc2, text = " " + x1).grid(row=7, column=2)
    Label(cbc2, text=" " + x2).grid(row=8, column=2)
    Label(cbc2, text=" " + x3).grid(row=9, column=2)
    Label(cbc2, text=" " + x4).grid(row=10, column=2)
    Label(cbc2, text=" " + x5).grid(row=11, column=2)
    Label(cbc2, text=" " + x6).grid(row=12, column=2)

    cbc2.rowconfigure(0, minsize=30)
    cbc2.rowconfigure(1, minsize=30)
    cbc2.columnconfigure(0, minsize=90)
    cbc2.rowconfigure(2, minsize=30)
    cbc2.rowconfigure(3, minsize=30)
    cbc2.rowconfigure(4, minsize=30)
    cbc2.rowconfigure(5, minsize=30)
    cbc2.rowconfigure(6, minsize=30)
    cbc2.rowconfigure(7, minsize=30)
    cbc2.rowconfigure(8, minsize=30)
    cbc2.rowconfigure(9, minsize=30)
    cbc2.rowconfigure(10, minsize=30)
    cbc2.rowconfigure(11, minsize=30)
    cbc2.rowconfigure(12, minsize=30)

    cbc2.mainloop()

#Individual subject remarks function
def collect(subjct):
    global mat, mats
    global eng, engs
    global kis, kisw
    global env, envs
    global rst, rsts
    global hng, hngs

    if(subjct=="Mathematics"):
        mat1 = int(clas.get())
        mat2 = int(att.get())
        mat3 = int(half.get())
        mat4 = int(fin.get())
        mat = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        mats = (mat1+mat2+mat3+mat4)/2.8

    elif(subjct=="English Activities"):
        eng = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        eng1 = int(clas.get())
        eng2 = int(att.get())
        eng3 = int(half.get())
        eng4 = int(fin.get())
        engs = (eng1+eng2+eng3+eng4)/2.8

    elif(subjct=="Kiswahili Activities"):
        kis = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        kis1 = int(clas.get())
        kis2 = int(att.get())
        kis3 = int(half.get())
        kis4 = int(fin.get())
        kisw = (kis1+kis2+kis3+kis4)/2.8

    elif(subjct=="Environmental Studies"):
        env = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        env1 = int(clas.get())
        env2 = int(att.get())
        env3 = int(half.get())
        env4 = int(fin.get())
        envs = (env1+env2+env3+env4)/2.8

    elif (subjct == "Religious Studies"):
        rst = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        rst1 = int(clas.get())
        rst2 = int(att.get())
        rst3 = int(half.get())
        rst4 = int(fin.get())
        rsts = (rst1+rst2+rst3+rst4)/2.8

    elif(subjct=="Hygiene and Nutrition"):
        hng = [int(clas.get()), int(att.get()), int(half.get()), int(fin.get())]
        hng1 = int(clas.get())
        hng2 = int(att.get())
        hng3 = int(half.get())
        hng4 = int(fin.get())
        hngs = (hng1+hng2+hng3+hng4)/2.8

    inpt.destroy()

def inputmarks(subjects):
    global att, fin, half, clas, inpt
    att = IntVar()
    fin = IntVar()
    half = IntVar()
    clas = IntVar()

    inpt = Tk()
    inpt.title(subjects)
    inpt.configure(bg="white")
    inpt.geometry("600x400")

    Label(inpt, text = "Enter Marks",fg="black", font=('arial', 14)).place(y=30, x=50)
    Label(inpt, text = "Class Work ",bg="light pink", font=('arial', 14)).place(y=80,x=40)
    clas=Entry(inpt, font=('arial', 14))
    clas.place(y=80,x=180)
    Label(inpt, text = "/30 ", font=('arial', 14)).place(y=80,x=410)

    Label(inpt, text = "Attendance ",bg="light pink", font=('arial', 14)).place(y=140,x=40)
    att=Entry(inpt, font=('arial', 14))
    att.place(y=140,x=180)
    Label(inpt, text = "/100 ", font=('arial', 14)).place(y=140,x=410)

    Label(inpt, text = "Half Term ",bg="light pink", font=('arial', 14)).place(y=200,x=40)
    half=Entry(inpt, font=('arial', 14))
    half.place(y=200,x=180)
    Label(inpt, text = "/50 ", font=('arial', 14)).place(y=200,x=410)

    Label(inpt, text = "Final Exam ",bg="light pink", font=('arial', 14)).place(y=260,x=40)
    fin=Entry(inpt, font=('arial', 14))
    fin.place(y=260,x=180)
    Label(inpt, text = "/100 ", font=('arial', 14)).place(y=260,x=410)
    
    Button(inpt, text="Submit",command=lambda: collect(subjects), width=20, height=2).place(y=320,x=300)
    
    inpt.mainloop()

def rubric():
    global x1, x2, x3, x4, x5, x6
    if (mats > 80):
        x1 = str("Mathematics: Exceeded Expectations.")
    elif (mats >= 65 and mats <= 79):
        x1 = str("Mathematics: Met Expectations.")
    elif (mats >=50 and mats <= 64):
        x1 = str("Mathematics: Approaching Expectation.")
    else:
        x1 = str("Mathematics: Below Expectation.")
    if (engs > 80):
        x2 = str("English Activities: Exceeded Expectations.")
    elif (engs >= 65 and engs <= 79):
        x2 = str("English Activities: Met Expectations.")
    elif (engs >=50 and engs <= 64):
        x2 = str("English Activities: Approaching Expectation.")
    else:
        x2 = str("English Activities: Below Expectation.")
    if (kisw > 80):
        x3 = str("Kiswahili Activities: Exceeded Expectations.")
    elif (kisw >= 65 and kisw <= 79):
        x3 = str("Kiswahili Activities: Met Expectations.")
    elif (kisw >=50 and kisw <= 64):
        x3 = str("Kiswahili ACtivities: Approaching Expectation.")
    else:
        x3 = str("Kiswahili Activities: Below Expectation.")
    if (envs > 80):
        x4 = str("Environmental Studies: Exceeded Expectations.")
    elif (envs >= 65 and envs <= 79):
        x4 = str("Environmental Studies: Met Expectations.")
    elif (envs >=50 and envs <= 64):
        x4 = str("Environmental Studies: Approaching Expectation.")
    else:
        x4 = str("Environmental Studies: Below Expectation.")
    if (rsts > 80):
        x5 = str("Religious Studies: Exceeded Expectations.")
    elif (rsts >= 65 and rsts <= 79):
        x5 = str("Religious Studies: Met Expectations.")
    elif (rsts >=50 and rsts <= 64):
        x5 = str("Religious Studies: Approaching Expectation.")
    else:
        x5 = str("Religious Studies: Below Expectation.")
    if (hngs > 80):
        x6 = str("Hygiene and Nutrition: Exceeded Expectations.")
    elif (hngs >= 65 and hngs <= 79):
        x6 = str("Hygiene and Nutrition: Met Expectations.")
    elif (hngs >=50 and hngs <= 64):
        x6 = str("Hygiene and Nutrition: Approaching Expectation.")
    else:
        x6 = str("Hygiene and Nutrition: Below Expectation.")

login()
