class RunInformation:
    def __init__(self, iterations=0, input_length=0, uuid='', gaps=False, is_running_gaps=False, max_steps=1,
                 identifier="", configuration_id=None, save=""):
        self.iterations = iterations
        self.uuid = uuid
        self.runtime = 0
        self.input_length = input_length
        self.configuration_id = configuration_id
        self.save = save
        self.image = ""
        self.gaps = gaps
        self.is_running_gaps = is_running_gaps
        self.loss = 1
        self.max_steps = max_steps
        self.steps = 0
        self.identifier = identifier

    def get_progress(self, epoch):
        scaler = self.steps / self.max_steps
        current_inline_progress = 1 / self.max_steps
        return (scaler + (epoch / self.iterations) * current_inline_progress) * 100

    def get_uuid(self):
        return self.uuid

    def get_iterations(self):
        return self.iterations

    def get_input_length(self):
        return self.input_length

    def save_model(self, base64_string: str):
        self.save = base64_string

    def get_save(self):
        return self.save

    def increment_step(self):
        self.steps = self.steps + 1

    def as_dict(self):
        """Utility method to easily convert the instance to a dictionary, if needed for compatibility."""
        return vars(self)
