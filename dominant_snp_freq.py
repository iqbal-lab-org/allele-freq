import sys
from collections import Counter

with open(sys.argv[1]) as f:
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

        counts = Counter()

        for sample in samples:
            sample = sample.split(':')

            filters = sample[fields.index('FT')]
            if filters != 'PASS':
                continue

            # Both alleles' call values should be the same since Clockwork does not produce heterozygous calls
            call_value = sample[fields.index('GT')].split('/')[0]

            try:
                call_value = int(call_value)

                if call_value == 0:
                    continue
                else:
                    alt = alts[call_value - 1]
                    if len(alt) == 1:
                        counts[alt] += 1

            except ValueError:
                # call_value == .
                pass

        if len(counts) == 0:
            a1 = a2 = 0
        elif len(counts) == 1:
            a1 = list(counts.values())[0]
            a2 = 0
        else:
            a1, a2 = (x[1] for x in counts.most_common(2))

        print(chrom, pos, a1/len(samples), a2/len(samples))
