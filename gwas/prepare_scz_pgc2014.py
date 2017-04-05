#!/usr/bin/env python

import os
import json
import numpy as np
import pandas as pd
from subprocess import call

# locations
bucket = 'gs://hail-annotation/'
local = '/home/hail/'

# trait
trait = 'scz'
version = 'pgc2014'
directory = 'gwas/' + trait + '/'

# file names
raw_file = trait + '_' + version + '.txt.gz'
prepared_file = trait + '_' + version + '.prepared.tsv.gz'

# copy raw file to master node
call('gsutil -m cp {} {}'.format(bucket + directory + raw_file, local + raw_file), shell=True)

# prepare schizophrenia summary statistics file
df = pd.read_csv(
    local + raw_file, 
    sep = '\t', 
    header = 0, 
    names = ['chr', 'alt', 'ref', 'pos', 'info', 'or', 'se', 'p', 'ngt']
)

# strip "chr" from beginning of chromsome column values
df.loc[:, 'chr'] = df['chr'].str[3:]

# subset to include only SNPs
condition = (df['alt'].isin(set(['A', 'C', 'G', 'T'])) & df['ref'].isin(set(['A', 'C', 'G', 'T'])))
df = df.loc[condition, :]

# flip ref and alt alleles
df_flip = df.rename(columns={'ref': 'alt', 'alt': 'ref'}, copy=True)

# invert odds ratios
df_flip.loc[:, 'or'] = 1.0/df_flip['or']

# stack regular and flipped dataframes
df_stack = pd.concat([df, df_flip], ignore_index=True)

# get beta value
df_stack.loc[:, 'beta'] = np.log(df_stack['or'])

# reorder columns
df_stack = df_stack[['chr', 'pos', 'ref', 'alt', 'or', 'beta', 'se', 'p', 'info', 'ngt']]

# sort by chr, pos, ref, alt
df_stack.sort_values(
    by = ['chr', 'pos', 'ref', 'alt'], 
    ascending = True, 
    inplace = True
)

# write transformed dataframe to gzipped local file on master node
df_stack.to_csv(
    local + prepared_file, 
    sep = '\t', 
    header = True, 
    index = False,
    compression = 'gzip'
)

# copy prepared file back to cloud bucket
call('gsutil -m cp {} {}'.format(local + prepared_file, bucket + directory + prepared_file), shell=True)

# prepare meta file
meta = {
    "text": trait,
    "nodes": [
        {"text": "or"},
        {"text": "beta"},
        {"text": "se"},
        {"text": "p"},
        {"text": "info"},
        {"text": "ngt"}
    ]
}

# write meta to json file
with open(local + trait + '_' + version + '.json', 'wb') as f:
    json.dump(meta, f)
    
# copy meta file to bucket
call('gsutil -m cp {} {}'.format(local + trait + '_' + version + '.json', bucket + directory), shell=True)
