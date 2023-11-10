from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
import string
import os

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():


    password_entry.delete(0, END)


    letters = list(string.ascii_letters)
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']



    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD -------------------------------#

def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Whoopsie 🙈", message="Please make sure all fields are completed.")
    else:

        is_ok = messagebox.askokcancel(title=website, message=f"Details entered: \nEmail: {email}\nPassword: {password} "
                                                      f"\nIs it ok to save?")

        if is_ok:

            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

            desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            desktop_file_path = os.path.join(desktop_path, "data.txt")

            with open(desktop_file_path, "w") as desktop_data_file:
                json.dump(data, desktop_data_file, indent=4)


# ---------------------------- Update Checkmarks ----------------------- #

def update_checkmarks(event):

    entry = event.widget
    checkmark1 = entry_checkmarks[entry]
    checkmark2 = entry_checkmarks[entry]
    if website_entry.get():  # If the entry is not empty
        checkmark1.grid(row=1, column=3)
    if email_entry.get():
        checkmark2.grid(row=2, column=3)
    else:
        checkmark.grid_remove()

# --------------------------- Finding Passwords ----------------------- #


def find_password():

    website = website_entry.get()
    with open("data.json") as data_file:
        data = json.load(data_file)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Oh no", message="Website Not Found.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Tired of forgetting your passwords?🤭")
window.config(padx=75, pady=75)



title_label = Label(text="Coffee and passwords are better when they are strong.", fg="black", font=("Courier", 10,
                                                                                                    "normal"))
title_label.place(x=0, y=-30)


canvas = Canvas(width=215, height=200)
logo_img = PhotoImage(file="locker.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

entry_checkmarks = {}



website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
website_entry.bind("<KeyRelease>", update_checkmarks)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.bind("<KeyRelease>", update_checkmarks)

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)
password_entry.bind("<KeyRelease>", update_checkmarks)


gener_pass_button = Button(text="Generate Password", command=generate_password)
gener_pass_button.grid(row=3, column=3)
add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=5, height=1, command=find_password)
search_button.place(x=315, y=200)



for entry in (website_entry, email_entry, password_entry):
    checkmark = Label(window, text="✓", fg="green", width=1, height=1)
    checkmark.grid_remove()
    entry_checkmarks[entry] = checkmark


window.mainloop()
