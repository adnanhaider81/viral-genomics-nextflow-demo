process HTML_REPORT {
    tag "$sample"
    publishDir "${params.outdir}/report", mode: 'copy'

    input:
    tuple val(sample), path(qc), path(depth), path(consensus)
    path report_script

    output:
    tuple val(sample), path("${sample}.report.html"), path("${sample}.report.qmd"), emit: report

    script:
    """
    python3 "${report_script}" \
      --sample "${sample}" \
      --qc "${qc}" \
      --depth "${depth}" \
      --consensus "${consensus}" \
      --out-html "${sample}.report.html" \
      --out-qmd "${sample}.report.qmd"
    """
}
