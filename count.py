import csv
import sys

CALL_TYPES = ['A', 'C', 'G', 'T', 'indel', 'heterozygous', 'non_mut', 'null']

with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(['chrom', 'pos', 'ref'] + CALL_TYPES)

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

        counts = {call_type: 0 for call_type in CALL_TYPES}

        for sample in samples:
            sample = sample.split(':')

            filters = sample[fields.index('FT')]
            if filters != 'PASS':
                counts['null'] += 1
                continue

            call_value = sample[fields.index('GT')].split('/')
            try:
                call_value = [int(allele) for allele in call_value]

                if call_value[0] == call_value[1] == 0:
                    call_type = 'non_mut'
                elif call_value[0] != 0 and call_value[1] != 0:
                    call_type = 'heterozygous'
                else:
                    mutated_value = call_value[0] if call_value[0] != 0 else call_value[1]
                    mutated_allele = alts[mutated_value - 1]
                    if len(mutated_allele) == 1:
                        call_type = mutated_allele
                    else:
                        call_type = 'indel'
            except ValueError:
                call_type = 'null'

            counts[call_type] += 1

        writer.writerow([chrom, pos, ref] + [counts[key] for key in CALL_TYPES])
