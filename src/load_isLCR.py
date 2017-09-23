#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

(
	hc
	.import_table(
		'gs://annotationdb/isLCR/isLCR.tsv.bgz',
		no_header=True,
		types={
			'f0': TString(),
			'f1': TInt(),
			'f2': TInt()
		}
	)
	.annotate('interval = Interval(Locus(f0, f1), Locus(f0, f2))')
	.key_by('interval')
	.select(['interval'])
	.write('gs://annotationdb/isLCR/isLCR.kt', overwrite=True)
)
