# Sounds taken from https://freesound.org

#IMPORTS
from tkinter import *
from datetime import datetime
from random import randint
import threading
import winsound
import math
import time

#Time taken now so we can see how long the player took when the game is finished
start = datetime.now()

# Few booleans and variables set up for later use in function
bosstoggle = False
paused = False
canpurchase = False
finished = False
purchaseprice = 10

#BOSSKEY FUNCTION
# If a key is pressed...
def keyGet(event):
      # If the key is "b"...
      if event.char == "b":
            global bosstoggle
            global bosswindow
            global bosstab
            # Toggle the boss boolean
            bosstoggle = not bosstoggle
            # If the boss boolean is True...
            if bosstoggle:
                  # Create a window ontop of the game which obscures it and imitates an excel window
                  bosstab = Toplevel()
                  # Make the window 720p
                  bosstab.minsize(1280, 720)
                  bosstab.maxsize(1280, 720)
                  bosswindow = Canvas(bosstab, height=1280, width=720)
                  bosswindow.pack(expand=YES, fill=BOTH)
                  bosswindow.create_image(0, 0, image=bossimage, anchor=NW)
            # Otherwise, close that window
            else:
                  bosstab.destroy()

#PAUSING FUNCTION
def pauser():
      global paused
      # Toggle the pause boolean
      paused = not paused
      # If the pause boolean is True...
      if paused == True:
            # Make the pause button reflect this
            pausetext.set("UNPAUSE GAME")
            pausebutton.configure(fg="red")
            time.sleep(1.5)
      # Otherwise, return the pause button to normal, and resume the autoCoin function
      else:
            pausetext.set("PAUSE GAME")
            pausebutton.configure(fg="black")
            miner.autoCoin()

