#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/eigen/eigen.json', './'])

with open('eigen.json', 'rb') as f:
    dct = json.load(f)

hc = hail.HailContext(parquet_compression = 'snappy')

# load into keytable
kt = (

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
    .annotate(
        'eigen = {{{0}}}'.format(','.join(['{0}: {0}'.format(x['id']) for x in dct['nodes']]))
    )
    .select(
        [
            'variant',
            'eigen'
        ]
    )

)

# create sites-only VDS
(
    hail
    .VariantDataset.from_keytable(kt)
    .write(
        'gs://annotationdb/eigen/eigen.vds',
        overwrite = True
    )
)
