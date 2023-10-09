import tkinter
from tkinter import messagebox
from pathlib import Path
import string
import random
import pyperclip
import json

letters = string.ascii_letters
digits = string.digits
symbols = string.punctuation

FONT_NAME = "Courier"
data_file = Path().cwd() / "data.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pwd():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(4, 10)
    nr_digits = random.randint(2, 4)

    pwd_letters = [random.choice(letters) for _ in range(nr_letters)]
    pwd_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    pwd_numbers = [random.choice(digits) for _ in range(nr_digits)]

    password_list = pwd_letters + pwd_symbols + pwd_numbers
    random.shuffle(password_list)
    password = "".join(password_list)

    pwd_input.delete(0, tkinter.END)
    pwd_input.insert(0, password)
    pyperclip.copy(password)


# ----
# Search password
# ----
def search_password():
    website = website_input.get()
    try:
        with open(data_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            data_for_website = data[website]
            email = data_for_website["email"]
            pwd = data_for_website["password"]
            msg = f"""
            Email: {email}
            Password: {pwd}
            """
    except (FileNotFoundError, KeyError):
        messagebox.showinfo(title=website, message=f"No info for {website}")
    else:
        messagebox.showinfo(title=website, message=msg)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    if not data_file.exists():
        data_file.touch()

    website = website_input.get()
    email = username_input.get()
    pwd = pwd_input.get()
    new_data = {
        website: {
            "email": email,
            "password": pwd
        }
    }

    # check empty data
    if website == "" or pwd == "":
        messagebox.showerror(title="Error", message="Some fields are empty")
    else:
        print("Entra a add")
        try:
            with open(data_file, mode="r", encoding="utf-8") as f:
                # Reading old data
                data = json.load(f)
        except FileNotFoundError:
            with open(data_file, mode="w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=4)
        else:
            # update dict
            data.update(new_data)
            with open(data_file, mode="w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        finally:
            # clear content
            website_input.delete(0, tkinter.END)
            pwd_input.delete(0, tkinter.END)


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
logo_image = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Website
website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0)
website_input = tkinter.Entry(width=21)
website_input.grid(row=1, column=1)
# Focus cursor on website
website_input.focus()

# Search
search_btn = tkinter.Button(text="Search", command=search_password, width=13)
search_btn.grid(row=1, column=2)

# Email/username
username_label = tkinter.Label(text="Email/Username:")
username_label.grid(row=2, column=0)

username_input = tkinter.Entry(width=35)
# Insert in the last character
username_input.insert(tkinter.END, "andresf.mesad@gmail")
username_input.grid(row=2, column=1, columnspan=2)

# Password
pwd_label = tkinter.Label(text="Password:")
pwd_label.grid(row=3, column=0)

gen_pwd_btn = tkinter.Button(text="Generate password", command=gen_pwd)
gen_pwd_btn.grid(row=3, column=2)

pwd_input = tkinter.Entry(width=21, font=FONT_NAME)
pwd_input.grid(row=3, column=1)

# Add password
add_pwd = tkinter.Button(text="Add password", width=36, command=save)
add_pwd.grid(row=4, column=1, columnspan=2)

window.mainloop()
