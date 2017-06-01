#!/usr/bin/env python

import time
import hail
from hail.expr import *

hc = hail.HailContext()

vds = hc.read('gs://annotationdb/test/raw.vds').split_multi()

start = time.time()
vds = vds.annotate_variants_db([
	'va.dann.score',
	'va.cadd.RawScore'
])
print(vds.variant_schema)
n = vds.count_variants()
print('Count time: {:.4f}s'.format(time.time() - start))
print('Variant count: {:,}'.format(n))
