from hail import *

hc = HailContext()

(
	hc.import_table('gs://annotationdb/targets/whole_exome_agilent_1.1_refseq_plus_3_boosters.interval_list', no_header=True)
	  .annotate(['chr = f0.split(":")[0]', 'start = f0.split(":")[1].split("-")[0].toInt()', 'end = f0.split(":")[1].split("-")[1].toInt() + 1'])
	  .annotate('exome_agilent_refseq_plus_3_boosters = Interval(chr, start, end)')
	  .key_by('exome_agilent_refseq_plus_3_boosters')
	  .select('exome_agilent_refseq_plus_3_boosters')
	  .write('gs://annotationdb/targets/exome_agilent_refseq_plus_3_boosters.kt', overwrite=True)
)

(
	hc.import_table('gs://annotationdb/targets/whole_exome_agilent_designed_120.interval_list', no_header=True)
	  .annotate(['chr = f0.split(":")[0]', 'start = f0.split(":")[1].split("-")[0].toInt()', 'end = f0.split(":")[1].split("-")[1].toInt() + 1'])
	  .annotate('exome_agilent_designed_120 = Interval(chr, start, end)')
	  .key_by('exome_agilent_designed_120')
	  .select('exome_agilent_designed_120')
	  .write('gs://annotationdb/targets/exome_agilent_designed_120.kt', overwrite=True)
)

(
	hc.import_table('gs://annotationdb/targets/whole_exome_illumina_coding_v1.interval_list', no_header=True)
	  .annotate(['chr = f0.split(":")[0]', 'start = f0.split(":")[1].split("-")[0].toInt()', 'end = f0.split(":")[1].split("-")[1].toInt() + 1'])
	  .annotate('exome_illumina_coding_v1 = Interval(chr, start, end)')
	  .key_by('exome_illumina_coding_v1')
	  .select('exome_illumina_coding_v1')
	  .write('gs://annotationdb/targets/exome_illumina_coding_v1.kt', overwrite=True)
)
