#!/usr/bin/env python

import hail
import json
import pandas as pd

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/dhs/dhs.json') as f:
    dct = json.load(f)

kt = (

	hc
	.import_keytable('gs://annotationdb/dhs/dhs.tsv.bgz')
	.annotate(
		"""
		interval = let chr = Chr.replace("chr", "") in
		    Interval(Locus(chr, Start.toInt()), Locus(chr, End.toInt()))
		"""
	)
	.key_by('interval')
	.rename({x['raw']: x['id'] for x in dct['nodes']})
)

for x in dct['nodes']:
	if x['type'] == 'Boolean':
		kt = kt.annotate(
			"""
			{0} = if ({0} == "0")
			          false
			      else
			          true
			""".format(x['id'])
		)
	elif x['type'] == 'Double':
		kt = kt.annotate('{0} = {0}.toDouble()'.format(x['id']))
	elif x['type'] == 'Int':
		kt = kt.annotate('{0} = {0}.toInt()'.format(x['id']))
	else:
		continue

(
	kt
	.annotate('dhs = {{{}}}'.format(','.join([x['id'] + ': ' + x['id'] for x in dct['nodes']])))
	.select(['interval', 'dhs'])
	.write(
		'gs://annotationdb/dhs/dhs.kt',
		overwrite = True
	)
)
