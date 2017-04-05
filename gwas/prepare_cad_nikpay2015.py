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
trait = 'cad'
version = 'nikpay2015'
directory = 'gwas/' + trait + '/'

# file names
raw_file = trait + '_' + version + '.txt.gz'
prepared_file = trait + '_' + version + '.prepared.tsv.gz'

# copy raw file to master node
call('gsutil -m cp {} {}'.format(bucket + directory + raw_file, local + raw_file), shell=True)

# prepare schizophrenia summary statistics file
df = pd.read_csv(
    local + raw_file, 
    delim_whitespace = True
)

# select columns of interest
df = df.loc[:, ['chr', 'bp_hg19', 'effect_allele', 'noneffect_allele', 'median_info', 'beta', 'se_dgc', 'p_dgc']]

# rename columns
df.columns = ['chr', 'pos', 'alt', 'ref', 'info', 'beta', 'se', 'p']

# filter to keep only SNPs
condition = (df['ref'].isin(set(['A', 'C', 'G', 'T'])) & df['alt'].isin(set(['A', 'C', 'G', 'T'])))
df = df.loc[condition, :]

# flip ref and alt alleles in new df
df_flip = df.rename(columns={'ref': 'alt', 'alt': 'ref'}, copy=True)

# reverse betas in flipped df
df_flip.loc[:, 'beta'] = -1.0 * df_flip['beta']

# stack regular and flipped dataframes
df_stack = pd.concat([df, df_flip], ignore_index=True).reset_index(drop=True)

# get odds ratios
df_stack.loc[:, 'or'] = np.exp(df_stack['beta'])

# order columns
df_stack = df_stack[['chr', 'pos', 'ref', 'alt', 'or', 'beta', 'se', 'p', 'info']]

# sort values by chr, pos, ref, alt
df_stack.sort_values(
    ['chr', 'pos', 'ref', 'alt'], 
    ascending=True,
    inplace=True
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
        {"text": "info"}
    ]
}

# write meta to json file
with open(local + trait + '_' + version + '.json', 'wb') as f:
    json.dump(meta, f)
    
# copy meta file to bucket
call('gsutil -m cp {} {}'.format(local + trait + '_' + version + '.json', bucket + directory), shell=True)
