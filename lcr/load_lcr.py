#!/usr/bin/env python

import hail

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_keytable(
		'gs://annotationdb/lcr/lcr.tsv.bgz',
		config = hail.utils.TextTableConfig(
			noheader = True
		)
	)
	.annotate('interval = Interval(Locus(_0, _1.toInt()), Locus(_0, _2.toInt()))')
	.key_by('interval')
	.select(['interval'])
	.annotate('isLCR = true')
	.write(
		'gs://annotationdb/lcr/lcr.kt',
		overwrite = True
	)
)
