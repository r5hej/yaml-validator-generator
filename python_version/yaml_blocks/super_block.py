from typing import List

from yaml_blocks import Block


class SuperBlock(Block):
    leaves: List[Block] = []

    def __init__(self, input_block: dict, block_name: str, leaves: List[Block] = []):
        self.is_valid(input_block)
        super().__init__(input_block, block_name)
        self.leaves = leaves

    def is_valid(self, input_block: dict):
        super().is_valid(input_block)

    def __str__(self) -> str:
        return f'block_name = {self.block_name}'
