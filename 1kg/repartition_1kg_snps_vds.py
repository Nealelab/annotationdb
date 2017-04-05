#!/usr/bin/env python

import hail

# Google bucket
bucket = 'gs://hail-annotation/'

(

# start Hail context
hail.HailContext(log = '/home/hail/hail.log')

# read in 1kg SNPs sites-only VDS
.read(bucket + '1kg/1kg_snps.vds', sites_only = True)

# repartition the VDS from 1 partition to 45 partitions (~16m each)
.repartition(45)

# write repartitioned VDS to bucket, overwriting original
.write(
    output = bucket + '1kg/1kg_snps.vds',
    overwrite = True
)

)