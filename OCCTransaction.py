class Transaction:
    def __init__(self, id):
        self.id = id
        self.startTS = None
        self.validationTS = None
        self.finishTS = None
        self.writeArr = []
        self.readArr = []