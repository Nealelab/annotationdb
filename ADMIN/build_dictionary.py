#!/usr/bin/env python

import os
import json
from urllib2 import urlopen
from pprint import pprint
from subprocess import call, Popen, PIPE

# variant annotations
annotations = [
    'cadd',
    'chromHMM',
    'dann',
    'dbNSFP',
    'dhs',
    'discovEHR',
    'eigen',
    'fantom5',
    'funseq2',
    'gencode19',
    'gene',
    'gnomAD',
    'isLCR',
    'ldscore',
    'linsight',
    'segway',
    'tfbs',
    'vep',
    'vista'
]

# collect each annotation's JSON dictionary into master JSON data dictionary
print('Building master JSON data dictionary...')
master_json = []
for annotation in annotations:
    print('-> fetching {} metadata...'.format(annotation))
    response = Popen(['gsutil', 'cat', 'gs://annotationdb/{0}/{0}.json'.format(annotation)], stdout=PIPE).communicate()[0].strip()
    #response = urlopen('http://storage.googleapis.com/annotationdb/{0}/{0}.json?ignoreCache=1'.format(annotation))
    master_json.append(json.loads(response))

# write master JSON to local
print('Master dictionary built!')
with open('tree.json', 'wb') as f:
    json.dump(master_json, f, indent=3)

# copy master JSON to Google bucket
print("Writing master dictionary to Google Cloud Storage...")
with open(os.devnull, 'wb') as f:
    call(['gsutil', 'cp', 'tree.json', 'gs://annotationdb/tree.json'], stdout=f, stderr=f)
print("Master dictionary written to 'gs://annotationdb/tree.json'.")

# create annotation: database file for each annotation
print("Creating annotation -> database file mapping...")

def get_exprs(node, prefix, db_root, current_exprs):

    current_exprs[node['hail']] = node['hail'].replace(db_root, prefix)

    if 'nodes' in node:

        children = node['nodes']

        if prefix == 'table' and len(children) == 1:
            current_exprs[children[0]['hail']] = 'table'

        else:
            # recurse through all remaining nodes on the branch
            for child in children:
                current_exprs = get_exprs(node=child, prefix=prefix, db_root=db_root, current_exprs=current_exprs) 

    elif not current_exprs:
        current_exprs[node['hail']] = prefix

    return current_exprs

def map_files(nodes, files):
    
    for node in nodes:
        
        # for each node, see if there is a 'db_file' field
        try:
            file = node['db_file']

        # if no 'db_file' field, run function again on child nodes
        except KeyError:
            map_files(node['nodes'], files)

        # if 'db_file' field, get paths of all annotations contained in that file
        else:
            prefix = 'vds' if file.endswith('.vds') else 'table'
            if file == 'gs://annotationdb/vep/vep.vds':
                prefix = 'vds.vep'
            entry = {
                'file': file,
                'annotations': get_exprs(node=node, prefix=prefix, db_root=node['hail'], current_exprs={'va': prefix})
            }
            files.append(entry)
           
    return files

# create map of files, the annotations they contain, and the exprs to bring in those annotations
files = map_files(master_json, [])

# write annotation: file map to pickle file
with open('file_map.json', 'wb') as f:
    json.dump(files, f, indent=3)
print("File mapping created!")

# copy to Google bucket
print("Writing file mapping to Google Cloud Storage...")
with open(os.devnull, 'wb') as f:
    call(['gsutil', 'cp', 'file_map.json', 'gs://annotationdb/file_map.json'], stdout=f, stderr=f)
print("File mapping written to 'gs://annotationdb/file_map.json'.")
