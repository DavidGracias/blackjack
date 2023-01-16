from .Hand import Hand
class Player:
        # constants: Player()
        hands = []
        i = 0
        myTurn = False
        max_splits = 1
        bank = 0
        name = ""
        bet = 0
        firstMove = ""

        def __init__(self, name):
            self.hands = [Hand()]
            self.i = 0
            self.name = name
            self.firstMove = ""
        
        def getBet(self): return self.bet
        def updateBet(self, bet): self.bet = bet
        def getBank(self): return self.bank
        def updateBank(self, money): self.bank += money
        def setFirstMove(self, move):
            if self.firstMove == "":
                self.firstMove = move
        def getFirstMove(self): return self.firstMove

        def getName(self): return self.name

        def getHand(self, i=0):
            if i < len(self.hands):
                return self.hands[i]
            return False
        
        def resetHands(self):
            self.hands = [Hand()]
            self.i = 0
            self.firstMove = ""

        def hit(self, deck):
            self.hands[self.i].add( deck.pop() )

            if self.hands[self.i].value() >= 21:
                self.stay()
        
        def canStay(self) -> bool:
            return self.hands[self.i].size() >= 2

        def stay(self):
            if self.i+1 == len(self.hands): self.endTurn()
            else: self.i += 1

        def canDouble(self) -> bool:
            return self.hands[self.i].size() == 2

        def double(self, deck):
            self.hit(deck)
            self.stay()

        def canSplit(self) -> bool:
            if len(self.hands) == self.max_splits+1: return False
            return self.hands[self.i].canSplit()
        
        def split(self):            
            splitHand = Hand()
            splitHand.add( self.hands[self.i].pop(0) )

            self.hands.insert(self.i, splitHand)

        def value(self): return self.hands[self.i].value()

        def startTurn(self): self.myTurn = True
        def endTurn(self): self.myTurn = False

        def isTurn(self) -> bool: return self.myTurn

        def __str__(self):
            return self.name + "'s hand(s): " + " ".join([str(hand) for hand in self.hands])
    
    # end of Player() class