
function shuffle(array) {
    let currentIndex = array.length;  // While there remain elements to shuffle...
    while (currentIndex != 0){  // Pick a remaining element...
      let randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--  // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
}

class card {  //card class
    constructor(suit,number){  //initialising card class
        this.suit = suit   //Each card has a suit
        this.number = number   // and a number
    }
    getNumber(){  //Returns actual number of the card (1-13)
        return this.number
    }
    getSuit(){  //Returns the suit of the card
        return this.suit
    }
    revealCard(){  //Prints the card out
        var new_html = ''
        const currentDir = window.location.origin + window.location.pathname.substring(0, window.location.pathname.lastIndexOf("/")) + "/Cards/";

        if (this.number == 11){ 
            new_html = '<img src="' + currentDir + this.number + this.suit + '.png" alt="Jack of ' + this.suit + '">';
        }
        else if (this.number == 12){
            new_html = '<img src="' + currentDir + this.number + this.suit + '.png" alt="Queen of ' + this.suit + '">';
        } else if (this.number == 13){
            new_html = '<img src="' + currentDir + this.number + this.suit + '.png" alt="King of ' + this.suit + '">';
        } else {
            new_html = '<img src="' + currentDir + this.number + this.suit + '.png" alt="' + this.number + ' of ' + this.suit + '">';
            console.log(this.number + ' of ' + this.suit);
        }
        return new_html;
    }
    getValue(){  //Finds the blackjack value of the card
        if (this.number > 10){  //Kings, Queens, and Jacks are worth 10
            return 10
        }
        else{
            return this.number
        }
    }
}

class deck{  //Deck of cards class
    constructor(cards){
        this.cards = cards   //Contains an array of cards
        shuffle(this.cards)  //Shuffles the cards
    }
    drawCard(){  //Draws a card from the top of the deck
        return this.cards.pop();
    }
    reAddCard(card){  //Readds card to top of deck
        this.cards.push(card)
    }
    shuffleCards(){  //Shuffles cards
        shuffle(this.cards)
    }
}
class hand{  //Each player has a hand which contains their cards
    constructor(){ 
        this.cards = []   //Hand is empty at the start
    }
    getCards(){  //Returns the cards in the hand as an array
        return this.cards
    }
    addCard(card){  //Adds a card to the hand
        this.cards.push(card)
    }
    resetHand(){  //Resets hand and returns the cards so they can be readded to the deck
        let temp =[];
        for (var i=0; i < this.cards.length; i++){
            var a_card = this.cards[i];
            temp.push(a_card)
        }
        this.cards = [];
        return temp
    }
}
class person{  //person superclass
    constructor(hand){
        this.hand = hand   //Each person has a hand
    }
    hit(card){  //Adds a card to their hand
        this.hand.addCard(card)
    }
    stay(){  //Does nothing, here in case I add more players in a future project
        
    }
    getValue(){  //Calculates the value of a player's hand
        var aceNumber = 0;
        var total = 0;
        var cards = this.hand.getCards();
        for (var i=0; i < cards.length; i++){
            var a_card = cards[i];
            if (a_card.getValue() != 1){
                total += a_card.getValue();
            } else{
                total += 11;
                aceNumber += 1 ;  //Accomidates for aces
            }
        }
        for (var i=0; i < aceNumber.length; i++){
            if (total > 21) {
                total += -10 ;  //Adjusts ace value if (total is larger than 21)
            }
        }
        return total
    }
    revealHand(identity){  //Reveals hand (prints out cards) Identity will make sure the cards are printed out the right area (to show who's cards they are)
        let cards = this.hand.getCards();
        var new_html = ''
        for (var i=0; i < cards.length; i++){
            var a_card = cards[i];
            new_html += a_card.revealCard();
            console.log(new_html)
        }
        document.getElementById(identity).innerHTML = new_html
    }
    resetHand(){  //Resets the hand
        return this.hand.resetHand();
    }
}


class player extends person{  //A player (person class who can bet)
    constructor(a_hand, balance){
        super(a_hand);
        this.balance = Number(balance);
    }
    bet(amount){  //Lets the player place a bet, with prompts 
        this.balance += -amount;   //Removes the amount from their account
        return amount;
    }
    addMoney(amount){  //Adds money to their balance
        this.balance += Number(amount);
    }
    getBalance(){  //Returns their balance
        return this.balance;
    }
}

class dealer extends person{  //A dealer (person class who automatically hits or stays)
    constructor(a_hand){
        super(a_hand);
    }
    decide(){  //Makes their decision
        var value = this.getValue();
        if (value >= 17){ ;
            return false  //false means stay
        }
        else{
            return true  //true means hit
        }
    }
    revealFirst(){  //Reveals the dealer's first card
        var a = this.hand.getCards();
        var new_html
        new_html = a[0].revealCard();
        document.getElementById('dealer-cards').innerHTML = new_html
    }
}

class game{  //The largest game class which conains all subclasses
    constructor(deck, player, dealer){
        this.deck = deck;
        this.player = player;
        this.dealer = dealer;
        this.pot = 0;
    }
    firstTurn(){  //Sets the game up for the first turn
        var a_card = this.deck.drawCard();
        var card1 = this.deck.drawCard();
        this.player.hit(a_card);
        this.player.hit(card1);  //Initialises players hand at the start
        document.getElementById('player-prompt').innerHTML = 'You drew: ';
        this.player.revealHand('player-cards'); //Reveals players hand
        document.getElementById('player-value').innerHTML = 'with a value of: ' + this.player.getValue(); //And shows value
        a_card = this.deck.drawCard();
        card1 = this.deck.drawCard();
        this.dealer.hit(a_card);
        this.dealer.hit(card1);  //Intialises dealer's hand at the start
        document.getElementById('dealer-prompt').innerHTML = 'First dealer card is ';
        this.dealer.revealFirst();  //Reveals his firstcard
    }
    playerDraw(){  //Lets the player draw a card
        var a_card = this.deck.drawCard();
        this.player.hit(a_card);
        document.getElementById('player-prompt').innerHTML = 'You now have: ';
        this.player.revealHand('player-cards');
        document.getElementById('player-value').innerHTML = 'with a value of: ' + this.player.getValue();  //Tells them their hand and its value
    }
    checkPlayerBust(){  //Checks if (the player has gone bust
        var value = this.player.getValue();
        if (value > 21){
            return true  //true means they've gone bust
        }
        else{
            return false  //false means they're under 21
        }
    }
    checkDealerBust(){  //Checks if (the dealer has gone bust
        var value = this.dealer.getValue();
        if (value > 21){
            return true;  //true means they've gone bust
        }
        else{
            return false;  //false means they're under 21
        }
    }
    checkBalance(){  //Lets the player check their betting balance
        document.getElementById('balance').innerHTML ='You have ' + this.player.getBalance();
    }
    checkPlayerHand(){  //Tells the player their hand and its value
        console.log('You have: ');
        this.player.revealHand('player-cards');
        console.log('with a value of: ' + this.player.getValue());
    }
    checkDealerHand(){  //Prints the dealer's first card
        console.log('The dealers first card is: ');
        this.dealer.revealFirst();  //Tells them the first card and its value
    }
    playerBet(){  //Lets the player place a bet and add it to the pot
        var amount = document.getElementById('myInput').value;   
        if (amount == ''){
            document.getElementById('prompt').innerHTML = 'Invalid input, how much would you like to bet?'
            return
        }
        if ((this.player.balance - amount) < 0) {  //Checks if (they have enough money
            document.getElementById('prompt').innerHTML = 'You do not have that much money, try again: '
            return
        }
        this.pot += (this.player.bet(amount))*2;   //Gives the player a prompt to bet and adds it to the pot (where the dealer matches it)
        document.getElementById('pot').innerHTML = 'The pot is now ' + this.pot; //prints out the pot
        this.checkBalance();
        document.getElementById('input-button').onclick = playerTurn;
    }
    checkPot(){  //Lets the player check the pot
        document.getElementById('pot').innerHTML = 'The pot is ' + this.pot
    }
    dealerTurn(){  //Lets the dealer decide their turn
        if (this.dealer.decide() == true){ 
            this.dealer.hit(this.deck.drawCard());  //Hits if below 17
            document.getElementById('dealer-prompt').innerHTML =  'The dealer has decided to hit, their cards are:';
            this.dealer.revealHand('dealer-cards');
            document.getElementById('dealer-value').innerHTML = 'with a value of: ' + this.dealer.getValue() + '\n ';  //Reveals the dealer's hand and value
            return true;
        }
        else{
            this.dealer.stay();  //Stays if 17 or under
            document.getElementById('dealer-prompt').innerHTML =  'The dealer has decided to stay, their cards are:;';
            this.dealer.revealHand('dealer-cards');
            document.getElementById('dealer-value').innerHTML = 'with a value of: ' + this.dealer.getValue() + '\n ';  //Reveals dealer's hand and value
            return false;
        }
    }
    roundStart(){  //Initialises the start of another round (different from first round)
        var a = this.player.resetHand();
        var b = this.dealer.resetHand();   //Resets hand
        for (var i=0; i < a.length; i++){
            var a_card = a[i];
            this.deck.reAddCard(a_card);
        }
        for (var i=0; i < b.length; i++){
            var a_card = b[i];
            this.deck.reAddCard(a_card); //Re adds them to the deck
        }
        this.deck.shuffleCards();  //Shuffles the deck
        var a_card = this.deck.drawCard();
        var card1 = this.deck.drawCard();
        this.player.hit(a_card);
        this.player.hit(card1);  //Initialises player's hand and reveals it
        document.getElementById('player-prompt').innerHTML = 'You drew: ';
        this.player.revealHand('player-cards'); //Reveals players hand
        document.getElementById('player-value').innerHTML = 'with a value of: ' + this.player.getValue(); //And shows value
        a_card = this.deck.drawCard();
        card1 = this.deck.drawCard();
        this.dealer.hit(a_card);
        this.dealer.hit(card1);  //Intialises dealer's hand at the start
        document.getElementById('dealer-prompt').innerHTML = 'First dealer card is ';
        this.dealer.revealFirst();  //Reveals his firstcard
    }
    decideWin(){
        var playerValue = this.player.getValue();
        var dealerValue = this.dealer.getValue();
        if (playerValue > dealerValue){
            return true;  //true means player won
        }
        else if (playerValue == dealerValue){
            return undefined;  //undefined means a draw
        }
        else{
            return false;  //false means dealer won
        }
    }
    playerWin(){  //For when the player wins
        document.getElementById('prompt').innerHTML = 'You won, the pot had: ' + this.pot;  //Tells them the value of the pot
        this.player.addMoney(this.pot);  //Adds the pot to their balance
        this.checkBalance();  //Tells them their balance
        this.pot = 0;   //Resets the pot
        this.checkPot();
    }
    Draw(){  //For when the player and the dealer draw
        document.getElementById('prompt').innerHTML = 'You drew with the dealer, the pot had: ' + this.pot  //Tells them the value of the pot
        var a = this.pot;
        a = Math.floor((a/2));  //Splits the money
        this.player.addMoney(a);  //Adds the money
        this.checkBalance();  //Tells them their balance
        this.pot = 0;   //Resets the pot
        this.checkPot()
    }
    dealerWin(){  //For when the dealer wins
        document.getElementById('prompt').innerHTML += 'You lost, the pot had: ' + this.pot;  //Tells them the value of the pot
        this.checkBalance();  //Tells them the value of their balance
        this.pot = 0;   //Resets the pot
        this.checkPot();
    }
    topUp(){
        var amount = document.getElementById('myInput').value;   
        if (amount == ''){
            document.getElementById('prompt').innerHTML = 'Invalid input, how much would you like to add?'
            return
        }
        this.player.addMoney(amount);
        this.checkBalance();
        document.getElementById('prompt').innerHTML = 'What would you like to do? '  
        document.getElementById('input-button').onclick = playerTurn;
    }
}
    
function printControls(){
    var new_html = 'Here are the controls: 1 = Hit    2 = Stay (ends your turn)     3 = Bet     4 = Top up balance';
    document.getElementById('controls').innerHTML = new_html
}

var suits, numbers, deck_list, suit, num, liveDeck, playerHand, dealerHand, balance, livePlayer, liveDealer, liveGame, running, Pturn, dealerWon, winnerOveride, DTurn;

function loadGame(){
    document.getElementById('start-button').onclick = null;
    suits = ['Clubs','Diamonds','Hearts','Spades'];
    numbers = [1,2,3,4,5,6,7,8,9,10,11,12];
    deck_list = [];
    for (var i=0; i < suits.length; i++){
        suit = suits[i];
        for (var j=0; j < numbers.length; j++){
            num = numbers[j];
            deck_list.push(new card(suit,num))  //Initialises all the cards
        }
    }
    liveDeck = new deck(deck_list);  //Initialises the deck
    playerHand = new hand();
    dealerHand = new hand();
    document.getElementById('prompt').innerHTML = 'How much money would you like to start with? (integer) '
    document.getElementById('input-button').onclick = loadBalance;
    return
}

function loadBalance(){
    balance = document.getElementById('myInput').value;   
    if (balance == ''){
        document.getElementById('prompt').innerHTML = 'Invalid input'
        return
    }
    balance = Math.floor(balance);   //Gets player balance 
    livePlayer = new player(playerHand,balance);
    liveDealer = new dealer(dealerHand);
    liveGame = new game(liveDeck,livePlayer,liveDealer);  //Initialises all classes into big class
    running = true;
    printControls();
    liveGame.firstTurn();  //Sets up first turn
    liveGame.checkPot();
    liveGame.checkBalance();
    dealerWon = false;   //Initialises variables for the loop
    winnerOveride = false;
    document.getElementById('input-button').onclick = playerTurn;
    document.getElementById('prompt').innerHTML = 'What would you like to do? '    
}

function roundStart(){
    liveGame.roundStart();
    document.getElementById('input-button').onclick = playerTurn;
}

function playerTurn(){
    var control = Number(document.getElementById('myInput').value);   //Runs through player controls while it is the player's turn
    if (typeof control != 'number'){   
        document.getElementById('prompt').innerHTML = 'Invalid input'
        return
    }
    control = Number(control);
    if (control == 1){
        liveGame.playerDraw();
        if (liveGame.checkPlayerBust() == true){
            document.getElementById('prompt').innerHTML = 'You went bust. ';
            liveGame.dealerWin();
            winnerOveride = false;
            document.getElementById('prompt').innerHTML += ' Press the confirm button when you are ready to start';
            document.getElementById('input-button').onclick = roundStart;
            return
        }
        return
    }
    else if (control == 2){
        document.getElementById('prompt').innerHTML = 'You stayed, click confirm to see dealer turn';
        document.getElementById('input-button').onclick = dealerTurn;
        return
    }
    else if (control == 3){
        document.getElementById('prompt').innerHTML = 'How much would you like to bet? ';
        document.getElementById('input-button').onclick = playerBetTrigger; //triggers livegame player bet
        return
    }
    else if (control == 4){
        document.getElementById('prompt').innerHTML = 'How much would you like to add? ';
        document.getElementById('input-button').onclick = playerTopUpTrigger; //triggers livegame player bet
        return
    }
    else{
        document.getElementById('prompt').innerHTML = 'Invalid prompt'
        return
    }
}

function playerBetTrigger(){
    liveGame.playerBet()
    return
}

function playerTopUpTrigger(){
    liveGame.topUp()
    return
}

function dealerTurn(){
    DTurn = liveGame.dealerTurn();
    if (liveGame.checkDealerBust() == true){
        winnerOveride = true;
    }
    if (DTurn == true && winnerOveride == false){
        return
    }
    else{
        document.getElementById('prompt').innerHTML = 'Dealer turn is done, click confirm to decide winner';
        document.getElementById('input-button').onclick = decideWinner;
        return
    }
}
function decideWinner(){
    winner = liveGame.decideWin();
    if (winner == true || winnerOveride == true){
        liveGame.playerWin();
    }
    else if (winner === undefined){
        liveGame.Draw();
    }
    else{
        liveGame.dealerWin();
    }
    dealerWon = false;
    winnerOveride = false;
    document.getElementById('input-button').onclick = roundStart;
    document.getElementById('prompt').innerHTML += 'Press confirm when you are ready to start ';
    return
}
