import os
import cv2
import sys
import shutil
import Mlpart
from tkinter import *
from tkinter.ttk import *
import warnings
from PIL import ImageTk,Image
import mysql.connector as msc
from tkinter import messagebox as tk1
from tkinter.filedialog import askopenfile,askopenfilenames

if not sys.warnoptions:
    warnings.simplefilter("ignore")

mydb = msc.connect(
    host = "localhost",
    user = "root",
    passwd ="nice",
    database = "project",
    auth_plugin='mysql_native_password'
)

mc = mydb.cursor()
mc.execute('select sid,spwd from student;')
ds = dict(mc.fetchall())

da = {
    "ts101" : "ts101",
    "ts102" : "ts102",
    "ts103" : "ts103"
}

mc.execute('select sid,sname from student;')
name_id = dict(mc.fetchall())

def admin_page(z):
    root1 = Tk()
    root1.resizable(False,False)
    root1.geometry('930x590')
    root1.title(z)

    uploadimage0 = Image.open("gui_icons/images_2.jpg")
    uploadimage0 = uploadimage0.resize((930,630),Image.ANTIALIAS)
    uploadimage0 = ImageTk.PhotoImage(uploadimage0)
    Label(root1,image=uploadimage0).place(x=0, y=0, width=930, height=630)
    
    img_file = StringVar()

    def create_stu():
        roots = Toplevel(root1)
        roots.resizable(False,False)
        roots.geometry('450x475')
        snamevar = StringVar()
        sidvar = StringVar()
        spwdvar = StringVar()
        sattendvar = StringVar()
        periodsvar = StringVar()
        u0 = Image.open("gui_icons/images_2.jpg")
        u0 = u0.resize((450,475),Image.ANTIALIAS)
        u0 = ImageTk.PhotoImage(u0)
        Label(roots,image=u0).place(x=0, y=0, width=450, height=450)
        roots.title("Student Registration")

        def dele(sidvar,snamevar):
            try:
                mc = mydb.cursor()
                a = sidvar.get()
                a1 = str(snamevar.get())
                mc.execute('delete from student where sid=%s;',(a,))
                mydb.commit()
                location = 'C:/Users/nk/Desktop/final_aas/data/train/'+a1+'/'
                shutil.rmtree(location)
                tk1.showinfo("Sucess","Student is Deleted")
            except Exception as e:
                print(e)
                tk1.showerror("Deletion failed","Error Occured")

        def verify(snamevar,sidvar,spwdvar,sattendvar,periodsvar):
            try :
                if str(snamevar.get()) and int(sidvar.get()) and int(spwdvar.get()) and int(sattendvar.get()) and int(periodsvar.get()):
                    mc = mydb.cursor()
                    mc.execute('select sid from student;')
                    li = [c[0] for c in mc.fetchall()]
                    a1 = str(snamevar.get())
                    a2 = str(sidvar.get())
                    a3 = str(spwdvar.get())
                    a4 = str(sattendvar.get())
                    a5 = str(periodsvar.get())
                    a6 = str(int(int(a4)*100/int(a5)))
                    if sidvar.get() not in li:
                        cmd = 'insert into student values(%s,%s,%s,%s,%s,%s);'
                        values = (a1,a2,a3,a4,a5,a6)
                        mc.execute(cmd,values)
                        mydb.commit()
                        face_folder = 'data/train/' + str(snamevar.get()) + "/"
                        if not os.path.exists(face_folder):
                            os.mkdir(face_folder)
                        roots.destroy()
                        tk1.showinfo("Sucess","Registration is Sucessful")
                    else:
                        cmd = 'update student set sname=%s,spwd=%s,sattend=%s,periods=%s,percen=%s where sid=%s;'
                        values = (a1,a3,a4,a5,a6,a2)
                        mc.execute(cmd,values)
                        mydb.commit()
                        roots.destroy()
                        tk1.showinfo("Sucess","Details are Updated")
                else:
                    tk1.showerror("Registration failed","Please enter the correct details")
            except :
                tk1.showerror("Registration failed","Please enter the correct details")

        Label(roots,text = "Student Registration",width=30,font=("Consolas",18)).place(x=100,y=30)

        Label(roots,text = "Student Name",width=15,font=("Consolas",10)).place(x=70,y=125)
        Entry(roots,width=23,textvariable=snamevar).place(x=245,y=125)

        Label(roots,text = "Student ID",width=15,font=("Consolas",10)).place(x=70,y=175)
        Entry(roots,width=23,textvariable=sidvar).place(x=245,y=175)

        Label(roots,text = "Student Password",width=25,font=("Consolas",10)).place(x=70,y=225)
        Entry(roots,width=23,textvariable=spwdvar).place(x=245,y=225)

        Label(roots,text = "Student Attendance",width=25,font=("Consolas",10)).place(x=70,y=275)
        Entry(roots,width=23,textvariable=sattendvar).place(x=245,y=275)

        Label(roots,text = "Periods Attended",width=25,font=("Consolas",10)).place(x=70,y=325)
        Entry(roots,width=23,textvariable=periodsvar).place(x=245,y=325)

        btn = Button(roots,text='Submit',width=20,command = lambda : verify(snamevar,sidvar,spwdvar,sattendvar,periodsvar))
        btn.place(x=240,y=400)
        btn2 = Button(roots,text='Delete',width=20,command = lambda : dele(sidvar,snamevar))
        btn2.place(x=80,y=400)
        roots.mainloop()

    def view_stu():
        roots = Tk()
        roots.resizable(False,False)
        roots.geometry("580x250")
        roots.title('database')
        mc = mydb.cursor()
        mc.execute('select * from student')
        mcc = mc.fetchall()
        i=1
        e=Label(roots,width=15,text='sname',borderwidth=3, relief='ridge',anchor='w')
        e.grid(row=0,column=0)
        e=Label(roots,width=15,text='sid',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=1)
        e=Label(roots,width=15,text='spwd',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=2)
        e=Label(roots,width=15,text='attendence',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=3)
        e=Label(roots,width=15,text='periods',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=4)
        e=Label(roots,width=15,text='percen',borderwidth=2, relief='ridge',anchor='w')
        e.grid(row=0,column=5)
        for student in mcc: 
            for j in range(len(student)):
                e = Entry(roots, width=15) 
                e.grid(row=i, column=j) 
                e.insert(END, student[j])
            i=i+1
        Button(roots,text='Close',width=20,command=roots.destroy).place(x=230,y=200)
        roots.mainloop()

    def upload_image():
        a = askopenfile(parent=root1,mode='rb',title='Choose a file')
        try:
            a = a.name
            if a != None:
                img_file.set(a)
                tk1.showinfo("Sucessful","The Image uploaded Sucessfully")
            else :
                tk1.showerror("Error","The Image is not uploaded Sucessfully")
        except:
            tk1.showerror("Error","The Image is not uploaded Sucessfully")

    def get_fac():
        if img_file.get() == '':
            tk1.showerror('Error','Image is not correctly uploaded')
            return
        else :
            try:
                rootg = Toplevel(root1)
                rootg.resizable(False,False)
                rootg.geometry('400x400')
                rootg.title('get_faces')
                u2 = Image.open("gui_icons/images_2.jpg")
                u2 = u2.resize((400,400),Image.ANTIALIAS)
                u2 = ImageTk.PhotoImage(u2)
                Label(rootg,image=u2).place(x=0, y=0, width=400, height=400)

                def update_database():
                    try :
                        mc = mydb.cursor()
                        presenties = [str(a) for a in l]
                        mc.execute('select sname from student;')
                        studs = [a[0] for a in mc.fetchall()]

                        for a in presenties:
                            if a in studs:
                                mc.execute('select sattend,periods,percen from student where sname = %s;',(a,))
                                le = mc.fetchall()[0]
                                att = int(le[0]) + 1
                                per = int(le[1]) + 1
                                percent = int(att*100/per)
                                cmd = 'update student set sattend = %s where sname = %s;'
                                values1 = (str(att),a)
                                cmd1 = 'update student set periods = %s where sname = %s;'
                                values2 = (str(per),a)
                                cmd2 = 'update student set percen = %s where sname = %s;'
                                values3 = (str(percent),a)
                                mc.execute(cmd,values1)
                                mc.execute(cmd1,values2)
                                mc.execute(cmd2,values3)
                            else:
                                print('Student is not our college ')
                        mydb.commit()
                        rootg.destroy()
                        tk1.showinfo("Sucess","Database is updated")
                    except Exception as e:
                        tk1.showerror("Error",e)


                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
                img = cv2.imread(img_file.get())
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                img = cv2.resize(img, (300, 150))
                im = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=im) 
                Label(rootg, image=imgtk).place(x=50,y=75)

                l = Mlpart.get_faces(img_file.get())
                Label(rootg, text = "the presenties are : "+str(l)).place(x=50,y=300)

                Button(rootg,text='Update database',width=20,command=update_database).place(x=130,y=350)
                rootg.mainloop()
            
            except Exception as e:
                tk1.showerror("Error",e)

    def create_dataset():
        try:
            os.system("start cmd /k python createdata.py")
        except Exception as e:
            tk1.showerror("Error",e)
            return

    def stu_images():
        rep = askopenfilenames(parent=root1,initialdir='C:/Users/nk/Desktop/final_aas/data/train/',initialfile='nice')
        print(rep)

    def help_desk():
        rooth = Tk()
        rooth.resizable(False,False)
        rooth.geometry('400x450')
        rooth.title('Help Desk')
        Label(rooth,text = "Instructions",width=20,font=("Consolas",17)).place(x=120,y=20)
        Label(rooth,text='1 . First upload the image which contains the \n student faces.',font=("Consolas",10)).place(x=20,y=80)
        Label(rooth,text='2 . Click on getfaces to identify the faces \n present in the photo.',font=("Consolas",10)).place(x=20,y=130)
        Label(rooth,text='3 . Click on show attendence to get the attendence \n of the students.',font=("Consolas",10)).place(x=20,y=180)
        Label(rooth,text="4 . Click on create dataset to create the dataset \n for testing. ",font=("Consolas",10)).place(x=20,y=230)
        Label(rooth,text="5 . Click on student details to get the student \n details.",font=("Consolas",10)).place(x=20,y=280)
        Label(rooth,text="6 . For further details contact \n   1 . 18311A0509@sreenidhi.edu.in  \n   2 . 18311A0519@sreenidhi.edu.in  \n   3 . 18311A0532@sreenidhi.edu.in  \n",font=("Consolas",10)).place(x=20,y=330)

        rooth.mainloop()


    Label(root1,text = "AUTOMATED ATTENDENCE SYSTEM",width=27,font=("Consolas",23)).place(x=230,y=40)
    
    #row1
    uploadimage = Image.open("gui_icons/stu_img1.png")
    uploadimage = uploadimage.resize((95,90))
    uploadimage = ImageTk.PhotoImage(uploadimage)
    Label(root1,image=uploadimage).place(x=85,y=145)

    uploadimage2 = Image.open("gui_icons/database.png")
    uploadimage2 = uploadimage2.resize((85,85))
    uploadimage2 = ImageTk.PhotoImage(uploadimage2)
    Label(root1,image=uploadimage2).place(x=325,y=150)

    uploadimage3 = Image.open("gui_icons/picture.png")
    uploadimage3 = uploadimage3.resize((90,85))
    uploadimage3 = ImageTk.PhotoImage(uploadimage3)
    Label(root1,image=uploadimage3).place(x=520,y=150)

    uploadimage4 = Image.open("gui_icons/help-desk.png")
    uploadimage4 = uploadimage4.resize((95,90))
    uploadimage4 = ImageTk.PhotoImage(uploadimage4)
    Label(root1,image=uploadimage4).place(x=735,y=145)

    #row2

    uploadimage5 = Image.open("gui_icons/face-detection.png")
    uploadimage5 = uploadimage5.resize((95,90))
    uploadimage5 = ImageTk.PhotoImage(uploadimage5)
    Label(root1,image=uploadimage5).place(x=93,y=340)

    uploadimage6 = Image.open("gui_icons/file-storage.png")
    uploadimage6 = uploadimage6.resize((85,85))
    uploadimage6 = ImageTk.PhotoImage(uploadimage6)
    Label(root1,image=uploadimage6).place(x=310,y=345)

    uploadimage7 = Image.open("gui_icons/student.png")
    uploadimage7 = uploadimage7.resize((100,95))
    uploadimage7 = ImageTk.PhotoImage(uploadimage7)
    Label(root1,image=uploadimage7).place(x=515,y=335)

    uploadimage8 = Image.open("gui_icons/log-out.png")
    uploadimage8 = uploadimage8.resize((95,90))
    uploadimage8 = ImageTk.PhotoImage(uploadimage8)
    Label(root1,image=uploadimage8).place(x=738,y=340)

    #row1
    Button(root1,text = "Upload Image",width=20,command=upload_image).place(x=80,y=255)
    Button(root1,text = "Student Details",width=20,command=view_stu).place(x=290,y=255)
    Button(root1,text = "Images",width=20,command=stu_images).place(x=500,y=255)
    Button(root1,text = "Help Desk",width=20,command=help_desk).place(x=720,y=255)

    #row2
    Button(root1,text = "Get Faces",width=20,command=get_fac).place(x=80,y=450)
    Button(root1,text = "Create Dataset",width=20,command=create_dataset).place(x=290,y=450)
    Button(root1,text = "Create Student",width=20,command=create_stu).place(x=500,y=450)
    Button(root1,text = "Exit",width=20,command=root1.destroy).place(x=720,y=450)

    #Button(root1,text='Logout',width=20,command=root1.destroy).place(x=390,y=550)
    
    root1.mainloop()

