from card import Card

class Hand:
    def __init__(self, cards=[]):
        self.cards = cards

    def add(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.add(card)

    def delete(self, card):
        self.cards.remove(card)

    def delete_cards(self, cards):
        for card in cards:
            self.delete(card)
    
    def clear_sets(self):
        counter = [0 for i in range(14)]
        for card in self.cards:
            counter[card.value] += 1
        for i in range(1, 14):
            if counter[i] == 4:
                for c in ["S","H","D","C"]:
                    self.delete(Card(c,i))

    def size(self):
        return len(self.cards)

    def empty(self):
        return not self.cards

    def __str__(self):
        return "[ " + ", ".join([str(card) for card in self.cards]) + " ]"