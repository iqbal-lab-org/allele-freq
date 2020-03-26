# Purpose

Count the number of SNPs, indels, heterozygous calls, non-mutations, and null calls from a VCF file.

# Usage

```shell script
python3 count.py <vcf_file> <output_csv>
```

# Run tests

```shell script
pip3 install pytest hypothesis
pip3 install -e .
pytest
```
