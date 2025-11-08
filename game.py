import tkinter as tk
from tkinter import messagebox
import json
import random

class GuessTheNumberGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess the Number Game")
        self.geometry("400x400")
        self.user_data_file = "user_data.json"
        self.current_user = None
        self.show_signup_form()

    def show_signup_form(self):
        self.clear_widgets()
        self.signup_frame = tk.Frame(self)
        self.signup_frame.pack(pady=20)

        tk.Label(self.signup_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.signup_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.signup_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.signup_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.signup_frame, text="Password").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.signup_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.signup_frame, text="Confirm Password").grid(row=3, column=0, padx=5, pady=5)
        self.confirm_password_entry = tk.Entry(self.signup_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=5, pady=5)

        signup_button = tk.Button(self.signup_frame, text="Sign Up", command=self.signup)
        signup_button.grid(row=4, columnspan=2, pady=10)

        login_label = tk.Label(self.signup_frame, text="Already have an account? Log In", fg="blue", cursor="hand2")
        login_label.grid(row=5, columnspan=2)
        login_label.bind("<Button-1>", lambda e: self.show_login_form())

    def show_login_form(self):
        self.clear_widgets()
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Email").grid(row=0, column=0, padx=5, pady=5)
        self.login_email_entry = tk.Entry(self.login_frame)
        self.login_email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(self.login_frame, text="Log In", command=self.login)
        login_button.grid(row=2, columnspan=2, pady=10)

        signup_label = tk.Label(self.login_frame, text="Don't have an account? Sign Up", fg="blue", cursor="hand2")
        signup_label.grid(row=3, columnspan=2)
        signup_label.bind("<Button-1>", lambda e: self.show_signup_form())

    def signup(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([name, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        users = self.load_user_data()
        if email in users:
            messagebox.showerror("Error", "User with this email already exists.")
            return

        users[email] = {"name": name, "password": password}
        self.save_user_data(users)
        self.current_user = email
        self.start_game()

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if not all([email, password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        users = self.load_user_data()
        if email not in users or users[email]["password"] != password:
            messagebox.showerror("Error", "Invalid email or password.")
            return

        self.current_user = email
        self.start_game()

    def start_game(self):
        self.clear_widgets()
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(pady=20)

        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        users = self.load_user_data()
        user_name = users[self.current_user]["name"]

        tk.Label(self.game_frame, text=f"Welcome, {user_name}!").pack()
        tk.Label(self.game_frame, text="I have selected a number between 1 and 100.").pack()
        tk.Label(self.game_frame, text="Guess the number:").pack()

        self.guess_entry = tk.Entry(self.game_frame)
        self.guess_entry.pack(pady=5)

        guess_button = tk.Button(self.game_frame, text="Guess", command=self.check_guess)
        guess_button.pack()

        self.result_label = tk.Label(self.game_frame, text="")
        self.result_label.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.secret_number:
                self.result_label.config(text="Too low! Try again.")
            elif guess > self.secret_number:
                self.result_label.config(text="Too high! Try again.")
            else:
                messagebox.showinfo("Congratulations!", f"You guessed the number in {self.attempts} attempts.")
                self.start_game()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def load_user_data(self):
        try:
            with open(self.user_data_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_user_data(self, users):
        with open(self.user_data_file, "w") as f:
            json.dump(users, f, indent=4)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = GuessTheNumberGame()
    app.mainloop()
