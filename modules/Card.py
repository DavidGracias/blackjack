class Card:

    # constants: Card()
    suitSym     = None # 0, 1, 2, 3
    val         = None # 1, ..., 10
    deckNum     = None
    number      = None # card id
    name        = None # A, 2, ..., 10, J, Q, K

    def __init__(self, id: int):
        self.suitSym = (id // 13) % 4
        self.val = (id % 13)+1
        self.deckNum = id // 52
        self.number = id

        if self.val == 1:
            self.name = "A"
        elif 2 <= self.val <= 10:
            self.name = str(self.val)
        elif 10 <= self.val <= 13:
            if self.val == 11: self.name = "J"
            if self.val == 12: self.name = "Q"
            if self.val == 13: self.name = "K"
            self.val = 10
    
    def value(self) -> int: return self.val
    
    def suit(self) -> int: return self.suitSym

    def deckNumber(self) -> int: return self.deckNum
    def id(self) -> int: return self.number

    # comparative functions
    def __eq__(self, other):  return self.name == other.name
    def __neq__(self, other): return not (self == other)


    def __str__(self): return self.name
    
# end of Card() class