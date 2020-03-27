from dominant_snp_freq import dominant_snp_freq


def test_example_input(capsys):
    with open('tests/data/test.vcf') as f, open('tests/data/expected_freq_output') as expected:
        dominant_snp_freq(f)
        captured = capsys.readouterr()

        assert captured.out == expected.read()
