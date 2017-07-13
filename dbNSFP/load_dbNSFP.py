#!/usr/bin/env python

import json
from hail import *

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/dbNSFP/dbNSFP.json') as f:
	dct = json.load(f)

# load into keytable
kt = (
	hc
	.import_table('gs://annotationdb/dbNSFP/dbNSFP.tsv.bgz', impute=True)
	.annotate('variant = Variant(`#chr`, `pos(1-coor)`, ref, alt)')
	.key_by('variant')
	.rename({x['raw'].strip('`'): x['id'] for x in dct['nodes']})
    .select(['variant'] + [x['id'] for x in dct['nodes']])
    .repartition(1024)
)

# create sites-only VDS
(
	VariantDataset
	.from_table(kt)
    .write('gs://annotationdb/dbNSFP/dbNSFP.vds', overwrite = True)
)
