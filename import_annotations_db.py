#!/usr/bin/env python
from __future__ import print_function

import hail
from types import MethodType

def import_annotations_db(self, *args):
  
    # import modules needed by this function
    import json
    import urllib2
    
    # collect annotations in a set to drop any duplicates
    annotations = set([arg for arg in args])
    
    # mapping from top-level annotations to list of paths to include from that struct
    top_levels = {}
    for x in annotations:
        top = x.split('.')[1]
        try:
            top_levels[top].append(x)
        except KeyError:
            tops[top] = [x]

    # read meta file from bucket into dictionary
    response = urllib2.urlopen('https://storage.googleapis.com/annotationdb/annotationdb.json')
    meta = json.load(response)
    
    # separate variant and interval annotations
    variants = [x['id'] for x in meta if x['id'] in top_levels.keys() and x['type'] == 'variant']
    intervals = [x['id'] for x in meta if x['id'] in top_levels.keys() and x['type'] == 'interval']

    # add variant annotations
    for v in variants:

        print()
        if len(top_levels[v]) == 1:
            print('Adding {} annotation...'.format(v))
        else:
            print('Adding {} annotations...'.format(v))

        self = self.annotate_variants_vds(
            hc.read('gs://annotationdb/{0}/{0}.vds'.format(v)),
            code = ','.join(['va.{0} = vds.{0}'.format(x.replace('va.', '')) for x in top_levels[v]])
        )

    # add interval annotations
    for i in intervals:

        print()
        if len(top_levels[i]) == 1:
            print('Adding {} annotation...'.format(i))
        else:
            print('Adding {} annotations...'.format(i))

        self = self.annotate_variants_table(
            hc.read_keytable('gs://annotationdb/{0}/{0}.kt'.format(i)),
            expr = ','.join(['va.{0} = table.{0}'.format(x.replace('va.', '')) for x in top_levels[i]])
        )

    ######### TO DO ############
    # add gene annotations    ##
    # add Nirvana annotations ##
    ############################

    # return annotated VDS
    return self
   
  
## test the import_annotations_db() function

hc = hail.HailContext(log = '/home/hail/hail.log')
sample_vds = hc.import_vcf('gs://hail-common/sample.vcf')
sample_vds.import_annotations_db = MethodType(import_annotations_db, sample_vds, hail.VariantDataset)

annotations = [
    'va.dann', 
    'va.eigen.PC_phred',
    'va.eigen.raw'
]

new_vds = sample_vds.import_annotations_db(*annotations)
print(new_vds.variant_schema)
