#Author: Thaddeus Wireman
#Date written: 7/15/23
#Assignment: Final GUI Project 
#Short Desc: The program is a game called "Mouse Reflex Test" that tests the users' abilities to click
#buttons that are generated randomly around the window. At the end of 30 seconds, the total amount of buttons
#that the user clicked and the average time per button click rounded to 3 decimal points. The "Hard" mode 
#(***************HARD MODE is still UNFINISHED AND IS CURRENTLY JUST A SMALLER TARGET BUTTON******************)
#has the added challenge of bringing the user to a "You Failed!" screen if the user ever clicks on the screen
#without clicking one of the generated buttons.


#necessary package imports
import tkinter as tk
from typing import List
import random
import time

#reset game screen
global scoreLabel
global aveTimeLabel
global resetButton
global zeroScoreLabel

#introduction screen
global userInfoFrame
global userLabel
global usernameEntry
global submitButton
global quitButton
global errorMessageLabel

#game mode choice screen
global levelFrame
global levelLable
global normalButton
global hardButton


#game layout screen
global infoFrame
global usernameLabel
global pointsLabel
global timeLabel
global gameFrame
global targetButton


#specifies where the target button can show up and their size
gameSettings = {'username': "",'difficulty_chosen': "",
    'normal': {'x': 6,'y': 3,'x_axis_max': 1020,'y_axis_max': 565},  
    'hard': {'x': 2,'y': 0,'x_axis_max': 1020,'y_axis_max': 565}}

#introduction screen that requests and requires a username to continue
def introduction():
    global userInfoFrame
    global userLabel
    global usernameEntry
    global submitButton
    global quitButton
    global errorMessageLabel

    #opens the frame and adds the instruction label
    userInfoFrame = tk.Frame(master=window)
    userInfoFrame.pack(fill=tk.BOTH, expand=True)
    userLabel = tk.Label(master=userInfoFrame, text="Please enter a username: ", font=("Calibra", 20), pady=22)
    userLabel.pack()

    #creates the username entry box, submit button, and quit button and places them on the page
    usernameEntry = tk.Entry(master=userInfoFrame, font=("Calibra", 12))
    usernameEntry.pack()

    submitButton = tk.Button(master=userInfoFrame, text="Submit", command=check_entry, font=("Calibra", 12))
    submitButton.pack()

    quitButton = tk.Button(master=userInfoFrame, text="Quit", command=quit_program, font=("Calibra", 12))
    quitButton.pack()

    #error handling message shown if the user does not input a name
    errorMessageLabel = tk.Label(master=userInfoFrame, text="", font=("Calibra", 14), fg="red")
    errorMessageLabel.pack()

    #creates the frame with the instructions for the game and places it
    gameInfoLabel = tk.Label(master=userInfoFrame, font=("Calibra", 13),
        text="The goal of this game is to click on \nthe red square as quickly as possible \nbefore the 30 seconds run out.")
    gameInfoLabel.pack()

#requires that the username box is not empty when the "Submit" button is clicked
def check_entry():
    username = usernameEntry.get()
    if username == "":
        errorMessageLabel.config(text="Please enter a username.")
        return
    difficulty_choice()
    

#gets rid of the introduction frame and brings up the difficulty options
def difficulty_choice():
    global levelFrame
    global levelLable
    global normalButton
    global hardButton
    global quitButton
    global gameSettings
    
    #sets the usernames entry as their name and gets rid of the introduction frame
    gameSettings['username'] = usernameEntry.get()
    userInfoFrame.pack_forget()
    userLabel.pack_forget()
    usernameEntry.pack_forget()
    submitButton.pack_forget()
    quitButton.pack_forget()

    #creates and places the difficulty frame and title label
    levelFrame = tk.Frame(master=window, height=760, width=760, borderwidth=4, relief=tk.RAISED, bg="#3bfffc")
    levelFrame.pack(fill=tk.BOTH)
    levelLable = tk.Label(master=levelFrame, text="Choose a Level:", pady=20, font=("Calibra", 15))
    levelLable.pack()

    #creates the Normal and Hard buttons
    normalButton = tk.Button(master=levelFrame,text="Normal",height=6, width=15,font=("Calibra", 12),
        command=lambda: game_layout(gameSettings['username'], gameSettings['normal']))
    
    hardButton = tk.Button(master=levelFrame,text="Hard",height=6, width=15,font=("Calibra", 12),
        command=lambda: game_layout(gameSettings['username'], gameSettings['hard']))

    #places the buttons
    normalButton.pack(fill=tk.BOTH)
    hardButton.pack(fill=tk.BOTH)
    
    #creates and places the quit mode button
    quitButton = tk.Button(master=levelFrame, text="Quit", height=2, width=8, command=quit_program, font=("Calibra", 12))
    quitButton.pack()

