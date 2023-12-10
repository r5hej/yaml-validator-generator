from typing import List

from generators import LanguageGenerator
from yaml_blocks import Block
from yaml_blocks.bool_block import BoolBlock
from yaml_blocks.enum_block import EnumBlock
from yaml_blocks.number_block import NumberBlock
from yaml_blocks.string_block import StringBlock
from yaml_blocks.super_block import SuperBlock


def _log(msg: str):
    print(msg)


def _recursive_gen(code_generator: LanguageGenerator, trace: str, level: int, block: Block):
    next_trace = f'{trace}.{block.block_name}'.removeprefix('.')
    _log(f'Generating {next_trace}')

    if isinstance(block, BoolBlock):
        code_generator.bool_block(trace, level, block)
    elif isinstance(block, EnumBlock):
        code_generator.enum_block(trace, level, block)
    elif isinstance(block, NumberBlock):
        code_generator.number_block(trace, level, block)
    elif isinstance(block, StringBlock):
        code_generator.string_block(trace, level, block)
    elif isinstance(block, SuperBlock):
        code_generator.super_block(trace, level, block)
        for leave in block.leaves:
            _recursive_gen(code_generator, next_trace, level + 1, leave)
    else:
        raise Exception('HOW!?!??!?!')


def generate(out_file_path: str, language: str, root_blocks: List[Block]):
    with open(f'{out_file_path}.py', 'w') as out_file:
        from generators import get_generator
        code_generator = get_generator(language)
        # code_generator = PythonLanguageGenerator()
        for r_block in root_blocks:
            level = 0
            code_generator.add_to_root_method(r_block)
            _recursive_gen(code_generator, '', level, r_block)

        out_file.write(code_generator.get_result())
