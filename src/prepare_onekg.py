#!/usr/bin/env python

import hail

hc = hail.HailContext(log = '/home/hail/hail.log', parquet_compression = 'snappy')

vds = (
	hc
	.import_vcf('gs://annotationdb/onekg/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.bgz', sites_only = True)
	.split_multi()
	.filter_variants_expr('v.ref.length() == 1 && v.alt().length() == 1', keep = True)
	.annotate_variants_expr(
		"""
		va.onekg = {
			chr: v.contig,
			pos: v.start.toInt(),
			ref: v.ref,
			alt: v.alt()
		}
		"""
	)
)

(
	vds
	.annotate_variants_expr('va = {}')
	.annotate_variants_vds(vds, code='va.onekg = vds.onekg')
	.write('gs://annotationdb/onekg/onekg.vds', overwrite = True)
)
