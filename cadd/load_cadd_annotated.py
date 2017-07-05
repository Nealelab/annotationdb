#!/usr/bin/env python

import json
from hail import *
from pprint import pprint

hc = HailContext(parquet_compression = 'snappy')

with hadoop_read('gs://annotationdb/cadd/cadd_annotated.json') as f:
    dct = json.load(f)

type_map = {
    'String': TString(),
    'Int': TInt(),
    'Boolean': TBoolean(),
    'Double': TDouble()
}

types = {'#Chrom': TString(), 'Pos': TInt(), 'Ref': TString(), 'Alt': TString()}
types.update({x['raw']: type_map[x['type']] for x in dct['nodes']})

kt = (
    hc
    .import_table(
        'gs://annotationdb/cadd/cadd_annotated.tsv.bgz',
        types = types
    )
    .annotate('variant = Variant(`#Chrom`, Pos, Ref, Alt)')
    .key_by('variant')
    .rename({x['raw'].strip('`'): x['id'] for x in dct['nodes']})
    .select(['variant'] + [x['id'] for x in dct['nodes']])
)

(
    VariantDataset
    .from_table(kt)
    .repartition(10000)
    .write('gs://annotationdb/cadd/cadd_annotated.vds', overwrite = True)
)
