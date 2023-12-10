import yaml

import generate
from yaml_blocks import Block, UnknownBlockTypeException
from yaml_blocks.bool_block import BoolBlock
from yaml_blocks.enum_block import EnumBlock
from yaml_blocks.number_block import NumberBlock
from yaml_blocks.string_block import StringBlock
from yaml_blocks.super_block import SuperBlock


def recursive_build_block_tree(current_key, obj) -> Block:
    leaves = []
    for key, val in obj.items():
        if isinstance(val, dict):
            leaves.append(recursive_build_block_tree(key, val))

    if 'type' in obj.keys():
        if obj['type'] == 'number':
            return NumberBlock(obj, current_key)
        elif obj['type'] == 'string':
            return StringBlock(obj, current_key)
        elif obj['type'] == 'bool':
            return BoolBlock(obj, current_key)
        else:
            raise UnknownBlockTypeException(obj['type'])
    elif 'enum' in obj.keys():
        return EnumBlock(obj, current_key)
    else:
        return SuperBlock(obj, current_key, leaves)


def load_file(input_file: str) -> dict:
    with open(input_file, 'r') as in_file:
        return yaml.safe_load(in_file)


def v():
    try:
        print('')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    from argparse import ArgumentParser
    import os
    import re
    regex = re.compile('lang_(?P<name>.+)\.py')

    langs = [regex.fullmatch(f) for f in os.listdir('./generators') if f.startswith('lang_')]
    langs = [f.group('name') for f in langs if f is not None]

    parser = ArgumentParser(description='Yaml validator')
    parser.add_argument('input', type=str, help='Path to validator schema file')
    parser.add_argument('output', type=str, help='Path to output file. Do not add file extension')
    parser.add_argument('lang', type=str, choices=langs, help='The programming language to generate to')
    args = parser.parse_args()
    content: dict = load_file(args.input)
    root_blocks = [recursive_build_block_tree(key, value) for key, value in content.items()]
    generate.generate(args.output, args.lang, root_blocks)
