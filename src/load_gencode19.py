from hail import *
from pprint import pprint
import pandas as pd
#import gzip
import sys

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/gencode19/gencode.v19.annotation.gtf.gz') as f:
	df = pd.read_table(f, skiprows=5, sep='\t', header=None, names=['chr', 'source', 'feature_type', 'start', 'end', 'score', 'strand', 'phase', 'info'], nrows=1000)

def split_fields(x):
	return {y.split(' ')[0]: y.split(' ')[1].strip('"') for y in x.split('; ')}

def extract_fields(x, key):
	try:
		return x[key]
	except KeyError:
		return 'NA'

df.loc[:, 'interval'] = df['chr'].replace('chr', '') + ':' + df['start'].astype(str) + '-' + df['end'].astype(str)
df.loc[:, 'info'] = df['info'].apply(split_fields)

fields = [
	'gene_id',
	'transcript_id',
	'gene_type',
	'gene_status',
	'gene_name',
	'transcript_type',
	'transcript_status',
	'transcript_name',
	'exon_number',
	'exon_id',
	'level',
	'tag',
	'ccdsid',
	'havana_gene',
	'havana_transcript',
	'protein_id',
	'ont',
	'transcript_support_level'
]

for f in fields:
	df.loc[:, f] = df['info'].apply(extract_fields, args=(f,))

df_gene = df.loc[df['feature_type'] == 'gene', :].sort_values(by=['start', 'end']).reset_index(drop=True)

def overlap(a, b):
    return (min(a[1], b[1]) - max(a[0], b[0])) > 0

def overlap_region(a, b):
	return max(0, min(a[1], b[1]) - max(a[0], b[0]))

previous = [0, 0]

for i, row in df_gene.iterrows():
	current = [row['start'], row['end']]
	if overlap(previous, current):
		print(df_gene.ix[i-1,:], df_gene.ix[i, :])
		print('OVERLAP REGION: ', str(current[0]) + '-' + str(previous[1]))
		break
	previous = current

with hadoop_write('gs://annotationdb/gencode19/gencode19.tsv') as f:
	df.to_csv(f, sep='\t', header=True, index=False)

kt = hc.import_table('gs://annotationdb/gencode19/gencode19.tsv', types={'interval': TInterval(), 'exon_number': TInt()}, key='interval')
pprint(kt.schema)

(
	hc
	.import_table(
		'gs://annotationdb/gencode19/gencode19.tsv.bgz',
		types = {
			'chr': TString(),
			'start': TInt(),
			'end': TInt(),
			'3utr': TBoolean(),
			'5utr': TBoolean(),
			'exonsc': TBoolean(),
			'exonsa': TBoolean(),
			'coding15': TBoolean(),
			'introns': TBoolean(),
			'promotersreg': TBoolean()
		}
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.rename({
		'3utr': 'three_prime_utr', 
		'5utr': 'five_prime_utr',
		'exonsa': 'exons',
		'exonsc': 'exons_coding',
		'coding15': 'exons_15bp'
	})
	.annotate('utr = three_prime_utr || five_prime_utr')
	.select([
		'interval',
		'three_prime_utr',
		'five_prime_utr',
		'exons',
		'exons_15bp',
		'exons_coding',
		'introns',
		'promotersreg'
	])
	.write('gs://annotationdb/gencode19/gencode19.kt', overwrite=True)
)

pprint(hc.read_table('gs://annotationdb/gencode19/gencode19.kt').schema)
