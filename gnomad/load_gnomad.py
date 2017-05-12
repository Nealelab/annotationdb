#!/usr/bin/env python

import sys
import hail

hc = hail.HailContext(parquet_compression = 'snappy')

kt_exomes = (
	hc
	.read('gs://gnomad-public/release-170228/gnomad.exomes.r2.0.1.sites.vds')
	.split_multi()
	.annotate_variants_expr(
		"""
 		va.info.AC = va.info.AC[va.aIndex - 1],
 		va.info.AF = va.info.AF[va.aIndex - 1],
        va.info.GQ_HIST_ALT = va.info.GQ_HIST_ALT[va.aIndex - 1],
        va.info.DP_HIST_ALT = va.info.DP_HIST_ALT[va.aIndex - 1],
        va.info.AB_HIST_ALT = va.info.AB_HIST_ALT[va.aIndex - 1],
        va.info.AC_AFR = va.info.AC_AFR[va.aIndex - 1],
        va.info.AC_AMR = va.info.AC_AMR[va.aIndex - 1],
        va.info.AC_ASJ = va.info.AC_ASJ[va.aIndex - 1],
        va.info.AC_EAS = va.info.AC_EAS[va.aIndex - 1],
        va.info.AC_FIN = va.info.AC_FIN[va.aIndex - 1],
        va.info.AC_NFE = va.info.AC_NFE[va.aIndex - 1],
        va.info.AC_OTH = va.info.AC_OTH[va.aIndex - 1],
        va.info.AC_SAS = va.info.AC_SAS[va.aIndex - 1],
        va.info.AC_Male = va.info.AC_Male[va.aIndex - 1],
        va.info.AC_Female = va.info.AC_Female[va.aIndex - 1],
        va.info.AF_AFR = va.info.AF_AFR[va.aIndex - 1],
        va.info.AF_AMR = va.info.AF_AMR[va.aIndex - 1],
        va.info.AF_ASJ = va.info.AF_ASJ[va.aIndex - 1],
        va.info.AF_EAS = va.info.AF_EAS[va.aIndex - 1],
        va.info.AF_FIN = va.info.AF_FIN[va.aIndex - 1],
        va.info.AF_NFE = va.info.AF_NFE[va.aIndex - 1],
        va.info.AF_OTH = va.info.AF_OTH[va.aIndex - 1],
        va.info.AF_SAS = va.info.AF_SAS[va.aIndex - 1],
        va.info.AF_Male = va.info.AF_Male[va.aIndex - 1],
        va.info.AF_Female = va.info.AF_Female[va.aIndex - 1],
        va.info.GC_AFR = va.info.GC_AFR[va.aIndex - 1],
        va.info.GC_AMR = va.info.GC_AMR[va.aIndex - 1],
        va.info.GC_ASJ = va.info.GC_ASJ[va.aIndex - 1],
        va.info.GC_EAS = va.info.GC_EAS[va.aIndex - 1],
        va.info.GC_FIN = va.info.GC_FIN[va.aIndex - 1],
        va.info.GC_NFE = va.info.GC_NFE[va.aIndex - 1],
        va.info.GC_OTH = va.info.GC_OTH[va.aIndex - 1],
        va.info.GC_SAS = va.info.GC_SAS[va.aIndex - 1],
        va.info.GC_Male = va.info.GC_Male[va.aIndex - 1],
        va.info.GC_Female = va.info.GC_Female[va.aIndex - 1],
        va.info.AC_raw = va.info.AC_raw[va.aIndex - 1],
        va.info.AF_raw = va.info.AF_raw[va.aIndex - 1],
        va.info.GC_raw = va.info.GC_raw[va.aIndex - 1],
        va.info.GC = va.info.GC[va.aIndex - 1],
        va.info.Hom_AFR = va.info.Hom_AFR[va.aIndex - 1],
        va.info.Hom_AMR = va.info.Hom_AMR[va.aIndex - 1],
        va.info.Hom_ASJ = va.info.Hom_ASJ[va.aIndex - 1],
        va.info.Hom_EAS = va.info.Hom_EAS[va.aIndex - 1],
        va.info.Hom_FIN = va.info.Hom_FIN[va.aIndex - 1],
        va.info.Hom_NFE = va.info.Hom_NFE[va.aIndex - 1],
        va.info.Hom_OTH = va.info.Hom_OTH[va.aIndex - 1],
        va.info.Hom_SAS = va.info.Hom_SAS[va.aIndex - 1],
        va.info.Hom_Male = va.info.Hom_Male[va.aIndex - 1],
        va.info.Hom_Female = va.info.Hom_Female[va.aIndex - 1],
        va.info.Hom_raw = va.info.Hom_raw[va.aIndex - 1],
        va.info.Hom = va.info.Hom[va.aIndex - 1],
        va.info.POPMAX = va.info.POPMAX[va.aIndex - 1],
        va.info.AC_POPMAX = va.info.AC_POPMAX[va.aIndex - 1],
        va.info.AN_POPMAX = va.info.AN_POPMAX[va.aIndex - 1],
        va.info.AF_POPMAX = va.info.AF_POPMAX[va.aIndex - 1],
        va.info.DP_MEDIAN = va.info.DP_MEDIAN[va.aIndex - 1],
        va.info.DREF_MEDIAN = va.info.DREF_MEDIAN[va.aIndex - 1],
        va.info.GQ_MEDIAN = va.info.GQ_MEDIAN[va.aIndex - 1],
        va.info.AB_MEDIAN = va.info.AB_MEDIAN[va.aIndex - 1],
        va.info.AS_RF = va.info.AS_RF[va.aIndex - 1],
        va.info.AS_FilterStatus = va.info.AS_FilterStatus[va.aIndex - 1],
        va.info.AF_NFE_Female = va.info.AF_NFE_Female[va.aIndex - 1],
        va.info.AF_EAS_Female = va.info.AF_EAS_Female[va.aIndex - 1],
        va.info.AF_EAS_Male = va.info.AF_EAS_Male[va.aIndex - 1],
        va.info.AC_AFR_Male = va.info.AC_AFR_Male[va.aIndex - 1],
        va.info.GC_ASJ_Male = va.info.GC_ASJ_Male[va.aIndex - 1],
        va.info.Hemi_SAS = va.info.Hemi_SAS[va.aIndex - 1],
        va.info.AF_AMR_Male = va.info.AF_AMR_Male[va.aIndex - 1],
        va.info.AC_EAS_Female = va.info.AC_EAS_Female[va.aIndex - 1],
        va.info.GC_AFR_Female = va.info.GC_AFR_Female[va.aIndex - 1],
        va.info.Hemi_NFE = va.info.Hemi_NFE[va.aIndex - 1],
        va.info.AF_AFR_Female = va.info.AF_AFR_Female[va.aIndex - 1],
        va.info.AC_FIN_Female = va.info.AC_FIN_Female[va.aIndex - 1],
        va.info.GC_AMR_Male = va.info.GC_AMR_Male[va.aIndex - 1],
        va.info.AC_AFR_Female = va.info.AC_AFR_Female[va.aIndex - 1],
        va.info.GC_FIN_Female = va.info.GC_FIN_Female[va.aIndex - 1],
        va.info.Hemi_AFR = va.info.Hemi_AFR[va.aIndex - 1],
        va.info.AC_ASJ_Female = va.info.AC_ASJ_Female[va.aIndex - 1],
        va.info.GC_NFE_Male = va.info.GC_NFE_Male[va.aIndex - 1],
        va.info.AF_OTH_Female = va.info.AF_OTH_Female[va.aIndex - 1],
        va.info.AF_AMR_Female = va.info.AF_AMR_Female[va.aIndex - 1],
        va.info.AF_FIN_Female = va.info.AF_FIN_Female[va.aIndex - 1],
        va.info.GC_NFE_Female = va.info.GC_NFE_Female[va.aIndex - 1],
        va.info.GC_OTH_Male = va.info.GC_OTH_Male[va.aIndex - 1],
        va.info.GC_FIN_Male = va.info.GC_FIN_Male[va.aIndex - 1],
        va.info.AC_AMR_Male = va.info.AC_AMR_Male[va.aIndex - 1],
        va.info.GC_AMR_Female = va.info.GC_AMR_Female[va.aIndex - 1],
        va.info.AC_NFE_Female = va.info.AC_NFE_Female[va.aIndex - 1],
        va.info.AC_EAS_Male = va.info.AC_EAS_Male[va.aIndex - 1],
        va.info.AC_OTH_Male = va.info.AC_OTH_Male[va.aIndex - 1],
        va.info.GC_SAS_Male = va.info.GC_SAS_Male[va.aIndex - 1],
        va.info.Hemi_OTH = va.info.Hemi_OTH[va.aIndex - 1],
        va.info.AC_NFE_Male = va.info.AC_NFE_Male[va.aIndex - 1],
        va.info.Hemi_AMR = va.info.Hemi_AMR[va.aIndex - 1],
        va.info.Hemi = va.info.Hemi[va.aIndex - 1],
        va.info.GC_EAS_Male = va.info.GC_EAS_Male[va.aIndex - 1],
        va.info.AC_AMR_Female = va.info.AC_AMR_Female[va.aIndex - 1],
        va.info.Hemi_FIN = va.info.Hemi_FIN[va.aIndex - 1],
        va.info.AC_FIN_Male = va.info.AC_FIN_Male[va.aIndex - 1],
        va.info.GC_EAS_Female = va.info.GC_EAS_Female[va.aIndex - 1],
        va.info.AF_ASJ_Male = va.info.AF_ASJ_Male[va.aIndex - 1],
        va.info.AF_ASJ_Female = va.info.AF_ASJ_Female[va.aIndex - 1],
        va.info.GC_ASJ_Female = va.info.GC_ASJ_Female[va.aIndex - 1],
        va.info.GC_SAS_Female = va.info.GC_SAS_Female[va.aIndex - 1],
        va.info.GC_SAS_Female = va.info.GC_SAS_Female[va.aIndex - 1],
        va.info.GC_AFR_Male = va.info.GC_AFR_Male[va.aIndex - 1],
        va.info.AF_FIN_Male = va.info.AF_FIN_Male[va.aIndex - 1],
        va.info.AF_AFR_Male = va.info.AF_AFR_Male[va.aIndex - 1],
        va.info.AF_SAS_Male = va.info.AF_SAS_Male[va.aIndex - 1],
     	va.info.AC_SAS_Female = va.info.AC_SAS_Female[va.aIndex - 1],
        va.info.Hemi_ASJ = va.info.Hemi_ASJ[va.aIndex - 1],
        va.info.AF_NFE_Male = va.info.AF_NFE_Male[va.aIndex - 1],
        va.info.AC_OTH_Female = va.info.AC_OTH_Female[va.aIndex - 1],
        va.info.AC_ASJ_Male = va.info.AC_ASJ_Male[va.aIndex - 1],
        va.info.Hemi_EAS = va.info.Hemi_EAS[va.aIndex - 1],
        va.info.Hemi_raw = va.info.Hemi_raw[va.aIndex - 1],
        va.info.AF_OTH_Male = va.info.AF_OTH_Male[va.aIndex - 1],
        va.info.GC_OTH_Female = va.info.GC_OTH_Female[va.aIndex - 1],
        va.info.AF_SAS_Female = va.info.AF_SAS_Female[va.aIndex - 1],
        va.info.AC_SAS_Male = va.info.AC_SAS_Male[va.aIndex - 1]
		"""
	)
	.variants_keytable()
	.annotate(
		"""
		exomes = {
			aIndex: va.aIndex,
			wasSplit: va.wasSplit,
			rsid: va.rsid,
			qual: va.qual,
			filters: va.filters,
			pass: va.pass,
			info: va.info
		}
		"""
	)
	.select(['v', 'exomes'])
)

