#!/usr/bin/env python

import hail
import pandas as pd

hc = hail.HailContext(parquet_compression = True)

kt = (
	hc
	.import_keytable(
		'gs://annotationdb/gencode19/gencode19.tsv.bgz',
		config = hail.TextTableConfig(
			types = """
				
			"""
		)
	)
)

print kt.schema
