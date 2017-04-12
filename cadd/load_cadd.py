#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/cadd/cadd.json', './'])

with open('cadd.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

kt = (

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
    .annotate(
        'cadd = {{{0}}}'.format(','.join(['{0}: {0}'.format(x['id']) for x in dct['nodes']]))
    )
    .select(
        [
            'variant',
            'cadd'
        ]
    )

)

# create sites-only VDS
(
    hail
    .VariantDataset.from_keytable(kt)
    .write(
        'gs://annotationdb/cadd/cadd.vds',
        overwrite = True
    )
)
