import random
from .Player import Player
from .Hand import Hand
from .Card import Card

class Blackjack:
    deck = Hand()
    minimum_bet = 1
    players = []
    dealer = Player("Dealer")
    numDecks = 1
    isSim = False
    numRounds = 0

    # A, 2, 3, ..., 10, J, Q, K
    cards = [ Card(i) for i in range(13) ]

    def __init__(self, numDecks = 2, isSim = False):
        self.players = []
        self.numDecks = numDecks if numDecks > 0 else 1
        self.isSim = isSim
        self.numRounds = 0

    def addPlayer(self, name="Player"):
        self.players.append(Player(name))

    def start(self):
        if not self.isSim:
            print("")
        self.shuffleDeck()

        # create one player (if needed)
        if not len(self.players): self.addPlayer()

        # run a round of Blackjack
        while self.players:
            print("")
            self.newRound()

    def shuffleDeck(self):
        if not self.isSim:
            print("---shuffling deck now---")
            print("")
        self.deck = Hand()
        for id in range(self.numDecks * 52): self.deck.add( Card(id) )
        self.deck.shuffle()

        burned = self.deck.pop() # burn top card

    def handleBets(self):
        # helper function for below
        def isNaN(num):
            try:
                float(num)
                return False
            except ValueError: return True
        
        if self.isSim:
            bet = self.minimum_bet
            self.players[0].updateBet(int(bet))
        else:
            for i in range(len(self.players)-1, -1, -1):
                if self.numRounds == 1: bet = input(f"{self.players[i].getName()}, please enter your bet: $")
                else: bet = input(f"{self.players[i].getName()}, if you'd like to play again please enter your bet, otherwise, type \"quit\": $")
                while 1:
                    if isNaN(bet):
                        # tried to enter a number
                        if any(char.isdigit() for char in bet):
                            bet = input(f"{self.players[i].getName()}, please enter an dollar amount bet (ex. $10.00): $")
                        # they are looking to exit the game
                        elif bet == "quit":
                            self.players = self.players[:i] + self.players[i+1:]
                            break
                        else:
                            again = " again " if self.numRounds != 1 else " "
                            bet = input(f"{self.players[i].getName()}, if you'd like to play{again}please enter your bet, otherwise, type \"quit\": $")
                    # is a float, but is invalid bet
                    elif round(float(bet), 2) < self.minimum_bet:
                        bet = input(f"{self.players[i].getName()}, please enter a bet above the minimum bet of (${self.minimum_bet}): $")
                    # valid bet, exit loop
                    else: break
                if bet != "quit":
                    self.players[i].updateBet(round(float(bet), 2))

    def handleResults(self):
        if not self.isSim:
            print(f"Dealer's hand ({self.dealer.value()}):")
            print("                                   ", self.dealer.getHand())

        playerBlackjack = False
        for player in self.players:
            output = ""
            winnings = 0
            i = 0
            curHand = player.getHand(i)
            while curHand:
                playerVal = "{:02d}".format(curHand.value())

                if curHand.value() > 21:
                    output += f"  [Loss: Player bust ({playerVal})         ]"
                    winnings -= player.getBet()

                elif curHand.value() == self.dealer.value():
                    output += f"  [Tie:  Player ({playerVal}) = Dealer ({self.dealer.value()})]"
                    winnings += 0

                elif self.dealer.value() == 21 and self.dealer.getHand().size() == 2:
                    output +=  "  [Loss: Dealer Blackjack         ]"
                    winnings -= player.getBet()

                elif curHand.value() == 21 and curHand.size() == 2:
                    output +=  "  [Win:  Player Blackjack!!       ]"
                    winnings += 3.0/2.0 * player.getBet()
                    playerBlackjack = True

                elif self.dealer.value() > 21:
                    output +=  "  [Win:  Dealer bust              ]"
                    winnings += player.getBet()

                elif curHand.value() > self.dealer.value():
                    output += f"  [Win:  Player ({playerVal}) > Dealer ({self.dealer.value()})]"
                    winnings += player.getBet()

                elif curHand.value() < self.dealer.value():
                    output += f"  [Loss: Player ({playerVal}) < Dealer ({self.dealer.value()})]"
                    winnings -= player.getBet()

                i += 1
                output += " " + str(curHand) + "\n"
                curHand = player.getHand(i)
            playerBlackjack = playerBlackjack and (i == 1) # one handed blackjack

            player.updateBank(winnings)
            
            # not BlackJack
            if self.isSim and not playerBlackjack: self.updateStrat(player, winnings)


            sym = "+" if winnings >= 0 else "-"
            bankSym = "+" if player.getBank() >= 0 else "-"
            output = player.getName() + f"'s results {sym}${abs(winnings)} (Bank: {bankSym}${abs(player.getBank())}):\n" + output
            if not self.isSim:
                print(output)
    
    def updateStrat(self, player, winnings):
        if winnings == 0: return
        # strat: 0 - hard, 1 - soft, 2 - pair
        # tuple: 0 - hit, 1 - stay, 2 - double, 3 - split

        # strat
        strat_ind = -1

        # row
        row_ind = -1

        # col
        dealerValue = self.dealer.getHand().get(0).value()
        col_ind = dealerValue-1

        # tuple
        tuple_ind = -1
        if player.getFirstMove() == "hit": tuple_ind = 0
        elif player.getFirstMove() == "stay": tuple_ind = 1
        elif player.getFirstMove() == "double": tuple_ind = 2
        elif player.getFirstMove() == "split":  tuple_ind = 3
        else: return # dealer blackjack (player doesn't get a first move)

        # pair policy
        if player.getHand(1) or player.getHand().get(0) == player.getHand().get(1):
            strat_ind = 2
            row_ind = player.getHand().get(0).value()
        # soft policy
        elif Card(0) == player.getHand().get(0) or Card(0) == player.getHand().get(1):
            strat_ind = 1
            other = player.getHand().pop()
            while other == Card(0): other = player.getHand().pop()
            row_ind = other.value()
        # hard policy
        else:
            strat_ind = 0
            row_ind = player.getHand().get(0).value() + player.getHand().get(1).value()

        # print(strat_ind, row_ind, col_ind, tuple_ind, player.getHand())

        t = self.isSim[1][strat_ind].loc[row_ind][col_ind]
        n = t[:tuple_ind] + ((t[tuple_ind][0] + winnings, t[tuple_ind][1]+1),) + t[tuple_ind+1:]
        self.isSim[1][strat_ind].loc[row_ind][col_ind] = n

     
    def newRound(self):
        self.numRounds += 1
        if not self.isSim:
            print("---beggining of round---")

        if self.deck.size() <= self.numDecks * 52 * .2: self.shuffleDeck()

        self.handleBets()
        if len(self.players) == 0: return # exit game if no one else wants to continue playing

        # deal 2 cards to each player
        self.deal()

        dealerFaceCard = self.dealer.getHand().get(0)

        if dealerFaceCard in (self.cards[0:1] + self.cards[9:13]):
            # TODO: implement insurance
            if self.dealer.value() == 21:
                self.endRound()
                return
        
        
        # play each player's turn
        for player in self.players:
            self.playTurn(player)

        # dealer's move (casino rules)
        self.dealerTurn()

        # evaluate who won
        self.endRound()

    def endRound(self):
        if not self.isSim:
            print("--game over---")
            print("")
        
        # updates winnings and displays the results
        self.handleResults()


        for player in self.players: player.resetHands()
        self.dealer.resetHands()

        if not self.isSim:
            print("")
            print("---end of round---")
            print("")

        if self.isSim:
            if self.numRounds % 1000 == 0: # update policy (csv)
                return
        # self.newRound()
                
    def playTurn(self, player):
        player.startTurn()

        # auto-stay on Blackjack
        if player.value() == 21: player.stay()

        displayHand = False

        while player.isTurn():
            validMoves = ["hit"]
            if player.canStay():    validMoves.append("stay")
            if player.canDouble():  validMoves.append("double")
            if player.canSplit():   validMoves.append("split")

            if displayHand:
                if not self.isSim:
                    print(player)
            displayHand = True

            if self.isSim:
                isSoft = Card(0) in player.getHand() and player.getHand().size() == 2
                if isSoft:
                    for i in range(2):
                        second = player.getHand().get(i)
                        if second != Card(0): break

                    # soft policy
                    pass
                else:
                    hardCount = player.value()
                    # hard policy
                    pass
                # TODO: implement isSim mode for policy convergence
                action = random.choice(validMoves)
            else:
                action = input("What would you like to do? " + "/".join(validMoves) + "\n")
                while not action in validMoves:
                    action = input("Please enter a valid move: " + "/".join(validMoves) + "\n")
            player.setFirstMove(action)

            if action == "hit": player.hit(self.deck)
            elif action == "stay": player.stay()
            elif action == "double":
                player.double(self.deck)
                player.updateBet(2 * player.getBet())
            elif action == "split":
                player.split()

            if not self.isSim:
                print("")

    def dealerTurn(self): 
        while self.dealer.value() < 17:
            self.dealer.hit(self.deck)

    def deal(self):
        if not self.isSim:
            print("---dealing cards---")
            print("")
        for _ in range(2):
            for player in self.players + [self.dealer]:
                player.hit(self.deck)
        
        self.printAllHands(False)
        if not self.isSim:
            print("")

    def printAllHands(self, showDealerSecond = False):
        players = self.players

        if not showDealerSecond:
            if not self.isSim:
                print("Dealer's hand: [", self.dealer.getHand().get(0), " X]", sep="")
        else:
            players.insert(0, self.dealer)

        for player in players:
            if not self.isSim:
                print(player)

    def getNextCard(self): return self.deck.pop(0)