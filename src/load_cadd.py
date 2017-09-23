from hail import *

hc = HailContext(parquet_compression='snappy')

kt = (
    hc
    .import_table(
        'gs://annotationdb/cadd/cadd_annotated.tsv.bgz',
        comment = '##',
        missing = '',
        types = {
            '`#Chrom`': TString(),
            'Pos': TInt(),
            'Ref': TString(),
            'Alt': TString(),
            'RawScore': TDouble(),
            'PHRED': TDouble()
        }
    )
    .annotate('variant = Variant(`#Chrom`, Pos, Ref, Alt)')
    .key_by('variant')
    .select(['variant', 'RawScore', 'PHRED'])
)

(
    VariantDataset
    .from_table(kt)
    .write('gs://annotationdb/cadd/cadd.vds', overwrite = True)
)

