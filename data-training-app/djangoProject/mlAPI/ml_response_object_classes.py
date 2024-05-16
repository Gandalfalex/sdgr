class SignalDataDTO:
    def __init__(self, name:str, values:dict):
        self.name = name
        self.values = values

    def get_data(self):
        return {
            "name": self.name,
            "data": self.values
        }