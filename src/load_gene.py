#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression='snappy')

kt_constraint = (
	hc
	.import_table(
		'gs://annotationdb/gene/constraint.tsv.bgz',
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
	.annotate(
		"""
		constraint = {
			transcript_ID: transcript_ID,
			chromosome: chromosome,
			n_exons: n_exons,
			n_bp: n_bp,
			syn_z: syn_z,
			mis_z: mis_z,
			lof_z: lof_z,
			pli: pli,
			syn_z_notcga: syn_z_notcga,
			mis_z_notcga: mis_z_notcga,
			lof_z_notcga: lof_z_notcga,
			pli_notcga: pli_notcga,
			syn_z_nopsych: syn_z_nopsych,
			mis_z_nopsych: mis_z_nopsych,
			lof_z_nopsych: lof_z_nopsych,
			pli_nopsych: pli_nopsych
		}
		"""
	)
	.select(['gene', 'constraint'])
)

kt_names = (
	hc
	.import_table('gs://annotationdb/gene/names.tsv.bgz', missing='.')
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
	.annotate(
		"""
		names = {
			ccds_ID: ccds_ID,
			chromosome: chromosome,
			ensembl_gene: ensembl_gene,
			entrez_gene_ID: entrez_gene_ID,
			gene_full_name: gene_full_name,
			gene_old_names: gene_old_names,
			gene_other_names: gene_other_names,
			mim_ID: mim_ID,
			refseq_ID: refseq_ID,
			ucsc_ID: ucsc_ID,
			uniprot_ID: uniprot_ID,
			uniprot_acc: uniprot_acc
		}
		"""
	)
	.select(['gene', 'names'])
)

(
	kt_constraint
	.join(kt_names, how='outer')
	.write('gs://annotationdb/gene.kt', overwrite=True)
)
