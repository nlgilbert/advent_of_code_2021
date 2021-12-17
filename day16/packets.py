from abc import ABC, abstractmethod
from typing import List

import numpy as np

class Packet(ABC):
    '''A packet of data.'''
    version: int
    type_id: int
    bit_length: int

    def __init__(self, bit_string: str):
        self.version = int(bit_string[0:3], base=2)
        self.type_id = int(bit_string[3:6], base=2)

    @abstractmethod
    def get_value(self) -> int:
        '''Computes the value of the packet.'''

    @abstractmethod
    def get_version_sum(self) -> int:
        '''Computes the sum of this packet and all subpackets.'''

class Literal(Packet):
    '''A packet representing a literal value.'''
    value: int

    def __init__(self, bit_string: str):
        super().__init__(bit_string)
        bit_idx = 6
        bin_value = ''
        last_group = False
        while not last_group:
            last_group = bit_string[bit_idx] == '0'
            bit_idx += 1
            bin_value += bit_string[bit_idx:bit_idx+4]
            bit_idx += 4
        self.value = int(bin_value, base=2)
        self.bit_length = bit_idx
    
    def get_version_sum(self) -> int:
        return self.version
    
    def get_value(self) -> int:
        return self.value

class Operator(Packet):
    '''An operator packet.'''
    length_type_id: int
    subpackets: List[Packet]

    def __init__(self, bit_string: str):
        super().__init__(bit_string)
        self.length_type_id = int(bit_string[6], base=2)
        self.subpackets = []

        if self.length_type_id == 0:
            # Total length in bits
            subpacket_length = int(bit_string[7:22], base=2)
            bit_idx = 22
            while bit_idx - 22 < subpacket_length:
                packet = convert_to_packet(bit_string[bit_idx:])
                bit_idx += packet.bit_length
                self.subpackets.append(packet)
            self.bit_length = bit_idx

        if self.length_type_id == 1:
            # Number of sub-packets immediately contained
            num_subpackets = int(bit_string[7:18], base=2)
            bit_idx = 18
            for _ in range(num_subpackets):
                packet = convert_to_packet(bit_string[bit_idx:])
                bit_idx += packet.bit_length
                self.subpackets.append(packet)
            self.bit_length = bit_idx
    
    def get_version_sum(self) -> int:
        version_sum = self.version
        for packet in self.subpackets:
            version_sum += packet.get_version_sum()
        return version_sum

class Sum(Operator):
    '''A sum operator.'''
    def get_value(self) -> int:
        value = 0
        for packet in self.subpackets:
            value += packet.get_value()
        return value

class Product(Operator):
    '''A product operator.'''
    def get_value(self) -> int:
        value = 1
        for packet in self.subpackets:
            value *= packet.get_value()
        return value

class Minimum(Operator):
    '''A minimum operator.'''
    def get_value(self) -> int:
        value = np.inf
        for packet in self.subpackets:
            value = min(value, packet.get_value())
        return value

class Maximum(Operator):
    '''A maximum operator.'''
    def get_value(self) -> int:
        value = 0
        for packet in self.subpackets:
            value = max(value, packet.get_value())
        return value

class GreaterThan(Operator):
    '''A greater than operator.'''
    def get_value(self) -> int:
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].get_value() > self.subpackets[1].get_value())

class LessThan(Operator):
    '''A less than operator.'''
    def get_value(self) -> int:
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].get_value() < self.subpackets[1].get_value())

class EqualTo(Operator):
    '''An equal to operator.'''
    def get_value(self) -> int:
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].get_value() == self.subpackets[1].get_value())

def convert_to_packet(bit_string: str) -> Packet:
    '''Converts the given bit string into a packet.'''
    type_id = int(bit_string[3:6], base=2)
    if type_id == 0:
        return Sum(bit_string)
    if type_id == 1:
        return Product(bit_string)
    if type_id == 2:
        return Minimum(bit_string)
    if type_id == 3:
        return Maximum(bit_string)
    if type_id == 4:
        return Literal(bit_string)
    if type_id == 5:
        return GreaterThan(bit_string)
    if type_id == 6:
        return LessThan(bit_string)
    if type_id == 7:
        return EqualTo(bit_string)
    assert False