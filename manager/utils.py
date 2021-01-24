def check_type(object,type_to_check):
    if not isinstance(object,type_to_check):
        raise TypeError('This object is not a ' + str(type_to_check) + ' but a ' + str(type(object)))