#!/usr/bin/env python

import os
import hail
import json
import sys
import pandas as pd
import subprocess as sp

# locations
bucket = 'gs://hail-annotation/'
trait = 'dhs'
local = '/home/hail/'

# start Hail context
hc = hail.HailContext(log = '/home/hail/hail.log')

# define json file name to look for
json_file = trait + '_' + version + '.json'
json_path = bucket + directory + trait + '/' + json_file

# copy companion json file to local directory if it exists
try:
    sp.check_output(
        'gsutil cp {} {}'.format(json_path, local + json_file), 
        stderr = sp.STDOUT,
        shell=True
    )
except sp.CalledProcessError:
    print "File '{}' does not exist!".format(json_path)
    
# load json file into dictionary
with open(local + json_file, 'rb') as f:
    json_dict = json.load(f)


kt = (
    hc
    .import_keytable(
        path = bucket + trait + '/' + '{}.prepared.tsv.gz'.format(trait), 
        key_names = ['chr', 'pos_start', 'pos_end'],
        config = config
)
