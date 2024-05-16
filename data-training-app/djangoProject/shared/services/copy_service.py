from shared.models import Preprocessor


def create_copy_of_preprocessor(original, model):
    original_processing = original.processing
    preprocessor = Preprocessor(type=original_processing.type, specific_config=original_processing.specific_config)
    preprocessor.save()
    model.processing = preprocessor
    model.save()
    return model


def copy_train_data(original, model):
    for train_data in original.train_data.all():
        model.train_data.add(train_data)
    model.save()
    return model