#PLAYER CLASS
class Miner():
      # Set up inital variable and booleans for use later
      def __init__(self):
            self.coins = 0
            self.clickvalue = 1
            self.autoamount = 1
            self.autospeed = 5
            self.cheatused = False
            #UPGRADE PRICES
            self.clickprice = 10
            self.minervalueprice = 15
            self.minerspeedprice = 20
            self.gamblingprice = 10
      # If the "Mine Coins" button is pressed, add the current "clickvalue" value to the player's coins
      def addCoin(self):
            if not paused:
                  self.coins += self.clickvalue
                  self.displayCoin()
      # This function adds a number of coins automatically over time
      def autoCoin(self):
            global timer
            global paused
            # Set up a timer in the background
            timer = threading.Timer(self.autospeed, miner.autoCoin)
            # Stop the timer when paused
            if paused:
                  timer.cancel()
            # Otherwise, add the "autoamount" of coins every "autospeed" seconds
            if not paused:
                  timer.start()
                  self.coins += self.autoamount
                  self.displayCoin()
      # If the player presses the "Check Cheat" button
      def checkCheat(self):
            # If the game isn't paused...
            if not paused:
                  # If a cheat hasn't already been used...
                  if not self.cheatused:
                        # If the cheatcode entered was correct...
                        cheat = cheatcode.get()
                        if cheat == "CASHCASHMONEY":
                              # Add and display the added 990 coins and indicate that the cheat has been used
                              self.coins += 990
                              self.displayCoin()
                              print("That cheat has added 990 coins to your balance.")
                              self.cheatused = True
                  # Otherwise tell the user their cheat has been used before
                  else:
                        print("Cheat has already been used!")
      # This function handles all bets the player can make
      def beteffect(self):
            if not paused:
                  global currentmult
                  win = True
                  # Random number is chosen to decide if the player wins their bet
                  randomchoice = randint(0, 100)
                  if randomchoice <= wager.get():
                        win = True
                  else:
                        win = False
                  # If the player wins the bet...
                  if win == True:
                        # Add the coins, print their win and play the success sound
                        self.coins -= betprice.get()
                        addition = math.floor(betprice.get() * currentmult)
                        self.coins += addition
                        print("You won the bet!")
                        print("Your " + str(betprice.get()) + " betted coins are now worth " + str(addition) + " coins.")
                        winsound.PlaySound("sounds/win.wav", winsound.SND_FILENAME)
                  # Otherwise...
                  else:
                        # Remove coins from the player's balance, print their loss and play the fail sound
                        self.coins -= betprice.get()
                        print("You lost the bet.")
                        print("We've taken " + str(betprice.get()) + " coins from your current balance.")
                        winsound.PlaySound("sounds/loss.wav", winsound.SND_FILENAME)
                  # Display the player's coins
                  self.displayCoin()
      # These functions handle the player's upgrades
      # Click upgrades multiply its value by 1.5
      def clickvalueup(self):
            self.coins -= self.clickprice
            self.clickprice = math.ceil(self.clickprice * 1.5)
            self.clickvalue = math.ceil(self.clickvalue * 1.5)
      # Miner upgrades multiply their value by 1.8
      def minervalueup(self):
            self.coins -= self.minervalueprice
            self.minervalueprice = math.ceil(self.minervalueprice * 1.8)
            self.autoamount = math.ceil(self.autoamount * 1.8)
            autotext.set("You are earning " + str(round((miner.autoamount / miner.autospeed), 2)) + " coin(s) a second.")
      # Miner speed upgrades multiply the speed by 0.85
      def minerspeedup(self):
            self.coins -= self.minerspeedprice
            self.minerspeedprice = math.ceil(self.minerspeedprice * 1.8)
            self.autospeed = self.autospeed * 0.85
            autotext.set("You are earning " + str(round((miner.autoamount / miner.autospeed), 2)) + " coin(s) a second.")
      # Gambling multiplier upgrades increase the maximum multiplier by 0.5
      def gamblingmultiplierup(self):
            global multiplier
            self.coins -= self.gamblingprice
            self.gamblingprice = int(self.gamblingprice * 2)
            multiplier += 0.5
            wagercalc(wager.get())
      def displayCoin(self):
            #BETTING
            global betprice
            betprice.configure(to=self.coins)
            #DISPLAY
            stats.delete("all")
            stats.create_text(52, 50, font = "Impact 30", text=(str(self.coins)))
            stats.pack()
            #UPGRADES
            optionChanger(uptypevariable.get())
            #ENDGAME
            global finished
            # If the player reaches 1000 coins...
            if self.coins >= 1000:
                  # The game is finished
                  finished = True
                  # The time taken to finish is calculated
                  end = datetime.now()
                  timetaken = end - start
                  totalseconds = timetaken.seconds
                  hourstaken = math.floor(totalseconds / 3600)
                  minandsec = totalseconds - (hourstaken * 3600)
                  minutestaken = math.floor(minandsec / 60)
                  secondstaken = minandsec - (minutestaken * 60)
                  secondstaken = int(secondstaken)
                  # Tkinter window is closed
                  window.destroy()
                  # Win sound is played and results are printed
                  print("YOU WIN!")
                  print("You finally accumulated 1,000 bitcoins! Now you can retire / pay off that student loan.")
                  print("This took you " + str(hourstaken) + " hours, " + str(minutestaken) + " minutes and " + str(secondstaken) + " seconds.")
                  winsound.PlaySound("sounds/end.wav", winsound.SND_FILENAME)
                  # Player's name and results are saved to a text file called "results.txt"
                  question = input("Enter Y if you want to save your result, or N if you don't: ")
                  if question == ("Y"):
                        name = input("Enter your first name: ")
                        if name != (""):
                              with open("results.txt", "a") as result:
                                    result.write((str(name) + " earned a time of "+ str(round(totalseconds, 2)) + " seconds.\n"))

# Instance of Miner class is created as "miner"                  
miner = Miner()

# This function updates the betting label to reflect the current state of the player's proposed bet
def wagercalc(val):
      global bettext
      global multiplier
      global currentmult
      currentmult =  round((((1 - (wager.get() / 100)) * (multiplier - 1)) + 1), 2)
      bettext.set("You can bet " + str(betprice.get()) + " bitcoins and take the odds of " + str(wager.get()) + "% for a " + str(currentmult) + "x multiplier.")

