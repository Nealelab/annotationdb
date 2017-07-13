#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

(
	hc
	.import_table('gs://annotationdb/tfbs/tfbs.tsv.bgz', types={'chr': TString(), 'start': TInt(), 'end': TInt(), 'tfbs': TString()})
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end))')
	.key_by('interval')
	.select(['interval', 'tfbs'])
	.write('gs://annotationdb/tfbs/tfbs.kt',overwrite=True)
)
