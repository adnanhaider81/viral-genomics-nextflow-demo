process FASTQ_QC {
    tag "$sample"
    publishDir "${params.outdir}/qc", mode: 'copy'

    input:
    tuple val(sample), path(reads)
    path qc_script

    output:
    tuple val(sample), path("${sample}.qc.tsv"), emit: qc

    script:
    """
    python3 "${qc_script}" \
      --sample "${sample}" \
      --fastq "${reads}" \
      --out "${sample}.qc.tsv"
    """
}
