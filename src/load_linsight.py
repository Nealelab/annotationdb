#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression = 'snappy')

(
	hc
	.import_table(
		'gs://annotationdb/linsight/linsight.tsv.bgz',
		no_header=True,
		types = {
			'f0': TString(),
			'f1': TInt(),
			'f2': TInt(),
			'f3': TDouble()
		}
	)
	.annotate('interval = Interval(Locus(f0, f1), Locus(f0, f2))')
	.key_by('interval')
	.annotate('score = f3')
	.select(['interval', 'score'])
	.write('gs://annotationdb/linsight/linsight.kt', overwrite=True)
)
