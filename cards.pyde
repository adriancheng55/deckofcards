# Name                          Type         Purpose                                        Restrictions
# tempDict                      Array        temporarily stores data necessary              N/A
# numofsuits/numofvals          Int          Used to make the deck                          N/A
# keepgoing                     Bool.        Used to switch between the game                True/ False
# winnerNames                   Array        Stores the str(names) of the winners           N/A
# rulesActivated                Bool.        If activated, shows the rule screen            True/ False
# numofplayers                  Int          Used to determine num of players               1<x<7
# pot                           Int          The money that will get distributed to winner  >0
# players                       Array        holds all the players as objects of class      N/A
# active player                 Int          Used to determine which player's turn          N/A
# cardnumberchange              Int          Limit num of times player changes card         0<=x<=2
# keyval                        Str          Takes a character input from keyPressed()      N/A
# string                        Str          Takes the characters from keyval               N/A
# clickedbutton                 Str          Returns which button was pressed               N/A
# differentscreens              Object       Objects of the Board class                     N/A
# Board                         Class        Manages the graphics of the game               N/A
# Player                        Class        Manages the player's attibutes                 N/A
# player in players             Object       Objects of the Player class                    N/A
# width/ height                 Int          Dimensions of the canvas                       N/A
# gamemode                      Int          Loads the approriate screen                    N/A
# player.hand                   Array        List of objects of the card class              N/A
# card()                        Class        Holds the attibutes for suit/value             N/A
# determineHand()               Func.        determines a player's hand rank                N/A
# getscreeninfo()               Func.        Function that globals the info from text       N/A
# filechecker()                 Func.        Function that opens a file and puts in array   N/A
# addAccount()                  Func.        Function that adds new player to the file      N/A
# idfsgms()                     Func.        Removes a player if they're too broke          N/A
# deckcard()                    Class        Deals with deck related stuff (add card)       N/A
# Boxes/Screentext/Buttons      Class        These are child classes of the Board class     N/A
# getcards()                    Func.        Adds a card to the player's hand               N/A
# filewriter()                  Func.        Writes the renewed info the file               N/A
# cardsorter()                  Func.        Sorts the card to easily determine hand        N/A
# gameplay()                    Func.        Deals with the player's actions in the game    N/A
# randomcard()                  Method       Picks random available card from deck          N/A
import random
from collections import Counter
import ast
width = 800
height = 600

#this is a filereading function which requires the name of the file you seek and returns an array of all its contents, split by newline
def filechecker(filename):
    d = open(filename, "r")
    lns = d.readlines() #an array of all the lines
    d.close()
    return lns

#this is a function which looks through a file holding every screen's characteristics, and records them globally
def getscreeninfo():
    tempDict = {}
    file = filechecker("info.txt")
    #getting info from file, running loop through the lines
    for k in file:
        #splitting elements by that symbol
        k = k.split("|")
        for i in k:
            #splitting the variable name and the value
            i = i.split(".")
            #since it is a string, this makes it a list
            i[1] = ast.literal_eval(i[1])
            #I make the variable name the key and the value what the variable equals, this makes it easy to add variables to the code
            tempDict[i[0]] = i[1]
    # I global the variables in the dictionary
    globals().update(tempDict)

numofsuits = 4
numofvalues = 13
rulesActivated = False
keepgoing = False
winnerNames = []
gamemode = 1
numofplayers = 2
pot = 0
players = [] #an array holding every Player class instance
cardnumberchange = 0
maxbet = 0 #the greatest amount bet
activeplayer = 0
messages = ["Type num of players and press Enter (1-7):", "Type next name and press Enter:", "Each player has added the blind of "]
blind = 15

#user input variables
clickedbutton = None #to hold the button that has been clicked
keyval = "" #single char from keyPressed()
string = "" #string which collects keyval values

