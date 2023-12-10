from typing import List

from yaml_blocks import Block, MissingRequiredPropertyException


class EnumBlock(Block):
    enum_values: List[str] = {}

    def __init__(self, input_block: dict, block_name: str):
        self.is_valid(input_block)
        super().__init__(input_block, block_name)
        self.enum_values = input_block['enum']

    def is_valid(self, input_block: dict):
        super().is_valid(input_block)

        for req_prop in ['enum']:
            if req_prop not in input_block.keys():
                raise MissingRequiredPropertyException(input_block, req_prop)

    def __str__(self) -> str:
        return f'block_name = {self.block_name}'
