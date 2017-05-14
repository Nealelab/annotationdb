#!/usr/bin/env python

import hail
import json
from subprocess import call

hc = hail.HailContext(log = '/home/hail/hail.log', parquet_compression = 'snappy')

with hail.hadoop_read('gs://annotationdb/cadd/cadd.json') as f:
    dct = json.load(f)
    
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
    .annotate('variant = Variant(`#Chrom`, Pos, Ref, Alt)')
    .key_by('variant')
    .rename({var['raw'].strip('`'): var['id'] for var in dct['nodes']})
    .annotate(','.join(['{0} = {0}'.format(x['id']) for x in dct['nodes']]))
    .select(
        ['variant'] +
        [x['id'] for x in dct['nodes']]
    )
)

print kt.schema

# create sites-only VDS
(
    hail
    .VariantDataset.from_keytable(kt)
    .repartition(10000)
    .write(
        'gs://annotationdb/cadd/cadd.vds',
        overwrite = True
    )
)

