#!/usr/bin/env python

import hail
import json
import urllib2
from subprocess import call

# variant annotations
variants = [
    'cadd',
    'dann',
    'dbNSFP',
    'discovEHR',
    'eigen',
    'funseq2'
]

# interval annotations
intervals = [
    'chromHMM',
    #'fantom5',
    'gencode19',
    'lcr',
    'ldscore',
    'linsight',
    'segway',
    'tfbs',
    #'vista'
]

# collect each annotation's .json file into master json file
master_json = []
for annotation in variants + intervals:
    print 'Fetching {} JSON...'.format(annotation)
    response = urllib2.urlopen('https://storage.googleapis.com/annotationdb/{0}/{0}.json'.format(annotation))
    master_json.append(json.loads(response.read()))

# write master JSON to cluster master machine
with open('annotationdb.json', 'wb') as f:
    json.dump(master_json, f)

# copy master JSON to Google bucket
call(['gsutil', 'cp', 'annotationdb.json', 'gs://annotationdb/master/annotationdb.json'])

# start Hail context
hc = hail.HailContext(parquet_compression = 'snappy')

# load variant annotation keytables
kts = {}
print ''
print 'Load keytables:'
for v in variants:
    print '  Reading {} keytable...'.format(v)
    kts[v] = hc.read_keytable('gs://annotationdb/{0}/{0}.kt'.format(v))
print 'Loaded keytables!'

# check schemas of keytables
#for v in kts:
#    print ''
#    print '{} schema:'.format(v)
#    print kts[v].schema

#print kts['dann'].query(['variant.filter(x => x.ref.length() > 1 || x.alt().length() > 1).count()'])[0]

#indels = set(kts[variants[0]].query(['variant.filter(x => !(x.ref.length() == 1 && x.alt().length() == 1)).collect()'])[0])
#for v in variants[1:]:
#    indels.update(kts[v].query(['variant.filter(x => !(x.ref.length() == 1 && x.alt().length() == 1)).collect()'])[0])

df_dann = kts['dann'].select(['variant']).to_dataframe()
df_discovEHR = kts['discovEHR'].select(['variant']).to_dataframe()

df_union = df_dann.union(df_discovEHR)
df_union = df_union.dropDuplicates()

kt_union = (

    hc
    .dataframe_to_keytable(df_union, keys=[])
    .annotate('variant = Variant(`variant.contig`, `variant.start`, `variant.ref`, `variant.altAlleles`[0].alt)')
    .key_by('variant')
    .select(['variant'])
    
)

vds = hail.VariantDataset.from_keytable(kt_union)

print vds.variant_schema

#for v in keys[1:]:
#    kt_all = kt_all.join(kts[v].select(['variant']), how = 'outer')

#print kt_all.count_rows()

# load DANN keytable as backbone
#kt_dann = hc.read_keytable('gs://annotationdb/dann/dann.kt')
#print kt_dann.count_rows()

"""
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
"""
