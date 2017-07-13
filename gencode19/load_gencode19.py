#!/usr/bin/env python

from hail import *
import json

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/gencode19/gencode19.json') as f:
    dct = json.load(f)

(
	hc
	.import_table(
		'gs://annotationdb/gencode19/gencode19.tsv.bgz',
		types = {
			'chr': TString(),
			'start': TInt(),
			'end': TInt(),
			'`3utr`': TBoolean(),
			'`5utr`': TBoolean(),
			'exonsc': TBoolean(),
			'exonsa': TBoolean(),
			'coding15': TBoolean(),
			'introns': TBoolean(),
			'promotersreg': TBoolean()
		}
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.rename({'3utr': 'three_prime_utr', '5utr': 'five_prime_utr'})
	.select(['interval'] + [x['id'] for x in dct['nodes']])
	.write('gs://annotationdb/gencode19/gencode19.kt',overwrite=True)
)
