---
title: "Write a New Feature: Adding a Database Element"
author: "[Felix Fischer]"
description: "This guide walks through the steps of adding a new ml or tsa algorithm"
tags: ["Python", "SQL", "Feature"]
---

### Create a new File inside the algorithm_implementation package:
Implement a new Model class
```python
class NewModel(GeneralMLModel):
    @save_model_to_db
    def run(self):

        try:
            model = self.train(generator, discriminator, gan_model, latent_dim, data)
            self.save(model)
            n = self.data[0]
            m = self.predict_data(model)
            self.create_image(n, m, "Model after {} iterations".format(self.run_information.get_iterations()))
        except Exception as e:
            logging.error(e)
        return self.run_information

    

    def predict_data_from_model(self):
        model = self.load_model()
        return self.predict_data(model)

    def predict_data(self, model):
        return smoothed_time_series
```
Implement the logic arround the run method, this will be the starting point.

### Add the new class to the model_strategy.py file:

```python
def get_ml_model(model: MLModel):
    match model.pyName:
        case "GAN.py":
            return GAN()
        case "NewModel.py:
            return NewModel()
        case None:
            return None

```
### Lastly, add it into your database
```sql
INSERT INTO ml_model (name, description,"i18n_key", "pyName", created_at, forcasting)
VALUES ('NewModel',
        'This is how to add a new model into you db',
        'new_model',
        'NewModel.py',
        '1990-01-01 00:00:00.000 +0100',
        false);
```

Since its using an i18n key here, add  the description into your translation files.
