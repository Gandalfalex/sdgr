from tsaAPI.model_generation.model_types import ModelTypes


class RunInformation:
    def __init__(self, input_length=0, uuid='', gaps=False, configuration_id=None, split=5,
                 display_mode: ModelTypes = ModelTypes.SPLITTING):
        self.uuid = uuid
        self.runtime = 0
        self.input_length = input_length
        self.configuration_id = configuration_id
        self.gaps = gaps
        self.split = 5
        self.display_mode = display_mode

    def get_input_length(self):
        return self.input_length

    def as_dict(self):
        """Utility method to easily convert the instance to a dictionary, if needed for compatibility."""
        return vars(self)
