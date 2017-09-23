#!/usr/bin/env python

import json
import pandas as pd
import subprocess as sp

# locations
bucket = 'gs://hail-annotation/'
directory = 'dhs/'
local = '/home/hail/'

# copy to master node
sp.call('gsutil -m cp {} {}'.format(bucket + directory + 'dhs.txt.gz', local + 'dhs.txt.gz'), shell=True)

# read into dataframe
df = pd.read_csv(local + 'dhs.txt.gz', delim_whitespace=True)

# rename some columns
df.rename(
    columns={
        'Chr': 'chr', 
        'Start': 'pos_start',
        'End': 'pos_end',
        'TSS.Status': 'TSS_Status'
    }, 
    inplace=True
)

# drop DHS.ID column
df.drop('DHS.ID', axis=1, inplace=True)

# prepend 'dhs' to each column name
new_names = {col: 'dhs.' + col for col in df.columns if col not in set(['chr', 'pos_start', 'pos_end'])}
df.rename(columns=new_names, inplace=True)

# strip prefix from chromosome
df.loc[:, 'chr'] = df['chr'].apply(lambda x: x[3:])

# convert 0's and 1's to falses and trues
for col in df.drop(['chr', 'pos_start', 'pos_end', 'dhs.Pvalue'], axis=1):
    df.loc[df[col] == 0, col] = False
    df.loc[df[col] == 1, col] = True
    df.loc[:, col] = df[col].astype(bool)

# write to master node
df.to_csv(
    local + 'dhs.prepared.tsv.gz',  
    sep='\t',
    header=True,
    index=False,
    compression='gzip'
)

# copy back to bucket
sp.call('gsutil -m cp {} {}'.format(local + 'dhs.prepared.tsv.gz', bucket + directory + 'dhs.prepared.tsv.gz'), shell=True)

# create meta json file
dict_dhs = {
    'text': 'dhs',
    'nodes': [{'text': col.split('.')[-1]} for col in df.drop(['chr', 'pos_start', 'pos_end'], axis=1)]
}

# write to json file
with open(local + 'dhs.json', 'wb') as f:
    json.dump(dict_dhs, f)

# copy json file to bucket
sp.call('gsutil -m cp {} {}'.format(local + 'dhs.json', bucket + directory + 'dhs.json'), shell=True)
