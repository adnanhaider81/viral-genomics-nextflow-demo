process MAP_READS {
    tag "$sample"
    publishDir "${params.outdir}/bam", mode: 'copy'

    input:
    tuple val(sample), path(reads)
    path reference

    output:
    tuple val(sample), path("${sample}.bam"), path("${sample}.bam.bai"), emit: bam

    script:
    """
    minimap2 -a -x sr "${reference}" "${reads}" | samtools sort -o "${sample}.bam" -
    samtools index "${sample}.bam"
    """
}
