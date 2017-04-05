#!/usr/bin/env python

import json
import hail
import urllib2

# locations
bucket = 'gs://hail-annotation/'
local = '/home/hail/'
link = 'https://storage.googleapis.com/hail-annotation/annotationdb.json'

# load metadata from json file
response = urllib2.urlopen(link)
meta = json.loads(response.read())

# get SNP annotations 
snp_annotations = [x for x in meta if x['type'] == 'snp']

# start Hail context
hc = hail.HailContext(log = local + 'hail.log')

# get backbone from DANN VDS
vds_master = (hc
    .read(bucket + 'dann/dann.vds', sites_only=True)
    .annotate_variants_expr('va = {}')
)

# annotate master VDS with component VDSs
for annotation in snp_annotations:
    annotation_id = annotation['id']
    annotation_hail = annotation['hail']
    vds_master = (vds_master
        .annotate_variants_vds(
            hc.read(bucket + '{0}/{0}.vds'.format(annotation_id), sites_only=True),
            root = annotation_hail
        )
    )

# write master VDS to bucket
(
vds_master
.repartition(5000)
.write(bucket + 'master.vds', overwrite = True)
)
