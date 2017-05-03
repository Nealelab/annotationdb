#!/usr/bin/env python

import hail
import json
from subprocess import call

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/chromHMM/chromHMM.json') as f:
	dct = json.load(f)

dct_enh = next(x for x in dct['nodes'] if x['id'] == 'chromHMM_enhancers')
dct_prom = next(x for x in dct['nodes'] if x['id'] == 'chromHMM_promoters')

kt_enhancer = (

	hc
	.import_keytable(
		'gs://annotationdb/chromHMM/enhancers.tsv.bgz',
		config = hail.TextTableConfig(
			types = ','.join([
				x['id'] + ': ' + x['type'] for x in dct_enh['nodes']
			])
		)
	)
	.annotate(
		"""
		interval = let chr = interval.split(":")[0] and
		               start = interval.split(":")[1].split("-")[0].toInt() and
		               end = interval.split(":")[1].split("-")[1].toInt() 
		           in 
		    Interval(Locus(chr, start), Locus(chr, end))
		"""
	)
	.key_by('interval')
    .annotate('enhancers = {{{}}}'.format(','.join([x['id'] + ': ' + x['id'] for x in dct_enh['nodes']])))
    .select(['interval', 'enhancers'])
)

kt_promoter = (

	hc
	.import_keytable(
		'gs://annotationdb/chromHMM/promoters.tsv.bgz',
		config = hail.TextTableConfig(
			types = ','.join([
				x['id'] + ': ' + x['type'] for x in dct_enh['nodes']
			])
		)
	)
	.annotate(
		"""
		interval = let chr = interval.split(":")[0] and
		               start = interval.split(":")[1].split("-")[0].toInt() and
		               end = interval.split(":")[1].split("-")[1].toInt() 
		           in 
		    Interval(Locus(chr, start), Locus(chr, end))
		"""
	)
	.key_by('interval')
    .annotate('promoters = {{{}}}'.format(','.join([x['id'] + ': ' + x['id'] for x in dct_prom['nodes']])))
    .select(['interval', 'promoters'])
)

kt_join = kt_enhancer.join(kt_promoter, how='outer')

kt_join.write('gs://annotationdb/chromHMM/chromHMM.kt', overwrite=True)
