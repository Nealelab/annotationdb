### Process fantom5 enhancers ##

tail -n +2 permissive_enhancers.bed | awk -v OFS='\t' '{gsub("chr","",$1); print $1, $2, $3}' | bgzip -c > permissive_enhancers.tsv.bgz

tail -n +2 robust_enhancers.bed | awk -v OFS='\t' '{gsub("chr","",$1); print $1, $2, $3}' | bgzip -c > robust_enhancers.tsv.bgz


gsutil cp permissive_enhancers.tsv.bgz gs://annotationdb/fantom5/

gsutil cp robust_enhancers.tsv.bgz gs://annotationdb/fantom5/

