#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

kt_enhancer = (
	hc
	.import_table('gs://annotationdb/chromHMM/enhancers.tsv.bgz', impute=True, types={'interval': TInterval()})
	.key_by('interval')
)

kt_promoter = (
	hc
	.import_table('gs://annotationdb/chromHMM/promoters.tsv.bgz', impute=True, types={'interval': TInterval()})
	.key_by('interval')
)

kt_enhancer.write('gs://annotationdb/chromHMM/enhancers.kt', overwrite=True)
kt_promoter.write('gs://annotationdb/chromHMM/promoters.kt', overwrite=True)
