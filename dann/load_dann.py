#!/usr/bin/env python

import hail

# start Hail context
hc = hail.HailContext(parquet_compression = 'snappy')                                  

# load into keytable
(
    
    hc
    .import_keytable(
        'gs://annotationdb/dann/dann.tsv.bgz',
        config = hail.TextTableConfig(
            noheader = True,
            types = """
                _0: String,
                _1: Int,
                _2: String,
                _3: String,
                _4: Double
            """
        )
    )
    .annotate('variant = Variant(_0, _1, _2, _3)')
    .key_by('variant')
    .rename({'_4': 'score'})
    .select(['variant', 'score'])
    .write('gs://annotationdb/dann/dann.kt', overwrite=True)
)
