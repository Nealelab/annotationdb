#!/usr/bin/env python

import hail
import json

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/ldscore/ldscore.json') as f:
    dct = json.load(f)

(
	hc
	.import_keytable(
		'gs://annotationdb/ldscore/ldscore.tsv.bgz',
		config = hail.utils.TextTableConfig(
			types = ','.join(
				['`' + x['id'] + '`: ' + x['type'] for x in dct['nodes']] +
				['chr: String', 'start: Int', 'end: Int']
			)
		)
	)
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.select(
		['interval'] + 
		[x['id'] for x in dct['nodes']]
	)
	.write(
		'gs://annotationdb/ldscore/ldscore.kt',
		overwrite = True
	)
)
