# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 22:36:12 2022

@author: COCKENPOT
"""

class Card:
    
    def _init_(self,suit,value):
        self.suit = ['heart','diamond','club','spade'][suit]
        self.value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][value]
        #the score of the card depend on its value
        if self.value == 'A':
            self.card_value = 11
        elif self.value == 'J' or self.value =='Q' or self.value == 'K':
            self.card_value = 10
        else:
            self.card_value = int(value)+1
            
    def show(self, hidden = False):
        
        #for the dealer's hidden card
        if hidden :
            print('┌───────┐')
            print('|   _   |')
            print('|  / \  |')
            print('|     | |')
            print('|    /  |')
            print('|   .   |')
            print('└───────┘') 
        #for the cards we can see
        else :
            suits_values = {"spade":"\u2664", "heart":"\u2661", "club": "\u2667", "diamond": "\u2662"}
            print('┌───────┐')
            print(f'| {self.value:<2}    |')
            print('|       |')
            print('|   {}   |'.format(suits_values[self.suit]))
            print('|       |')
            print(f'|    {self.value:>2} |')
            print('└───────┘')
            
import random

class Deck:
    
    def _init_(self):
        self.cards = Deck.generate()
        
    def generate():
        # 52 cards of the 4 suits
        cards = []
        for values in range(13):
            for suits in range(4):
                c = Card()
                c._init_(suits, values)
                cards.append(c)
        return cards
    
    def draw(self):
        #choose 1 card in the deck to add it to the player's hand
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
    
    def number_of_cards(self):
        return len(self.cards)
    
    
class Player:
    
    def _init_(self, deck, name = '', plays = True, dealer = False):
        self.cards = [] #cards of the player
        self.dealer = dealer #if this player is the dealer or not
        self.deck = deck
        self.bet = 2 #initial bet
        self.wallet = 50 #original amount you can bet, dealer's one doesn't matter
        self.score = 0 #initial score
        if dealer == True:
            self.name = "Dealer"
        else :
            self.name =  name #name of the player
        self.bust = (plays == False) #turns True if the player is busted or if the player don't play (depending on the nb of players)
    
    #decrease the score if the player has a A and if needed 
    def check_score(self):
        counter = 0 #nb of A
        self.score = 0
        for card in self.cards:
            if card.card_value == 11: #initial value of A is 11
                counter+=1
            self.score += card.card_value
            
        while counter != 0 and self.score > 21: #if there are some A and the score is too high
            counter -=1
            self.score -= 10 #the score of A becomes 1
        return self.score
    
    #if the player has a bj
    def check_bj(self,status):
        if status == True:
            print(self.name + " has a blackjack ! Congrats, you win $"+str(1.5*self.bet))
            self.wallet+= 1.5*self.bet
        
    #when his turn comes, the player can choose to hit or stand
    #return true if busted, false ow
    def hit(self):
        self.cards.append(self.deck.draw())
        self.check_score()
        if self.score > 21:
            self.bust = True
            return True #busted !!
        return False
    
    #In first, each player have 2 cards. If the amount he has on 2 cards = 21, he has a blackjack.
    #return true if blackjack, false ow
    def deal(self, dealer = False):
        c = self.deck.draw()
        self.cards.append(c)
        
        while dealer == True and self.cards[0].card_value == 11: #the 1st card of the dealer's hand cannot be an A
            self.cards = []
            self.deck = self.deck._init_()
            c = self.deck.draw()
            self.cards.append(c)
            
        c = self.deck.draw()    
        self.cards.append(c)
        self.check_score()
        if self.score == 21 and dealer == False :
            print(self.name + ", you have a blackjack !")
            for card in self.cards:
                card.show()
            return True #blackjack !!
        return False
    
    def bet_for_one_player(self, plays = True):
        if plays == True: #for the players who don't play
            mispelling = True
            while mispelling == True:
                print(self.name + ", how much do you want to bet on this game ? You have $"+str(self.wallet)+" remaining.")
                bet = input("Please enter an integer, minimum is $2 : ")
                try :
                    bet = int(bet)
                    if bet<=self.wallet and bet>=2:
                        self.bet = bet
                        mispelling = False
                    else:
                        print("Your bet needs to be more than $2 and equal or less than the money remaining in your wallet.")
                except ValueError:
                    print("Please enter an integer")
    
    #shows the cards and the score of the player    
    def show(self, final = False):
        hidden = False
        if self.dealer:
            print("DEALER'S CARDS")
            if final == False : #show all the cards of the dealer's hand only if it's the end
                hidden = True
        else:
            print("YOUR CARDS")
        
        if hidden == False:
            for i in self.cards:
                i.show()
            print("SCORE : " + str(self.score))
        else:
            self.cards[0].show()
            self.cards[1].show(hidden)
        input()
    
    #shows the bet and the money remaining in the player's wallet
    def final_show(self):
        print("Your bet was $"+str(self.bet)+" and your wallet is now at $"+str(self.wallet)+".")
                
import os

class Blackjack:
    
    def _init_(self, nb_p, nbOfRounds):
        self.deck = Deck()
        self.deck._init_()
        self.nbOfPlayers = int(nb_p)
        self.nbOfRounds = int(nbOfRounds)
        
        self.dealer = Player()
        self.dealer._init_(self.deck, '', True, True)
        
        name_p1 = input("Name of player 1 : ")
        self.player1 = Player()
        self.player1._init_(self.deck, name_p1)
        self.player1.bet_for_one_player()
        
        name_p2 = name_p3 = name_p4 = ''
        self.player2 = Player()
        self.player2._init_(self.deck, name_p2, (self.nbOfPlayers > 1)) #plays only if there are more than 1 player
        self.player3 = Player()
        self.player3._init_(self.deck, name_p3, (self.nbOfPlayers > 2))
        self.player4 = Player()
        self.player4._init_(self.deck, name_p4, (self.nbOfPlayers > 3)) 
        #players 2,3,4 are always created but do not play if the nbOfPlayers is less
        
        if self.nbOfPlayers>1:
            name_p2 = input('Name of player 2 : ')
            self.player2.name = name_p2
            self.player2.bet_for_one_player()
        if self.nbOfPlayers>2:
            name_p3 = input('Name of player 3 : ')
            self.player3.name = name_p3
            self.player3.bet_for_one_player()
        if self.nbOfPlayers>3:
            name_p4 = input('Name of player 4 : ')
            self.player4.name = name_p4
            self.player4.bet_for_one_player()
            
            
    def switch(action, player):
        action = action.upper()
        if action =='D':
            if player.wallet >= 2*player.bet:
                player.bet += player.bet #the bet is doubled
            else :
                print("You can't double your bet as you don't have enough money left.")
            action = 'H' #you can double your bet but you have to hit then
        if action == 'H':
            bust = player.hit()
            player.check_score()
            player.show()
            if bust == True:
                print(player.name+" busted ! You loose $"+str(player.bet)+".")
                player.wallet -= player.bet
                return True
            return False
        if action == 'S':
            return True
    
    #same for dealer, return True if the dealer busted and false ow
    def reveal(self):
        self.dealer.show(True)
        self.dealer.check_score()
        while self.dealer.score < 17:
            bust = self.dealer.hit()
            self.dealer.show(True)
            if bust == True:
                print("Dealer busted ! Everyone win his bet if not busted.")
                self.player1.wallet += self.player1.bet*(self.player1.bust==False)
                self.player2.wallet += self.player1.bet*(self.player2.bust==False)
                self.player3.wallet += self.player1.bet*(self.player3.bust==False)
                self.player4.wallet += self.player1.bet*(self.player4.bust==False)
                return True
            if self.dealer.score == 21:
                print("Dealer has blackjack ! You all loose your bet.")
                self.player1.wallet -= self.player1.bet*(self.player1.bust==False)
                self.player2.wallet -= self.player1.bet*(self.player2.bust==False)
                self.player3.wallet -= self.player1.bet*(self.player3.bust==False)
                self.player4.wallet -= self.player1.bet*(self.player4.bust==False)
        return 
            
    #check every remaining money of the players    
    #returns True if one of the wallet is over, false ow
    def check_scores(self):
        print(self.player1.name + "wallet : "+ str(self.player1.wallet))
        if self.nbOfPlayers>1:
            print(self.player2.name + "wallet : "+ str(self.player2.wallet))
        if self.nbOfPlayers>2:
            print(self.player3.name + "wallet : "+ str(self.player3.wallet))
        if self.nbOfPlayers>3:
            print(self.player4.name + "wallet : "+ str(self.player4.wallet))
        if self.player1.wallet<=0 or self.player2.wallet<=0 or self.player3.wallet<=0 or self.player4.wallet<=0:
            return True
        
    #game for one player, after deal(), return True if blackjack, False ow
    def round_for_one_player(self, player):
        if player.bust == False :
            self.dealer.show()
            print("It's "+ player.name +"'s turn !")
            player.show()
        
            rnd = False
        
            while rnd == False: #while player do not stand or have a blackjack
                bounce = False
                while bounce==False:
                    print("Hit or stand ?")
                    choice = input("Write H to hit, S to stand or D to double : ")
                    choice = choice.upper()
                    if choice != 'H' and choice != 'S' and choice != 'D':
                        os.system('cls')
                        print("Wrong choice! Try Again")
                    else:
                        bounce = True
                rnd = Blackjack.switch(choice, player)
                if player.score == 21:
                    print(player.name + ", you have a blackjack !")
                    input()
                    return True
            input()
        return False
    
    #check if anyone has a bj
    def check(self,p1_st,p2_st,p3_st,p4_st):
        self.player1.check_bj(p1_st)
        self.player2.check_bj(p2_st)
        self.player3.check_bj(p3_st)
        self.player4.check_bj(p4_st)
        end = p1_st == True or p2_st == True or p3_st == True or p4_st == True
        return end
    
    def final_scores(self, player):
        if player.bust == False:
            sc = self.dealer.score
            print(player.name+" : ")
            if player.score == sc:
                print("It's a push ! ("+ str(sc)+"). You keep your bet.")
            elif player.score<sc:
                print("You lost your bet. ("+str(player.score)+" against "+str(sc)+")")
                player.wallet -= player.bet
            else :
                print("You win ! ("+str(player.score)+" against "+str(sc)+")")
                player.wallet += player.bet
    
    def play(self):
        
        #throw all player's card if there are
        self.dealer.cards = []
        self.player1.cards = []
        self.player2.cards = []
        self.player3.cards = []
        self.player4.cards = []
        
        #every player draw 2 cards
        self.dealer.deal(True)
        p1_st = self.player1.deal()
        p2_st = p3_st = p4_st = False
        if self.nbOfPlayers > 1:
            p2_st = self.player2.deal()
        if self.nbOfPlayers > 2:
            p3_st = self.player3.deal()
        if self.nbOfPlayers > 3:
            p4_st = self.player4.deal()
        
        end = self.check(p1_st, p2_st, p3_st, p4_st)
        if end ==  True:
            return True
        
        #every player
        p1_st = self.round_for_one_player(self.player1)
        p2_st = self.round_for_one_player(self.player2)
        p3_st = self.round_for_one_player(self.player3)
        p4_st = self.round_for_one_player(self.player4)
        #reveal
        
        end = self.check(p1_st, p2_st, p3_st, p4_st)
        if end ==  True:
            return True
        
        end = self.reveal()
        if end == True:
            return True
        input()
        self.final_scores(self.player1)
        self.final_scores(self.player2)
        self.final_scores(self.player3)
        self.final_scores(self.player4)
        return False
        
    #return true if the wallet of one of the players is too low to bet again
    def check_wallet(self):
        return self.player1.wallet < 2 or self.player2.wallet < 2 or self.player3.wallet < 2 or self.player4.wallet < 2
        
    def game(self):
        rnd = 1
        self.play()
        
        while rnd<self.nbOfRounds and self.check_wallet()==False:
            
            #reboot bust parameter
            self.player1.bust = False
            self.player2.bust = self.nbOfPlayers<2
            self.player3.bust = self.nbOfPlayers<3
            self.player4.bust = self.nbOfPlayers<4
            
            #bets
            self.player1.bet_for_one_player()
            self.player2.bet_for_one_player(self.player2.bust == False)
            self.player3.bet_for_one_player(self.player3.bust == False)
            self.player4.bet_for_one_player(self.player4.bust == False)
            
            self.play()
            rnd+=1
            
        print("The game is over !")
        print("Here are the final scores : ")
        
        first = self.player1
        second = self.player2
        third = self.player3
        fourth = self.player4
        w1 = self.player1.wallet
        w2 = self.player2.wallet
        w3 = self.player3.wallet
        w4 = self.player4.wallet
        
        if self.nbOfPlayers == 1:
            print("Your wallet is at $"+str(w1)+".")
            if(w1 < 50):
                print("You lost $"+str(50-w1)+"... Don't play in real Casinos for now !")
            elif(w1 == 50):
                print("Did you... Even played ? At least you don't lost any money")
            else:
                print("You are ready to play in real Casinos ! You won $"+str(w1-50)+" in "+str(self.nbOfRounds)+" rounds. Congrats !")
        if self.nbOfPlayers == 2:
            if(w1 == w2):
                print("You are ex-aequo with a wallet of $"+str(w1)+" !")
                if(w1 < 50):
                    print("Both of you lost $"+str(50-w1)+"... Don't play in real Casinos for now !")
                else:
                    print("You are ready to play in real Casinos ! You won $"+str(w1-50)+" in "+str(self.nbOfRounds)+" rounds. Congrats !")
            else:
                if(w1<w2):
                    first = self.player2
                    second = self.player1
                print("First : "+first.name+ " with a wallet of $"+str(first.wallet)+" ! Congrats !")
                print(second.name + " has a final wallet of $"+str(second.wallet)+" ! Good game !")
        if self.nbOfPlayers == 3:
            if w2>w1 and w2>=w3:
                first = self.player2
                second = self.player1
                if w3>w1:
                    second = self.player3
                    third = self.player1
            elif w3>w1 and w3>w2:
                first = self.player3
                third = self.player1
                if w1>=w2:
                    second = self.player1
                    third = self.player2
            elif w3>w2:
                second = self.player3
                third = self.player2
            print("First : "+first.name+ " with a wallet of $"+str(first.wallet)+" ! Congrats !")
            print("Second : "+second.name +" with a wallet of $"+str(second.wallet)+" ! Congrats !")
            print(third.name +" has a final wallet of $"+str(third.wallet)+" ! Good game !")
        if self.nbOfPlayers >= 4:
            if w2>w1 and w2>=w3 and w2>=w4:
                first = self.player2
                second = self.player1
                if w3>w1 and w3>=w4:
                    second = self.player3
                    third = self.player1
                    if w4>w1:
                        third = self.player4
                        fourth = self.player1
                elif w4>w1 and w4>w3:
                    second = self.player4
                    fourth = self.player1
                    if w1>=w3:
                        third = self.player1
                        fourth = self.player3
                elif w4>w3:
                    third = self.player4
                    fourth = self.player3
            elif w3>w1 and w3>w2 and w3>=w4:
                first = self.player3
                third = self.player1
                if w1>=w2 and w1>=w4:
                    second = self.player1
                    third = self.player2
                    if w4>w2:
                        third = self.player4
                        fourth = self.player2
                elif w4>w1 and w4>w2:
                    second = self.player4
                    fourth = self.player2
                    if w2>w1:
                        third = self.player2
                        fourth = self.player1
                elif w4>w1:
                    third = self.player4
                    fourth = self.player1
            elif w4>w1 and w4>w2 and w4>w3:
                first = self.player4
                fourth = self.player1
                if w1>=w2 and w1>=w3:
                    second = self.player1
                    fourth = self.player2
                    if w2>=w3:
                        third = self.player2
                        fourth = self.player3
                elif w3>w2 and w3>w1:
                    second = self.player3
                    fourth = self.player2
                    if w2>w1:
                        third = self.player2
                        fourth = self.player1
                elif w1>=w3:
                    third = self.player1
                    fourth = self.player4
            elif w3>w2 and w3>=w4:
                second = self.player3
                third = self.player2
                if w4>w2:
                    third = self.player4
                    fourth = self.player2
            elif w4>w2 and w4>w3:
                second = self.player4
                fourth = self.player2
                if w2>w3:
                    third = self.player2
                    fourth = self.player3
            elif w4>w3:
                third = self.player4
                fourth = self.player3
            print("First : "+first.name+ " with a wallet of $"+str(first.wallet)+" ! Congrats !")
            print("Second : "+second.name +" with a wallet of $"+str(second.wallet)+" ! Congrats !")
            print("Third : "+third.name +" with a wallet of $"+str(third.wallet)+" !")
            print(fourth.name +" has a final wallet of $"+str(fourth.wallet)+" ! Good game !")

        
def beggining():
    mispelling = True
    os.system('cls')
    while mispelling == True:
        print("How many players will play ? The maximum is 4.")
        nb_p = input("type the number of players : ")
        try:
            nb = int(nb_p)
            if nb == 1 or nb == 2 or nb == 3 or nb == 4:
                mispelling = False
            else:
                os.system('cls')
                ("Please write a number between 1 and 4.")
        except ValueError:
            print("Please enter an integer")
    mispelling = True
    os.system('cls')
    while mispelling == True:
        print()
        print("You all " + str(nb_p) + " start the party with $50 in your wallet. The game will finish if one of you don't have enought money in your wallet to continue.")
        print("For that the game lasts less time, please choose how many rounds do you want to play.")
        nb_r = input("type the number of rounds : ")
        try:
            nb_r = int(nb_r)
            mispelling = False
        except ValueError :
            print("Please enter an integer")
    bj = Blackjack()
    bj._init_(nb_p,nb_r)
    bj.game()
    
def essais():
    bj = Blackjack()
    bj._init_(1,2)
    bj.game()