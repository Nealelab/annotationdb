#!/usr/bin/env python

import hail

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_keytable(
		'gs://annotationdb/vista/vista.tsv.bgz',
		config = hail.utils.TextTableConfig(
			types = """
				chr: String,
				start: Int,
				end: Int,
				location: String
			"""
		)
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.select(['interval', 'location'])
	.write(
		'gs://annotationdb/vista/vista.kt',
		overwrite = True
	)
)