# This function changes the label next to the upgrades depending on the currently selected upgrade
# It also changes the purchase button to reflect whether or not the upgrade can be bought
def optionChanger(val):
      global purchaseprice
      global canpurchase
      if val == "Click Value Increase":
            purchaseprice = miner.clickprice
            upinfo.set("This ups the coins earnt by clicking to " + str(math.ceil(miner.clickvalue * 1.5)) + ".")
      elif val == "Auto-Miner Value":
            purchaseprice = miner.minervalueprice
            upinfo.set("This ups the coins earnt by your mining script to " + str(math.ceil(miner.autoamount * 1.8)) + " per block.")
      elif val == "Auto-Miner Speed":
            purchaseprice = miner.minerspeedprice
            upinfo.set("This ups the speed of your auto-miner to " + str(round((miner.autoamount / (miner.autospeed * 0.8)), 2)) + " blocks per second.")
      elif val == "Gambling Multiplier":
            purchaseprice = miner.gamblingprice
            upinfo.set("This ups the maximum gambling multiplier to " + str(multiplier + 0.5) + ".")
      if miner.coins >= purchaseprice:
            canpurchase = True
            purchasebutton.configure(state = NORMAL, relief=RAISED)
            warning.set("This upgrade costs " + str(purchaseprice) + " coins so you can afford it.")
            warninglabel.configure(fg="green")
      else:
            canpurchase = False
            purchasebutton.configure(state = DISABLED, relief=SUNKEN)
            warning.set("This upgrade costs " + str(purchaseprice) + " coins so you can't afford it.")
            warninglabel.configure(fg="red")

# When the buy upgrade button is pressed, the corresponding function is called depending on the current selected upgrade
def buyselector():
      global uptype
      if uptypevariable.get() == "Click Value Increase":
            miner.clickvalueup()
      elif uptypevariable.get() == "Auto-Miner Value":
            miner.minervalueup()
      elif uptypevariable.get() == "Auto-Miner Speed":
            miner.minerspeedup()
      elif uptypevariable.get() == "Gambling Multiplier":
            miner.gamblingmultiplierup()
      miner.displayCoin()
            
# Screen is set as windowed and the resolution is set to 550 x 445.
# Screen height and width are locked
window = Tk()
window.title("Bitcoin Boss")
window.geometry("550x445")
window.minsize(550, 445)
window.maxsize(550, 445)

#FRAMES
# This is where the frames of the GUI are setup
# Some frames are kept inside each other to divide the whole display into three rows
topframe = Frame(window)
topframe.pack(side=TOP, expand=True, fill="both")

bitcoinframe = LabelFrame(topframe, text="Main Interface")
bitcoinframe.pack(side=LEFT, expand=True, fill="both")

rulesframe = LabelFrame(topframe, text="Instructions")
rulesframe.pack(side=RIGHT, expand=True, fill="both")

middleframe = LabelFrame(window, text="Upgrades")
middleframe.pack(expand=True, fill="both")

upgradeframe = Frame(middleframe)
upgradeframe.pack(side=LEFT, expand=True, fill="both")

selectframe = LabelFrame(middleframe, text="Shop")
selectframe.pack(side=RIGHT, expand=True, fill="both")

bottomframe = Frame(window)
bottomframe.pack(side=BOTTOM, expand=True, fill="both")

gamblingframe = LabelFrame(bottomframe, text="Gambling")
gamblingframe.pack(side=LEFT, expand=True, fill="x")

cheatframe = LabelFrame(bottomframe, text="Cheats")
cheatframe.pack(side=RIGHT, expand=True, fill="x")

