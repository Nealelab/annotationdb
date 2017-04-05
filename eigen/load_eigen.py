#!/usr/bin/env python

import hail

# Google bucket
bucket = 'gs://hail-annotation/'
                                      
(

# start Hail context
hail.HailContext(
    log = '/home/hail/hail.log',
    parquet_compression = 'snappy'
)

# load EIGEN text file into sites-only VDS
.import_annotations_table(
    path = bucket + 'eigen/' + 'eigen.tsv.bgz',
    variant_expr = 'Variant(chr, position, ref, alt)',
    code = """
           va.raw = table.`Eigen-raw`,
           va.phred = table.`Eigen-phred`,
           va.PC_raw = table.`Eigen-PC-raw`,
           va.PC_phred = table.`Eigen-PC-phred`
           """,
    config = hail.TextTableConfig(
                 types = """
                         chr: String,
                         position: Int,
                         ref: String,
                         alt: String,
                         `Eigen-raw`: Double,
                         `Eigen-phred`: Double,
                         `Eigen-PC-raw`: Double,
                         `Eigen-PC-phred`: Double
                         """ 
    )
)

# write VDS to bucket                                          
.write(
    output = bucket + 'eigen/' + 'eigen.vds', 
    overwrite = True
)

)