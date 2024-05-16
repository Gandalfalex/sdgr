class TSAValueElement:
    def __init__(self, element_id: int, name: str, values: [], levels: int, element_type: str):
        self.element_id = element_id
        self.name = name
        self.values = values
        self.levels = levels
        self.element_type = element_type

    def get_data(self):
        return {
            "id": self.element_id,
            "name": self.name,
            "levels": self.levels,
            "values": self.values,
            "type": self.element_type
        }
