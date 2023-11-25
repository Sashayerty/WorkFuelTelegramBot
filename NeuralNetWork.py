class NeuralNetWork:
    def __init__(self, data: list):
        self.data = data
        self.medium = 0

    def medium_of_list(self):
        self.medium = sum(self.data) // len(self.data)
        return self.medium

    def relevant_of_prod(self):
        return True if self.medium > 5 else False