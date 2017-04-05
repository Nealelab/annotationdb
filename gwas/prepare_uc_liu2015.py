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
trait = 'uc'
version = 'liu2015'
directory = 'gwas/' + trait + '/'

# file names
raw_file = trait + '_' + version + '.txt.gz'
prepared_file = trait + '_' + version + '.prepared.tsv.gz'

# copy raw file to master node
call('gsutil -m cp {} {}'.format(bucket + directory + raw_file, local + raw_file), shell=True)

# read in raw file
df = pd.read_csv(
    local + raw_file,
    delim_whitespace = True
)

# select only columns of interest
df = df.loc[:, ['CHR', 'BP', 'A2', 'A1', 'INFO', 'OR', 'SE', 'P']]

# rename columns
df.columns = ['chr', 'pos', 'ref', 'alt', 'info', 'or', 'se', 'p']

# filter to keep only SNPs
condition = (df['ref'].isin(set(['A', 'C', 'G', 'T'])) & df['alt'].isin(set(['A', 'C', 'G', 'T'])))
df = df.loc[condition, :]

# flip ref and alt alleles in new df
df_flip = df.rename(columns={'ref': 'alt', 'alt': 'ref'}, copy=True)

# invert odds ratio in flipped df
df_flip.loc[:, 'or'] = 1.0/df_flip['or']

# stack regular and flipped dataframes
df_stack = pd.concat([df, df_flip], ignore_index=True).reset_index(drop=True)

# get beta values
df_stack.loc[:, 'beta'] = np.log(df_stack['or'])

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
