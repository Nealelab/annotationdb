#!/usr/bin/env python

import hail
from types import MethodType

def import_annotations_db(self, *args):
  
    # import modules needed by this function
    import json
    import urllib2
    
    # path to Google storage bucket holding master vds and interval files
    db_bucket = 'gs://hail-annotation/'
    
    # separate sites-only VDS from analysis VDS
    annotated_vds = self.filter_samples_all()
    
    # collect annotations in a set to drop any duplicates
    arguments = set([arg for arg in args])
    
    # read meta file from bucket into dictionary
    url = 'https://storage.googleapis.com/hail-annotation/annotationdb.json'
    response = urllib2.urlopen(url)
    dct_meta = json.load(response)
    
    # build dictionary with annotation ids as keys
    dct_anno = {d['id']: d for (index, d) in enumerate(dct_meta)}
    
    # separate into snp and interval annotations
    snps = [x for x in arguments if dct_anno[x.split('.')[1]]['type'] == 'snp']
    intervals = [x for x in arguments if dct_anno[x.split('.')[1]]['type'] == 'interval']
    
    ## process snp annotations ##
    if snps:
        master_vds = self.hc.read(db_bucket + 'master.vds')
        snp_code = ','.join([x + ' = vds.' + x.strip('va.') for x in snps if x.split('.') != 'gwas'])
        ## logic to deal with merging summary stats/flipping betas ##
        annotated_vds = annotated_vds.annotate_variants_vds(master_vds, code=snp_code)
     
    ## process interval annotations ##
    if intervals:
        
        dct_intervals = {x.split('.')[1]: [] for x in intervals}
        for x in intervals:
            dct_intervals[x.split('.')[1]].append(x.split('.')[2])
        
        set_intervals = set(dct_intervals.keys())
        
        def get_keytable(annotation, dct_intervals):
            ## to do ( [chr, pos_start, pos_end] keys for each keytable --> expand intervals in each to loci? )
            pass
        
        kt_intervals = get_keytable(set_intervals[0], dct_intervals)
        
        if len(set_intervals) > 1:
            for key in set_intervals[1:]:
                kt = get_keytable(key, dct_intervals)
                kt_intervals = kt_intervals.join(kt, how='outer')
                
        # annotate vds with intervals keytable
                
    ## more to do (VEP, etc.)            
                
                
    return self.annotate_variants_vds(annotated_vds, code='va = merge(va, vds)')
   
   
  
## test the import_annotations_db() function

hc = hail.HailContext(log = '/home/hail/hail.log')
sample_vds = hc.import_vcf('gs://hail-common/sample.vcf')

sample_vds.import_annotations_db = MethodType(import_annotations_db, sample_vds, hail.VariantDataset)

arguments = ['va.gwas.cad', 'va.dann.score1', 'va.dhs.TSS_Status', 'va.dhs.Pvalue']
new_vds = sample_vds.import_annotations_db(*arguments)
print new_vds.variant_schema