def setup():
    global bg, deckofcards, rule
    global playerbetscreen, playerswitchscreen, rulescreen, playerbettingscreen, playermatchscreen, menuscreen, playerwinscreen, cardchangescreen, startscreen
    rectMode(CORNERS)
    stroke(0)
    size(width, height)
    deckofcards = loadImage("cards.png")
    bg = loadImage("Pokerback.jpg")
    rule = loadImage("rules.png")
    rule.resize(width,height)
    bg.resize(width, height) #image to fit background
    f = createFont("Bodoni MT Condensed Bold", 50)
    textFont(f) #this font is very thicc, and uses little space, so we can write much but it's still clear
    getscreeninfo()
    startscreentext[0] += str(blind)
    #makes the clickable area for the 5 different cards
    for i in range(5): #five cards
        cardchangeleft.append(150 + (100*i))
        cardchangetop.append(200)
        cardchangeright.append(250 + (100*i))
        cardchangebottom.append(360)
        cardchangemessages.append(str(i)) #cards will b labled 12345

    ## FORMAT: buttontext, boxcolour, boxborder, box topleft x, box toplefty y, box bottomright x, box bottomright y, button topleft x, button toplefty y, button bottomright x, button bottomright y, text x&y, text messages
    playerbetscreen = Board(playerbetmessages, playerbetboxcolour, playerbetboxline, playerbetboxleft, playerbetboxtop, playerbetboxright, playerbetboxbottom, playerbetscreenleft, playerbetscreentop, playerbetscreenright, playerbetscreenbottom, playerbetscreeninfo, playerbettext ) #it would be true on this screen tho
    
    menuscreen = Board(menubuttonmessages, [], [], [], [], [], [], menubuttonleft, menubuttontop, menubuttonright, menubuttonbottom, [], [])
    
    playerswitchscreen = Board(playerswitchscreenmessages, playerswitchboxcolour, playerswitchboxline, playerswitchboxleft, playerswitchboxtop, playerswitchboxright, playerswitchboxbottom, playerswitchscreenleft, playerswitchscreentop, playerswitchscreenright, playerswitchscreenbottom, playerswitchscreeninfo, playerswitchtext)

    playerbettingscreen = Board(playerbettingmessages, playerbettingboxcolour, playerbettingboxline, playerbettingboxleft, playerbettingboxtop, playerbettingboxright, playerbettingboxbottom, playerbettingscreenleft, playerbettingscreentop, playerbettingscreenright, playerbettingscreenbottom, playerbettingscreeninfo, playerbettingtext)
    
    playermatchscreen = Board(playermatchscreenmessages, playermatchboxcolour, playermatchboxline, playermatchboxleft, playermatchboxtop, playermatchboxright, playermatchboxbottom, playermatchscreenleft, playermatchscreentop, playermatchscreenright, playermatchscreenbottom, playermatchscreeninfo, playermatchtext)

    playerwinscreen = Board(playerwinscreenmessages, playerwinboxcolour, playerwinboxline, playerwinboxleft, playerwinboxtop, playerwinboxright, playerwinboxbottom, playerwinscreenleft, playerwinscreentop, playerwinscreenright, playerwinscreenbottom, playerwinscreeninfo, playerwinscreentext)

    cardchangescreen = Board(cardchangemessages, cardchangeboxcolour, cardchangeboxline, cardchangeboxleft, cardchangeboxtop, cardchangeboxright, cardchangeboxbottom, cardchangeleft, cardchangetop, cardchangeright, cardchangebottom, cardchangeinfo, cardchangetext)

    rulescreen = Board(rulescreenmessages, [], [], [], [], [], [], rulescreenleft, rulescreentop, rulescreenright, rulescreenbottom, [], [])

    startscreen = Board(startmessages, startscreencolour, startscreenboxline, [0], [0], [0], [0], startscreenleft, startscreentop, startscreenright, startscreenbottom, startinfo, startscreentext)

