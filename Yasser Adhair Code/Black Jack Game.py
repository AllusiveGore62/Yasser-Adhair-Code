import random as random #random package for shuffling

class card: #card class
    def __init__(self,suit,number): #initialising card class
        self.__suit = suit #Each card has a suit
        self.__number = number # and a number
    def getNumber(self): #Returns actual number of the card (1-13)
        return self.__number
    def getSuit(self): #Returns the suit of the card
        return self.__suit
    def revealCard(self): #Prints the card out
        if self.__number == 11:
            print('Jack of ' + self.__suit)
        elif self.__number == 12:
            print('Queen of ' + self.__suit)
        elif self.__number == 13:
            print('King of ' + self.__suit)
        else:
            print(str(self.__number) + ' of ' + str(self.__suit))
    def getValue(self): #Finds the blackjack value of the card
        if self.__number > 10: #Kings, Queens, and Jacks are worth 10
            return 10
        else:
            return self.__number


class deck: #Deck of cards class
    def __init__(self,cards):
        self.__cards = cards #Contains an array of cards
        random.shuffle(self.__cards) #Shuffles the cards
    def getCards(self): #Prints out the cards (for testing) 
        for card in self.__cards:
            card.revealCard()
    def drawCard(self): #Draws a card from the top of the deck
        return self.__cards.pop()
    def reAddCard(self, card): #Readds card to top of deck
        self.__cards.append(card)
    def shuffleCards(self): #Shuffles cards
        random.shuffle(self.__cards)

class hand: #Each player has a hand which contains their cards
    def __init__(self): 
        self.__cards = [] #Hand is empty at the start
    def getCards(self): #Returns the cards in the hand as an array
        return self.__cards
    def addCard(self, card): #Adds a card to the hand
        self.__cards.append(card)
    def resetHand(self): #Resets hand and returns the cards so they can be readded to the deck
        temp =[]
        for card in self.__cards:
            temp.append(card)
        self.__cards = []
        return temp

class person: #person superclass
    def __init__(self, hand):
        self._hand = hand #Each person has a hand
    def hit(self, card): #Adds a card to their hand
        self._hand.addCard(card)
    def stay(self): #Does nothing, here in case I add more players in a future project
        pass
    def getValue(self): #Calculates the value of a player's hand
        aceNumber = 0
        total = 0
        cards = self._hand.getCards()
        for card in cards:
            if card.getValue() != 1:
                total += card.getValue()
            else:
                total += 11
                aceNumber += 1 #Accomidates for aces
        for i in range(aceNumber):
            if total > 21:
                total += -10 #Adjusts ace value if total is larger than 21
        return total
    def revealHand(self): #Reveals hand (prints out cards)
        cards = self._hand.getCards()
        for card in cards:
            card.revealCard()
    def resetHand(self): #Resets the hand
        return self._hand.resetHand()
    


class player(person): #A player (person class who can bet)
    def __init__(self, hand, balance):
        super().__init__(hand)
        self.__balance = balance
    def bet(self): #Lets the player place a bet, with prompts
        amount = int(input('How much would you like to bet? '))
        while (self.__balance - amount) < 0: #Checks if they have enough money
            amount = int(input('You do not have that much money, try again: '))
        self.__balance += -amount #Removes the amount from their account
        return amount
    def addMoney(self, pot): #Adds money to their balance
        self.__balance += pot
    def getBalance(self): #Returns their balance
        return self.__balance

class dealer(person): #A dealer (person class who automatically hits or stays)
    def __init__(self, hand):
        super().__init__(hand)
    def decide(self): #Makes their decision
        value = self.getValue()
        if value >= 17: 
            return False #False means stay
        else:
            return True #True means hit
    def revealFirst(self): #Reveals the dealer's first card
        a = self._hand.getCards()
        a[0].revealCard()

