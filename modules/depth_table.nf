process DEPTH_TABLE {
    tag "$sample"
    publishDir "${params.outdir}/depth", mode: 'copy'

    input:
    tuple val(sample), path(bam), path(bai)
    path reference

    output:
    tuple val(sample), path("${sample}.depth.tsv"), emit: depth

    script:
    """
    samtools depth -aa "${bam}" > "${sample}.depth.tsv"
    """
}