def draw():
    global keepgoing, rulesActivated, gamemode, numofplayers, players, pot, activeplayer, Deck
    global keyval, string, cardnumberchange, winnerNames
    background(bg)
    textSize(75)
    if keepgoing:
        message = ""
        if keyval == "`" and string != "":
            string = string[:-1]
        #gamemodes 1 & 2 are for inputing text
        if gamemode == 1: #this gamemode acquires the num of players
            if keyval != "":
                if keyval.isdigit() and 2 <= int(keyval) <= 7:
                    numofplayers = int(keyval)
                elif keyval == "~":
                    Deck = deckCard(4, 13) #initialize 1 instance of deck class, each time a new game is started
                    gamemode += 1
                    keyval = ""
            text(numofplayers, 100, 300) #temp display of num of players
            message = messages[0]

        elif gamemode == 2: #this gamemode if for getting playernames 1 by 1
            if len(players) == numofplayers:
                namechecker() #gives the players wallets respective to their accounts
                gamemode += 1
                keyval = ""

            elif len(players) < numofplayers:
                if keyval != "":
                    if keyval != "~" and keyval != "`" and len(string) <= 9:
                        string += keyval
                    elif keyval == "~" and len(string) > 0 and not any(x.name == string for x in players): #makes sure someone else can't enter another player's name
                        players.append(Player(string)) #initialize this instance of the player
                        string = ""
            text(string, 100, 300)
            message = messages[1]

        elif gamemode == 3: #this gamemode plays the blind and gives players their cards; involves the board class
            startscreen.displayBoxes()
            startscreen.displayText([])    
            #if this press the only button...
            if startscreen.displayButtons() != None:
                for player in players:
                    player.bet = blind
                    player.betting()
                    player.bet = -1
                    player.hand = getcards(5) #five cards is a fixed constant
                    player.handrank = determineHand(player.hand)
                gamemode += 1
                keepgoing = False

        elif gamemode == 4: #this gamemode goes over the first round of betting
            if gameplay():
                gamemode += 1

        elif gamemode == 5: #this gamemode is to switch les cards
            cardchangescreen.displayBoxes()
            choice = cardchangescreen.displayButtons()
            cardchangescreen.displayText([players[activeplayer].name])
            cardchangescreen.displayHand(players[activeplayer].hand)
            if choice == "FINISHED" or players[activeplayer].folded or players[activeplayer].wallet == 0:
                keepgoing = False
                players[activeplayer].handrank = determineHand(players[activeplayer].hand)
                cardnumberchange = 0
                activeplayer += 1
                if activeplayer == len(players):
                    activeplayer = 0
                    gamemode += 1
            # limits number of cards player can change
            elif choice != None and choice != "" and cardnumberchange < 2:
                players[activeplayer].hand = switchcard(players[activeplayer].hand, int(choice))
                # everytime player changes card, it adds one to here
                cardnumberchange += 1

        elif gamemode == 6: #this gamemode goes over the second round of betting
            if gameplay():
                gamemode += 1
                
        elif gamemode == 7: #this gamemode is to determine the winner and return the accounts to the file
            winners = determineWinner()
            for i in winners:
                winnerNames.append(i.name)
            pot /= len(winners)
            for i in winners:
                i.wallet += pot
            addAccount() #does the file
            keepgoing = False

        textSize(50)
        text(message, 100, 200)
    else:
        if gamemode == 4 or gamemode == 5 or gamemode == 6: #the playerswitch buffer
            button = playerswitchscreen.displayButtons()
            playerswitchscreen.displayText([players[activeplayer].name, players[activeplayer].wallet])
            if button == "CONTINUE":
                keepgoing = True
            if button == "RULES":
                rulesActivated = True
                
        elif gamemode == 7: #game is over, announce winners
            playerwinscreen.displayBoxes()
            #lists the name if there's multiple winners
            playerwinscreen.displayText([', '.join(winnerNames), pot])
            if playerwinscreen.displayButtons() != None:
                players = []
                numofplayers = 2
                gamemode = 1
             #display winner screen, the buttoncheck here will make gamemode = 1
        elif gamemode == 1: #starting screen
            button = menuscreen.displayButtons()
            pot = 0
            if button == "Start Gameru":
                keepgoing = True
            if button == "RULES":
                rulesActivated = True

    #rule screen            
    if rulesActivated:
        background(rule)
        button = rulescreen.displayButtons()
        if button == "BACK":
            rulesActivated = False  
                  
    keyval = "" #reset all input variables so we don't input endlessly

