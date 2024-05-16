def validate_ml_solution_builder(request):
    """
    check if the request body is valid
    :param request:
    :return: True if valid
    """
    if not isinstance(request, dict):
        return False

    if 'train_data' not in request:
        return False

    if 'name' not in request:
        return False

    if (not isinstance(request['name'], str) or not isinstance(request['train_data'], list)
            or not all(isinstance(item, int) for item in request['train_data'])):
        return False

    return True
