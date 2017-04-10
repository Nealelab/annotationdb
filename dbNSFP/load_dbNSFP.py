#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/dbNSFP/dbNSFP.json', './'])

with open('dbNSFP.json', 'rb') as f:
	dct = json.load(f)

hc = hail.HailContext(log = '/home/labbott/hail.log', parquet_compression = 'snappy')

kt = (

	hc
	.import_keytable(
		'gs://annotationdb/dbNSFP/dbNSFP.tsv.gz',
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
	.annotate(
		'variant = Variant(`#chr`, `pos(1-coor)`, ref, alt)'
	)
	.key_by(
		'variant'
	)
)
#	.rename(
#		{
#			var['raw'].strip('`'): var['id'] for var in dct['nodes']
#		}
#	)
	#.filter(
	#	'ref.length() == 1 && alt.length() == 1',
	#	keep = True
	#)
#	.select(
#		['variant'] #+ [variable['id'] for variable in dct['nodes']]
#	)
	#.write(
	#	'gs://annotationdb/dbNSFP/dbNSFP.kt',
	#	overwrite = True
	#)

#)

vds = hail.VariantDataset.from_keytable(kt)

print vds.variant_schema
