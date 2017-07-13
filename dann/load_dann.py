#!/usr/bin/env python

from hail import *

# start Hail context
hc = HailContext(parquet_compression='snappy')                                  

# load into keytable
kt = (
    hc
    .import_table(
        'gs://annotationdb/dann/dann.tsv.bgz',
        no_header=True,
        types={
            'f0': TString(),
            'f1': TInt(),
            'f2': TString(),
            'f3': TString(),
            'f4': TDouble()
        }
    )
    .annotate('variant = Variant(f0, f1, f2, f3)')
    .key_by('variant')
    .rename({'f4': 'score'})
    .select(['variant','score'])
    .repartition(2001)
)

# create sites-only VDS
(
    VariantDataset
    .from_table(kt)
    .write('gs://annotationdb/dann/dann.vds', overwrite = True)
)
