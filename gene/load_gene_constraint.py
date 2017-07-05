#!/usr/bin/env python

import hail
from hail.expr import *

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_table(
		'gs://annotationdb/gene/constraint/constraint.tsv.bgz',
		types = {
			'gene_name': TString(),
			'transcript': TString(),
			'chr': TString(),
			'n_exons': TInt(),
			'bp': TInt(),
			'syn_z': TDouble(),
			'mis_z': TDouble(),
			'lof_z': TDouble(),
			'pli': TDouble(),
			'syn_z_notcga': TDouble(),
			'mis_z_notcga': TDouble(),
			'lof_z_notcga': TDouble(),
			'pli_notcga': TDouble(),
			'syn_z_nopsych': TDouble(),
			'mis_z_nopsych': TDouble(),
			'lof_z_nopsych': TDouble(),
			'pli_nopsych': TDouble()
		}
	)
	.rename({
		'gene_name': 'gene_symbol',
		'transcript': 'transcript_ID',
		'chr': 'chromosome',
		'bp': 'n_bp'
	})
	.annotate('gene = gene_symbol')
	.key_by('gene')
	.write('gs://annotationdb/gene/constraint/constraint.kt', overwrite = True)
)
