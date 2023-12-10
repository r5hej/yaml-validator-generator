from yaml_blocks import Block


class BoolBlock(Block):
    def __init__(self, input_block: dict, block_name: str):
        super().is_valid(input_block)
        super().__init__(input_block, block_name)
        self.block_type = bool

    def __str__(self):
        return f'block_name = {self.block_name}'

    def generate_block(self) -> str:
        return 'i am a bool block'



