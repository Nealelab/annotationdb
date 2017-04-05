#!/usr/bin/env python

import hail

# Google bucket
bucket = 'gs://hail-annotation/'

# TextTableConfig for 1kg SNPs
config = hail.TextTableConfig(
	types = """
			chr: String,
			pos: Int,
			ref: String,
			alt: String
			"""
)

(

# initialize Hail context
hail.HailContext(log = '/home/hail/hail.log')

# import 1kg SNPs table to sites-only VDS
.import_annotations_table(
	path = bucket + '1kg/1kg_snps.tsv.gz',
	variant_expr = 'Variant(chr, pos, ref, alt)',
	config = config
)

# split multi-allelic variants in vds
.split_multi()

# write vds to bucket
.write(
    output = bucket + '1kg/1kg_snps.vds'
)

)