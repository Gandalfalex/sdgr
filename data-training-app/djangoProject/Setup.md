This file will help you to build the django api


urls.py in main folder for main paths

urls.py in app folder for specific path



commands:

````bash
python manage.py makemigrations

python manage.py migrate

python manage.py runserver

python manage.py createsuperuser
````

## saving m:n
save object first (with foreign key if exists), add all necessary information,
after saved, add your other m:n objects


# JWT Support
use for classes,  @jwt_authenticated for normal
```` bash
@method_decorator(jwt_authenticated, name='dispatch')
````

# Extension of algorithm
The extension of algorithm is done in the via the GeneralMLModel.
After defining it, save if with a unique name in database and method
```` python
mlAPI.service.ml_runner extend model_strategy.get_ml_model
```` 

do the same for the Preprocessing.
```` python
shared.preprocessing extend preprocessing_strategy.get_preprocessor
```` 


## speed up with gpu:
https://stackoverflow.com/questions/45662253/can-i-run-keras-model-on-gpu


## TODO

Adjust length of training data, save reduction value also in Training data object, later needed to restore original value!
Also, implement iteration and accuracy limit
Save length of data also in db

find a way to build the form of the data, or simply cut it.

Need to rework many methods, good luck!


when deleting solution, also delete the .keras file!


TODO add django environment variable to db

kind of a dirty workaround, use prefix for mails in validation forms