#a function which takes the previous file with accounts, updates/adds new game's info, and puts it back
def addAccount():
    global players
    accounts = filechecker("Player Accounts.txt")
    for i in range(len(accounts)):
        n = accounts[i].split(" |")
        for j in players:
            if j.name == n[0]:
                n[1] = j.wallet
                accounts[i] = (n[0] + " |" + str(j.wallet) + " |" + n[2])
                players.remove(j)

    for i in players:
        accounts.append(i.name + " |" + str(i.wallet) + " |" + "\n")
    accounts = idfsgms(accounts)
    filewriter(accounts)

#a function which removes an account from the file if the player doesn't have enough money to play future games
def idfsgms(lns): #passes in the new account list and returns it without poor people
    for i in lns:
        n = int(i.split(" |")[1])
        #if the person's wallets less than $30, remove them
        if n < 30:
            lns.remove(i)
    return lns

#a function directly in the draw which conducts game display and gameplay choices, and returns true if the turn is over
def gameplay():
    global activeplayer, maxbet, keepgoing
    player = players[activeplayer]
    rankText = ["Royal Flush", "Straight Flush", "Four of a kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"]
    if player.wallet == 0:
        player.bet = 0 #if they spent all their money in previous rounds, they are no longer able to join game, but must still be activated to be counted in current round to avoid loop

    if player.bet == maxbet and player.betted: #we've made afull go-around with no betting
        for each in players:
            each.betting()
            each.bet = -1 #default bet is -1 to avoid automatic crossover with maxbet default and loop endlessly, this only turns on if they actually play
        maxbet = 0
        activeplayer = 0
        return True

    else:
        if not player.betted: #we are waiting for this player to bet; this state is not to skip to next player once an action is commited
            playerbettingscreen.displayBoxes()
            playeraction = playerbettingscreen.displayButtons()
            playerbettingscreen.displayText([player.bet, player.wallet, maxbet])
            if playeraction == "OK":
                player.betted = True
                if player.bet > maxbet:
                    maxbet = player.bet
            elif playeraction == "ALL IN":
                player.betted = True
                player.bet = player.wallet
                if player.bet > maxbet:
                    maxbet = player.bet
            elif playeraction == "+" and player.bet < player.wallet: #and wallet
                player.bet += 5
            elif playeraction == "-" and player.bet > maxbet:
                player.bet -= 5
        elif maxbet == 0: #check or bet options
            playerbetscreen.displayBoxes()
            playeraction = playerbetscreen.displayButtons()
            playerbetscreen.displayText([player.name, player.wallet, pot, rankText[player.handrank]])
            playerbetscreen.displayHand(player.hand)
            if playeraction == "BET":
                player.betted = False
                maxbet = 5
                player.bet = maxbet
            if playeraction == "CHECK":
                player.bet = 0
        elif maxbet > 0: #raise and call options
            playermatchscreen.displayBoxes()
            playeraction = playermatchscreen.displayButtons()
            playermatchscreen.displayText([player.name, player.wallet, pot, player.bet, maxbet, rankText[player.handrank]])
            playermatchscreen.displayHand(player.hand)
            if playeraction == "CALL":
                if player.wallet < maxbet:
                    player.bet += player.wallet - player.bet
                else:
                    player.bet += maxbet - player.bet
            if playeraction == "RAISE":
                if player.wallet < maxbet+5:
                    activeplayer -= 1
                else:
                    player.betted = False
                    maxbet += 5
                    player.bet = maxbet
        if playeraction == "FOLD":
            if sum(bool(x.folded) for x in players) < len(players)-1: #checks if everyone else folded
                player.folded = True
            else:
                activeplayer -= 1

        #you've got no more money so you're all in, or you've folded; u can't take part in gameplay anymore and will be automatically skipped
        if player.bet == player.wallet or player.folded or (player.betted and playeraction != None and playeraction != ""): #itterates player if an action has been committed
            if activeplayer < len(players)-1:
                activeplayer += 1
            else:
                activeplayer = 0
            keepgoing = False

