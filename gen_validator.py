
class WrongValueTypeException(Exception):
    def __init__(self, property_name, expected_type: type, actual_type: type):
        super().__init__(
            f'Wrong type for property {property_name}. Expected -> {expected_type}, actual -> {actual_type}'
        )


class MissingRequiredPropertyException(Exception):
    def __init__(self, property_name):
        super().__init__(f'Missing required property {property_name}')


class InvalidEnumPropertyValue(Exception):
    def __init__(self, property_name, allowed, actual):
        super().__init__(f'Invalid value for property {property_name}. Allowed {allowed}, actual {actual}')


class RegexMismatchException(Exception):
    def __init__(self, property_name, regex):
        super().__init__(f'Property -> {property_name} failed regex match -> {regex}')


class WrongPrefixException(Exception):
    def __init__(self, property_name, prefix):
        super().__init__(f'Property -> {property_name} failed prefix validation. Expected prefix {prefix}')


class FailedLowerBoundaryException(Exception):
    def __init__(self, property_name, lower_boundary, actual):
        super().__init__(f'Property -> {property_name} failed lower boundary. Lower boundary -> {lower_boundary}, value -> {actual}')


class FailedUpperBoundaryException(Exception):
    def __init__(self, property_name, upper_boundary, actual):
        super().__init__(f'Property -> {property_name} failed upper boundary. Upper boundary -> {upper_boundary}, value -> {actual}')



def enter_log(property_name: str):
    print(f'Validating property:\t{property_name}')


def l_0_enabled(block):
    """
    field for testing bool
    """
    trace = 'enabled'
    property_name = 'enabled'
    enter_log(trace)
    if property_name not in block.keys():
        raise MissingRequiredPropertyException(trace)
    if not isinstance(block[property_name], bool):
        raise WrongValueTypeException(property_name, bool, type(block[property_name]))


def l_0_enums_checker(block):
    """
    field for testing enums
    """
    trace = 'enums_checker'
    property_name = 'enums_checker'
    enter_log(trace)
    if property_name not in block.keys():
        raise MissingRequiredPropertyException(trace)
    valid_values = [
       'enum_uno',
       'enum_dos',
    ]
    if block[property_name] not in valid_values:
        raise InvalidEnumPropertyValue(property_name, valid_values, block[property_name])


def l_0_services(block):
    trace = 'services'
    property_name = 'services'
    enter_log(trace)
    if property_name not in block.keys():
        raise MissingRequiredPropertyException(trace)
    next_block = block[property_name]
    l_1_nested_broker(next_block)
    l_1_brokers(next_block)
    l_1_consumer(next_block)
    l_1_fisker(next_block)



def l_1_nested_broker(block):
    trace = 'services.nested_broker'
    property_name = 'nested_broker'
    enter_log(trace)
    if property_name not in block.keys():
        return
    next_block = block[property_name]
    l_2_super_nested(next_block)



def l_2_super_nested(block):
    trace = 'services.nested_broker.super_nested'
    property_name = 'super_nested'
    enter_log(trace)
    if property_name not in block.keys():
        raise MissingRequiredPropertyException(trace)
    if not isinstance(block[property_name], int):
        raise WrongValueTypeException(trace, int, type(block[property_name]))
    lower_boundary = 0
    if block[property_name] <= lower_boundary:
        raise FailedLowerBoundaryException(trace, lower_boundary, block[property_name])
    


def l_1_brokers(block):
    """
    field for testing regex
    """
    trace = 'services.brokers'
    property_name = 'brokers'
    enter_log(trace)
    if property_name not in block.keys():
        return
    if not isinstance(block[property_name], str):
        raise WrongValueTypeException(trace, str, type(block[property_name]))


def l_1_consumer(block):
    """
    field for testing string prefixes
    """
    trace = 'services.consumer'
    property_name = 'consumer'
    enter_log(trace)
    if property_name not in block.keys():
        raise MissingRequiredPropertyException(trace)
    if not isinstance(block[property_name], str):
        raise WrongValueTypeException(trace, str, type(block[property_name]))


def l_1_fisker(block):
    """
    field for testing numbers
    """
    trace = 'services.fisker'
    property_name = 'fisker'
    enter_log(trace)
    if property_name not in block.keys():
        return
    if not isinstance(block[property_name], int):
        raise WrongValueTypeException(trace, int, type(block[property_name]))
    lower_boundary = 0
    if block[property_name] <= lower_boundary:
        raise FailedLowerBoundaryException(trace, lower_boundary, block[property_name])
    upper_boundary = 128
    if block[property_name] >= upper_boundary:
        raise FailedUpperBoundaryException(trace, upper_boundary, block[property_name])



def root_block(block: dict):
    try:
            l_0_enabled(block)
        l_0_enums_checker(block)
        l_0_services(block)

    except Exception as ex:
        print(ex)



def validate(in_file: str):
    import yaml
    with open(in_file, 'r') as file:
        content: dict = yaml.safe_load(file)
        root_block(content)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Yaml validator')
    parser.add_argument('file', type=str, help='Path to file to validate')
    args = parser.parse_args()
    validate(args.file)
    