def student_page(z):
    root1 = Tk()
    print(z)
    root1.resizable(False,False)
    root1.geometry('530x530')
    u1 = Image.open("gui_icons/images_2.jpg")
    u1 = u1.resize((550,550),Image.ANTIALIAS)
    u1 = ImageTk.PhotoImage(u1)
    Label(root1,image=u1).place(x=0, y=0, width=550, height=550)
    root1.title(z)

    def upload(z):
        tk1.showinfo("message ","click ok to start your images")
        Mlpart.create_face(name_id[z])

    def view_att(z):
        mc = mydb.cursor()
        mc.execute('select sattend,percen from student where sid = %s;',(z,))
        l = mc.fetchall()[0]
        att,att1 = l[0],l[1]
        s = "the attendence of "+str(z)+" is "+att +"\n\nthe attendence percentage is "+att1
        tk1.showinfo("Attendence",s)

    def view_student(z):
        mc = mydb.cursor()
        mc.execute('select * from student where sid = %s;',(z,))
        att = list(mc.fetchall()[0])
        rootv = Tk()
        rootv.resizable(False,False)
        rootv.geometry('410x500')
        Label(rootv,text = "Student Details",width=18,font=("Consolas",17)).place(x=100,y=40)
        Label(rootv,text = "Student Name             :  "+str(att[0]),font=("Consolas",10)).place(x=30,y=110)
        Label(rootv,text = "Student ID               :  "+str(att[1]),font=("Consolas",10)).place(x=30,y=160)
        Label(rootv,text = "Student pwd              :  "+str(att[2]),font=("Consolas",10)).place(x=30,y=210)
        Label(rootv,text = "Student Attendence       :  "+str(att[3]),font=("Consolas",10)).place(x=30,y=260)
        Label(rootv,text = "Periods Attended         :  "+str(att[4]),font=("Consolas",10)).place(x=30,y=310)
        Label(rootv,text = "Attendence Percentage    :  "+str(att[5]),font=("Consolas",10)).place(x=30,y=360)
        Button(rootv,text="Close",width=20,command = rootv.destroy).place(x=140,y=430)
        rootv.title('Help Desk')
        rootv.mainloop()

    Label(root1,text = "Student Portal",width=18,font=("Consolas",20)).place(x=155,y=30)
    
    #row1
    uploadimage = Image.open("gui_icons/stu_img1.png")
    uploadimage = uploadimage.resize((95,90))
    uploadimage = ImageTk.PhotoImage(uploadimage)
    Label(root1,image=uploadimage).place(x=85,y=120)

    uploadimage2 = Image.open("gui_icons/student.png")
    uploadimage2 = uploadimage2.resize((95,90))
    uploadimage2 = ImageTk.PhotoImage(uploadimage2)
    Label(root1,image=uploadimage2).place(x=335,y=120)

    #row2
    uploadimage3 = Image.open("gui_icons/stu_img2.png")
    uploadimage3 = uploadimage3.resize((85,85))
    uploadimage3 = ImageTk.PhotoImage(uploadimage3)
    Label(root1,image=uploadimage3).place(x=95,y=325)

    uploadimage4 = Image.open("gui_icons/log-out.png")
    uploadimage4 = uploadimage4.resize((85,85))
    uploadimage4 = ImageTk.PhotoImage(uploadimage4)
    Label(root1,image=uploadimage4).place(x=345,y=330)

    #row1
    Button(root1,text="Upload Images",width=20,command= lambda :upload(z)).place(x=77,y=230)
    Button(root1,text = "Student Details",width=20,command=lambda : view_student(z)).place(x=315,y=230)
    
    #row2
    Button(root1,text="View Attendence",width=20,command=lambda : view_att(z)).place(x=77,y=435)
    Button(root1,text = "Exit",width=20,command=root1.destroy).place(x=315,y=435)

    root1.mainloop()

