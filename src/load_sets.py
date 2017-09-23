from hail import *

hc = HailContext()

kt_common9k = (
	hc
	.import_table('gs://annotationdb/pruned_sets/exome_common9k.tsv', no_header=True, types={'f3': TInt()})
	.annotate(['variant1 = Variant(f0, f3, f4, f5)', 'variant2 = Variant(f0, f3, f5, f4)'])
	.select(['variant1', 'variant2'])
)

(
	hc
	.read('gs://annotationdb/onekg/onekg.sites.vds')
	.annotate_variants_table(kt_common9k.key_by('variant1').select('variant1'), expr='va.isSet1 = table')
	.annotate_variants_table(kt_common9k.key_by('variant2').select('variant2'), expr='va.isSet2 = table')
	.filter_variants_expr('va.isSet1 || va.isSet2')
	.variants_table()
	.annotate('exome_common9k = v')
	.key_by('exome_common9k')
	.select('exome_common9k')
	.repartition(1)
	.write('gs://annotationdb/pruned_sets/exome_common9k.kt', overwrite=True)
)

(
	hc
	.import_table('gs://annotationdb/pruned_sets/purcell5k.interval_list', no_header=True, types={'f0': TInterval()})
	.rename({'f0': 'purcell5k'})
	.key_by('purcell5k')
	.select('purcell5k')
	.write('gs://annotationdb/pruned_sets/purcell5k.kt', overwrite=True)
)
