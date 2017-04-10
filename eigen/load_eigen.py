#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/eigen/eigen.json', './'])

with open('eigen.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

(

    hc
    .import_keytable(
        'gs://annotationdb/eigen/eigen.tsv.bgz',
        config = hail.TextTableConfig(
            types = ','.join(
                [
                    'chr: String',
                    'pos: Int',
                    'ref: String',
                    'alt: String'
                ] +
                [
                    var['raw'] + ': ' + var['type'] for var in dct['nodes']
                ]
            )
        )
    )
    .annotate(
        'variant = Variant(chr, pos, ref, alt)'
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
        'gs://annotationdb/eigen/eigen.kt',
        overwrite = True
    )

)