def login_page():
    root = Tk()
    root.resizable(False,False)
    root.geometry('450x450')
    uservar = StringVar()
    pwdvar = StringVar()
    loginasvar = IntVar()
    u0 = Image.open("gui_icons/images_2.jpg")
    u0 = u0.resize((450,450),Image.ANTIALIAS)
    u0 = ImageTk.PhotoImage(u0)
    Label(root,image=u0).place(x=0, y=0, width=450, height=450)
    root.title("Login Form")
    loginimage = Image.open("gui_icons/loginicon.jpg")
    loginimage = loginimage.resize((105,122))
    loginicon = ImageTk.PhotoImage(loginimage)
    Label(root,image=loginicon).place(x=175,y=35)

    def verify(uservar,pwdvar,loginasvar):
        x = str(uservar.get())
        y = str(pwdvar.get())
        z = int(loginasvar.get())
        try:
            if z == 2 and ds[x] == y:
                root.destroy()
                student_page(x)
                return
            elif z == 1 and da[x] == y:
                root.destroy()
                admin_page(x)
                return
            else :
                tk1.showerror("login failed","Please enter the correct details")
                return
        except Exception as e:
            tk1.showerror("login failed","Please enter the correct details")

    Label(root,text = "Username",width=20,font=("Consolas",10)).place(x=100,y=205)
    Entry(root,width=23,textvariable=uservar).place(x=225,y=205)

    Label(root,text = "Password",width=20,font=("Consolas",10)).place(x=100,y=255)
    Entry(root,width=23,textvariable=pwdvar).place(x=225,y=255)


    Label(root,text = "Login as",width=20,font=("Consolas",10)).place(x=100,y=305)
    Radiobutton(root,text="Admin",variable=loginasvar,value=1).place(x=225,y=305)
    Radiobutton(root,text="Student",variable=loginasvar,value=2).place(x=295,y=305)

    btn = Button(root,text='Submit',width=20,command = lambda : verify(uservar,pwdvar,loginasvar))
    btn.place(x=160,y=370)
    root.mainloop()

login_page()