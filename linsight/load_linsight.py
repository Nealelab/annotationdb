#!/usr/bin/env python

import hail

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_keytable(
		'gs://annotationdb/linsight/linsight.tsv.bgz',
		config = hail.utils.TextTableConfig(
			noheader = True
		)
	)
	.annotate('interval = Interval(Locus(_0, _1.toInt()), Locus(_0, _2.toInt() + 1))')
	.key_by('interval')
	.annotate('score = _3.toDouble()')
	.select(['interval', 'score'])
	.write(
		'gs://annotationdb/linsight/linsight.kt',
		overwrite = True
	)
)
