#!/usr/bin/env python

from hail import *

hc = HailContext(parquet_compression = 'snappy')  

kt = (
	hc
	.import_table(
		'gs://annotationdb/funseq2/hg19_NCscore_funseq216.tsv.bgz',
		types={
			'`#chr': TString(),
			'pos': TInt(),
			'ref': TString(),
			'alt': TString(),
			'score': TDouble()
		}
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
    .select(['variant', 'score'])
    .repartition(1024)
)

(
    VariantDataset
    .from_table(kt)
    .write('gs://annotationdb/funseq2/funseq2.vds', overwrite=True)
)
