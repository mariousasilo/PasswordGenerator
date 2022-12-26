import pyperclip
import json
import tkinter as tk
from tkinter import END
from tkinter import messagebox

from password_generator import PasswordGenerator

# Create Screen
root = tk.Tk()
root.title("Password Manager")
root.config(pady=50, padx=50)

# Create the canvas for the logo
logo = tk.PhotoImage(file='logo.png')
canvas = tk.Canvas(master=root, height=200, width=190)
canvas.create_image(100, 95, image=logo)
canvas.grid(row=0, column=1)


# Generate Password
def pw_generate():
    my_pw_generator = PasswordGenerator()
    pw = my_pw_generator.generate()
    pyperclip.copy(pw)
    entry_password.delete(0, END)
    entry_password.insert(0, pw)


# Create confirmation pop-up window
def pop_up():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    new_data = {
        website:
            {'email': username,
             'password': password}
    }
    if password == '' or website == '' or username == '':
        tk.messagebox.showerror(title='Oops', message="Please don't leave any fields empty.")
    else:
        try:
            with open(file='password.json') as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            with open(file='password.json', mode='w') as file:
                json.dump(new_data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open(file='password.json', mode='w') as file:
                json.dump(new_data, file, indent=4)
        else:
            with open(file='password.json', mode='w') as file:
                json.dump(data, file, indent=4)
                entry_password.delete(0, END)
                entry_website.delete(0, END)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)


def search():
    with open(file='password.json') as file:
        data = json.load(file)
    try:
        search_website = data[entry_website.get()]
    except KeyError:
        messagebox.showerror(title='Details Not Found', message=f'There is no {entry_website.get()} on file')
    else:
        search_username = search_website['email']
        search_password = search_website['password']
        messagebox.showinfo(title=entry_website.get(), message=f'Email: {search_username}\nPassword: {search_password}')


# Create widgets for buttons, labels and entry
tk.Label(text='Website: ', master=root).grid(row=1, column=0)
tk.Label(text='Email/Username: ', master=root).grid(row=2, column=0)
tk.Label(text='Password: ', master=root).grid(row=3, column=0)

tk.Button(text='Search', master=root, width=14, command=search).grid(row=1, column=2)
tk.Button(text='Generate Password', master=root, command=pw_generate).grid(row=3, column=2)
tk.Button(text='Add', width=42, master=root, command=pop_up).grid(row=4, column=1, columnspan=2, pady=2)

entry_website = tk.Entry(width=30, master=root)
entry_website.grid(row=1, column=1, columnspan=1, sticky='w', pady=2)
entry_website.focus()
entry_username = tk.Entry(width=50, master=root)
entry_username.grid(row=2, column=1, columnspan=2, sticky='w', pady=2)
entry_password = tk.Entry(width=30, master=root)
entry_password.grid(row=3, column=1, sticky='w', pady=2)

root.mainloop()
