#!/usr/bin/env python

import hail

# locations
log = '/mnt/lustre/labbott/annotationdb/hail.log'
raw = 'file:///mnt/lustre/labbott/annotationdb/dann/dann.tsv.bgz'
vds = 'file:///mnt/lustre/labbott/annotationdb/dann/dann.vds'
                                      
(

# start Hail context
hail.HailContext(
    log = log,
    parquet_compression = 'snappy'
)

# load DANN text file into sites-only VDS
.import_annotations_table(
    path = raw,
    variant_expr = 'Variant(chr, pos, ref, alt)',
    code = """
           va.score1 = table.dann1,
           va.score2 = table.dann2
           """,
    config = hail.TextTableConfig(
                 types = """
                         chr: String,
                         pos: Int,
                         ref: String,
                         alt: String,
                         dann1: Double,
                         dann2: Double
                         """
    )
)

# write VDS to bucket                                          
.write(
    output = vds, 
    overwrite = True
)

)
