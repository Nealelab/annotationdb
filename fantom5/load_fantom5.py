#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/fantom5/fantom5.json', './'])

with open('fantom5.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

kt_robust = (

	hc
	.import_keytable(
		'gs://annotationdb/fantom5/robust_enhancers.tsv.bgz',
		config = hail.TextTableConfig(noheader = True)
	)
	.annotate(
		"""
		interval = let chr = _0.replace("chr", "") in
		    Interval(Locus(chr, _1.toInt()), Locus(chr, _2.toInt()))
		"""
	)
	.key_by('interval')
	.select(['interval'])
	.annotate('robust = true')
)

kt_permissive = (

	hc
	.import_keytable(
		'gs://annotationdb/fantom5/permissive_enhancers.tsv.bgz',
		config = hail.TextTableConfig(noheader = True)
	)
	.annotate(
		"""
		interval = let chr = _0.replace("chr", "") in
		    Interval(Locus(chr, _1.toInt()), Locus(chr, _2.toInt()))
		"""
	)
	.key_by('interval')
	.select(['interval'])
	.annotate('permissive = true')
)

kt_join = (

	kt_robust
	.join(kt_permissive, how = 'outer')
	.annotate(
		"""
		fantom5 = {
			robust: isDefined(robust),
			permissive: isDefined(permissive)
		}
		"""
	)
	.select([
		'interval',
		'fantom5'
	])
)

kt_join.write('gs://annotationdb/fantom5/fantom5.kt', overwrite=True)
