from abc import ABCMeta, abstractmethod
from typing import Dict

from yaml_blocks import Block
from yaml_blocks.bool_block import BoolBlock
from yaml_blocks.enum_block import EnumBlock
from yaml_blocks.number_block import NumberBlock
from yaml_blocks.string_block import StringBlock
from yaml_blocks.super_block import SuperBlock


class LanguageGenerator(metaclass=ABCMeta):

    @abstractmethod
    def add_to_root_method(self, block: Block):
        pass

    @abstractmethod
    def bool_block(self, trace: str, level: int, block: BoolBlock):
        pass

    @abstractmethod
    def string_block(self, trace: str, level: int, block: StringBlock):
        pass

    @abstractmethod
    def enum_block(self, trace: str, level: int, block: EnumBlock):
        pass

    @abstractmethod
    def number_block(self, trace: str, level: int, block: NumberBlock):
        pass

    @abstractmethod
    def super_block(self, trace: str, level: int, block: SuperBlock):
        pass

    @abstractmethod
    def get_result(self) -> str:
        pass


_language_to_generator_mapper: Dict[str, LanguageGenerator] = {}

def get_generator(language: str) -> LanguageGenerator:
    generator = _language_to_generator_mapper.get(language)
    if generator is None:
        raise Exception('Unknown language')