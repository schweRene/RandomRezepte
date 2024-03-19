import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random

import pyglet

bg_colour = "#3d6466"

pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT title, primary_key FROM recipes;")
    titles = cursor.fetchall()

    idx = random.randint(0, len(titles)-1)

    #fetch records from table
    recipe_name = titles[idx][0]
    cursor.execute("SELECT name, qty, unit FROM ingredients WHERE recipe_key=:k;", {"k": idx})
    table_records = cursor.fetchall()

    connection.close()

    return recipe_name, table_records


def pre_process(recipe_name, table_records):
    title = recipe_name

    ingredients = []

    #ingredients
    for i in table_records:
        name = i[0]
        unit = i[2]
        if type(i[1]) == float:
            qty = int(i[1])
        else:
            qty = i[1]

        if qty == None:
            ingredients.append(name)
        elif unit == None:
            ingredients.append(str(qty) + " " + name)
        else:
            ingredients.append(str(qty) + " " + str(unit) + " of" + name)


    return title, ingredients



def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # frame1 widgets
    logo_img = ImageTk.PhotoImage(file="assets/recipe.jpg")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(frame1, text="Ready for your random recipe?", bg=bg_colour, fg="white", font=("Shanti", 14)).pack()

    # button widget
    tk.Button(frame1, text="SHUFFLE", font=("Ubuntu", 20), bg="#28393a", fg="white", cursor="hand2",
              activebackground="#badee2",
              activeforeground="black", command=lambda: load_frame2()).pack(pady=20)

def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()

    recipe_name, table_records = fetch_db()
    print("Recipe Name:", recipe_name)  # Debugging output
    print("Table Records:", table_records)  # Debugging output

    title, ingredients = pre_process(recipe_name, table_records)
    print("Title:", title)  # Debugging output
    print("Ingredients:", ingredients)  # Debugging output

    logo_img = ImageTk.PhotoImage(file="assets/recipe.jpg")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    tk.Label(frame2, text=title, bg=bg_colour, fg="white", font=("Ubuntu", 20), wraplength=800).pack(pady=25, padx=25)



    for i in ingredients:
        tk.Label(frame2, text=i, bg="#28393a", fg="white", font=("Shanti", 12)).pack(fill="both", padx=25)

    tk.Button(frame2, text="BACK", font=("Ubuntu", 18), bg="#28393a", fg="white", cursor="hand2",
              activebackground="#badee2",
              activeforeground="black", command=lambda: load_frame1()).pack(pady=20)


#initialize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")


#x = root.winfo_screenmmwidth() // 2
#y = int(root.winfo_screenheight() * 0.1)
#root.geometry('500x600+' + str(x) + '+' + str(y))

#create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
frame2 = tk.Frame(root, bg=bg_colour)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

load_frame1()

# run app
root.mainloop()