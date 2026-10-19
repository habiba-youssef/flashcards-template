from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = 'Arial'

# Change CSV file into dictionary of French word and English translation
new_random_word = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

words_dicts = data.to_dict(orient='records')


def correct_pressed():
    global new_random_word

    words_dicts.remove(new_random_word)
    df = pandas.DataFrame(words_dicts)
    df.to_csv('data/words_to_learn.csv', index=False)
    next_card()

def flip_card():
    global new_random_word
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=new_random_word['English'], fill='white')

def next_card():
    global new_random_word, flip_timer
    window.after_cancel(flip_timer)
    new_random_word = random.choice(words_dicts)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=new_random_word['French'], fill='black')

    flip_timer = window.after(2000, func=flip_card)

window = Tk()
window.title("Quizlet Dupe")
window.config(padx=40, pady=40, background=BACKGROUND_COLOR)

flip_timer = window.after(2000, func=flip_card)

canvas = Canvas(width=800,height=526,highlightthickness=0, background=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card = canvas.create_image(400,263,image=card_front)
canvas.grid(column=1,row=1,columnspan=2)

card_title = canvas.create_text(400,150,text='Title',font=(FONT_NAME,40,'italic'),fill='black')
card_word = canvas.create_text(400,263,text='Word',font=(FONT_NAME,60,'bold'),fill='black')

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=correct_pressed)
correct_button.grid(row=2,column=1)

incorrect_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, command=next_card)
incorrect_button.grid(row=2,column=2)

next_card()

window.mainloop()