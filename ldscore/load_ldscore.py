#!/usr/bin/env python

import hail
import json

hc = hail.HailContext(parquet_compression = 'snappy')

(
	hc
	.import_table(
		'gs://annotationdb/ldscore/ldscore.tsv.bgz',
		types = {
			'chr': TString(),
			'start': TInt(),
			'end': TInt(),
			'coding_ucsc': TBoolean(),
			'conserved': TBoolean(),
			'ctcf': TBoolean(),
			'dgf': TBoolean(),
			'dhsp': TBoolean(),
			'dhs': TBoolean(),
			'enhancers': TBoolean(),
			'fantom5': TBoolean(),
			'dhsf': TBoolean(),
			'h3k4me1p': TBoolean(),
			'h3k4me1': TBoolean(),
			'h3k4me3p': TBoolean(),
			'h3k4me3': TBoolean(),
			'h3k9acp': TBoolean(),
			'h3k9ac': TBoolean(),
			'h3k27ac': TBoolean(),
			'intron_ucsc': TBoolean(),
			'promoter_ucsc': TBoolean(),
			'promoter_flanking': TBoolean(),
			'repressed': TBoolean(),
			'superenh': TBoolean(),
			'tfbs': TBoolean(),
			'transcribed': TBoolean(),
			'tss': TBoolean(),
			'3utr': TBoolean(),
			'5utr': TBoolean(),
			'weakenh': TBoolean()
		}
	)
	.rename({'3utr': 'three_prime_utr', '5utr': 'five_prime_utr'})
	.annotate('interval = Interval(Locus(chr, start), Locus(chr, end + 1))')
	.key_by('interval')
	.select([
		'interval',
		'coding_ucsc',
		'conserved',
		'ctcf',
		'dgf',
		'dhsp',
		'dhs',
		'enhancers',
		'fantom5',
		'dhsf',
		'h3k4me1p',
		'h3k4me1',
		'h3k4me3p',
		'h3k4me3',
		'h3k9acp',
		'h3k9ac',
		'h3k27ac',
		'intron_ucsc',
		'promoter_ucsc',
		'promoter_flanking',
		'repressed',
		'superenh',
		'tfbs',
		'transcribed',
		'tss',
		'three_prime_utr',
		'five_prime_utr',
		'weakenh'
	]),
	.write('gs://annotationdb/ldscore/ldscore.kt', overwrite = True)
)
