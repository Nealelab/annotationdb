#!/usr/bin/env python

from hail import *
from pprint import pprint

hc = HailContext(log = '/home/labbott/hail.log')

vds = (
    hc
    .import_vcf('gs://annotationdb/test/sample.vcf')
    .split_multi()
    .annotate_variants_db('va')
    .annotate_variants_expr('va.my_gene = va.vep.transcript_consequences[0].gene_symbol')
    .annotate_variants_db('va.gene.constraint.pli', gene_key = 'va.my_gene')
)

pprint(vds.variant_schema)
