#!/mnt/lustre/labbott/anaconda2/bin/python

import json
import hail

# locations
meta = '/mnt/lustre/labbott/annotationdb/cadd/cadd.json'
raw = 'file:///mnt/lustre/shared_resources/CADD/whole_genome_SNVs_inclAnno_noheader.tsv.bgz'
log = '/mnt/lustre/labbott/annotationdb/hail.log'
vds = 'file:///mnt/lustre/labbott/annotationdb/cadd/cadd.vds'
        
# read in meta data about annotations
with open(meta, 'rb') as f:
    meta = json.load(f)
    
# code to load annotations
code = ','.join(['va.{0} = table.{0}'.format(x['id']) 
                 if '-' not in x['text'] 
                 else 'va.{0} = table.`{1}`'.format(x['id'], x['text'])
                 for x in meta['nodes']]) 

# data types of annotations
types = ','.join(['`#Chrom`: String, Pos: Int, Ref: String, Alt: String'] +
                 ['{0}: {1}'.format(x['id'], x['type']) 
                  if '-' not in x['text']
                  else '`{0}`: {1}'.format(x['text'], x['type'])
                  for x in meta['nodes']])
                           
(

# start Hail context
hail.HailContext(
    log = log,
    parquet_compression = 'snappy'
)

# load CADD text file into sites-only VDS
.import_annotations_table(
    path = raw,
    variant_expr = 'Variant(`#Chrom`, Pos, Ref, Alt)',
    code = code,
    npartitions = '10000',
    config = hail.TextTableConfig(
                 missing = 'NA',
                 types = types
    )
)

# write VDS to bucket                                          
.write(
    output = vds, 
    overwrite = True
)

)
