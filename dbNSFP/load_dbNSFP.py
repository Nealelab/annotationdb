#!/usr/bin/env python

import sys
import hail
import json
from subprocess import call

hc = hail.HailContext(parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/dbNSFP/dbNSFP.json') as f:
	dct = json.load(f)

# load into keytable
kt = (

	hc
	.import_keytable(
		'gs://annotationdb/dbNSFP/dbNSFP.tsv.bgz',
		config = hail.TextTableConfig(
			types = ','.join(
				[
					'`#chr`: String',
					'`pos(1-coor)`: Int',
					'ref: String',
					'alt: String'
				] +
				[
					var['raw'] + ': ' + var['type'] for var in dct['nodes']
				]
			)
		)
	)
	.annotate('variant = Variant(`#chr`, `pos(1-coor)`, ref, alt)')
	.key_by('variant')
	.rename({var['raw'].strip('`'): var['id'] for var in dct['nodes']})
    .annotate(','.join(['{0} = {0}'.format(x['id']) for x in dct['nodes']]))
    .select(
    	['variant'] +
    	[x['id'] for x in dct['nodes']]
    )
)

# create sites-only VDS
vds = (
    hail
    .VariantDataset.from_keytable(kt)
    .repartition(1024)
    .write(
        'gs://annotationdb/dbNSFP/dbNSFP.vds',
        overwrite = True
    )
)
