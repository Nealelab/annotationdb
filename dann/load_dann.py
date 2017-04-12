#!/usr/bin/env python

import hail
import json
from subprocess import call

call(['gsutil', 'cp', 'gs://annotationdb/dann/dann.json', './'])

with open('dann.json', 'rb') as f:
    dct = json.load(f)

# start Hail context
hc = hail.HailContext(parquet_compression = 'snappy')                                  

# load into keytable
kt = (
    
    hc
    .import_keytable(
        'gs://annotationdb/dann/dann.tsv.bgz',
        config = hail.TextTableConfig(
            noheader = True,
            types = ','.join(
                [
                    '_0: String',
                    '_1: Int',
                    '_2: String',
                    '_3: String'
                ] +
                [
                    var['raw'] + ': ' + var['type'] for var in dct['nodes']
                ]
            )
        )
    )
    .annotate(
        'variant = Variant(_0, _1, _2, _3)'
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
        'dann = {{{0}}}'.format(','.join(['{0}: {0}'.format(x['id']) for x in dct['nodes']]))
    )
    .select(
        [
            'variant',
            'dann'
        ]
    )
)

# create sites-only VDS
(
    hail
    .VariantDataset.from_keytable(kt)
    .write(
        'gs://annotationdb/dann/dann.vds',
        overwrite = True
    )
)
