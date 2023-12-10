from yaml_blocks import Block, UnknownPropertyException


class NumberBlock(Block):
    lower_boundary: int = None
    upper_boundary: int = None

    def __init__(self, input_block: dict, block_name: str):
        self.validate_input_block(input_block)
        super().__init__(input_block, block_name)
        self.block_type = int
        if 'min' in input_block.keys():
            self.lower_boundary = input_block['min']
        if 'max' in input_block.keys():
            self.upper_boundary = input_block['max']

    def validate_input_block(self, input_block):
        super().is_valid(input_block)
        all_keys = super()._get_all_block_keys().union({'min', 'max', 'type'})
        for prop in input_block.keys():
            if prop not in all_keys:
                raise UnknownPropertyException(prop, input_block)

    def __str__(self) -> str:
        return f'block_name = {self.block_name}'
        # return f'type={self.block_type}, leaves count={len(self.leaves)}, min={self.min}, max={self.max}, description={self.description}'