#a function which passes in the player's hand and the index of the garbage card, and returns the hand with a new card in its place
def switchcard(cardarray, cardindex):
    cardarray.pop(cardindex)
    cardarray.append(getcards(1))
    return cardsorter(cardarray)

#a function that recieves the number of cards required and the player to give them to, and gives an array of all the cards
def getcards(cardamount): #cardamount is an int
    allcards = []
    for i in range(cardamount):
        acard = Deck.randomCard() #returns one card from the deck instance Deck
        if acard != None:
            if cardamount == 1:
                return acard
            allcards.append(acard)
    return cardsorter(allcards)

#sorts an array of cards by value then by suit, then returns it
def cardsorter(cards): #must recieve an array of card instances
    allvals = []
    allsuits = []
    for j in range(len(cards)): #to create an array of values, we must get that attribute of each card instance
        allsuits.append(cards[j].suit) #allvals is optained to compare ints instead of card instances

    sorted = False
    while not sorted: #sorts by number
        sorted = True #tests whether bubble switch is necessary
        for i in range(len(allsuits)-1):
            if allsuits[i] < allsuits[i+1]: #the bubble switch
                cards[i], cards[i+1] = cards[i+1], cards[i] #sorts the actual instances parallel to their values
                allsuits[i], allsuits[i+1] = allsuits[i+1], allsuits[i]
                sorted = False

    for j in range(len(cards)):
        allvals.append(cards[j].val)
    sorted = False
    while not sorted: #sorts by number
        sorted = True #tests whether bubble switch is necessary
        for i in range(len(allvals)-1):
            if allvals[i] > allvals[i+1]: #the bubble switch
                cards[i], cards[i+1] = cards[i+1], cards[i]
                allvals[i], allvals[i+1] = allvals[i+1], allvals[i]
                sorted = False #allvals must also be sorted or each bubble pass will lose sync with the cards and run endlessly
    return cards

#a function that recieves a hand of cards, and returns its rank as an int
def determineHand(ahand):
    handrank = 9 #highcard is default
    tempList = []
    for i in ahand:
        tempList.append((i.suit, i.val))
    dupeOfsuits = Counter(x for (x,y) in tempList)
    dupeOfvals = Counter(y for (x,y) in tempList)
    samesuits = False
    consecutive = True
    numofpairs = 0
    tempNum = 0
    royalNum = 42 #adds the king value(12), queen(11), jack(10), ten(9), and ace(0) only possible sum
    
    #the key is the value.suit while the key's value is the number of duplicates
    if len(dupeOfsuits) == 1:
        samesuits = True
        
    #checks to see if the numbers are consecutice and if this statement is true, they're not
    for i in range (len(tempList)):
        tempNum += tempList[i][1]
        if i+1 != len(tempList) and tempList[i][1] + 1 != tempList[i+1][1]: 
            consecutive = False    
        elif tempNum == royalNum:
            consecutive = True

    if samesuits:
        if consecutive:
            for i in tempList:
                if tempNum == royalNum: # checks to see if the sum is the royal sum, if it is, it's a royal flush
                    handrank = 0 #royal flush
                else:
                    handrank = 1 #straight flush
        else:
            handrank = 4 #flush
    elif consecutive:
        handrank = 5 #straight
    else:
        for value, theKey in dupeOfvals.items():
            if theKey == 4: #Checks for four of a kind
                handrank = 2
            elif theKey == 3:
                handrank = 6 #this means there's only a 3 of a kind
                for x,y in dupeOfvals.items():
                    if y == 2: #if there's a two, that means that it is a full house
                        handrank = 3
            elif theKey == 2:
                numofpairs += 1 #this is used to count the number of pairs
        if numofpairs == 2:
            handrank = 7 #two pairs
        elif numofpairs == 1:
            handrank = 8 #one pair
    return handrank

