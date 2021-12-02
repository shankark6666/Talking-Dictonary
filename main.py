from tkinter import *
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3

engine=pyttsx3.init()


def wordaudio():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(enterwordentry.get())
    engine.runAndWait()


def  meaningaudio():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(textarea.get(1.0,END))
    engine.runAndWait()


def iexit():
    res = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if res == True:
        window.destroy()

    else:
        pass


def clear():
    textarea.config(state=NORMAL)
    enterwordentry.delete(0, END)
    textarea.delete(1.0, END)
    textarea.config(state=DISABLED)

def search():
    data = json.load(open('data.json'))
    word = enterwordentry.get()

    word = word.lower()

    if word in data:
        meaning = data[word]

        textarea.config(state=NORMAL)
        textarea.delete(1.0, END)
        for item in meaning:
            textarea.insert(END, u'\u2022' + item + '\n\n')

        textarea.config(state=DISABLED)

    elif len(get_close_matches(word, data.keys())) > 0:

        close_match = get_close_matches(word, data.keys())[0]

        res = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead?')

        if res == True:

            meaning = data[close_match]
            textarea.delete(1.0, END)
            textarea.config(state=NORMAL)
            for item in meaning:
                textarea.insert(END, u'\u2022' + item + '\n\n')

            textarea.config(state=DISABLED)

        else:
            textarea.delete(1.0, END)
            messagebox.showinfo('Information', 'Please type a correct word')
            enterwordentry.delete(0, END)

    else:
        messagebox.showerror('Error', 'The word doesnt exist.Please double check it.')
        enterwordentry.delete(0, END)




window=Tk()

window.geometry('1000x626+100+50')

window.title('Talking Dictionary')

window.resizable(False, False)


bgimage = PhotoImage(file='b1.png')

bgLabel = Label(window, image=bgimage)
bgLabel.place(x=0, y=0)

enterwordLabel = Label(window, text='Enter Word', font=('castellar', 29, 'bold'), fg='red3', bg='whitesmoke')
enterwordLabel.place(x=530, y=20)
enterwordentry = Entry(window, font=('arial', 23, 'bold'), bd=8, relief=GROOVE, justify=CENTER)
enterwordentry.place(x=510, y=80)

enterwordentry.focus_set()

searchimage = PhotoImage(file='search.png')
searchButton = Button(window, image=searchimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',command=search)
searchButton.place(x=620, y=150)

micimage = PhotoImage(file='mic.png')
micButton = Button(window, image=micimage, bd=0, bg='whitesmoke', activebackground='whitesmoke',
                   cursor='hand2',command=wordaudio)
micButton.place(x=710, y=153)

meaninglabel = Label(window, text='Meaning', font=('castellar', 29, 'bold'), fg='red3', bg='whitesmoke')
meaninglabel.place(x=580, y=240)

textarea = Text(window, font=('arial', 18, 'bold'), height=8, width=34, bd=8, relief=GROOVE, wrap='word')
textarea.place(x=460, y=300)

audioimage = PhotoImage(file='microphone.png')
audioButton = Button(window, image=audioimage, bd=0, bg='whitesmoke', activebackground='whitesmoke',
                     cursor='hand2',command=meaningaudio)
audioButton.place(x=530, y=555)

clearimage = PhotoImage(file='clear.png')
clearButton = Button(window, image=clearimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2'
                     , command=clear)
clearButton.place(x=660, y=555)

exitimage = PhotoImage(file='exit.png')
exitButton = Button(window, image=exitimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                    command=iexit)
exitButton.place(x=790, y=555)

enterwordentry.focus_set()

def enter_function(event):
    searchButton.invoke()

window.bind('<Return>', enter_function)

window.mainloop()
