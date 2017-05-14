#!/usr/bin/env python

import hail
import json

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/gencode19/gencode19.json') as f:
    dct = json.load(f)

(
	hc
	.import_keytable(
		'gs://annotationdb/gencode19/gencode19.tsv.bgz',
		config = hail.utils.TextTableConfig(
			types = """
				chr: String,
				start: Int,
				end: Int,
				`3utr`: Boolean,
				`5utr`: Boolean,
				exonsc: Boolean,
				exonsa: Boolean,
				coding15: Boolean,
				introns: Boolean,
				promotersreg: Boolean
			"""
		)
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.select(
		['interval'] + 
		[x['id'] for x in dct['nodes']]
	)
	.write(
		'gs://annotationdb/gencode19/gencode19.kt',
		overwrite = True
	)
)
