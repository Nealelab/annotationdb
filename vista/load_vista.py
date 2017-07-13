#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

(
	hc
	.import_table('gs://annotationdb/vista/vista.tsv.bgz', types={'chr': TString(), 'start': TInt(), 'end': TInt(), 'location': TString()})
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end))')
	.key_by('interval')
	.select(['interval', 'location'])
	.write('gs://annotationdb/vista/vista.kt', overwrite=True)
)