#a function for the end of the game that returns the players who won the game
def determineWinner():
    tempDict = {}
    lst = []
    #makes a dictionary for easy comparisons
    for player in players:
        if not player.folded:
            tempDict[player] = player.handrank

    #finds the smallest rank (highest rank) and removes all the bigger ranks (lower ranks)
    for x, y in tempDict.items():
        if y != min(tempDict.values()):
            tempDict.pop(x, None)

    #if multiple highcards, gets the highest card value and suit
    
    #splits the winning if they have the same rank
    for i in tempDict:
        lst.append(i)
    return (lst)

class Buttons: #all individual button characteristics
    def __init__(self, butleft, buttop, butright, butbottom, buttext):
        self.butleft = butleft
        self.buttop = buttop
        self.butright = butright
        self.butbottom = butbottom
        self.buttext = buttext
        self.butstate = True #whether button is active

class Screentext: #all individual text characteristics
    def __init__(self, playertextx, playertexty, playertext):
        self.playertextx = playertextx
        self.playertexty = playertexty
        self.playertext = playertext

class Boxes: #all individual box characteristics
    def __init__(self, boxleft, boxtop, boxright, boxbottom, boxcolour, boxline):
        self.boxleft = boxleft
        self.boxtop = boxtop
        self.boxright = boxright
        self.boxbottom = boxbottom
        self.boxcolour = boxcolour
        self.boxline = boxline

class Board: #holds all boxes, buttons, and text on a screen iside the instance
    #attributes contain screen characteristics;
    #functions pass in information for display
    def __init__(self, screenboxmessages, screenboxcolour, screenboxline, screenbuttonleft, screenbuttontop, screenbuttonright, screenbuttonbottom, screenboxleft, screenboxtop, screenboxright, screenboxbottom, screeninfo, screentext):
        self.buttons = []
        self.boxes = []
        self.texts = []
        self.screeninfo = screeninfo
        for i in range(len(screenboxleft)): #create individual buttons each with its own characteristics
            self.buttons.append(Buttons(screenboxleft[i], screenboxtop[i], screenboxright[i], screenboxbottom[i], screenboxmessages[i]))
            
        for i in range(len(screenbuttonleft)):
            self.boxes.append(Boxes(screenbuttonleft[i], screenbuttontop[i], screenbuttonright[i], screenbuttonbottom[i], screenboxcolour[i], screenboxline[i]))
          
        for i in range(len(screeninfo)):
            self.texts.append(Screentext(screeninfo[i][0], screeninfo[i][1], screentext[i]))

    def displayBoxes(self):
        strokeWeight(12)
        for i in range(len(self.boxes)):
            if self.boxes[i].boxcolour[i] != None and self.boxes[i].boxcolour[i] != "":
                fill(self.boxes[i].boxcolour[0], self.boxes[i].boxcolour[1], self.boxes[i].boxcolour[2])
            if self.boxes[i].boxline != None and self.boxes[i].boxline != "":
                #consider passing a strokeweight too
                stroke(self.boxes[i].boxline[0], self.boxes[i].boxline[1], self.boxes[i].boxline[2])
            rect(self.boxes[i].boxleft, self.boxes[i].boxtop, self.boxes[i].boxright, self.boxes[i].boxbottom)

    def displayButtons(self): #this function displays all the buttons in the instance, and returns their text if clicked and if active
        global currentbuttons, clickedbutton
        currentbuttons = []
        strokeWeight(4)
        stroke(255)
        for button in self.buttons:
            fill(0)
            rect(button.butleft, button.buttop, button.butright, button.butbottom)
            fill(255)
            textSize(30) #we could pass the textsize in too, but might b complicating, maybe not...
            #text put at at a percentage after the topleft coordinates of button
            text(button.buttext, button.butleft + ((button.butright - button.butleft) * 0.3), button.buttop + ((button.butbottom - button.buttop) * 0.6))
            
            if button.butstate: #tests whether button is activated
                currentbuttons.append((button.butleft, button.butright, button.buttop, button.butbottom))
            if clickedbutton == (button.butleft, button.butright, button.buttop, button.butbottom): #the button has now been clicked and reset
                clickedbutton = None
                currentbuttons = []
                return button.buttext #the draw will continue with the button info it recieves

    def displayText(self, playerinfo):
        for i in range(len(playerinfo)): #range and length required for some reason
            if type(playerinfo[i]) != str:
                playerinfo[i] = str(playerinfo[i])
        strokeWeight(2)
        fill(255)
        textSize(50) #size and colour are fixed variables here so no need to pass them in
        if len(playerinfo) < len(self.texts):
            for i in range(len(self.texts) - len(playerinfo)):
                playerinfo.append(" ")
        if len(playerinfo) == len(self.texts):
            for i in range(len(self.texts)):
                text(self.texts[i].playertext + playerinfo[i], self.texts[i].playertextx, self.texts[i].playertexty) #each line will contain fixed text and passed in text

    def displayHand(self, thishand):
        cardw = 80 #the variables here are fixed for the unique image we're using; better not to pull that from a file
        cardl = 110
        cardx = self.boxes[-1].boxleft ##HAND DISPLAY WILL FOLLOW THE MOST RECENT BOX IN THE SCREEN'S DATA
        outputcardw = 100
        outputcardl = 160
        for i in range (len(thishand)):
            copy(deckofcards, cardw * thishand[i].val, cardl * thishand[i].suit, cardw, cardl, cardx + (outputcardw * i), self.boxes[-1].boxtop, outputcardw, outputcardl)

