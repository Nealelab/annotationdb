#!/usr/bin/env python

import hail
import json

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/segway/segway.json') as f:
    dct = json.load(f)

(
	hc
	.import_keytable(
		'gs://annotationdb/segway/segway.tsv.bgz',
		config = hail.utils.TextTableConfig(
			types = """
				sum_score: Double,
				mean_score: Double
			"""
		)
	)
	.annotate('interval = Interval(Locus(chrom, start.toInt()), Locus(chrom, end.toInt() + 1))')
	.key_by('interval')
	.rename({x['raw']: x['id'] for x in dct['nodes']})
	.select(
		['interval'] + 
		[x['id'] for x in dct['nodes']]
	)
	.write(
		'gs://annotationdb/segway/segway.kt',
		overwrite = True
	)
)
