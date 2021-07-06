class Card:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return f"{self.type}{self.value}"

    def __eq__(self, other):
        return str(self) == str(other)

    #TODO: define getters and setters