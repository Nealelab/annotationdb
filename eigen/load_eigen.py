#!/usr/bin/env python

import json
from hail import *

hc = HailContext(parquet_compression='snappy')

with hadoop_read('gs://annotationdb/eigen/eigen.json') as f:
    dct = json.load(f)

kt = (
    hc
    .import_table('gs://annotationdb/eigen/eigen.tsv.bgz', impute=True, types={'chr': TString()})
    .annotate('variant = Variant(chr, pos, ref, alt)')
    .key_by('variant')
    .select(['variant', 'raw', 'phred', 'PC_raw', 'PC_phred'])
    .repartition(1024)
)

(
    VariantDataset
    .from_table(kt)
    .write('gs://annotationdb/eigen/eigen.vds', overwrite=True)
)
