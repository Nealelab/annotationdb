#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/cadd/cadd.json', './'])

with open('cadd.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

(

    hc
    .import_keytable(
        'gs://annotationdb/cadd/cadd.tsv.bgz',
        config = hail.TextTableConfig(
            types = ','.join(
                [
                    '`#Chrom`: String',
                    'Pos: Int',
                    'Ref: String',
                    'Alt: String'
                ] +
                [
                    var['raw'] + ': ' + var['type'] for var in dct['nodes']
                ]
            )
        )
    )
    .annotate(
        'variant = Variant(`#Chrom`, Pos, Ref, Alt)'
    )
    .key_by(
        'variant'
    )
    .rename(
        {
            var['raw'].strip('`'): var['id'] for var in dct['nodes']
        }
    )
    .select(
        ['variant'] + [variable['id'] for variable in dct['nodes']]
    )
    .write(
        'gs://annotationdb/cadd/cadd.kt',
        overwrite = True
    )

)
