import csv
import sys

with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(['chrom', 'pos', 'ref', 'snp', 'indel', 'heterozygous', 'non_mut', 'null'])

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

        counts = {call_type: 0 for call_type in ['snp', 'indel', 'heterozygous', 'non_mut', 'null']}

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
                else:
                    alleles = [alts[call_value[0] - 1], alts[call_value[1] - 1]]

                    for i, allele in enumerate(alleles):
                        if len(allele) == 1:
                            alleles[i] = 'snp'
                        else:
                            alleles[i] = 'indel'

                    if alleles[0] == alleles[1]:
                        call_type = alleles[0]
                    else:
                        call_type = 'heterozygous'
            except ValueError:
                call_type = 'null'

            counts[call_type] += 1

        writer.writerow([chrom, pos, ref, counts['snp'], counts['indel'], counts['heterozygous'], counts['non_mut'],
                         counts['null']])
