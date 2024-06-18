import tkinter as tk
from tkinter import messagebox, ttk
import random
from datetime import datetime

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")

        self.users = {}
        self.timesheet = {}

        # Create Tabs
        self.tab_control = ttk.Notebook(root)
        self.user_tab = ttk.Frame(self.tab_control)
        self.timesheet_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.user_tab, text='User Management')
        self.tab_control.add(self.timesheet_tab, text='Timesheet')
        self.tab_control.pack(expand=1, fill="both")

        # User Management Tab
        self.user_frame = ttk.LabelFrame(self.user_tab, text='User Management')
        self.user_frame.pack(fill="both", expand="yes", padx=20, pady=20)

        ttk.Label(self.user_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.user_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_user_button = ttk.Button(self.user_frame, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=0, column=2, padx=10, pady=10)

        self.del_user_button = ttk.Button(self.user_frame, text="Delete User", command=self.del_user)
        self.del_user_button.grid(row=0, column=3, padx=10, pady=10)

        self.user_listbox = tk.Listbox(self.user_frame)
        self.user_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        # Timesheet Tab
        self.timesheet_frame = ttk.LabelFrame(self.timesheet_tab, text='Timesheet')
        self.timesheet_frame.pack(fill="both", expand="yes", padx=20, pady=20)

        ttk.Label(self.timesheet_frame, text="User:").grid(row=0, column=0, padx=10, pady=10)
        self.user_timesheet_entry = ttk.Entry(self.timesheet_frame)
        self.user_timesheet_entry.grid(row=0, column=1, padx=10, pady=10)

        self.signin_button = ttk.Button(self.timesheet_frame, text="Sign In", command=self.sign_in)
        self.signin_button.grid(row=0, column=2, padx=10, pady=10)

        self.signout_button = ttk.Button(self.timesheet_frame, text="Sign Out", command=self.sign_out)
        self.signout_button.grid(row=0, column=3, padx=10, pady=10)

        self.timesheet_listbox = tk.Listbox(self.timesheet_frame)
        self.timesheet_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="we")

    def generate_pin(self):
        return str(random.randint(1000, 9999))

    def add_user(self):
        name = self.name_entry.get()
        if name:
            if name in self.users:
                messagebox.showerror("Error", "User already exists!")
            else:
                pin = self.generate_pin()
                self.users[name] = pin
                self.user_listbox.insert(tk.END, f"{name} (PIN: {pin})")
                self.timesheet[name] = {"sign_in": None, "sign_out": None}
                messagebox.showinfo("Success", f"User '{name}' added with PIN: {pin}")
                self.name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Name cannot be empty!")

    def del_user(self):
        selected_user = self.user_listbox.curselection()
        if selected_user:
            user_info = self.user_listbox.get(selected_user)
            name = user_info.split(" (")[0]
            del self.users[name]
            del self.timesheet[name]
            self.user_listbox.delete(selected_user)
            messagebox.showinfo("Success", f"User '{name}' deleted")
        else:
            messagebox.showerror("Error", "No user selected!")

    def sign_in(self):
        name = self.user_timesheet_entry.get()
        if name in self.users:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.timesheet[name]["sign_in"] = current_time
            self.update_timesheet_listbox()
            messagebox.showinfo("Success", f"User '{name}' signed in at {current_time}")
            self.user_timesheet_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "User does not exist!")

    def sign_out(self):
        name = self.user_timesheet_entry.get()
        if name in self.users:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.timesheet[name]["sign_out"] = current_time
            self.update_timesheet_listbox()
            messagebox.showinfo("Success", f"User '{name}' signed out at {current_time}")
            self.user_timesheet_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "User does not exist!")

    def update_timesheet_listbox(self):
        self.timesheet_listbox.delete(0, tk.END)
        for user, times in self.timesheet.items():
            signin = times["sign_in"] if times["sign_in"] else "Not signed in"
            signout = times["sign_out"] if times["sign_out"] else "Not signed out"
            self.timesheet_listbox.insert(tk.END, f"{user} - Sign In: {signin}, Sign Out: {signout}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()