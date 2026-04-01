from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
import re
from datetime import datetime

# ── Modern Color Palette (matching hi.py) ─────────────────────────────────────
BG        = "#0F1C2E"   # Deep navy background
SIDEBAR   = "#0A1628"   # Darker sidebar
CARD_BG   = "#162032"   # Card backgrounds
TOPBAR    = "#111E30"   # Top navigation bar
ACCENT    = "#4361EE"   # Modern blue accent
ACCENT2   = "#3A56D4"   # Darker blue for hover states
GREEN     = "#06D6A0"   # Vibrant green
ORANGE    = "#FF9E00"   # Modern amber
PURPLE    = "#8338EC"   # Vibrant purple
TEXT      = "#FFFFFF"   # Primary text
SUBTEXT   = "#A0AEC0"   # Secondary text
WHITE     = "#FFFFFF"
SEP       = "#2D3748"   # Separator lines
HOVER     = "#1E2E42"   # Hover effect color
LIGHT_BG  = "#1E2E42"   # Lighter background for entries

FONT_TITLE  = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_LARGE  = ("Segoe UI", 24, "bold")

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Create Account")
        self.root.geometry("1400x750+0+0")
        self.root.config(bg=BG)
        self.root.resizable(False, False)

        # Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_question = StringVar()
        self.var_answer = StringVar()
        self.var_password = StringVar()
        self.var_cpassword = StringVar()
        self.var_chk = IntVar()

        self.entry_fields = []

        self._build_layout()

    def _build_layout(self):
        # Main container
        main_container = Frame(self.root, bg=BG)
        main_container.pack(fill=BOTH, expand=True)

        # Left decorative panel with gradient
        left_panel = Frame(main_container, bg=ACCENT, width=500)
        left_panel.pack(side=LEFT, fill=Y)
        left_panel.pack_propagate(False)

        # Gradient background on left panel
        left_canvas = Canvas(left_panel, bg=ACCENT, highlightthickness=0)
        left_canvas.pack(fill=BOTH, expand=True)

        def update_left_gradient(event):
            left_canvas.delete("gradient")
            for i in range(event.height):
                r = int(67 - (i * 0.12))
                g = int(97 - (i * 0.1))
                b = int(238 - (i * 0.35))
                color = f"#{max(0, r):02x}{max(0, g):02x}{max(0, b):02x}"
                left_canvas.create_line(0, i, event.width, i, fill=color, width=1, tags="gradient")

        left_canvas.bind("<Configure>", update_left_gradient)

        # Left panel content
        try:
            left_img = ImageTk.PhotoImage(file="images/side.png")
            left_canvas.create_image(250, 350, image=left_img, tags="image")
            self.left_img = left_img
        except:
            pass

        Label(left_panel, text="🎓", font=("Segoe UI", 70), 
              bg=ACCENT, fg=WHITE).place(relx=0.5, rely=0.25, anchor=CENTER)
        Label(left_panel, text="Welcome to", font=("Segoe UI", 18), 
              bg=ACCENT, fg=WHITE).place(relx=0.5, rely=0.4, anchor=CENTER)
        Label(left_panel, text="Student Result\nManagement System", 
              font=("Segoe UI", 26, "bold"), bg=ACCENT, fg=WHITE, justify=CENTER
              ).place(relx=0.5, rely=0.52, anchor=CENTER)
        Label(left_panel, text="Create your account\nto get started", 
              font=("Segoe UI", 12), bg=ACCENT, fg=SUBTEXT, justify=CENTER
              ).place(relx=0.5, rely=0.72, anchor=CENTER)

        # Right panel - Registration Form
        right_panel = Frame(main_container, bg=CARD_BG)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        # Title
        title_frame = Frame(right_panel, bg=CARD_BG)
        title_frame.pack(fill=X, pady=(30, 15))
        Label(title_frame, text="Create Account", font=("Segoe UI", 28, "bold"),
              bg=CARD_BG, fg=WHITE).pack()
        Label(title_frame, text="Please fill in the details below to register", 
              font=FONT_BODY, bg=CARD_BG, fg=SUBTEXT).pack()

        # Separator
        Frame(right_panel, bg=SEP, height=2).pack(fill=X, padx=50, pady=10)

        # Form container with scrollbar
        form_canvas = Canvas(right_panel, bg=CARD_BG, highlightthickness=0)
        form_scrollbar = Scrollbar(right_panel, orient=VERTICAL, command=form_canvas.yview)
        form_frame = Frame(form_canvas, bg=CARD_BG)

        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw", width=700)
        form_frame.bind("<Configure>", lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))

        form_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=30, pady=15)
        form_scrollbar.pack(side=RIGHT, fill=Y)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Row 1 - First Name & Last Name
        Label(form_frame, text="First Name", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=0, padx=(20, 10), pady=(15, 5), sticky=W)
        self.txt_fname = Entry(form_frame, textvariable=self.var_fname, font=FONT_BODY,
                               bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                               insertbackground=WHITE)
        self.txt_fname.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky=EW)
        self.txt_fname.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_fname)

        Label(form_frame, text="Last Name", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=1, padx=(10, 20), pady=(15, 5), sticky=W)
        self.txt_lname = Entry(form_frame, textvariable=self.var_lname, font=FONT_BODY,
                               bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                               insertbackground=WHITE)
        self.txt_lname.grid(row=1, column=1, padx=(10, 20), pady=(0, 15), sticky=EW)
        self.txt_lname.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_lname)

        # Row 2 - Contact & Email
        Label(form_frame, text="Contact No.", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=2, column=0, padx=(20, 10), pady=(5, 5), sticky=W)
        self.txt_contact = Entry(form_frame, textvariable=self.var_contact, font=FONT_BODY,
                                 bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                                 insertbackground=WHITE)
        self.txt_contact.grid(row=3, column=0, padx=(20, 10), pady=(0, 15), sticky=EW)
        self.txt_contact.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_contact)

        Label(form_frame, text="Email", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=2, column=1, padx=(10, 20), pady=(5, 5), sticky=W)
        self.txt_email = Entry(form_frame, textvariable=self.var_email, font=FONT_BODY,
                               bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                               insertbackground=WHITE)
        self.txt_email.grid(row=3, column=1, padx=(10, 20), pady=(0, 15), sticky=EW)
        self.txt_email.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_email)

        # Row 3 - Security Question
        Label(form_frame, text="Security Question", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=4, column=0, padx=(20, 10), pady=(5, 5), sticky=W)
        
        self.cmb_quest = ttk.Combobox(form_frame, textvariable=self.var_question, 
                                      font=FONT_BODY, state="readonly", width=28)
        self.cmb_quest['values'] = ("Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name")
        self.cmb_quest.grid(row=5, column=0, padx=(20, 10), pady=(0, 15), sticky=EW)
        self.cmb_quest.current(0)
        self.cmb_quest.bind("<Return>", self._on_enter_pressed)

        Label(form_frame, text="Answer", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=4, column=1, padx=(10, 20), pady=(5, 5), sticky=W)
        self.txt_answer = Entry(form_frame, textvariable=self.var_answer, font=FONT_BODY,
                                bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                                insertbackground=WHITE)
        self.txt_answer.grid(row=5, column=1, padx=(10, 20), pady=(0, 15), sticky=EW)
        self.txt_answer.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_answer)

        # Row 4 - Password & Confirm Password
        Label(form_frame, text="Password", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=6, column=0, padx=(20, 10), pady=(5, 5), sticky=W)
        self.txt_password = Entry(form_frame, textvariable=self.var_password, font=FONT_BODY,
                                  bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                                  insertbackground=WHITE, show="•")
        self.txt_password.grid(row=7, column=0, padx=(20, 10), pady=(0, 15), sticky=EW)
        self.txt_password.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_password)

        Label(form_frame, text="Confirm Password", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=6, column=1, padx=(10, 20), pady=(5, 5), sticky=W)
        self.txt_cpassword = Entry(form_frame, textvariable=self.var_cpassword, font=FONT_BODY,
                                   bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=30,
                                   insertbackground=WHITE, show="•")
        self.txt_cpassword.grid(row=7, column=1, padx=(10, 20), pady=(0, 15), sticky=EW)
        self.txt_cpassword.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_cpassword)

        # Terms & Conditions
        chk_frame = Frame(form_frame, bg=CARD_BG)
        chk_frame.grid(row=8, column=0, columnspan=2, padx=20, pady=(10, 10), sticky=W)
        
        Checkbutton(chk_frame, text="I Agree The Terms & Conditions", 
                   variable=self.var_chk, onvalue=1, offvalue=0,
                   bg=CARD_BG, fg=SUBTEXT, font=FONT_BODY,
                   selectcolor=CARD_BG, activebackground=CARD_BG).pack(side=LEFT)

        # Register Button
        btn_frame = Frame(form_frame, bg=CARD_BG)
        btn_frame.grid(row=9, column=0, columnspan=2, padx=20, pady=(15, 10), sticky=EW)

        btn_register = Button(btn_frame, text="🔐 REGISTER", font=FONT_TITLE,
                             bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                             activebackground="#05b88a", command=self.register_data, pady=12)
        btn_register.pack(fill=X)
        btn_register.bind("<Return>", lambda e: self.register_data())

        # Login Link
        login_frame = Frame(form_frame, bg=CARD_BG)
        login_frame.grid(row=10, column=0, columnspan=2, padx=20, pady=(5, 20), sticky=EW)

        Label(login_frame, text="Already have an account?", font=FONT_BODY,
              bg=CARD_BG, fg=SUBTEXT).pack(side=LEFT)
        
        btn_login = Button(login_frame, text="Sign In Here", font=("Segoe UI", 10, "bold"),
                          bg=CARD_BG, fg=ACCENT, cursor="hand2", relief=FLAT,
                          activebackground=CARD_BG, command=self.login_window)
        btn_login.pack(side=LEFT, padx=5)
        btn_login.bind("<Return>", lambda e: self.login_window())

        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

    def _on_enter_pressed(self, event):
        """Handle Enter key - move to next field"""
        current = event.widget
        try:
            index = self.entry_fields.index(current)
            if index < len(self.entry_fields) - 1:
                self.entry_fields[index + 1].focus()
            else:
                self.register_data()
        except ValueError:
            pass
        return "break"

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def validate_contact(self, contact):
        """Validate contact number"""
        return contact.isdigit() and len(contact) == 10

    def login_window(self):
        self.root.destroy()
        os.system("python login.py")

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.cmb_quest.current(0)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.var_chk.set(0)

    def register_data(self):
        # Validation
        if self.txt_fname.get() == "":
            messagebox.showerror("Error", "First Name is required", parent=self.root)
            self.txt_fname.focus()
            return
        
        if self.txt_lname.get() == "":
            messagebox.showerror("Error", "Last Name is required", parent=self.root)
            self.txt_lname.focus()
            return
        
        if self.txt_contact.get() == "":
            messagebox.showerror("Error", "Contact Number is required", parent=self.root)
            self.txt_contact.focus()
            return
        
        if not self.validate_contact(self.txt_contact.get()):
            messagebox.showerror("Error", "Contact Number must be 10 digits", parent=self.root)
            self.txt_contact.focus()
            return
        
        if self.txt_email.get() == "":
            messagebox.showerror("Error", "Email is required", parent=self.root)
            self.txt_email.focus()
            return
        
        if not self.validate_email(self.txt_email.get()):
            messagebox.showerror("Error", "Invalid email format", parent=self.root)
            self.txt_email.focus()
            return
        
        if self.cmb_quest.get() == "Select":
            messagebox.showerror("Error", "Please select a security question", parent=self.root)
            self.cmb_quest.focus()
            return
        
        if self.txt_answer.get() == "":
            messagebox.showerror("Error", "Answer is required", parent=self.root)
            self.txt_answer.focus()
            return
        
        if self.txt_password.get() == "":
            messagebox.showerror("Error", "Password is required", parent=self.root)
            self.txt_password.focus()
            return
        
        if len(self.txt_password.get()) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=self.root)
            self.txt_password.focus()
            return
        
        if self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Password and Confirm Password should be same", parent=self.root)
            self.txt_cpassword.focus()
            return
        
        if self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree our terms & conditions", parent=self.root)
            return

        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            
            # Check if email already exists
            cur.execute("SELECT * FROM employee WHERE email=?", (self.txt_email.get(),))
            row = cur.fetchone()
            
            if row is not None:
                messagebox.showerror("Error", "User already exists, please try with another email", parent=self.root)
                con.close()
                return
            
            # Insert new user
            cur.execute("""INSERT INTO employee (f_name, l_name, contact, email, question, answer, password) 
                          VALUES(?,?,?,?,?,?,?)""", (
                self.txt_fname.get(),
                self.txt_lname.get(),
                self.txt_contact.get(),
                self.txt_email.get(),
                self.cmb_quest.get(),
                self.txt_answer.get(),
                self.txt_password.get()
            ))
            
            con.commit()
            con.close()
            
            messagebox.showinfo("Success", 
                               f"Registration Successful!\n\nWelcome {self.txt_fname.get()} {self.txt_lname.get()}!\nYou can now login.",
                               parent=self.root)
            
            self.clear()
            self.login_window()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()