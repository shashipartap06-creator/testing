import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os
import re
import sys

# ── Configure CustomTkinter Appearance ─────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(1.4)
ctk.set_window_scaling(1.4)

# ── High DPI Scaling for Linux ─────────────────────────────────────────────────
def setup_high_dpi():
    """Configure high DPI scaling for Linux"""
    try:
        if sys.platform == "linux":
            os.environ['GDK_SCALE'] = '2'
            os.environ['GDK_DPI_SCALE'] = '0.5'
            
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)
        
    except:
        pass

setup_high_dpi()

# ── Light Theme Colors (only) ──────────────────────────────────────────────────
LIGHT_THEME = {
    "bg": "#F0F2F5",
    "glass_bg": "#FFFFFF",
    "glass_border": "#E2E8F0",
    "accent": "#6366F1",
    "accent_hover": "#818CF8",
    "green": "#10B981",
    "orange": "#F59E0B",
    "purple": "#8B5CF6",
    "text_primary": "#1E293B",
    "text_secondary": "#475569",
    "subtext": "#94A3B8",
    "error": "#EF4444",
    "success": "#059669",
    "card_bg": "#F8FAFC"
}

FONT_TITLE   = ("Segoe UI", 24, "bold")
FONT_HEADING = ("Segoe UI", 16, "bold")
FONT_BODY    = ("Segoe UI", 12)
FONT_SMALL   = ("Segoe UI", 11)

