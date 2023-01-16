import random
from .Card import Card
class Hand:
    # constants: Hand()
    cards = []

    def __init__(self):
        self.cards = []

    def add(self, card: Card) -> None: self.cards.append( Card( card.id() ) )
    def get(self, i: int) -> Card: return self.cards[i]

    def pop(self, i=0) -> Card: return self.cards.pop(i)

    def clear(self) -> None: self.cards = []
    
    def value(self) -> int:
        isSoft, s = False, 0

        # handle all non-aces
        for card in self.cards:
            if card == Card(0): isSoft = True
            s += card.value()
        
        # handle potential aces
        if isSoft and s+10 <= 21: s += 10

        return s
    
    def canSplit(self) -> bool: return len(self.cards) == 2 and self.cards[0] == self.cards[1]

    def copy(self):
        h = Hand()
        for card in self.cards: h.add(card)
        return h

    def shuffle(self): random.shuffle(self.cards)
    def size(self): return len(self.cards)

    def __contains__(self, v): return v in self.cards
    
    def __str__(self): return "[" + " ".join([str(card) for card in self.cards]) + "]"

# end of Hand() class