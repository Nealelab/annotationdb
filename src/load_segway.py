#!/usr/bin/env python

import json
from hail import *

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/segway/segway.json') as f:
    dct = json.load(f)

(
	hc
	.import_table('gs://annotationdb/segway/segway.tsv.bgz', types={'sum_score': TDouble(), 'mean_score': TDouble(), 'start': TInt(), 'end': TInt()})
	.annotate('interval = Interval(Locus(chrom, start), Locus(chrom, end))')
	.key_by('interval')
	.rename({x['raw']: x['id'] for x in dct['nodes']})
	.select(['interval'] + [x['id'] for x in dct['nodes']])
	.write('gs://annotationdb/segway/segway.kt', overwrite=True)
)
