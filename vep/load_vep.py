#!/usr/bin/env python

import hail

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.read('gs://annotationdb/vep/vep.vds')
	.annotate_variants_expr('va = va.vep')
	.write('gs://annotationdb/vep/vep2.vds', overwrite = True)
)
