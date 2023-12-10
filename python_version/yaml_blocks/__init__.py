import abc
from typing import Set


class Block(abc.ABC):
    block_name: str
    required: bool
    description: str = None

    def __init__(self, obj: dict, block_name: str):
        self.block_name = block_name
        self.required = obj['required']
        if 'description' in obj.keys():
            self.description = obj['description']

    def is_valid(self, obj: dict):
        for required_property in ['required']:
            if required_property not in obj.keys():
                raise Exception(f'Invalid block. Missing key={required_property} in block\n{obj}')

    def _get_all_block_keys(self) -> Set[str]:
        return {'required', 'description'}


    def generate_block(self) -> str:
        pass


class UnknownPropertyException(Exception):
    def __init__(self, property_name: str, block: dict) -> None:
        super().__init__(f'Unknown property={property_name} for a Block. Block\n{block}')


class ConflictingPropertiesException(Exception):
    def __int__(self, block: dict, *properties: str):
        super().__init__(f'Properties={properties} conflict in same block. Block\n{block}')


class UnknownBlockTypeException(Exception):
    def __int__(self, block_type: str):
        super().__init__(f'Unknown block type={block_type}')


class MissingRequiredPropertyException(Exception):
    def __init__(self, block: dict, property: str):
        super().__init__(f'Missing required property={property} in block\n{block}')
