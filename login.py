from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
from datetime import *
from math import *
import sqlite3
import os
class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        # =======Left Panel=======
        left_lbl = Label(self.root, bg="#08a3d2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        # =======Right Panel=======
        right_lbl = Label(self.root, bg="#031f3c", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # =======Login Frame=======
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=550, y=80, width=500, height=550)

        title = Label(login_frame, text="LOGIN HERE", font=("times new roman", 25, "bold"), bg="white", fg="#0b5377")
        title.place(x=100, y=30)

        # Email
        email = Label(login_frame, text="EMAIL ADDRESS", font=("times new roman", 13, "bold"), bg="white", fg="#333")
        email.place(x=50, y=120)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=50, y=150, width=400)

        # Password
        pass_ = Label(login_frame, text="PASSWORD", font=("times new roman", 13, "bold"), bg="white", fg="#333")
        pass_.place(x=50, y=210)
        self.txt_pass = Entry(login_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass.place(x=50, y=240, width=400)

        # Register & Forget Password links
        btn_register = Button(login_frame, text="Register new Account?", font=("times new roman", 12),
                              bd=0, cursor="hand2", fg="#c0392b", bg="white", command=self.register_window)
        btn_register.place(x=50, y=295)

        btn_forget = Button(login_frame, text="Forget Password?", font=("times new roman", 12),
                            bd=0, cursor="hand2", fg="#c0392b", bg="white", command=self.forget_password)
        btn_forget.place(x=270, y=295)

        # Login Button
        btn_login = Button(login_frame, text="Login", font=("times new roman", 15, "bold"),
                           bg="#c0392b", fg="white", cursor="hand2", command=self.login)
        btn_login.place(x=50, y=350, width=200, height=45)

        # =======Clock on Left Panel=======
        self.lbl = Label(self.root, text="WebCode Clock", font=("Book Antiqua", 20, "bold"), bg="#08a3d2", fg="white")
        self.lbl.place(x=150, y=100)

        self.clock_lbl = Label(self.root, bg="#08a3d2", bd=0)
        self.clock_lbl.place(x=100, y=150, width=400, height=400)

        self.working()

    def working(self):
        now = datetime.now()
        hr = now.hour % 12
        min_ = now.minute
        sec_ = now.second

        hr_angle  = (hr * 30) + (min_ * 0.5)
        min_angle = min_ * 6
        sec_angle = sec_ * 6

        self.clock_image(hr_angle, min_angle, sec_angle)
        self.root.after(1000, self.working)

    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)

        # Clock face
        draw.ellipse((10, 10, 390, 390), outline="white", width=3)

        # Hour markers
        for i in range(12):
            angle = radians(i * 30)
            x1 = 200 + 170 * sin(angle)
            y1 = 200 - 170 * cos(angle)
            x2 = 200 + 185 * sin(angle)
            y2 = 200 - 185 * cos(angle)
            draw.line((x1, y1, x2, y2), fill="white", width=3)

        # Number labels (12, 3, 6, 9)
        for num, angle in [(12, 0), (3, 90), (6, 180), (9, 270)]:
            a = radians(angle)
            x = int(200 + 145 * sin(a)) - 8
            y = int(200 - 145 * cos(a)) - 10
            draw.text((x, y), str(num), fill="white")

        # Hour hand
        draw.line((200, 200, 200 + 60 * sin(radians(hr)), 200 - 60 * cos(radians(hr))), fill="white", width=5)
        # Minute hand
        draw.line((200, 200, 200 + 90 * sin(radians(min_)), 200 - 90 * cos(radians(min_))), fill="lightgreen", width=3)
        # Second hand
        draw.line((200, 200, 200 + 110 * sin(radians(sec_)), 200 - 110 * cos(radians(sec_))), fill="red", width=2)
        # Center dot
        draw.ellipse((193, 193, 207, 207), fill="cyan")

        self.clock_photo = ImageTk.PhotoImage(clock)
        self.clock_lbl.config(image=self.clock_photo)

    def forget_password(self):
        self.root2 = Toplevel()
        self.root2.title("Forget Password")
        self.root2.geometry("400x420+500+100")
        self.root2.config(bg="white")
        self.root2.focus_force()

        t = Label(self.root2, text="Forget Password", font=("times new roman", 20, "bold"), bg="white", fg="#0b5377")
        t.place(x=50, y=30)

        email_lbl = Label(self.root2, text="Email", font=("times new roman", 15, "bold"), bg="white")
        email_lbl.place(x=50, y=80)
        self.fp_email = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
        self.fp_email.place(x=50, y=110, width=300)

        question = Label(self.root2, text="Select Security Question", font=("times new roman", 13, "bold"), bg="white")
        question.place(x=50, y=150)
        self.cmb_quest = ttk.Combobox(self.root2, font=("times new roman", 13), state="readonly", justify=CENTER)
        self.cmb_quest['values'] = ("Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name")
        self.cmb_quest.place(x=50, y=180, width=300)
        self.cmb_quest.current(0)

        answer = Label(self.root2, text="Answer", font=("times new roman", 15, "bold"), bg="white")
        answer.place(x=50, y=220)
        self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=50, y=250, width=300)

        new_password = Label(self.root2, text="New Password", font=("times new roman", 15, "bold"), bg="white")
        new_password.place(x=50, y=290)
        self.txt_new_pass = Entry(self.root2, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_new_pass.place(x=50, y=320, width=300)

        btn_change = Button(self.root2, text="Reset Password", font=("times new roman", 13, "bold"),
                            bg="#0b5377", fg="white", cursor="hand2", command=self.reset_password)
        btn_change.place(x=50, y=370, width=300)

    def reset_password(self):
        if self.cmb_quest.get() == "Select" or self.txt_answer.get() == "" or self.txt_new_pass.get() == "" or self.fp_email.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root2)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=? and question=? and answer=?",
                            (self.fp_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Incorrect email, question or answer", parent=self.root2)
                else:
                    cur.execute("update employee set password=? where email=?",
                                (self.txt_new_pass.get(), self.fp_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Password reset successfully!", parent=self.root2)
                    self.root2.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root2)

    def register_window(self):
        self.root.destroy()
        os.system("python register.py")

    def login(self):
        if self.txt_email.get() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=? and password=?",
                            (self.txt_email.get(), self.txt_pass.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome to Student Result Management System{self.txt_email.get()}", parent=self.root)
                    self.root.destroy()
                    os.system("python hi.py")
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Login_window(root)
    root.mainloop()