class Register(ctk.CTkToplevel):
    def __init__(self, root=None):
        if root is None:
            self.root = ctk.CTk()
        else:
            self.root = root
            self.root.destroy()
            self.root = ctk.CTk()
            
        self.root.title("SRMS — Create Account")
        self.theme = LIGHT_THEME.copy()
        
        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        width = 1000
        height = 700
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(900, 600)
        self.root.configure(fg_color=self.theme["bg"])
        
        # Variables
        self.var_fname = ctk.StringVar()
        self.var_lname = ctk.StringVar()
        self.var_contact = ctk.StringVar()
        self.var_email = ctk.StringVar()
        self.var_question = ctk.StringVar(value="Select")
        self.var_answer = ctk.StringVar()
        self.var_password = ctk.StringVar()
        self.var_cpassword = ctk.StringVar()
        self.var_chk = ctk.IntVar()
        
        self.entry_fields = []
        
        self._build_layout()
        
    def _build_layout(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ── Left Panel ─────────────────────────────────────────────────────────
        left_panel = ctk.CTkFrame(
            main_container, 
            fg_color=self.theme["glass_bg"],
            corner_radius=24,
            width=320
        )
        left_panel.pack(side="left", fill="y", padx=(0, 20), pady=0)
        left_panel.pack_propagate(False)
        
        # Left panel content
        left_content = ctk.CTkFrame(left_panel, fg_color="transparent")
        left_content.pack(expand=True, fill="both", padx=25, pady=40)
        
        # Logo
        logo_frame = ctk.CTkFrame(left_content, fg_color="transparent")
        logo_frame.pack(pady=(0, 20))
        
        ctk.CTkLabel(logo_frame, text="🎓", 
                    font=("Segoe UI", 56, "bold"),
                    text_color=self.theme["accent"]).pack()
        
        ctk.CTkLabel(left_content, text="SRMS",
                    font=FONT_TITLE, text_color=self.theme["text_primary"]).pack()
        
        ctk.CTkLabel(left_content, text="Student Result Management System",
                    font=FONT_SMALL, text_color=self.theme["text_secondary"],
                    wraplength=250).pack(pady=(5, 30))
        
        # Stats Card
        stats_card = ctk.CTkFrame(
            left_content, 
            fg_color=self.theme["card_bg"],
            corner_radius=16
        )
        stats_card.pack(fill="x", pady=20)
        
        ctk.CTkLabel(stats_card, text="📊",
                    font=("Segoe UI", 32), text_color=self.theme["green"]).pack(pady=(15, 5))
        
        ctk.CTkLabel(stats_card, text="500+",
                    font=FONT_HEADING, text_color=self.theme["text_primary"]).pack()
        
        ctk.CTkLabel(stats_card, text="Active Students",
                    font=FONT_SMALL, text_color=self.theme["text_secondary"]).pack(pady=(0, 15))
        
        # Features
        features = ["✓ Easy Result Management", "✓ Real-time Reports", "✓ Secure & Reliable"]
        for feature in features:
            ctk.CTkLabel(left_content, text=feature,
                        font=FONT_SMALL, text_color=self.theme["text_secondary"],
                        anchor="w").pack(anchor="w", pady=5)
        
        # ── Right Panel - Form ─────────────────────────────────────────────────
        right_panel = ctk.CTkFrame(
            main_container, 
            fg_color=self.theme["glass_bg"],
            corner_radius=24
        )
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Scrollable form
        form_container = ctk.CTkScrollableFrame(
            right_panel, 
            fg_color="transparent",
            scrollbar_button_color=self.theme["accent"],
            scrollbar_button_hover_color=self.theme["accent_hover"]
        )
        form_container.pack(fill="both", expand=True, padx=35, pady=35)
        
        # Form Header
        ctk.CTkLabel(form_container, text="Create Account",
                    font=FONT_TITLE, text_color=self.theme["text_primary"]).pack(anchor="w")
        
        ctk.CTkLabel(form_container, text="Please fill in the details to get started",
                    font=FONT_BODY, text_color=self.theme["text_secondary"]).pack(anchor="w", pady=(5, 25))
        
        # Separator
        ctk.CTkFrame(form_container, height=2, fg_color=self.theme["glass_border"]).pack(fill="x", pady=(0, 25))
        
        # Two-column layout for name
        name_row = ctk.CTkFrame(form_container, fg_color="transparent")
        name_row.pack(fill="x", pady=(0, 15))
        
        # First Name
        fname_frame = ctk.CTkFrame(name_row, fg_color="transparent")
        fname_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(fname_frame, text="First Name", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_fname = ctk.CTkEntry(
            fname_frame, textvariable=self.var_fname,
            placeholder_text="Enter first name",
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_fname.pack(fill="x", pady=(5, 0))
        self.txt_fname.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_fname)
        
        # Last Name
        lname_frame = ctk.CTkFrame(name_row, fg_color="transparent")
        lname_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(lname_frame, text="Last Name", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_lname = ctk.CTkEntry(
            lname_frame, textvariable=self.var_lname,
            placeholder_text="Enter last name",
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_lname.pack(fill="x", pady=(5, 0))
        self.txt_lname.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_lname)
        
        # Contact
        contact_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        contact_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(contact_frame, text="Contact Number", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_contact = ctk.CTkEntry(
            contact_frame, textvariable=self.var_contact,
            placeholder_text="Enter 10-digit mobile number",
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_contact.pack(fill="x", pady=(5, 0))
        self.txt_contact.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_contact)
        
        # Email
        email_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(email_frame, text="Email Address", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_email = ctk.CTkEntry(
            email_frame, textvariable=self.var_email,
            placeholder_text="Enter email address",
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_email.pack(fill="x", pady=(5, 0))
        self.txt_email.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_email)
        
        # Security Question
        sec_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        sec_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(sec_frame, text="Security Question", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.cmb_quest = ctk.CTkComboBox(
            sec_frame, variable=self.var_question,
            values=["Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name"],
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            button_color=self.theme["accent"],
            button_hover_color=self.theme["accent_hover"],
            text_color=self.theme["text_primary"]
        )
        self.cmb_quest.pack(fill="x", pady=(5, 0))
        
        # Answer
        answer_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        answer_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(answer_frame, text="Answer", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_answer = ctk.CTkEntry(
            answer_frame, textvariable=self.var_answer,
            placeholder_text="Enter your security answer",
            height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_answer.pack(fill="x", pady=(5, 0))
        self.txt_answer.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_answer)
        
        # Password
        pass_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        pass_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(pass_frame, text="Password", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_password = ctk.CTkEntry(
            pass_frame, textvariable=self.var_password,
            placeholder_text="Enter password (min 6 characters)",
            show="•", height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_password.pack(fill="x", pady=(5, 0))
        self.txt_password.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_password)
        
        # Confirm Password
        cpass_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        cpass_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(cpass_frame, text="Confirm Password", font=FONT_BODY,
                    text_color=self.theme["text_secondary"]).pack(anchor="w")
        
        self.txt_cpassword = ctk.CTkEntry(
            cpass_frame, textvariable=self.var_cpassword,
            placeholder_text="Confirm your password",
            show="•", height=44, corner_radius=12, border_width=1,
            fg_color=self.theme["card_bg"],
            border_color=self.theme["glass_border"],
            text_color=self.theme["text_primary"]
        )
        self.txt_cpassword.pack(fill="x", pady=(5, 0))
        self.txt_cpassword.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_cpassword)
        
        # Terms & Conditions
        terms_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        terms_frame.pack(fill="x", pady=(0, 20))
        
        self.chk_terms = ctk.CTkCheckBox(
            terms_frame, text="I agree to the Terms & Conditions",
            variable=self.var_chk, onvalue=1, offvalue=0,
            text_color=self.theme["text_secondary"],
            fg_color=self.theme["accent"],
            hover_color=self.theme["accent_hover"],
            border_color=self.theme["glass_border"]
        )
        self.chk_terms.pack(anchor="w")
        
        # Register Button
        self.btn_register = ctk.CTkButton(
            form_container, text="🔐 CREATE ACCOUNT",
            font=FONT_HEADING, height=52, corner_radius=14,
            fg_color=self.theme["green"],
            hover_color="#059669",
            text_color="white",
            command=self.register_data
        )
        self.btn_register.pack(fill="x", pady=(10, 15))
        self.btn_register.bind("<Return>", lambda e: self.register_data())
        
        # Login Link
        login_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        login_frame.pack(fill="x", pady=(5, 10))
        
        ctk.CTkLabel(login_frame, text="Already have an account?",
                    font=FONT_BODY, text_color=self.theme["text_secondary"]).pack(side="left")
        
        self.btn_login = ctk.CTkButton(
            login_frame, text="Sign In",
            font=FONT_BODY, fg_color="transparent",
            hover_color=self.theme["glass_bg"],
            text_color=self.theme["accent"],
            command=self.login_window
        )
        self.btn_login.pack(side="left", padx=(10, 0))
        
        # Set focus
        self.txt_fname.focus()
    
    def _on_enter_pressed(self, event):
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
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)
    
    def validate_contact(self, contact):
        return contact.isdigit() and len(contact) == 10
    
    def login_window(self):
        self.root.destroy()
        try:
            import login
            login_root = ctk.CTk()
            if hasattr(login, 'LoginClass'):
                login.LoginClass(login_root)
            login_root.mainloop()
        except ImportError:
            pass
    
    def clear(self):
        self.txt_fname.delete(0, 'end')
        self.txt_lname.delete(0, 'end')
        self.txt_contact.delete(0, 'end')
        self.txt_email.delete(0, 'end')
        self.cmb_quest.set("Select")
        self.txt_answer.delete(0, 'end')
        self.txt_password.delete(0, 'end')
        self.txt_cpassword.delete(0, 'end')
        self.var_chk.set(0)
        self.txt_fname.focus()
    
    def register_data(self):
        # Validation
        if self.txt_fname.get().strip() == "":
            messagebox.showerror("Error", "First Name is required", parent=self.root)
            self.txt_fname.focus()
            return
        
        if self.txt_lname.get().strip() == "":
            messagebox.showerror("Error", "Last Name is required", parent=self.root)
            self.txt_lname.focus()
            return
        
        if self.txt_contact.get().strip() == "":
            messagebox.showerror("Error", "Contact Number is required", parent=self.root)
            self.txt_contact.focus()
            return
        
        if not self.validate_contact(self.txt_contact.get().strip()):
            messagebox.showerror("Error", "Contact Number must be 10 digits", parent=self.root)
            self.txt_contact.focus()
            return
        
        if self.txt_email.get().strip() == "":
            messagebox.showerror("Error", "Email is required", parent=self.root)
            self.txt_email.focus()
            return
        
        if not self.validate_email(self.txt_email.get().strip()):
            messagebox.showerror("Error", "Invalid email format", parent=self.root)
            self.txt_email.focus()
            return
        
        if self.cmb_quest.get() == "Select":
            messagebox.showerror("Error", "Please select a security question", parent=self.root)
            self.cmb_quest.focus()
            return
        
        if self.txt_answer.get().strip() == "":
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
            messagebox.showerror("Error", "Please agree to the terms & conditions", parent=self.root)
            return
        
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            
            cur.execute("SELECT * FROM employee WHERE email=?", (self.txt_email.get(),))
            row = cur.fetchone()
            
            if row is not None:
                messagebox.showerror("Error", "User already exists, please try with another email", parent=self.root)
                con.close()
                return
            
            cur.execute("""INSERT INTO employee (f_name, l_name, contact, email, question, answer, password) 
                          VALUES(?,?,?,?,?,?,?)""", (
                self.txt_fname.get().strip(),
                self.txt_lname.get().strip(),
                self.txt_contact.get().strip(),
                self.txt_email.get().strip(),
                self.cmb_quest.get(),
                self.txt_answer.get().strip(),
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
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = Register()
    app.root.mainloop()