import sys
from collections import Counter


def dominant_snp_freq(f):
    print('chrom', 'pos', 'freq1', 'freq2', sep='\t')

    for line in f:
        if line.startswith('#'):
            continue

        line = line.rstrip().split('\t')
        chrom = line[0]
        pos = line[1]
        ref = line[3]
        alts = line[4].split(',')
        fields = line[8].split(':')
        samples = line[9:]

        if len(ref) > 1 or any([len(alt) > 1 for alt in alts]):
            continue

        bases = [ref] + alts

        counts = Counter()

        for sample in samples:
            sample = sample.split(':')

            filters = sample[fields.index('FT')]
            if filters != 'PASS':
                continue

            call_value = sample[fields.index('GT')].split('/')

            try:
                call_value = [int(v) for v in call_value]

                if call_value[0] != call_value[1]:
                    # Heterozygous
                    continue

                base_values = [bases[v] for v in set(call_value)]
                for base in base_values:
                    counts[base] += 1

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

        print(chrom, pos, a1/len(samples), a2/len(samples), sep='\t')


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        dominant_snp_freq(f)
