#!/usr/bin/env python

from hail import *
from pprint import pprint

hc = HailContext(log = '/home/labbott/hail.log')

vds = hc.import_vcf('gs://annotationdb/test/sample.vcf').split_multi()

vds1 = (vds.annotate_variants_db('va.vep')
		   .annotate_variants_expr('va.my_gene = va.vep.transcript_consequences[0].gene_symbol')
		   .annotate_variants_db('va.gene.constraint.pli', gene_key='va.my_gene'))

pprint(vds1.variant_schema)

vds2 = vds.annotate_variants_db('va.isLCR')

pprint(vds2.variant_schema)
n = vds2.count_variants()
print('nVariants: {:,d}'.format(n))
