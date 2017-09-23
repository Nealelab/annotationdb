from hail import *

hc = HailContext()

(hc.import_vcf('gs://annotationdb/onekg/chr*.vcf.bgz', drop_samples=True)
   .split_multi()
   .annotate_variants_expr(
	     	"""
	     	va = {
	     		qual: va.qual,
	     		filters: va.filters,
	     		CIEND: va.info.CIEND[va.aIndex - 1],
	     		CIPOS: va.info.CIPOS[va.aIndex - 1],
	     		CS: va.info.CS,
	     		END: va.info.END,
	     		IMPRECISE: va.info.IMPRECISE,
	     		MC: va.info.MC[va.aIndex - 1],
	     		MEINFO: va.info.MEINFO[va.aIndex - 1],
	     		MEND: va.info.MEND,
	     		MLEN: va.info.MLEN,
	     		MSTART: va.info.MSTART,
	     		SVTYPE: va.info.SVTYPE,
	     		SVLEN: va.info.SVLEN[va.aIndex - 1],
	     		TSD: va.info.TSD,
	     		AC: va.info.AC[va.aIndex - 1],
	     		AF: va.info.AF[va.aIndex - 1],
	     		NS: va.info.NS,
	     		AN: va.info.AN,
	     		EAS_AF: va.info.EAS_AF[va.aIndex - 1],
	     		EUR_AF: va.info.EUR_AF[va.aIndex - 1],
	     		AFR_AF: va.info.AFR_AF[va.aIndex - 1],
	     		AMR_AF: va.info.AMR_AF[va.aIndex - 1],
	     		SAS_AF: va.info.SAS_AF[va.aIndex - 1],
	     		DP: va.info.DP,
	     		AA: va.info.AA,
	     		VT: va.info.VT,
	     		EX_TARGET: va.info.EX_TARGET,
	     		MULTI_ALLELIC: va.info.MULTI_ALLELIC
	     	}
	     	"""
   )
   .write('gs://annotationdb/onekg/onekg.sites.vds', overwrite=True))
