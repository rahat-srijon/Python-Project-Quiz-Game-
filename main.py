from tkinter import *
import random
import json

root = Tk()
root.geometry('800x600+200+200')
root.configure(bg='#ffffff')
root.title('IQuiz Game')
root.resizable(FALSE, FALSE)
root.iconbitmap('logo.ico')

qus = open('question.json', "r")
pre_question = json.loads(qus.read())

ans = open('answer.json', "r")
pre_answer = json.loads(ans.read())

opt = open('option.json', "r")
pre_option = json.loads(opt.read())

lead = open('leaderboard.json', "r")
led = json.loads(lead.read())

ranks = ["Rank"]
for i in range(1, 11):
    ranks.append(str(i))

correct_answer = 0
wrong_answer = 0
cur = 0


# background==========================================
def bgcng(n):
    photo = PhotoImage(file=str(n) + ".gif")
    bgimg = Label(root, image=photo)
    bgimg.image = photo
    bgimg.place(x=0, y=0, width=800, height=600)


# background==========================================


# timer===============================================
class Timer:
    def __init__(self, parent):
        self.seconds = 0
        self.label = Label(parent,
                           text="Elapsed 0",
                           font="Arial 30",
                           width=10,
                           bg="#56003c",
                           fg="#00cdff"
                           )
        self.label.pack()
        self.label.after(1000, self.refresh_label)

    def refresh_label(self):
        self.seconds += 1
        self.label.configure(text="Elapsed %i" % self.seconds)
        if self.seconds == 61:
            gameover()
        self.label.after(1000, self.refresh_label)


# timer===============================================


# initializing========================================
iD = []


def shuffl():
    global iD
    for j in range(len(pre_question)):
        iD.append(j)
    iD = random.sample(iD, len(iD))


