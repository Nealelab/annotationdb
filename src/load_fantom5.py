#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

(
	hc
	.import_table('gs://annotationdb/fantom5/robust_enhancers.tsv.bgz', no_header=True, types={'f3': TString()})
	.annotate('interval = Interval(f3[3:])')
	.key_by('interval')
	.select(['interval'])
	.write('gs://annotationdb/fantom5/robust_enhancers.kt', overwrite=True)
)

(
	hc
	.import_table('gs://annotationdb/fantom5/permissive_enhancers.tsv.bgz', no_header=True, types={'f3': TString()})
	.annotate('interval = Interval(f3[3:])')
	.key_by('interval')
	.select(['interval'])
	.write('gs://annotationdb/fantom5/permissive_enhancers.kt', overwrite=True)
)