#gets rid of the difficulty choice screen and starts the main game frame
def game_layout(username: str, difficulty: List):
    global infoFrame
    global usernameLabel
    global pointsLabel
    global timeLabel
    global gameFrame
    global targetButton
    global quitButton

    #getting rid of the previous screen
    levelFrame.pack_forget()
    levelLable.pack_forget()
    normalButton.pack_forget()
    hardButton.pack_forget()
    quitButton.pack_forget()

    #display username and points during game
    infoFrame = tk.Frame(master=window, padx=10, pady=5, bg="#81f7f5")
    usernameLabel = tk.Label(master=infoFrame, text="Name: "+ username + "            Score:" ,
        font=("Calibra", 20), bg="#81f7f5")

    pointsLabel = tk.Label(master=infoFrame, text=0, font=("Calibra", 20), bg="#81f7f5")
    timeLabel = tk.Label(master=infoFrame, text=30, font=("Calibra", 25), bg="#81f7f5")
    infoFrame.pack(fill=tk.BOTH, side=tk.TOP)
    usernameLabel.pack(side=tk.LEFT)
    pointsLabel.pack(side=tk.LEFT)
    timeLabel.place(relx = 0.5, rely = 0.5, anchor = 'center')

    #creates and places a quit button
    quitButton = tk.Button(master=infoFrame, text="Quit", command=quit_program, font=("Calibra", 12))
    quitButton.pack(side=tk.RIGHT)

    #creates game frame and the target button
    gameFrame = tk.Frame(master=window, height=660, width=1100, relief=tk.RAISED, borderwidth=2, bg="#ededed")
    targetButton = tk.Button(master=gameFrame,height=difficulty['y'],width=difficulty['x'],
        borderwidth=2,command=lambda: btn_position(difficulty),bg="red")

    #places the game frame and initial target button
    gameFrame.pack()
    targetButton.place(x=400, y=330)

    timer()

#generates and places the buttons at random positions
def btn_position(game_level):
    x_axis = random.randint(0, game_level['x_axis_max'])
    y_axis = random.randint(16, game_level['y_axis_max'])
    pointsLabel['text'] += 1
    targetButton.place(x=x_axis, y=y_axis)

#makes the timer and score counter
def timer():
    global timeLabel
    global targetButton
    global gameFrame
    global pointsLabel
    global scoreLabel
    global aveTimeLabel
    global resetButton
    global quitButton
    global zeroScoreLabel
    #ensures the timer label counts down
    timeLabel['text'] -= 1

    #stops the target buttons from being placed, calculates and displays scores, and places the button to reset the game
    if timeLabel['text'] == 0:
        #removes the target button, quit button, and score label from the info frame
        targetButton.place_forget()
        quitButton.pack_forget()
        timeLabel.place_forget()

        #prevents the program from trying to calculate an average time per target button click when 0 target buttons were pressed
        if pointsLabel['text'] == 0:
            zeroScoreLabel = tk.Label(master=gameFrame, text=f"YOU DIDN'T CLICK ANY TARGETS! \nYour average isn't calculateable.",
                font = ("Calibra", 30), fg="red")
            zeroScoreLabel.pack(expand=True)
            scoreLabel = tk.Label(master=gameFrame, text=f"Your score was: {pointsLabel['text']}", font=("Calibra", 20))
            resetButton = tk.Button(master=gameFrame, text="Reset?", command=reset, font=("Calibra", 12))
            quitButton = tk.Button(master=gameFrame, text="Quit", command=quit_program, font=("Calibra", 12))
            zeroScoreLabel.pack(expand=True)
            scoreLabel.pack(expand=True)
            resetButton.pack(expand=True)
            quitButton.pack(expand=True)

        #calculates the average time per target label, score label, and reset button
        else:
            zeroScoreLabel = tk.Label(master=gameFrame, text=f"", font = ("Calibra", 4), fg="red")
            averageTime = round(30/(float(pointsLabel['text'])), 3)
            aveTimeLabel = tk.Label(master=gameFrame, text=f"Your average time per target was: {averageTime} seconds", font=("Calibra", 15))
            scoreLabel = tk.Label(master=gameFrame, text=f"Your score was: {pointsLabel['text']}", font=("Calibra", 20))
            resetButton = tk.Button(master=gameFrame, text="Reset?", command=reset, font=("Calibra", 12))
            quitButton = tk.Button(master=gameFrame, text="Quit", command=quit_program, font=("Calibra", 12))
        
        

            #places the labels and buttons
            scoreLabel.pack(expand=True)
            aveTimeLabel.pack(expand=True)
            resetButton.pack(expand=True)
            quitButton.pack(expand=True)
            return 0

    #sets the timer to countdown every 1000ms, or 1 second
    timeLabel.after(1000, timer)

#creates the reset function for the "Reset?" button at the end of the game
def reset():
    global scoreLabel
    global resetButton
    global userInfoFrame
    global userLabel
    global usernameEntry
    global submitButton
    global quitButton
    global zeroScoreLabel

    #removes the information from the frame that shows the user's scores
    scoreLabel.pack_forget()
    resetButton.pack_forget()
    infoFrame.pack_forget()
    gameFrame.pack_forget()
    quitButton.pack_forget()
    zeroScoreLabel.pack_forget()

    #resets username field
    usernameEntry.delete(0, tk.END)
    
    #resets score and time values
    pointsLabel['text'] = 0
    timeLabel['text'] = 30
    
    #returns the game to the introduction screen for the user to put in their username
    introduction()

#ensures that the "Quit" buttons in each window frame end the program
def quit_program():
    global quitButton
    
    window.destroy()

#creates the tkinter window
window = tk.Tk()

#titles and sizes the tkinter window
window.title("Mouse Reflex Test")
window.geometry("1100x680")
window.config(bg="#c2c4c4")

#calls the introduction function to place the initial screen
introduction()

#calls the mainloop of Tk
window.mainloop()