kt_genomes = (
	hc
	.read('gs://gnomad-public/release-170228/gnomad.genomes.r2.0.1.sites.vds')
	.split_multi()
	.annotate_variants_expr(
		"""
 		va.info.AC = va.info.AC[va.aIndex - 1],
 		va.info.AF = va.info.AF[va.aIndex - 1],
        va.info.GQ_HIST_ALT = va.info.GQ_HIST_ALT[va.aIndex - 1],
        va.info.DP_HIST_ALT = va.info.DP_HIST_ALT[va.aIndex - 1],
        va.info.AB_HIST_ALT = va.info.AB_HIST_ALT[va.aIndex - 1],
        va.info.AC_AFR = va.info.AC_AFR[va.aIndex - 1],
        va.info.AC_AMR = va.info.AC_AMR[va.aIndex - 1],
        va.info.AC_ASJ = va.info.AC_ASJ[va.aIndex - 1],
        va.info.AC_EAS = va.info.AC_EAS[va.aIndex - 1],
        va.info.AC_FIN = va.info.AC_FIN[va.aIndex - 1],
        va.info.AC_NFE = va.info.AC_NFE[va.aIndex - 1],
        va.info.AC_OTH = va.info.AC_OTH[va.aIndex - 1],
        va.info.AC_Male = va.info.AC_Male[va.aIndex - 1],
        va.info.AC_Female = va.info.AC_Female[va.aIndex - 1],
        va.info.AF_AFR = va.info.AF_AFR[va.aIndex - 1],
        va.info.AF_AMR = va.info.AF_AMR[va.aIndex - 1],
        va.info.AF_ASJ = va.info.AF_ASJ[va.aIndex - 1],
        va.info.AF_EAS = va.info.AF_EAS[va.aIndex - 1],
        va.info.AF_FIN = va.info.AF_FIN[va.aIndex - 1],
        va.info.AF_NFE = va.info.AF_NFE[va.aIndex - 1],
        va.info.AF_OTH = va.info.AF_OTH[va.aIndex - 1],
        va.info.AF_Male = va.info.AF_Male[va.aIndex - 1],
        va.info.AF_Female = va.info.AF_Female[va.aIndex - 1],
        va.info.GC_AFR = va.info.GC_AFR[va.aIndex - 1],
        va.info.GC_AMR = va.info.GC_AMR[va.aIndex - 1],
        va.info.GC_ASJ = va.info.GC_ASJ[va.aIndex - 1],
        va.info.GC_EAS = va.info.GC_EAS[va.aIndex - 1],
        va.info.GC_FIN = va.info.GC_FIN[va.aIndex - 1],
        va.info.GC_NFE = va.info.GC_NFE[va.aIndex - 1],
        va.info.GC_OTH = va.info.GC_OTH[va.aIndex - 1],
        va.info.GC_Male = va.info.GC_Male[va.aIndex - 1],
        va.info.GC_Female = va.info.GC_Female[va.aIndex - 1],
        va.info.AC_raw = va.info.AC_raw[va.aIndex - 1],
        va.info.AF_raw = va.info.AF_raw[va.aIndex - 1],
        va.info.GC_raw = va.info.GC_raw[va.aIndex - 1],
        va.info.GC = va.info.GC[va.aIndex - 1],
        va.info.Hom_AFR = va.info.Hom_AFR[va.aIndex - 1],
        va.info.Hom_AMR = va.info.Hom_AMR[va.aIndex - 1],
        va.info.Hom_ASJ = va.info.Hom_ASJ[va.aIndex - 1],
        va.info.Hom_EAS = va.info.Hom_EAS[va.aIndex - 1],
        va.info.Hom_FIN = va.info.Hom_FIN[va.aIndex - 1],
        va.info.Hom_NFE = va.info.Hom_NFE[va.aIndex - 1],
        va.info.Hom_OTH = va.info.Hom_OTH[va.aIndex - 1],
        va.info.Hom_Male = va.info.Hom_Male[va.aIndex - 1],
        va.info.Hom_Female = va.info.Hom_Female[va.aIndex - 1],
        va.info.Hom_raw = va.info.Hom_raw[va.aIndex - 1],
        va.info.Hom = va.info.Hom[va.aIndex - 1],
        va.info.POPMAX = va.info.POPMAX[va.aIndex - 1],
        va.info.AC_POPMAX = va.info.AC_POPMAX[va.aIndex - 1],
        va.info.AN_POPMAX = va.info.AN_POPMAX[va.aIndex - 1],
        va.info.AF_POPMAX = va.info.AF_POPMAX[va.aIndex - 1],
        va.info.DP_MEDIAN = va.info.DP_MEDIAN[va.aIndex - 1],
        va.info.DREF_MEDIAN = va.info.DREF_MEDIAN[va.aIndex - 1],
        va.info.GQ_MEDIAN = va.info.GQ_MEDIAN[va.aIndex - 1],
        va.info.AB_MEDIAN = va.info.AB_MEDIAN[va.aIndex - 1],
        va.info.AS_RF = va.info.AS_RF[va.aIndex - 1],
        va.info.AS_FilterStatus = va.info.AS_FilterStatus[va.aIndex - 1],
        va.info.AF_NFE_Female = va.info.AF_NFE_Female[va.aIndex - 1],
        va.info.AF_EAS_Female = va.info.AF_EAS_Female[va.aIndex - 1],
        va.info.AF_EAS_Male = va.info.AF_EAS_Male[va.aIndex - 1],
        va.info.AC_AFR_Male = va.info.AC_AFR_Male[va.aIndex - 1],
        va.info.GC_ASJ_Male = va.info.GC_ASJ_Male[va.aIndex - 1],
        va.info.AF_AMR_Male = va.info.AF_AMR_Male[va.aIndex - 1],
        va.info.AC_EAS_Female = va.info.AC_EAS_Female[va.aIndex - 1],
        va.info.GC_AFR_Female = va.info.GC_AFR_Female[va.aIndex - 1],
        va.info.Hemi_NFE = va.info.Hemi_NFE[va.aIndex - 1],
        va.info.AF_AFR_Female = va.info.AF_AFR_Female[va.aIndex - 1],
        va.info.AC_FIN_Female = va.info.AC_FIN_Female[va.aIndex - 1],
        va.info.GC_AMR_Male = va.info.GC_AMR_Male[va.aIndex - 1],
        va.info.AC_AFR_Female = va.info.AC_AFR_Female[va.aIndex - 1],
        va.info.GC_FIN_Female = va.info.GC_FIN_Female[va.aIndex - 1],
        va.info.Hemi_AFR = va.info.Hemi_AFR[va.aIndex - 1],
        va.info.AC_ASJ_Female = va.info.AC_ASJ_Female[va.aIndex - 1],
        va.info.GC_NFE_Male = va.info.GC_NFE_Male[va.aIndex - 1],
        va.info.AF_OTH_Female = va.info.AF_OTH_Female[va.aIndex - 1],
        va.info.AF_AMR_Female = va.info.AF_AMR_Female[va.aIndex - 1],
        va.info.AF_FIN_Female = va.info.AF_FIN_Female[va.aIndex - 1],
        va.info.GC_NFE_Female = va.info.GC_NFE_Female[va.aIndex - 1],
        va.info.GC_OTH_Male = va.info.GC_OTH_Male[va.aIndex - 1],
        va.info.GC_FIN_Male = va.info.GC_FIN_Male[va.aIndex - 1],
        va.info.AC_AMR_Male = va.info.AC_AMR_Male[va.aIndex - 1],
        va.info.GC_AMR_Female = va.info.GC_AMR_Female[va.aIndex - 1],
        va.info.AC_NFE_Female = va.info.AC_NFE_Female[va.aIndex - 1],
        va.info.AC_EAS_Male = va.info.AC_EAS_Male[va.aIndex - 1],
        va.info.AC_OTH_Male = va.info.AC_OTH_Male[va.aIndex - 1],
        va.info.Hemi_OTH = va.info.Hemi_OTH[va.aIndex - 1],
        va.info.AC_NFE_Male = va.info.AC_NFE_Male[va.aIndex - 1],
        va.info.Hemi_AMR = va.info.Hemi_AMR[va.aIndex - 1],
        va.info.Hemi = va.info.Hemi[va.aIndex - 1],
        va.info.GC_EAS_Male = va.info.GC_EAS_Male[va.aIndex - 1],
        va.info.AC_AMR_Female = va.info.AC_AMR_Female[va.aIndex - 1],
        va.info.Hemi_FIN = va.info.Hemi_FIN[va.aIndex - 1],
        va.info.AC_FIN_Male = va.info.AC_FIN_Male[va.aIndex - 1],
        va.info.GC_EAS_Female = va.info.GC_EAS_Female[va.aIndex - 1],
        va.info.AF_ASJ_Male = va.info.AF_ASJ_Male[va.aIndex - 1],
        va.info.AF_ASJ_Female = va.info.AF_ASJ_Female[va.aIndex - 1],
        va.info.GC_ASJ_Female = va.info.GC_ASJ_Female[va.aIndex - 1],
        va.info.GC_AFR_Male = va.info.GC_AFR_Male[va.aIndex - 1],
        va.info.AF_FIN_Male = va.info.AF_FIN_Male[va.aIndex - 1],
        va.info.AF_AFR_Male = va.info.AF_AFR_Male[va.aIndex - 1],
        va.info.Hemi_ASJ = va.info.Hemi_ASJ[va.aIndex - 1],
        va.info.AF_NFE_Male = va.info.AF_NFE_Male[va.aIndex - 1],
        va.info.AC_OTH_Female = va.info.AC_OTH_Female[va.aIndex - 1],
        va.info.AC_ASJ_Male = va.info.AC_ASJ_Male[va.aIndex - 1],
        va.info.Hemi_EAS = va.info.Hemi_EAS[va.aIndex - 1],
        va.info.Hemi_raw = va.info.Hemi_raw[va.aIndex - 1],
        va.info.AF_OTH_Male = va.info.AF_OTH_Male[va.aIndex - 1],
        va.info.GC_OTH_Female = va.info.GC_OTH_Female[va.aIndex - 1]
		"""
	)
	.variants_keytable()
	.annotate(
		"""
		genomes = {
			aIndex: va.aIndex,
			wasSplit: va.wasSplit,
			rsid: va.rsid,
			qual: va.qual,
			filters: va.filters,
			pass: va.pass,
			info: va.info
		}
		"""
	)
	.select(['v', 'genomes'])
)

kt_join = (
	kt_genomes
	.select(['v'])
	.join(kt_exomes.select(['v']), how='outer')
	.cache()
)

vds_join = (
	hail
	.VariantDataset
	.from_keytable(kt_join)
	.repartition(7000)
	.cache()
)

print vds_join.count_variants()

#vds_join.write('gs://annotationdb/gnomad/gnomad.vds', overwrite=True)