#RULES
# Rules are written and packed to display in top right of screen
rules = Label(rulesframe, text="Welcome to Bitcoin Boss!")
rules2 = Label(rulesframe, text="Click the 'Mine Bitcoin' button to get mining.")
rules3 = Label(rulesframe, text="You can select upgrades to buy in the shop.")
rules4 = Label(rulesframe, text="You can also gamble or enter a cheatcode.")
rules5 = Label(rulesframe, text="To win you must earn a thousand bitcoin!")
rules6 = Label(rulesframe, text="(By the way, the boss key is 'B')")
rules.pack()
rules2.pack()
rules3.pack()
rules4.pack()
rules5.pack()
rules6.pack()

#BITCOIN
# Coin counter display is created
stats = Canvas(bitcoinframe, height=100, width=100)
stats.create_text(52, 50, font = "Impact 30", text=(str(miner.coins)))
stats.pack(side=RIGHT)

# "Mine Bitcoin" button is created
bitcoinbutton = Button(bitcoinframe, text = "Mine Bitcoin", command = miner.addCoin)
bitcoinbutton.pack(side=RIGHT)

#UPGRADES
# Upgrade buttons and label are created to dynamically change due to the player's actions
autotext = StringVar()
autotext.set("You are earning " + str(round((miner.autoamount / miner.autospeed), 2)) + " coin(s) a second.")
autoinfo = Label(upgradeframe, textvariable = autotext)
autoinfo.pack(side=TOP)

upinfo = StringVar()
upinfo.set("You have not selected an upgrade.")
infolabel = Label(upgradeframe, textvariable = upinfo)
infolabel.pack()

warning = StringVar()
warning.set("You have not selected an upgrade.")
warninglabel = Label(upgradeframe, textvariable = warning, fg = "red")
warninglabel.pack()

uptypeinfo = Label(selectframe, text="Select an upgrade type.")
uptypeinfo.pack()

uptypevariable = StringVar()
uptypevariable.set("None")
uptype = OptionMenu(selectframe, uptypevariable, "Click Value Increase", "Auto-Miner Value", "Auto-Miner Speed", "Gambling Multiplier", command=optionChanger)
uptype.pack()

purchasebutton = Button(selectframe, text = "Purchase Upgrade?", command=buyselector)
purchasebutton.pack()

# BOSSKEY AND PAUSE
# BossKey image set as a .gif for tkinter to display
bossimage = PhotoImage(file="bossKey.gif")
# When a key is pressed, give it to the keyGet function
window.bind("<Key>", keyGet)

# Create the pause button
pausetext = StringVar()
pausebutton = Button(bitcoinframe, textvariable = pausetext, fg="black", command = pauser)
pausetext.set("PAUSE GAME")
pausebutton.pack(side=LEFT)

#GAMBLING
#Scales are created to control the player's bet
betprice = Scale(gamblingframe, activebackground = "yellow", orient = HORIZONTAL, command = wagercalc, label = "Coins to bet.", to=miner.coins, from_=0)
betprice.pack()

wager = Scale(gamblingframe, activebackground = "green", orient = HORIZONTAL, resolution = 5, command = wagercalc, label = "Percentage odds?")
wager.pack()

# Gambling multiplier is defined here for use later
multiplier = 2
currentmult = multiplier

# Variable label created to inform the player
bettext = StringVar()
betinfo = Label(gamblingframe, textvariable = bettext)
bettext.set("You can bet " + str(betprice.get()) + " bitcoins and take the odds of " + str(wager.get()) + "% for a " + str(multiplier) + "x multiplier.")
betinfo.pack()

# "MAKE BET" button calls the "beteffect" function from the Miner class
betbutton = Button(gamblingframe, text = "MAKE BET", command = miner.beteffect)
betbutton.pack()

#CHEATS
# Entry widget and button are created for users to enter and submit a cheat
cheatcode = Entry(cheatframe)
cheatcode.pack(side=TOP)
cheatchecker = Button(cheatframe, text = "Check Cheat Code", command = miner.checkCheat)
cheatchecker.pack(side=BOTTOM)

# autoCoin is set to start so the player starts earning coins automatically
miner.autoCoin()

#Game set into motion
mainloop()

#SOLVES THE THREADING ERROR ISSUE
timer.cancel()
