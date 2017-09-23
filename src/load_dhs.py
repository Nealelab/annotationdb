#!/usr/bin/env python

import json
from hail import *

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/dhs/dhs.json') as f:
    dct = json.load(f)

kt = (
	hc
	.import_table('gs://annotationdb/dhs/dhs.tsv.bgz', types={'Chr': TString(), 'Start': TInt(), 'End': TInt()})
	.annotate('interval = Interval(Locus(Chr[3:], Start), Locus(Chr[3:], End))')
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
	.select(['interval'] + [x['id'] for x in dct['nodes']])
	.write('gs://annotationdb/dhs/dhs.kt', overwrite=True)
)