#a function which checks for the player accounts inside the accounts file, and creates to their wallet respectively
def namechecker(): #function to check if any accounts exist
    cash = filechecker("Player Accounts.txt") #cash is an array of the entire file
    for player in players:
        for i in range(len(cash)):
            n = cash[i].split(" |")
            if player.name == n[0]: #checks playername
                player.wallet = int(n[1]) #replace wallet with the one from the file

#this functions writes to the accounts file, recieving the most recent info from the game
def filewriter(playerinfo): #pass in the entire array of all lines as in the other file
    e = open("Player Accounts.txt", "w")
    e.writelines(playerinfo)
    e.close()

class Player:
    def __init__(self, name):
        self.name = name
        self.wallet = 200
        self.bet = -1
        self.hand = []
        self.handrank = 0
        self.betted = True #test in the draw whether this player is currently betting
        self.folded = False #test in the draw whether to include this player in the game

    def betting(self): #the player bets
        global pot
        if self.wallet >= self.bet and self.bet > 0:
            self.wallet -= self.bet
            pot += self.bet

#Unique characteristics for each card in here
class Card: #instances of this class will each hold a suit & val
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
    
#deals with the deck specific attributes
class deckCard:
    def __init__(self, numofsuits, numofvals):
        self.deck = []
        for suit in range(numofsuits):
            for val in range(numofvals):
                self.deck.append(Card(suit,val)) #puts all possible combinations inside instances of Card class

    #selects a random card from the deck
    #this method will be called in the draw a number of times to remove a card from deck each time
    def randomCard(self):
        if len(self.deck) > 0:
            i = random.randint(1, len(self.deck))
            card = self.deck[i-1]
            self.deck.pop(i-1)
            return card #this card has been removed and assigned to player hand by a function in the draw/gameplay

def mouseReleased():
    global clickedbutton
    for i in currentbuttons: #all buttons currently being checked
        if i[0] < mouseX < i[1] and i[2] < mouseY < i[3]:
            clickedbutton = i #the button that was clicked is now recognized

def keyPressed():
    global keyval, gamemode
    if gamemode == 1 or gamemode == 2: #the only times one would input info via key
        if key != ENTER and key != CODED and (str(key).isalnum() or str(key).isspace()): #valid keys
            keyval = str(key)
        elif key == ENTER:
            keyval = "~"
        elif key == BACKSPACE:
            keyval = "`"
        else:
            keyval = ""