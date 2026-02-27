
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import numpy as np
import sqlite3
import hashlib
from datetime import datetime

def initialize_db():
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL)''')
  conn.commit()
  conn.close()

def register_user(username, password):
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  try:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    messagebox.showinfo("Success", "Registration successful")
  except sqlite3.IntegrityError:
    messagebox.showerror("Error", "Username already exists")
  conn.close()

def login_user(username, password):
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('SELECT password FROM users WHERE username = ?', (username,))
  result = c.fetchone()
  conn.close()

  if result:
    stored_password = result[0]
    if stored_password == hashlib.sha256(password.encode()).hexdigest():
      messagebox.showinfo("Success", "Login successful")
      show_dashboard(username)
    else:
      messagebox.showerror("Error", "Incorrect password")
  else:
    messagebox.showerror("Error", "Username not found")

def show_register_form():
  clear_window()

  register_frame = tk.Frame(root, bg="#ffffff")
  register_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

  tk.Label(register_frame, text="Register", font=("Arial", 24, "bold"), bg="#ffffff", fg="black").pack(pady=20)

  username_label = tk.Label(register_frame, text="Username:", font=("Arial", 14), bg="#ffffff", fg="black")
  username_label.pack()
  username_entry = tk.Entry(register_frame, font=("Arial", 14))
  username_entry.pack(pady=5)

  password_label = tk.Label(register_frame, text="Password:", font=("Arial", 14), bg="#ffffff", fg="black")
  password_label.pack()
  password_entry = tk.Entry(register_frame, show="*", font=("Arial", 14))
  password_entry.pack(pady=5)

  register_button = tk.Button(register_frame, text="Register", font=("Arial", 14), command=lambda: register_user(username_entry.get(), password_entry.get()), bg="#4CAF50", fg="black")
  register_button.pack(pady=20)

  back_button = tk.Button(register_frame, text="Back to Login", font=("Arial", 12), command=show_login_form, bg="#f44336", fg="black")
  back_button.pack(pady=10)

def show_login_form():
  clear_window()

  login_frame = tk.Frame(root, bg="#ffffff")
  login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.5)

  tk.Label(login_frame, text="Login", font=("Arial", 24, "bold"), bg="#ffffff", fg="black").pack(pady=20)

  username_label = tk.Label(login_frame, text="Username:", font=("Arial", 14), bg="#ffffff", fg="black")
  username_label.pack()
  username_entry = tk.Entry(login_frame, font=("Arial", 14))
  username_entry.pack(pady=5)

  password_label = tk.Label(login_frame, text="Password:", font=("Arial", 14), bg="#ffffff", fg="black")
  password_label.pack()
  password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14))
  password_entry.pack(pady=5)

  login_button = tk.Button(login_frame, text="Login", font=("Arial", 14), command=lambda: login_user(username_entry.get(), password_entry.get()), bg="#4CAF50", fg="black")
  login_button.pack(pady=20)

  register_button = tk.Button(login_frame, text="Register", font=("Arial", 12), command=show_register_form, bg="#2196F3", fg="black")
  register_button.pack(pady=10)

def show_dashboard(username):
  clear_window()

  dashboard_frame = tk.Frame(root, bg="#ffffff")
  dashboard_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

  tk.Label(dashboard_frame, text=f"Welcome, {username}!", font=("Arial", 24, "bold"), bg="#ffffff", fg="black").pack(pady=20)

  category_label = tk.Label(dashboard_frame, text="Select Category:", font=("Arial", 14), bg="#ffffff", fg="black")
  category_label.pack()
  category_options = ["electricity_price", "natural_gas_price", "oil_price", "biomass_price", "hydrogen_price", "synthetic_fuels", "hard_coal_price", "lignite_price"]
  category_var = tk.StringVar(root)
  category_dropdown = ttk.Combobox(dashboard_frame, textvariable=category_var, values=category_options, state="readonly", width=30)
  category_dropdown.pack(pady=5)

  date_label = tk.Label(dashboard_frame, text="Date Range:", font=("Arial", 14), bg="#ffffff", fg="black")
  date_label.pack()
  start_date_label = tk.Label(dashboard_frame, text="Start Date:", font=("Arial", 12), bg="#ffffff", fg="black")
  start_date_label.pack()
  start_date_entry = DateEntry(dashboard_frame, font=("Arial", 12), date_pattern="dd/mm/yyyy", mindate=datetime(2023, 1, 1), maxdate=datetime(2023, 12, 31))
  start_date_entry.pack(pady=5)
  end_date_label = tk.Label(dashboard_frame, text="End Date:", font=("Arial", 12), bg="#ffffff", fg="black")
  end_date_label.pack()
  end_date_entry = DateEntry(dashboard_frame, font=("Arial", 12), date_pattern="dd/mm/yyyy", mindate=datetime(2023, 1, 1), maxdate=datetime(2023, 12, 31))
  end_date_entry.pack(pady=5)

  time_label = tk.Label(dashboard_frame, text="Select Time:", font=("Arial", 14), bg="#ffffff", fg="black")
  time_label.pack()

  time_frame = tk.Frame(dashboard_frame, bg="#ffffff")
  time_frame.pack(pady=5)

  hour_options = [str(i) for i in range(1, 25)]
  hour_var = tk.StringVar(root)
  hour_dropdown = ttk.Combobox(time_frame, textvariable=hour_var, values=hour_options, state="readonly", width=5)


  hour_dropdown.pack(side=tk.LEFT, padx=5)
  hour_label = tk.Label(time_frame, text="Hour", font=("Arial", 12), bg="#ffffff", fg="black")
  hour_label.pack(side=tk.LEFT)

  algorithm_label = tk.Label(dashboard_frame, text="Select Algorithm:", font=("Arial", 14), bg="#ffffff", fg="black")
  algorithm_label.pack()
  algorithm_options = ["KMeans", "DBSCAN", "Agglomerative"]
  algorithm_var = tk.StringVar(root)
  algorithm_dropdown = ttk.Combobox(dashboard_frame, textvariable=algorithm_var, values=algorithm_options, state="readonly", width=30)
  algorithm_dropdown.pack(pady=5)

  submit_button = tk.Button(dashboard_frame, text="Submit", font=("Arial", 14), command=lambda: perform_clustering(username, category_var.get(), start_date_entry.get(), end_date_entry.get(), hour_var.get(), algorithm_var.get()), bg="#4CAF50", fg="black")
  submit_button.pack(pady=20)

def perform_clustering(username, category, start_date, end_date, time, algorithm):
  data = pd.read_csv('data.csv')

  start_date = datetime.strptime(start_date, "%d/%m/%Y")
  end_date = datetime.strptime(end_date, "%d/%m/%Y")
  data['Date'] = pd.to_datetime(data['Date'], format="%d/%m/%y")


def clear_window():
  for widget in root.winfo_children():
    widget.destroy()

root = tk.Tk()
root.title("App Clustering System")
root.geometry("800x600")
initialize_db()
show_login_form()
root.mainloop()
