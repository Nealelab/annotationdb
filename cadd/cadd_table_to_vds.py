#!/usr/bin/env python

from hail import *
from pprint import *

hc = HailContext()

kt = hc.read_table('gs://annotationdb/cadd/cadd.kt')
vds = VariantDataset.from_table(kt)
vds.write('gs://annotationdb/cadd/cadd_annotated.vds', overwrite = True)
