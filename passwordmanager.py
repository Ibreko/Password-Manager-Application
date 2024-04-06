import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import pyperclip

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        self.geometry("400x300")

        # Predefined credentials
        self.credentials_file = "credentials.json"
        self.passwords_file = "passwords.json"

        self.credentials = self.load_credentials()
        self.passwords = self.load_passwords()

        # Initialize login screen
        self.login_frame = tk.Frame(self, bg="#D6EAF8")  # Blue background
        self.login_frame.pack(expand=True, fill='both')
        self.create_login_widgets()

        self.logged_in_user = None

    def create_login_widgets(self):
        tk.Label(self.login_frame, text="Username:", bg="#D6EAF8").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", bg="#D6EAF8").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        register_button = ttk.Button(self.login_frame, text="Register", command=self.register)
        register_button.pack(pady=10)

        # Bind Enter key to login action
        self.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.credentials and self.credentials[username] == password:
            self.logged_in_user = username
            self.login_frame.destroy()
            self.create_password_manager_widgets()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = simpledialog.askstring("Register", "Enter new username:")
        if username:
            if username in self.credentials:
                messagebox.showerror("Error", "Username already exists.")
            else:
                password = simpledialog.askstring("Register", "Enter new password:")
                if password:
                    self.credentials[username] = password
                    self.save_credentials()
                    messagebox.showinfo("Success", "Registration successful.")
                else:
                    messagebox.showerror("Error", "Please enter a password.")
        else:
            messagebox.showerror("Error", "Please enter a username.")

    def create_password_manager_widgets(self):
        self.password_manager_frame = tk.Frame(self, bg="#ABEBC6")  # Green background
        self.password_manager_frame.pack(expand=True, fill='both')

        add_button = ttk.Button(self.password_manager_frame, text="Add Password", command=self.add_password)
        add_button.pack(pady=10)

        view_button = ttk.Button(self.password_manager_frame, text="View Passwords", command=self.view_passwords)
        view_button.pack(pady=10)

        delete_button = ttk.Button(self.password_manager_frame, text="Delete Password", command=self.delete_password)
        delete_button.pack(pady=10)

        copy_button = ttk.Button(self.password_manager_frame, text="Copy Password", command=self.copy_password)
        copy_button.pack(pady=10)

        exit_button = ttk.Button(self.password_manager_frame, text="Exit", command=self.exit_app)
        exit_button.pack(pady=10)

        # Bind Enter key to add password action
        self.bind("<Return>", lambda event: self.add_password())

    def add_password(self):
        url = simpledialog.askstring("Add Password", "Enter URL:")
        if url:
            credentials = simpledialog.askstring("Add Password", "Enter login credentials:")
            if credentials:
                self.passwords.setdefault(self.logged_in_user, {})
                self.passwords[self.logged_in_user][url] = credentials
                self.save_passwords()
                messagebox.showinfo("Success", "Password added successfully.")
            else:
                messagebox.showerror("Error", "Please enter login credentials.")
        else:
            messagebox.showerror("Error", "Please enter URL.")

    def view_passwords(self):
        if self.logged_in_user in self.passwords and self.passwords[self.logged_in_user]:
            # Sorting options
            sorted_passwords = sorted(self.passwords[self.logged_in_user].items(), key=lambda x: x[0])  # Sort alphabetically by URL
            passwords_list = "\n".join([f"{url}: {credentials}" for url, credentials in sorted_passwords])
            messagebox.showinfo("Your Passwords", f"Your passwords:\n{passwords_list}")
        else:
            messagebox.showinfo("No Passwords", "No passwords saved for this user.")

    def delete_password(self):
        if self.logged_in_user in self.passwords and self.passwords[self.logged_in_user]:
            password_to_delete = simpledialog.askstring("Delete Password", "Enter URL of password to delete:")
            if password_to_delete in self.passwords[self.logged_in_user]:
                del self.passwords[self.logged_in_user][password_to_delete]
                self.save_passwords()
                messagebox.showinfo("Success", "Password deleted successfully.")
            else:
                messagebox.showerror("Error", "Password not found.")
        else:
            messagebox.showinfo("No Passwords", "No passwords saved for this user.")

    def copy_password(self):
        if self.logged_in_user in self.passwords and self.passwords[self.logged_in_user]:
            password_to_copy = simpledialog.askstring("Copy Password", "Enter URL of password to copy:")
            if password_to_copy in self.passwords[self.logged_in_user]:
                pyperclip.copy(self.passwords[self.logged_in_user][password_to_copy])
                messagebox.showinfo("Success", "Password copied to clipboard.")
            else:
                messagebox.showerror("Error", "Password not found.")
        else:
            messagebox.showinfo("No Passwords", "No passwords saved for this user.")

    def exit_app(self):
        self.destroy()

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def load_passwords(self):
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_credentials(self):
        with open(self.credentials_file, 'w') as file:
            json.dump(self.credentials, file)

    def save_passwords(self):
        with open(self.passwords_file, 'w') as file:
            json.dump(self.passwords, file)

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
