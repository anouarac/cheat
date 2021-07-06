class Card:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return f"{self.type}{self.value}"

    #TODO: define getters and setters