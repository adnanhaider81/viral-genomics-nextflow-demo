process MASKED_CONSENSUS {
    tag "$sample"
    publishDir "${params.outdir}/consensus", mode: 'copy'

    input:
    tuple val(sample), path(depth)
    path reference
    path consensus_script

    output:
    tuple val(sample), path("${sample}.consensus.fasta"), emit: consensus

    script:
    """
    python3 "${consensus_script}" \
      --sample "${sample}" \
      --reference "${reference}" \
      --depth "${depth}" \
      --min-depth "${params.min_depth}" \
      --out "${sample}.consensus.fasta"
    """
}
