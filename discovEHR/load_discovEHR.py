#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/discovEHR/discovEHR.json', './'])

with open('discovEHR.json', 'rb') as f:
	dct = json.load(f)

hc = hail.HailContext(log = '/home/labbott/hail.log', parquet_compression = 'snappy')

(

	hc
	.import_vcf(
		'gs://annotationdb/discovEHR/GHS_Freeze_50.L3DP10.pVCF.frq.vcf.bgz',
		sites_only = True
	)
	.annotate_variants_expr(
		"""
		va.AF = if (isDefined(va.info.AF))
			     va.info.AF[0]
		     else
		         0.001
		"""
	)
	.split_multi()
	.annotate_variants_expr('va = {discovEHR: {AF: va.AF}}')
	.write(
		'gs://annotationdb/discovEHR/discovEHR.vds',
		overwrite = True
	)
)
