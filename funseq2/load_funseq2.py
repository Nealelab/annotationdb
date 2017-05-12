#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/funseq2/funseq2.json', './'])

with open('funseq2.json', 'rb') as f:
    dct = json.load(f)

# start Hail context
hc = hail.HailContext(parquet_compression = 'snappy')   

kt = (

	hc
	.import_keytable(
		'gs://annotationdb/funseq2/hg19_NCscore_funseq216.tsv.bgz',
		config = hail.TextTableConfig(
			types = """
				`#chr`: String,
				pos: Int,
				ref: String,
				alt: String,
				score: Double
			"""
		)
	)
	.rename({'alt': 'alt_combined'})
	.annotate(
		"""
		chr = `#chr`.replace("chr", ""),
		alt = alt_combined.split("\\\|")
		"""
	)
	.explode('alt')
	.annotate('variant = Variant(chr, pos, ref, alt)')
	.key_by('variant')
    .annotate(','.join(['{0} = {0}'.format(x['id']) for x in dct['nodes']]))
    .select(
    	['variant'] +
    	[x['id'] for x in dct['nodes']]
    )
)

# create sites-only VDS
(
    hail
    .VariantDataset.from_keytable(kt)
    .repartition(1024)
    .write(
        'gs://annotationdb/funseq2/funseq2.vds',
        overwrite = True
    )
)
