from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from create_db import create_db
from result import resultClass

class reportClass:
    def __init__(self,root):

        self.root=root
        self.root.title("STUDENT RESULT MANAGEMENT SYSTEM")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        #----------title------
        title=Label(self.root,text="View Student Results ",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)

        #---------srearch panel------
        self.var_search=StringVar()
        self.var_id=""
        lbl_search=Label(self.root,text="Search by Roll No",font=("goudy old style",20),bg="white").place(x=280,y=100)
        txt_search=Entry(self.root,textvariable=self.var_search ,font=("goudy old style",20),bg="lightyellow").place(x=520,y=100,width=150)
        btn_search=Button(self.root,text="Search",font=("goudy old style",15,"bold"),bg="#0390d6",fg="white",cursor="hand2",command=self.search).place(x=680,y=100,width=100,height=35)
        btn_clear=Button(self.root,text="Clear",font=("goudy old style",15,"bold"),bg="grey",fg="white",cursor="hand2",command=self.clear).place(x=800,y=100,width=100,height=35)


        #result label
        lbl_roll=Label(self.root,text="Roll No",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=150,y=230,width=150,height=50)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=300,y=230,width=150,height=50)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=450,y=230,width=150,height=50)
        lbl_marks=Label(self.root,text="Marks Obtained",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=600,y=230,width=150,height=50)
        lbl_fullmarks=Label(self.root,text="Total Marks",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=750,y=230,width=150,height=50)
        lbl_per=Label(self.root,text="Percentage",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE).place(x=900,y=230,width=150,height=50)
       
       
       
        self.roll=Label(self.root,font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self.roll.place(x=150,y=280,width=150,height=50)
        self._name=Label(self.root,font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self._name.place(x=300,y=280,width=150,height=50)
        self.course=Label(self.root,font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self.course.place(x=450,y=280,width=150,height=50)
        self.marks=Label(self.root,text="",font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self.marks.place(x=600,y=280,width=150,height=50)
        self.fullmarks=Label(self.root,font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self.fullmarks.place(x=750,y=280,width=150,height=50)
        self.per=Label(self.root,font=("goudy old style",15,"bold"),bg="lightblue",bd=2,relief=GROOVE)
        self.per.place(x=900,y=280,width=150,height=50)
        
        #---------button delete------
        btn_delete=Button(self.root,text="Delete",font=("goudy old style",15,"bold"),bg="red",fg="white",cursor="hand2",command=self.delete).place(x=500,y=350,width=150,height=35)

        #---------search function------
    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Roll No should be required",parent=self.root)
            else:
                cur.execute("select * from result where roll=?",(self.var_search.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.var_id=row[0]
                    self.roll.config(text=row[1])
                    self._name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[4])
                    self.fullmarks.config(text=row[5])
                    self.per.config(text=row[6])
                #self.per.config(text=str(per)+"%")
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

    def clear(self):
        self.var_id=""
        self.var_search.set("")
        self.roll.config(text="")
        self._name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.fullmarks.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_id=="":
                messagebox.showerror("Error","Search for a record to delete",parent=self.root)
            else:
                cur.execute("select * from result where rid=?",(self.var_id,))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Record not found, try different",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from result where rid=?",(self.var_id,))
                        con.commit()
                        messagebox.showinfo("Delete","Result deleted successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")            
if __name__=="__main__":

    root=Tk()
    obj=reportClass(root)
    root.mainloop()