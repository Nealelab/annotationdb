#!/usr/bin/env python

import hail

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_keytable(
		'gs://annotationdb/tfbs/tfbs.tsv.bgz',
		config = hail.utils.TextTableConfig(
			types = """
				chr: String,
				start: Int,
				end: Int,
				tfbs: String
			"""
		)
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.select(['interval', 'tfbs'])
	.write(
		'gs://annotationdb/tfbs/tfbs.kt',
		overwrite = True
	)
)