def initialize():
    bgcng(5)
    shuffl()
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Button(splash,
                   text='Start now!!',
                   command=lambda: timestart(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d4b',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=300, y=300)
    global correct_answer, wrong_answer
    correct_answer = 0
    wrong_answer = 0


def timestart():
    splash = Frame(root, bg='#571d4b')
    splash.place(x=0, y=0, width=800, height=600)
    photo = PhotoImage(file=str(5) + ".gif")
    bgimg = Label(splash, image=photo)
    bgimg.image = photo
    bgimg.place(x=0, y=0, width=800, height=600)
    Timer(splash)
    startgame()


# initializing========================================


# startgame===========================================
def rearrange(n):
    global led
    led['11'] = [n, correct_answer, wrong_answer]
    for k in range(11, 0, -1):
        for j in range(k - 1, 0, -1):
            if led[str(j)][1] < led[str(k)][1]:
                temp = dict()
                temp[str(k)] = led[str(j)]
                temp[str(j)] = led[str(k)]
                led.update(temp)
            elif led[str(j)][1] == led[str(k)][1]:
                if led[str(j)][2] > led[str(k)][2]:
                    temp = dict()
                    temp[str(k)] = led[str(j)]
                    temp[str(j)] = led[str(k)]
                    led.update(temp)
    json.dump(led, open('leaderboard.json', "w"), indent=4)
    startpage()


def leadadd():
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Label(splash,
                  text="Congratulations\nYou made to the top 10",
                  justify=CENTER,
                  bd=0,
                  bg='#571d4b',
                  fg='#60ff7b',
                  font=("Courier", 15, 'bold')
                  )
    itemm.place(x=225, y=100)
    itemm = Label(splash,
                  text="Enter your name ",
                  justify=RIGHT,
                  bd=0,
                  bg='#571d4b',
                  fg='#ff6c6c',
                  font=("Courier", 15, 'bold')
                  )
    itemm.place(x=200, y=200)
    enteredname = StringVar()
    addname = Entry(splash,
                    bg="#d69aff",
                    fg="#a200ff",
                    textvariable=enteredname,
                    bd=0,
                    font=("consolas", 15, 'bold'),
                    width=10
                    )
    addname.place(x=410, y=200)
    itemm = Button(splash,
                   text='Enter',
                   command=lambda: rearrange(enteredname.get()),
                   justify=CENTER,
                   relief=FLAT,
                   bg='#571d5f',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("Courier", 15, 'bold')
                   )
    itemm.place(x=500, y=192)


def nogo():
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Label(splash,
                  text="Sorry you couldn't\nmake it to the top 10. :(\nBetter luck next time. ;(",
                  justify=CENTER,
                  bd=0,
                  bg='#571d4b',
                  fg='#ff6c6c',
                  font=("Courier", 15, 'bold')
                  )
    itemm.place(x=200, y=100)
    itemm = Button(splash,
                   text='Exit',
                   command=lambda: startpage(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d4b',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=200, y=300)
    itemm = Button(splash,
                   text='Try Again',
                   command=lambda: initialize(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d4b',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=300, y=300)


def check():
    print(correct_answer, "and", led['10'][1])
    if correct_answer > led['10'][1]:
        leadadd()
    elif correct_answer == led['10'][1]:
        if wrong_answer < led['10'][2]:
            leadadd()
    else:
        nogo()


def illegal():
    bgcng(5)
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Button(splash,
                   text='Repent',
                   command=lambda: startpage(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d30',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=300, y=300)
    itemm = Label(splash,
                  text="You are too good",
                  justify=CENTER,
                  bd=0,
                  bg='#571d4b',
                  fg='#6cff6c',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=210, y=200)
    itemm = Label(splash,
                  text="to be true",
                  justify=CENTER,
                  bd=0,
                  bg='#571d4b',
                  fg='#ff2020',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=250, y=230)


def gameover():
    bgcng(5)
    shuffl()
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Button(splash,
                   text='Proceed',
                   command=lambda: check(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d4b',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=300, y=300)
    itemm = Label(splash,
                  text="Correct Answers :" + str(correct_answer),
                  bd=0,
                  bg='#571d4b',
                  fg='#6cff6c',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=200, y=200)
    itemm = Label(splash,
                  text="Wrong Answers   :" + str(wrong_answer),
                  bd=0,
                  bg='#571d4b',
                  fg='#ff6c6c',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=200, y=250)


cr = 0


def ok(s, c):
    if s == c:
        global correct_answer
        correct_answer += 1
    else:
        global wrong_answer
        wrong_answer += 1
    global cur, cr
    cr = cr + 1
    cr = cr % len(iD)
    cur = iD[cr]
    cr %= len(iD)
    startgame()


def startgame():
    splash = Frame(root, bg='#571d4b')
    splash.place(x=50, y=50, width=700, height=500)
    if wrong_answer > 25 or correct_answer > 40:
        illegal()
    itemm = Button(splash,
                   text='Give up :(',
                   command=lambda: startpage(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#571d4b',
                   fg='#ff503e',
                   activebackground='#571d4b',
                   activeforeground='#ff0000',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=300, y=462)

    question = pre_question[str(cur)]
    option = pre_option[str(cur)]
    random.shuffle(option)
    correct = pre_answer[str(cur)]

    itemm = Label(splash,
                  text=question,
                  width=44,
                  justify=CENTER,
                  bd=0,
                  bg='#571d4b',
                  fg='#b287c9',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=00, y=100)

    itemm = Label(splash,
                  text=str(correct_answer),
                  bd=0,
                  bg='#571d4b',
                  fg='#6cff6c',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=10, y=0)

    itemm = Label(splash,
                  text=str(wrong_answer),
                  bd=0,
                  bg='#571d4b',
                  fg='#ff6c6c',
                  font=("Courier", 20, 'bold')
                  )
    itemm.place(x=10, y=30)

    opt1 = Button(splash,
                  text=option[0],
                  command=lambda: ok(option[0], correct),
                  width=15,
                  justify=CENTER,
                  relief=FLAT,
                  bg='#900071',
                  fg='#cac3cd',
                  activebackground='#612654',
                  activeforeground='#ff897c',
                  font=("consolas", 15, 'bold'),
                  )
    opt1.place(x=170, y=250)
    opt1 = Button(splash,
                  text=option[1],
                  command=lambda: ok(option[1], correct),
                  width=15,
                  justify=CENTER,
                  relief=FLAT,
                  bg='#900071',
                  fg='#cac3cd',
                  activebackground='#612654',
                  activeforeground='#ff897c',
                  font=("consolas", 15, 'bold'),
                  )
    opt1.place(x=355, y=250)
    opt1 = Button(splash,
                  text=option[2],
                  command=lambda: ok(option[2], correct),
                  width=15,
                  justify=CENTER,
                  relief=FLAT,
                  bg='#900071',
                  fg='#cac3cd',
                  activebackground='#612654',
                  activeforeground='#ff897c',
                  font=("consolas", 15, 'bold'),
                  )
    opt1.place(x=170, y=300)
    opt1 = Button(splash,
                  text=option[3],
                  command=lambda: ok(option[3], correct),
                  width=15,
                  justify=CENTER,
                  relief=FLAT,
                  bg='#900071',
                  fg='#cac3cd',
                  activebackground='#612654',
                  activeforeground='#ff897c',
                  font=("consolas", 15, 'bold'),
                  )
    opt1.place(x=355, y=300)


# startgame===========================================

# endpage=============================================
def exitpage():
    splash = Frame(root, bg='#000000')
    splash.place(x=25, y=25, width=750, height=550)
    itemm = Label(splash,
                  text="Thank",
                  bd=0,
                  bg='#000000',
                  fg='#ffa0ff',
                  justify=CENTER,
                  font=("Arial Black", 110, 'bold')
                  )
    itemm.place(x=0, y=0)
    itemm = Label(splash,
                  text="You",
                  bd=0,
                  bg='#000000',
                  fg='#ffffa0',
                  justify=CENTER,
                  font=("Arial Black", 100, 'bold')
                  )
    itemm.place(x=0, y=170)
    itemm = Label(splash,
                  text="for playing",
                  bd=0,
                  bg='#000000',
                  fg='#a0ffff',
                  justify=CENTER,
                  font=("Arial Black", 60, 'bold')
                  )
    itemm.place(x=100, y=390)
    itemm = Button(splash,
                   text='--\nClick\nto Close\nWindow Now',
                   justify=RIGHT,
                   command=lambda: root.destroy(),
                   relief=FLAT,
                   bg='#000000',
                   fg='#6666ff',
                   activebackground='#000000',
                   activeforeground='#ffeeee',
                   font=("consolas", 20, 'bold')
                   )
    itemm.place(x=580, y=400)


# endpage=============================================

# leaderboard==========================================
def leaderboardpage():
    splash = Frame(root, bg='#000000')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Label(splash,
                  text="Top 10 of all Time",
                  width=50,
                  bg='#009eff',
                  fg='#ffdb58',
                  justify=CENTER,
                  font=("Fixedsys", 30)
                  )
    itemm.pack()
    for m in range(11):
        if m == 0:
            norm = '#d4a4ff'
        elif m == 1:
            norm = '#fbff00'
        elif m == 2:
            norm = '#cccccc'
        elif m == 3:
            norm = '#e5aa70'
        else:
            norm = '#66ccff'
        itemm = Label(splash,
                      text=ranks[m],
                      width=5,
                      bg='#0078b9',
                      fg=norm,
                      justify=RIGHT,
                      font=("Consolas", 20, 'bold')
                      )
        itemm.place(x=0, y=51 + m * 41)
        itemm = Label(splash,
                      text=led[ranks[m]][0],
                      width=17,
                      bg='#00669e',
                      fg=norm,
                      justify=RIGHT,
                      font=("Consolas", 20)
                      )
        itemm.place(x=87, y=51 + m * 41)
        itemm = Label(splash,
                      text=led[ranks[m]][1],
                      width=11,
                      bg='#005583',
                      fg=norm,
                      justify=CENTER,
                      font=("Consolas", 20)
                      )
        itemm.place(x=355, y=51 + m * 41)
        itemm = Label(splash,
                      text=led[ranks[m]][2],
                      width=11,
                      bg='#00466c',
                      fg=norm,
                      justify=CENTER,
                      font=("Consolas", 20)
                      )
        itemm.place(x=532, y=51 + m * 41)
    itemm = Button(splash,
                   text='Mainmenu',
                   command=lambda: startpage(),
                   justify=LEFT,
                   relief=FLAT,
                   bg='#009eff',
                   fg='#bdeaff',
                   activebackground='#009eff',
                   activeforeground='#00466c',
                   font=("consolas", 15, 'bold'),
                   )
    itemm.place(x=600, y=0)


# leaderboard==========================================

# rules===============================================
def rulespage():
    splash = Frame(root, bg='#c1eaf4')
    splash.place(x=50, y=50, width=700, height=500)
    itemm = Label(splash,
                  text="Rules and How to's of the IQuiz game\n\n",
                  bg='#c1eaf4',
                  fg='#5c95ad',
                  justify=CENTER,
                  font=("Baskerville Old Face", 20, 'bold')
                  )
    itemm.pack()
    itemm = Label(splash,
                  text="There will be questions\n"
                       "There will be  choices\n"
                       "You'll have to  click\n"
                       "The correct answer\n"
                       "of 10 Questions\n"
                       "in <=60  seconds\n"
                       "it's all or  nothing\n"
                       "make it in the top 10\n"
                       "to place in leaderboard",
                  bg='#c4f3ff',
                  fg='#89c3cd',
                  justify=CENTER,
                  font=("System", 20,)
                  )
    itemm.pack()
    itemm = Button(splash,
                   text='Top 10?',
                   command=lambda: leaderboardpage(),
                   relief=FLAT,
                   pady=0,
                   bg='#c1eaf4',
                   fg='#006178',
                   activebackground='#c1eaf4',
                   activeforeground='#89c5cd',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=0, y=450)
    itemm = Button(splash,
                   text='Go Back',
                   command=lambda: startpage(),
                   relief=FLAT,
                   bg='#c1eaf4',
                   fg='#006178',
                   activebackground='#c1eaf4',
                   activeforeground='#89c5cd',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=575, y=450)


# rules===============================================

# startpage============================================

def startpage():
    global cr
    cr = 0
    bgcng(6)
    splash = Frame(root, bg='#daf3ff')
    splash.place(x=50, y=50, width=700, height=500)

    itemm = Label(splash,
                  text="Game",
                  pady=0,
                  bd=0,
                  bg='#daf3ff',
                  fg='#4d80e4',
                  justify=RIGHT,
                  font=("Stencil", 80,)
                  )
    itemm.place(x=422, y=400)

    itemm = Label(splash,
                  text="IQuiz",
                  pady=0,
                  bd=0,
                  bg='#daf3ff',
                  fg='#2e279d',
                  justify=RIGHT,
                  font=("Bell MT", 110, 'bold')
                  )
    itemm.place(x=325, y=240)

    itemm = Button(splash,
                   text='      Click to Start',
                   command=lambda: initialize(),
                   relief=FLAT,
                   bg='#4d80e4',
                   fg='#ade5ff',
                   activebackground='#2e279d',
                   activeforeground='#ffffff',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=0, y=0)

    itemm = Button(splash,
                   text='         Leaderboard',
                   command=lambda: leaderboardpage(),
                   relief=FLAT,
                   bg='#4d80e4',
                   fg='#ade5ff',
                   activebackground='#2e279d',
                   activeforeground='#ffffff',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=0, y=70)

    itemm = Button(splash,
                   text='           The Rules',
                   command=lambda: rulespage(),
                   relief=FLAT,
                   bg='#4d80e4',
                   fg='#ade5ff',
                   activebackground='#2e279d',
                   activeforeground='#ffffff',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=0, y=140)

    itemm = Button(splash,
                   text='             Exit it',
                   command=lambda: exitpage(),
                   relief=FLAT,
                   bg='#4d80e4',
                   fg='#ade5ff',
                   activebackground='#2e279d',
                   activeforeground='#ffffff',
                   font=("consolas", 20, 'bold'),
                   )
    itemm.place(x=0, y=210)


# startpage============================================

startpage()
root.mainloop()
