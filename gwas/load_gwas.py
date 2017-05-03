#!/usr/bin/env python

import os
import hail
import json
import sys
import pandas as pd
import subprocess as sp

# locations
bucket = 'gs://hail-annotation/'
directory = 'gwas/'
local = '/home/hail/'

# start Hail context
hc = hail.HailContext(
    log = '/home/hail/hail.log',
    parquet_compression = 'snappy'
)

# load 1kg SNPs sites-only VDS
vds = hc.read(bucket + '1kg/1kg_snps.vds')

# send 1kg SNPs sites-only VDS to keytable
kt_master = (
    
    vds.variants_keytable()
    
    # munge 1kg keytable to get chr, pos, ref, alt columns
    .select(['v'])
    .expand_types()
    .flatten()
    .annotate(['alt = `v.altAlleles`[0].alt'])
    .select(['v.contig', 'v.start', 'v.ref', 'alt'])
    .rename(['chr', 'pos', 'ref', 'alt'])
    .key_by(['chr', 'pos', 'ref', 'alt'])
    
)

def get_keytable(path):
    
    # define types of possible summary stat variables
    types = {
        'chr': 'String',
        'pos': 'Int',
        'ref': 'String',
        'alt': 'String',
        'or': 'Double',
        'beta': 'Double',
        'se': 'Double',
        'p': 'Double',
        'info': 'Double',
        'ngt': 'Int'
    }

    # extract trait, version from path names
    trait, version = path.split('.prepared')[0].split('/')[-1].split('_')

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

    # extract summary stat variables from json dictionary
    variables = [ node['text'] for node in json_dict['nodes'] ]

    # variant key and types
    key_types = ['chr: String', 'pos: Int', 'ref: String', 'alt: String']

    # use type dictionary to get types for all variables
    var_types =  [variable + ': ' + types[variable] for variable in variables]

    # create Hail TextTableConfig
    config = hail.TextTableConfig(
        types = ', '.join(key_types + var_types)
    )

    # load summary stats into keytable
    kt_stats = hc.import_keytable(
        path = path,
        key_names = ['chr', 'pos', 'ref', 'alt'],
        npartitions = '50',
        config = config
    )
    
    # define new column names
    new_names = { name: trait + '.' + name for name in kt_stats.column_names if name not in set(['chr', 'pos', 'ref', 'alt']) }

    # rename keytable columns
    kt_stats = kt_stats.rename(new_names)
    
    return kt_stats


# get list of summary statistic paths to load, and associated json files for each
paths = sp.Popen('gsutil ls -r {}'.format(bucket + directory + '**.prepared.tsv.gz'), shell=True, stdout=sp.PIPE).communicate()[0].split()    

# initialize summary stats keytable with stats from first path
kt_stats = get_keytable(paths[0])

# iterate through summary stat files
for path in paths[1:]:
    
    # get summary stats keytable
    kt = get_keytable(path)
    
    # intersection of master keytable and summary stats keytable
    kt_stats = kt_stats.join(kt, how='outer')

# join 1kg master keytable to summary stats keytable
kt_master = kt_master.join(kt_stats, how='inner')

# add column to keytable indicating that variant has summary stats from at least one GWAS
kt_master = kt_master.annotate('hasGWAS = true')

# create keytable annotation condition
condition = ['va.{0} = table.`{0}`'.format(column) for column in kt_master.column_names if column not in set(['chr', 'pos', 'ref', 'alt'])]

(
vds

# add indicator
.annotate_variants_expr('va.hasGWAS = false')

# use master keytable to annotate 1kg VDS
.annotate_variants_keytable(
    keytable = kt_master,
    condition = condition,
    vds_key = ['va.chr', 'va.pos', 'va.ref', 'va.alt']
)

# filter to only variants with summary stats from at least one GWAS
.filter_variants_expr('va.hasGWAS', keep=True)

# write to bucket
.write(output = bucket + directory + 'gwas.vds', overwrite=True)

)
