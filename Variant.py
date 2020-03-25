from enum import Enum


class Variant(Enum):
    A = 'A'
    C = 'C'
    G = 'G'
    T = 'T'
    INDEL = 'indel'
    HET = 'heterozygous'
    NON_MUT = 'non_mut'
    NULL = 'null'

    @classmethod
    def values(cls):
        return [c.value for c in list(cls)]
