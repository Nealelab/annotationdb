#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/gwas/cad/cad.json', './'])

with open('cad.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

# read in 1kg VDS
vds = hc.read('gs://annotationdb/onekg/onekg.vds')

# create 1kg keytable
kt_onekg = (
	vds
	.variants_keytable()
	.flatten()
	.annotate('locus = Locus(`va.onekg.chr`, `va.onekg.pos`)')
	.rename(
		{
			'va.onekg.chr': 'onekg_chr',
			'va.onekg.pos': 'onekg_pos',
			'va.onekg.ref': 'onekg_ref',
			'va.onekg.alt': 'onekg_alt'
		}
	)
	.key_by('locus')
)

# read into keytable
kt = (

	hc
	.import_keytable(
		'gs://annotationdb/gwas/cad/cad_nikpay2015.tsv.bgz',
		config = hail.TextTableConfig(
			types = """
				markername: String,
				chr: String,
				bp_hg19: Int,
				effect_allele: String,
				noneffect_allele: String,
				effect_allele_freq: Double,
				median_info: Double,
				model: String,
				beta: Double,
				se_dgc: Double,
				p_dgc: Double,
				het_pvalue: Double,
				n_studies: Int
			"""
		)
	)
	.annotate('locus = Locus(chr, bp_hg19)')
	.key_by('locus')
)

print(kt.schema)
print()
print(kt_onekg.schema)
print()
n = kt.count_rows()
print('CAD number of rows: {}'.format(str(n)))
print()

# left-join summary stats to onekg keytable on loci
kt_join = kt.join(kt_onekg, how='left')
kt_join = kt_join.filter(
	"""
	((effect_allele == onekg_ref) && (noneffect_allele == onekg_alt)) ||
	((effect_allele == onekg_alt) && (noneffect_allele == onekg_ref))
	""",
	keep = True
)

print(kt_join.schema)
print()
print('Join, post-filter number of rows: {}'.format(str(n)))
print()

