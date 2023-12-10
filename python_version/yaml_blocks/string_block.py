from yaml_blocks import Block, UnknownPropertyException, ConflictingPropertiesException


class StringBlock(Block):
    regex: str = None
    prefix: str = None

    def __int__(self, input_block: dict, block_name: str):
        self.is_valid(input_block)
        super().__init__(input_block, block_name)
        self.block_type = str

        if 'regex' in input_block.keys():
            self.regex = input_block['regex']

        if 'prefix' in input_block.keys():
            self.prefix = input_block['prefix']

    def is_valid(self, input_block: dict):
        super().is_valid(input_block)
        all_keys = super()._get_all_block_keys().union({'regex', 'prefix'})
        for prop in input_block.keys():
            if prop not in all_keys:
                raise UnknownPropertyException(prop, input_block)

        if 'regex' in input_block.keys() and 'prefix' in input_block.keys():
            raise ConflictingPropertiesException(input_block, 'regex', 'prefix')

    def __str__(self) -> str:
        return f'block_name = {self.block_name}'
