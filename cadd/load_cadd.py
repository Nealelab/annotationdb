#!/usr/bin/env python

import hail
from hail.expr import *

hc = hail.HailContext(parquet_compression = 'snappy')

kt = (

    hc
    .import_table(
        'gs://annotationdb/cadd/cadd_annotated.tsv.bgz',
        comment = '##',
        types = {
            '`#Chrom`': TString(),
            'Pos': TInt(),
            'Ref': TString(),
            'Alt': TString(),
            'RawScore': TDouble(),
            'PHRED': TDouble()
        }
    )
    .annotate('variant = Variant(`#Chrom`, Pos, Ref, Alt)')
    .key_by('variant')
    .select(['variant', 'RawScore', 'PHRED'])
    .repartition(2001)
)

# create sites-only VDS
(
    hail
    .VariantDataset
    .from_table(kt)
    .write(
        'gs://annotationdb/cadd/cadd.vds',
        overwrite = True
    )
)

