def validate(yaml_obj):
    handle_enabled(yaml_obj['enabled'])
    enum_checker(yaml_obj['enums_checker'])


def handle_enabled(yaml_obj):
    print('enabled field is valid' if isinstance(yaml_obj, bool) else 'enabled failed')


def enum_checker(yaml_obj):
    if not isinstance(yaml_obj, str):
        print('enums_checker failed')
        return

    print('enums_checker is valid' if yaml_obj in ['enum_uno', 'enum_dos'] else 'enums_checker failed')
    """
    services:
      required: true
      nested_broker:
        required: false
        super_nested:
          required: true
          type: number
          format: unsigned
          min: 0
      brokers:
        description: 'field for testing regex'
        required: false
        type: string
        regex: '\d'
      consumer:
        description: 'field for testing string prefixes'
        required: true
        type: string
        prefix: 'olla'
      fisker:
        required: false
        description: 'field for testing numbers'
        type: number
        format: signed|unsigned
        min: 0
        max: 128
    """
