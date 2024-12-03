UTIL_CARD_VALUES = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
                    'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def next_card(self):
        if isinstance(self.value, int):
            if self.value == 10:
                return Card(self.suit, "J")
            else:
                return Card(self.suit, self.value + 1)
        else:
            if self.value == "J":
                return Card(self.suit, "Q")
            elif self.value == "Q":
                return Card(self.suit, "K")
            elif self.value == "K":
                return Card(self.suit, "A")


    def __lt__(self, other):
        return UTIL_CARD_VALUES[self.value] < UTIL_CARD_VALUES[other.value]

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return UTIL_CARD_VALUES[self.value] == UTIL_CARD_VALUES[other.value]

    def __gt__(self, other):
        return UTIL_CARD_VALUES[self.value] > UTIL_CARD_VALUES[other.value]

    def __ge__(self, other):
        if other is None:
            return False
        else:
            return UTIL_CARD_VALUES[self.value] >= UTIL_CARD_VALUES[other.value]

    def __le__(self, other):
        if other is None:
            return False
        else:
            return UTIL_CARD_VALUES[self.value] <= UTIL_CARD_VALUES[other.value]