#!/usr/bin/env python

import hail
from hail.expr import *

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_table(
		'gs://annotationdb/isLCR/isLCR.tsv.bgz',
		no_header = True,
		types = {
			'f0': TString(),
			'f1': TInt(),
			'f2': TInt()
		}
	)
	.annotate('interval = Interval(Locus(f0, f1), Locus(f0, f2 + 1))')
	.key_by('interval')
	.select(['interval'])
	.write(
		'gs://annotationdb/isLCR/isLCR.kt',
		overwrite = True
	)
)
