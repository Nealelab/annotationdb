#!/usr/bin/env python

from hail import *
from pprint import pprint

hc = HailContext()

vds = (hc.read('gs://epi25/data/filterGT.annotated.20170119.hardcalls.vds')
		 .annotate_variants_expr('va = {}')
		 .annotate_variants_db([
		 	'va.targets.exome_agilent_designed_120',
		 	'va.targets.exome_agilent_refseq_plus_3_boosters',
		 	'va.targets.exome_illumina_coding_v1',
		 	'va.pruned_sets.exome_common9k',
		 	'va.pruned_sets.purcell5k',
		 	'va.onekg'
		 ]))

pprint(vds.variant_schema)
print vds.count_variants()
