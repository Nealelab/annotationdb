#!/usr/bin/env python

import os
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
    'dhs',
    #'fantom5',
    #'gencode19',
    #'lcr',
    #'ldscore',
    #'linsight',
    #'segway',
    #'tfbs',
    #'vista'
]

# collect each annotation's JSON dictionary into master JSON data dictionary
print 'Building master JSON data dictionary...'
master_json = []
for annotation in variants + intervals:
    print '-> fetching {} metadata...'.format(annotation)
    response = urllib2.urlopen('http://storage.googleapis.com/annotationdb/{0}/{0}.json'.format(annotation))
    master_json.append(json.loads(response.read()))

# write master JSON to local
print 'Master dictionary built!'
with open('annotationdb.json', 'wb') as f:
    json.dump(master_json, f, indent=3)

# copy master JSON to Google bucket
print "Writing master dictionary to Google Cloud Storage..."
with open(os.devnull, 'wb') as f:
    call(['gsutil', 'cp', 'annotationdb.json', 'gs://annotationdb/annotationdb.json'], stdout=f, stderr=f)
print "Master dictionary written to 'gs://annotationdb/annotationdb.json'."
