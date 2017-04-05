#!/usr/bin/env python

import os
import gc
import json
import gzip
import pandas as pd
import subprocess as sp

# locations
bucket = 'gs://hail-annotation/'
directory = 'gwas/'
local = '/home/hail/'

# copy 1kg sites file to master node
sp.call('gsutil -m cp {} {}'.format(bucket + '1kg/1kg_snps.tsv.gz', local + '1kg_snps.tsv.gz'), shell=True)

# master dataframe
df_master = pd.read_csv(
    local + '1kg_snps.tsv.gz', 
    sep='\t',
    header=0,
    names=['chr', 'pos', 'ref', 'alt'],
    dtype={
        'chr': str,
        'pos': int,
        'ref': str,
        'alt': str
    }
)

# indicator column
df_master.loc[:, 'exists'] = False

# define types of possible summary stat variables
types = {
    'chr': str,
    'pos': int,
    'ref': str,
    'alt': str,
    'or': float,
    'beta': float,
    'se': float,
    'p': float,
    'info': float,
    'ngt': int
}

"""
def get_dataframe(path):
    
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
    sp.call('gsutil -m cp {} {}'.format(path, local + trait + '.tsv.gz'), shell=True)
    
    # use type dictionary to get types for all variables
    var_types = {variable: types[variable] for variable in variables}
    
    # load into dataframe
    df = pd.read_csv(
        local + trait + '.tsv.gz',
        sep='\t',
        dtype=var_types
    )
    
    # rename columns
    new_names = {column: trait + '.' + column for column in df.columns if column not in set(['chr', 'pos', 'ref', 'alt'])}
    df.rename(columns=new_names, inplace=True)
    
    # indicator column
    df.loc[:, 'exists'] = True
    
df_join = pd.concat([get_dataframe(path) for path in paths], axis=1, join='outer')
"""

# get list of summary statistic paths to load, and associated json files for each
paths = sp.Popen('gsutil ls -r {}'.format(bucket + directory + '**.prepared.tsv.gz'), shell=True, stdout=sp.PIPE).communicate()[0].split()

# copy files to master node
for path in paths:
    
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
    sp.call('gsutil -m cp {} {}'.format(path, local + trait + '.tsv.gz'), shell=True)
    
    # use type dictionary to get types for all variables
    var_types = {variable: types[variable] for variable in variables}
    
    # load into dataframe
    df = pd.read_csv(
        local + trait + '.tsv.gz',
        sep='\t',
        dtype=var_types
    )
    
    # rename columns
    new_names = {column: trait + '.' + column for column in df.columns if column not in set(['chr', 'pos', 'ref', 'alt'])}
    df.rename(columns=new_names, inplace=True)
    
    # indicator column
    df.loc[:, 'exists'] = True
    
    # join to master dataframe
    df_master = pd.merge(df_master, df, on=['chr', 'pos', 'ref', 'alt'], how='left', suffixes=['', '_tmp'])
    
    # fill indicator missing values as false
    df_master['exists_tmp'].fillna(False, inplace=True)
    
    # reset indicator
    df_master.loc[df_master['exists_tmp'], 'exists'] = True
    df_master.drop('exists_tmp', axis=1, inplace=True)
    
    # remove df to avoid memory issues
    del df
    gc.collect()
      
# remove rows with no summary statistics
df_master = df_master.loc[df_master['exists'], :].reset_index(drop=True)

# drop indicator column
df_master.drop('exists', axis=1, inplace=True)

# write master dataframe to master node
df_master.to_csv(
    local + 'gwas.tsv.gz',
    sep='\t',
    header=True,
    index=False,
    compression='gzip'
)

# copy to bucket
sp.call('gsutil -m cp {} {}'.format(local + 'gwas.tsv.gz', bucket + directory + 'gwas.tsv.gz'), shell=True)
    