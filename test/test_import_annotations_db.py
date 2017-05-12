#!/usr/bin/env python

import time
import hail
from hail.expr import *

hc = hail.HailContext()

vds = (
	hc
	.read('gs://annotationdb/test/chr16.1kg.hardcalls.vds')
	.import_annotations_db(
    	'va.dann'
	)
)

print vds.variant_schema

start = time.time()
print ''
print '\n\nVariant count: {:,}'.format(vds.count_variants())
print 'Count time: {:.4f}s'.format(time.time() - start)
print ''
