from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = []

try:
    french_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = french_data.to_dict(orient="records")


def nextcard():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_text1, text="French", fill="black")
    canvas.itemconfig(canvas_text2, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=front_img)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    nextcard()


def flip_card():
    canvas.itemconfig(canvas_text1, text="English", fill="white")
    canvas.itemconfig(canvas_text2, text=current_card["English"], fill="white")
    canvas.itemconfig(card, image=back_img)


window = Tk()
window.title("Flash Cards")
window.minsize(width=500, height=400)
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
card = canvas.create_image((400, 263), image=front_img)
canvas_text1 = canvas.create_text((400, 150), text="", font=("Ariel", 40, "italic"))
canvas_text2 = canvas.create_text((400, 263), text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")

tick_button = Button(image=right_img, highlightthickness=0, command=is_known)
tick_button.config(background=BACKGROUND_COLOR)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=nextcard)
wrong_button.config(background=BACKGROUND_COLOR)
tick_button.grid(row=1, column=0)
wrong_button.grid(row=1, column=1)

nextcard()

window.mainloop()
