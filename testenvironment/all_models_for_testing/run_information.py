class RunInformation:
    prediction = None
    loss = 1

    def __init__(self, iterations=0, input_length=0, max_steps=1, get_all=False, precision=0, forcast=False):
        self.iterations = iterations
        self.runtime = 0
        self.input_length = input_length
        self.loss = 0
        self.max_steps = max_steps
        self.steps = 0
        self.split = 4
        self.get_all = False
        self.precision = precision
        self.forcast = forcast

    def get_progress(self, epoch):
        scaler = self.steps / self.max_steps
        current_inline_progress = 1 / self.max_steps
        return (scaler + (epoch / self.iterations) * current_inline_progress) * 100

    def get_iterations(self):
        return self.iterations

    def get_input_length(self):
        return self.input_length

    def increment_step(self):
        self.steps = self.steps + 1

    def as_dict(self):
        return {
            "loss": self.loss
        }

    def get_prediction(self):
        return self.prediction

    def set_prediction(self, prediction):
        self.prediction = prediction

    def set_loss(self, loss):
        self.loss = loss

    def set_forcast(self, forcast):
        self.forcast = forcast

    def get_forcast(self):
        return self.forcast
