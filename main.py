from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_input.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(0, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_letters = [random.choice(letters) for _ in range(nr_letters)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_input.get()
    email = email_input.get()
    new_password = password_input.get()
    new_data = {website: {
        "email": email,
        "password": new_password
    }}

    if len(website) == 0 or len(new_password) == 0:
        messagebox.showinfo(title="Fields left empty", message="Hey! you have left some fields empty"
                                                               " Please fill up those fields")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered \n"
                                                              f"Website: {website} \n Email: {email} \n Password: {new_password} "
                                                              f"\n Is it okay to save?")

        if is_ok:
            try:
                with open(file="data.json", mode="r") as data_file:
                    # Reading old data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open(file="data.json", mode="w") as data_file:
                    # saving the updated data
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new one
                data.update(new_data)
                with open(file="data.json", mode="w") as data_file:
                    # saving the updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# -------------------------------- Search File for password -----------------------

def find_password():
    website = website_input.get()

    try:
        with open(file="data.json", mode="r") as data_file:
            # Reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="File not present", message="No file found")

    else:
        if website in data:
            password = data[website]["password"]
            email = data[website]["email"]
            messagebox.showinfo(title="File found", message=f"Email : {email}\n"
                                                            f"Password : {password}")
        else:
            messagebox.showinfo(title=f"No data found", message=f"No details for the {website} found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

# displaying the photo in the canvas
canvas = Canvas(height=200, width=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0)

# website label

website_label = Label(text="Website: ")
# website_label.config(padx=10)
website_label.grid(column=0, row=1)

# Email/Username label

user_credentials = Label(text="Email/Username: ")
user_credentials.grid(column=0, row=3)

# Password label

password = Label(text="Password: ")
password.grid(column=0, row=4)

# input box beside website

website_input = Entry(width=35)
website_input.grid(column=1, row=1, columnspan=1)
website_input.focus()

# long input box 2

email_input = Entry(width=35)
email_input.insert(0, "rajmihir945@gmail.com")
email_input.grid(column=1, row=3, columnspan=2)

# password input box

password_input = Entry(width=35)
password_input.grid(column=1, row=4)

# search Button

search_button = Button(text="Search", width=30, command=find_password)
search_button.grid(column=1, row=2)

# generate password button

generate = Button(text="Generate Password", width=30, command=generate_password)
generate.grid(column=1, row=5)
# generate.config(padx=0)

# Add password button

add = Button(text="Add", width=30, command=save_password)
add.grid(column=1, row=6, columnspan=2)

window.mainloop()
