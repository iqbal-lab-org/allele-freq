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

    @staticmethod
    def classify(alts, gt, ft):
        if ft != 'PASS' or any([call_value == '.' for call_value in gt]):
            return Variant.NULL

        if all([call_value == 0 for call_value in gt]):
            return Variant.NON_MUT

        mutated = [call_value for call_value in gt if call_value > 0]

        if len(set(mutated)) > 1:
            return Variant.HET

        alt = alts[mutated[0] - 1]
        if len(alt) > 1:
            return Variant.INDEL
        else:
            return Variant[alt]
