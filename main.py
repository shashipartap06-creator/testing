from tkinter import Tk, messagebox
from login import Login_window
from hi import RMS

class AppManager:
    """Manages the application flow between login and dashboard"""
    
    def __init__(self):
        self.login_root = None
        self.dashboard_root = None
    
    def start_dashboard(self):
        """Start the dashboard after successful login"""
        # Destroy login window if exists
        if self.login_root:
            try:
                self.login_root.destroy()
            except:
                pass
            self.login_root = None
        
        # Create dashboard window
        self.dashboard_root = Tk()
        self.dashboard_root.tk.call('tk', 'scaling', 1.4)
        app = RMS(self.dashboard_root)
        
        # Override logout to go back to login
        def new_logout():
            if messagebox.askyesno("Confirm", "Do you really want to logout?"):
                self.dashboard_root.destroy()
                self.dashboard_root = None
                self.show_login()
        
        app.logout = new_logout
        self.dashboard_root.mainloop()
    
    def show_login(self):
        """Show login window"""
        # Destroy dashboard window if exists
        if self.dashboard_root:
            try:
                self.dashboard_root.destroy()
            except:
                pass
            self.dashboard_root = None
        
        # Create login window with callback
        self.login_root = Tk()
        self.login_root.tk.call('tk', 'scaling', 1.4)
        login_app = Login_window(self.login_root, callback=self.start_dashboard)
        self.login_root.mainloop()

def main():
    """Main entry point"""
    app_manager = AppManager()
    app_manager.show_login()

if __name__ == "__main__":
    main()