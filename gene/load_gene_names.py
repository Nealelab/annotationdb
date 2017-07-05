#!/usr/bin/env python

import hail
from hail.expr import *

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_table('gs://annotationdb/gene/names/names.tsv.bgz', missing = '.')
	.rename({
		'Gene_name': 'gene_symbol',
		'Ensembl_gene': 'ensembl_gene',
		'chr': 'chromosome',
		'Gene_old_names': 'gene_old_names',
		'Gene_other_names': 'gene_other_names',
		'Uniprot_acc': 'uniprot_acc',
		'Uniprot_id': 'uniprot_ID',
		'Entrez_gene_id': 'entrez_gene_ID',
		'CCDS_id': 'ccds_ID',
		'Refseq_id': 'refseq_ID',
		'ucsc_id': 'ucsc_ID',
		'MIM_id': 'mim_ID',
		'Gene_full_name': 'gene_full_name'
	})
	.annotate('gene = gene_symbol')
	.key_by('gene')
	.write('gs://annotationdb/gene/names/names.kt', overwrite = True)
)
