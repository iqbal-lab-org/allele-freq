import csv
import sys

from Variant import Variant

VARIANTS = list(Variant)

with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(['chrom', 'pos', 'ref', 'atl'] + Variant.values())

    for line in f:
        if line.startswith('#'):
            continue

        line = line.split('\t')
        chrom = line[0]
        pos = line[1]
        ref = line[3]
        alts = line[4].split(',')
        fields = line[8].split(':')
        samples = line[9:]

        counts = {call_type: 0 for call_type in VARIANTS}

        for sample in samples:
            sample = sample.split(':')

            filters = sample[fields.index('FT')]
            if filters != 'PASS':
                counts[Variant.NULL] += 1
                continue

            call_value = sample[fields.index('GT')].split('/')

            try:
                call_value = [int(allele) for allele in call_value]

                if call_value[0] == call_value[1] == 0:
                    call_type = Variant.NON_MUT
                elif call_value[0] != call_value[1] and call_value[0] != 0 and call_value[1] != 0:
                    call_type = Variant.HET
                else:
                    mutated_value = call_value[0] if call_value[0] != 0 else call_value[1]
                    mutated_allele = alts[mutated_value - 1]

                    if len(mutated_allele) == 1:
                        call_type = Variant(mutated_allele)
                    else:
                        call_type = Variant.INDEL

            except ValueError:
                call_type = Variant.NULL

            counts[call_type] += 1

        writer.writerow([chrom, pos, ref, ','.join(alts)] + [counts[key] for key in VARIANTS])