class game: #The largest game class which conains all subclasses
    def __init__(self, deck, player, dealer):
        self.__deck = deck
        self.__player = player
        self.__dealer = dealer
        self.__pot = 0
    def firstTurn(self): #Sets the game up for the first turn
        card = self.__deck.drawCard()
        card1 = self.__deck.drawCard()
        self.__player.hit(card)
        self.__player.hit(card1) #Initialises players hand at the start
        print('You drew: ')
        self.__player.revealHand() #Reveals players hand
        print('with a value of: ' + str(self.__player.getValue())) #And shows value
        card = self.__deck.drawCard()
        card1 = self.__deck.drawCard()
        self.__dealer.hit(card)
        self.__dealer.hit(card1) #Intialises dealer's hand at the start
        print('First dealer card is ')
        self.__dealer.revealFirst() #Reveals his firstcard
    def playerDraw(self):#Lets the player draw a card
        card = self.__deck.drawCard() 
        self.__player.hit(card) 
        print('You now have: ')
        self.__player.revealHand()
        print('with a value of: ' + str(self.__player.getValue())) #Tells them their hand and its value
    def checkPlayerBust(self): #Checks if the player has gone bust
        value = self.__player.getValue()  
        if value > 21:
            return True #True means they've gone bust
        else:
            return False #False means they're under 21
    def checkDealerBust(self): #Checks if the dealer has gone bust
        value = self.__dealer.getValue()  
        if value > 21:
            return True #True means they've gone bust
        else:
            return False #False means they're under 21
    def checkBalance(self): #Lets the player check their betting balance
        print('You have ' + str(self.__player.getBalance()))
    def checkPlayerHand(self): #Tells the player their hand and its value
        print('You have: ')
        self.__player.revealHand()
        print('with a value of: ' + str(self.__player.getValue()))
    def checkDealerHand(self): #Prints the dealer's first card
        print('The dealers first card is: ')
        self.__dealer.revealFirst() #Tells them the first card and its value
    def playerBet(self): #Lets the player place a bet and add it to the pot
        self.checkBalance() #Prints the player's balance
        self.__pot += (self.__player.bet())*2 #Gives the player a prompt to bet and adds it to the pot (where the dealer matches it)
        print('The pot is now ' + str(self.__pot)) #prints out the pot
    def checkPot(self): #Lets the player check the pot
        print('The pot is ' + str(self.__pot))
    def dealerTurn(self): #Lets the dealer decide their turn
        if self.__dealer.decide() == True: 
            self.__dealer.hit(self.__deck.drawCard()) #Hits if below 17
            print('The dealer has decided to hit, their cards are:')
            self.__dealer.revealHand()
            print('with a value of: ' + str(self.__dealer.getValue())) #Reveals the dealer's hand and value
            return True
        else:
            self.__dealer.stay() #Stays if 17 or under
            print('The dealer has decided to stay, their cards are:')
            self.__dealer.revealHand()
            print('with a value of: ' + str(self.__dealer.getValue())) #Reveals dealer's hand and value
            return False
    def roundStart(self): #Initialises the start of another round (different from first round)
        a = self.__player.resetHand()
        b = self.__dealer.resetHand() #Resets hand
        for card in a:
            self.__deck.reAddCard(card)
        for card in b:
            self.__deck.reAddCard(card) #Re adds them to the deck
        self.__deck.shuffleCards()  #Shuffles the deck
        card = self.__deck.drawCard()
        card1 = self.__deck.drawCard()
        self.__player.hit(card)
        self.__player.hit(card1) #Initialises player's hand and reveals it
        print('You drew: ')
        self.__player.revealHand()
        print('with a value of: ' + str(self.__player.getValue()))
        card = self.__deck.drawCard()
        card1 = self.__deck.drawCard()
        self.__dealer.hit(card)
        self.__dealer.hit(card1)
        print('First dealer card is ')
        self.__dealer.revealFirst() #Initialises dealer's hand and reveals the first card
    def decideWin(self):
        playerValue = self.__player.getValue()
        dealerValue = self.__dealer.getValue()
        if playerValue > dealerValue:
            return True #True means player won
        elif playerValue == dealerValue:
            return None #None means a draw
        else:
            return False #False means dealer won
    def playerWin(self): #For when the player wins
        print('You won, the pot had: ' + str(self.__pot)) #Tells them the value of the pot
        self.__player.addMoney(self.__pot) #Adds the pot to their balance
        self.checkBalance() #Tells them their balance
        self.__pot = 0 #Resets the pot
    def Draw(self): #For when the player and the dealer draw
        print('You drew with the dealer, the pot had: ' + str(self.__pot)) #Tells them the value of the pot
        a = self.__pot 
        a = ((a/2)//1) #Splits the money
        self.__player.addMoney(a) #Adds the money
        self.checkBalance() #Tells them their balance
        self.__pot = 0 #Resets the pot
    def dealerWin(self): #For when the dealer wins
        print('You lost, the pot had: ' + str(self.__pot)) #Tells them the value of the pot
        self.checkBalance() #Adds the pot to their balance
        self.__pot = 0 #Rests the pot
    def topUp(self):
        amount = int(input('How much would you like to add? (integer) '))
        self.__player.addMoney(amount)
        self.checkBalance()
    
def printControls():
    print('Here are the controls: ')
    print('1 = Hit')
    print('2 = Stay (ends your turn)')
    print('3 = Bet')
    print('4 = Check your cards')
    print('5 = Check your balance')
    print('6 = Check dealers first card')
    print('7 = Check pot')
    print('8 = Top up balance')
    print('9 = End Game')
    print('0 = Check controls')


suits = ['Clubs','Diamonds','Hearts','Spades']
numbers = [1,2,3,4,5,6,7,8,9,10,11,12]
deck_list = []
for suit in suits:
    for num in numbers:
        deck_list.append(card(suit,num)) #Initialises all the cards
liveDeck = deck(deck_list) #Initialises the deck
playerHand = hand()
dealerHand = hand()
balance = int(input('How much money would you like to start with? (integer) ')) #Gets player balance
livePlayer = player(playerHand,balance)
liveDealer = dealer(dealerHand)
liveGame = game(liveDeck,livePlayer,liveDealer) #Initialises all classes into big class
running = True
printControls()
liveGame.firstTurn() #Sets up first turn
print('Scroll up for controls')
Pturn = True
dealerWon = False #Initialises variables for the loop
winnerOveride = False
while running == True: 
    while Pturn == True:
        control = input('What would you like to do? ') #Runs through player controls while it is the player's turn
        if control.isdigit() == False:
            print('Invalid input')
            continue
        control = int(control)
        if control == 1:
            liveGame.playerDraw()
            if liveGame.checkPlayerBust() == True:
                print('You went bust')
                liveGame.dealerWin()
                Pturn = False
                dealerWon = True
                winnerOveride = False
                a = input('Enter anything when you are ready to start ')
                liveGame.roundStart()
                break
            continue
        elif control == 2:
            print('You stayed')
            Pturn = False
            break
        elif control == 3:
            liveGame.playerBet()
            continue
        elif control == 4:
            liveGame.checkPlayerHand()
            continue
        elif control == 5:
            liveGame.checkBalance()
            continue
        elif control == 6:
            liveGame.checkDealerHand()
            continue
        elif control == 7:
            liveGame.checkPot()
        elif control == 8:
            liveGame.topUp()
            continue
        elif control == 9:   
            print('Ending program...')  
            running = False
            break
        elif control == 0:
            printControls()
            continue
        else:
            print('Invalid input')
            continue
    if dealerWon == True: #Conditions for the loop to end early
        Pturn = True
        dealerWon = False
        winnerOveride = False
        continue
    if running == False:
        break
    dealerTurn = liveGame.dealerTurn()
    if liveGame.checkDealerBust() == True:
        winnerOveride = True
    while dealerTurn == True and winnerOveride == False:
        dealerTurn = liveGame.dealerTurn()
        if liveGame.checkDealerBust() == True:
            winnerOveride = True
    winner = liveGame.decideWin()
    if winner == True or winnerOveride == True:
        liveGame.playerWin()
    elif winner is None:
        liveGame.Draw()
    else:
        liveGame.dealerWin()  
    Pturn = True
    dealerWon = False
    winnerOveride = False
    a = input('Enter anything when you are ready to start ')
    liveGame.roundStart() #Restarts round

    
        
        

        
        
