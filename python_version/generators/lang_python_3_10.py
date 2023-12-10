from typing import List

from generators import LanguageGenerator, _language_to_generator_mapper
from yaml_blocks import Block
from yaml_blocks.bool_block import BoolBlock
from yaml_blocks.enum_block import EnumBlock
from yaml_blocks.number_block import NumberBlock
from yaml_blocks.string_block import StringBlock
from yaml_blocks.super_block import SuperBlock


class PythonLanguageGenerator(LanguageGenerator):
    _generated_code_blocks: List[str] = []
    _root_code_blocks: List[str] = []

    def add_to_root_method(self, block: Block):
        self._root_code_blocks.append(f'{self._get_method_name(0, block)}')

    def bool_block(self, trace: str, level: int, block: BoolBlock):
        code = f"""def {self._get_method_name(level, block)}:
    {self._get_method_header(trace, block)}
    {self._get_required_block(block)}
    if not isinstance(block[property_name], bool):
        raise WrongValueTypeException(property_name, bool, type(block[property_name]))"""

        self._generated_code_blocks.append(code)

    def string_block(self, trace: str, level: int, block: StringBlock):
        def _prefix_validation(block: StringBlock) -> str:
            return f"""prefix = '{block.prefix}'
    if not block[property_name].startswith(prefix):
        raise WrongPrefixException(trace, prefix)"""

        def _regex_validation(block: StringBlock) -> str:
            return f"""import re
    regex = re.compile('{block.regex}')
    if regex.fullmatch(block[property_name]) is None:
        raise RegexMismatchException(trace, '{block.regex}')"""

        code = f"""def {self._get_method_name(level, block)}:
    {self._get_method_header(trace, block)}
    {self._get_required_block(block)}
    if not isinstance(block[property_name], str):
        raise WrongValueTypeException(trace, str, type(block[property_name]))"""

        if block.prefix is not None:
            code += _prefix_validation(block)
        if block.regex is not None:
            code += _regex_validation(block)

        self._generated_code_blocks.append(code)

    def enum_block(self, trace: str, level: int, block: EnumBlock):
        def get_valid_values(block: EnumBlock) -> str:
            tmp = ['valid_values = [\n']
            for enum_value in block.enum_values:
                tmp.append(f"       '{enum_value}',\n")
            tmp.append('    ]')
            return ''.join(tmp)

        code = f"""def {self._get_method_name(level, block)}:
    {self._get_method_header(trace, block)}
    {self._get_required_block(block)}
    {get_valid_values(block)}
    if block[property_name] not in valid_values:
        raise InvalidEnumPropertyValue(property_name, valid_values, block[property_name])"""

        self._generated_code_blocks.append(code)

    def number_block(self, trace: str, level: int, block: NumberBlock):
        def lower_boundary_validation(block: NumberBlock):
            return f"""lower_boundary = {block.lower_boundary}
    if block[property_name] <= lower_boundary:
        raise FailedLowerBoundaryException(trace, lower_boundary, block[property_name])"""

        def upper_boundary_validation(block: NumberBlock):
            return f"""upper_boundary = {block.upper_boundary}
    if block[property_name] >= upper_boundary:
        raise FailedUpperBoundaryException(trace, upper_boundary, block[property_name])"""

        code = f"""def {self._get_method_name(level, block)}:
    {self._get_method_header(trace, block)}
    {self._get_required_block(block)}
    if not isinstance(block[property_name], int):
        raise WrongValueTypeException(trace, int, type(block[property_name]))
    {'' if block.lower_boundary is None else lower_boundary_validation(block)}
    {'' if block.upper_boundary is None else upper_boundary_validation(block)}"""

        self._generated_code_blocks.append(code)

    def super_block(self, trace: str, level: int, block: SuperBlock):
        code = f"""def {self._get_method_name(level, block)}:
    {self._get_method_header(trace, block)}
    {self._get_required_block(block)}
    next_block = block[property_name]\n"""
        for leaf in block.leaves:
            code += f'    {self._get_method_name(level + 1, leaf, parameter_name="next_block")}\n'
        self._generated_code_blocks.append(code)

    def get_result(self) -> str:
        self._generated_code_blocks.append(self._get_root_method())
        self._generated_code_blocks.append(self._get_initial_method())
        self._generated_code_blocks.insert(0, self._get_logger_code())
        self._generated_code_blocks.insert(0, self._get_exceptions_code())
        return str.join('\n\n\n', self._generated_code_blocks)

    def _get_required_block(self, block: Block) -> str:
        return f"""if property_name not in block.keys():
        {'raise MissingRequiredPropertyException(trace)' if block.required else 'return'}"""

    def _get_method_header(self, trace: str, block: Block) -> str:
        code = f"""trace = '{(trace + '.' + block.block_name).removeprefix(".")}'
    property_name = '{block.block_name}'
    enter_log(trace)"""
        if block.description is None:
            return code

        desc = f"""\"\"\"
    {block.description}
    \"\"\"
    """
        return desc + code

    def _get_method_name(self, level: int, block: Block, parameter_name: str = 'block') -> str:
        return f"""l_{level}_{block.block_name}({parameter_name})"""

    def _get_root_method(self) -> str:
        methods = '\n'
        for r_block in self._root_code_blocks:
            methods += f'        {r_block}\n'
        code = f"""
def root_block(block: dict):
    try:
    {methods}
    except Exception as ex:
        print(ex)
"""

        return code

    def _get_logger_code(self) -> str:
        return """
def enter_log(property_name: str):
    print(f'Validating property:\\t{property_name}')"""

    def _get_initial_method(self) -> str:
        return """def validate(in_file: str):
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
    """

    def _get_exceptions_code(self) -> str:
        return """
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
        super().__init__(f'Property -> {property_name} failed upper boundary. Upper boundary -> {upper_boundary}, value -> {actual}')"""


_language_to_generator_mapper['python_3_10'] = PythonLanguageGenerator()
