#!/home/unix/labbott/anaconda2/bin/python
#$ -cwd
#$ -j y
#$ -o /dev/null
#$ -l h_vmem=8g
#$ -q long

import os
import gzip

directory = os.path.abspath('/psych/genetics_data/labbott/1kg/variant-calls/')
in_path = os.path.join(directory, 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz')
out_path = os.path.join(directory, '1kg_snps.tsv.gz')

snps = set(['A', 'C', 'T', 'G'])

with gzip.open(in_path, 'rb') as fin, gzip.open(out_path, 'wb') as fout:
    header = '\t'.join(['chr', 'pos', 'ref', 'alt']) + '\n'
    fout.write(header)
    for line in fin:
        if line[0] == '#':
            continue
        fields = [x.strip() for x in line.split()]
        if (fields[3] in snps and fields[4] in snps):
            out = '\t'.join([fields[0], fields[1], fields[3], fields[4]]) + '\n'
            fout.write(out)
        