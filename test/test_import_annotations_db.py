#!/usr/bin/env python

import time
import hail

hc = hail.HailContext()

vds = hc.read('gs://annotationdb/test/onekg.hardcalls.vds')

vds = vds.import_annotations_db(
    'va.dbNSFP.aaref',
    'va.dbNSFP.rs_dbsnp147',
    'va.dbNSFP.hg38_chr',
    'va.dbNSFP.uniprot_acc'
)
print vds.variant_schema
