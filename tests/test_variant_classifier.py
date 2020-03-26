from hypothesis import given, assume
from hypothesis.strategies import integers, lists, text, just, one_of

from Variant import Variant


@given(alts=lists(elements=text()), gt=lists(elements=integers()), ft=text())
def test_classifying_non_pass_filters(alts, gt, ft):
    assume(ft != 'PASS')
    assert Variant.classify(alts, gt, ft) == Variant.NULL


@given(alts=lists(elements=text()), gt=lists(elements=one_of(integers(), just('.'))), ft=just('PASS'))
def test_classifying_null_calls(alts, gt, ft):
    assume(any([call_value == '.' for call_value in gt]))
    assert Variant.classify(alts, gt, ft) == Variant.NULL


@given(alts=lists(elements=text()), gt=lists(elements=just(0)), ft=just('PASS'))
def test_classifying_non_mutations(alts, gt, ft):
    assert Variant.classify(alts, gt, ft) == Variant.NON_MUT


@given(alts=lists(elements=text()), gt=lists(elements=integers(min_value=1)), ft=just('PASS'))
def test_classifying_heterozygous_calls(alts, gt, ft):
    assume(len(set(gt)) > 1)
    assert Variant.classify(alts, gt, ft) == Variant.HET


@given(snp=text(min_size=1, max_size=1, alphabet='ACGT'), indel=text(min_size=2), ft=just('PASS'))
def test_classifying_indels(snp, indel, ft):
    assert Variant.classify([snp, indel], [0, 2], ft) == Variant.INDEL
    assert Variant.classify([snp, indel], [2, 0], ft) == Variant.INDEL
    assert Variant.classify([snp, indel], [2, 2], ft) == Variant.INDEL

    assert Variant.classify([indel, snp], [0, 1], ft) == Variant.INDEL
    assert Variant.classify([indel, snp], [1, 0], ft) == Variant.INDEL
    assert Variant.classify([indel, snp], [1, 1], ft) == Variant.INDEL


@given(snp=text(min_size=1, max_size=1, alphabet='ACGT'), indel=text(min_size=2), ft=just('PASS'))
def test_classifying_snps(snp, indel, ft):
    assert Variant.classify([snp, indel], [0, 1], ft) == Variant[snp]
    assert Variant.classify([snp, indel], [1, 0], ft) == Variant[snp]
    assert Variant.classify([snp, indel], [1, 1], ft) == Variant[snp]

    assert Variant.classify([indel, snp], [0, 2], ft) == Variant[snp]
    assert Variant.classify([indel, snp], [2, 0], ft) == Variant[snp]
    assert Variant.classify([indel, snp], [2, 2], ft) == Variant[snp]
