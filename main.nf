nextflow.enable.dsl = 2

include { FASTQ_QC } from './modules/fastq_qc'
include { MAP_READS } from './modules/map_reads'
include { DEPTH_TABLE } from './modules/depth_table'
include { MASKED_CONSENSUS } from './modules/masked_consensus'
include { HTML_REPORT } from './modules/html_report'

workflow {
    reads_ch = Channel
        .fromPath(params.reads, checkIfExists: true)
        .map { reads -> tuple(reads.baseName.replaceFirst(/_R1$/, ''), reads) }

    reference_ch = Channel.value(file(params.reference, checkIfExists: true))
    fastq_qc_script_ch = Channel.value(file("${projectDir}/scripts/fastq_qc.py", checkIfExists: true))
    consensus_script_ch = Channel.value(file("${projectDir}/scripts/depth_mask_consensus.py", checkIfExists: true))
    report_script_ch = Channel.value(file("${projectDir}/scripts/make_report.py", checkIfExists: true))

    FASTQ_QC(reads_ch, fastq_qc_script_ch)
    MAP_READS(reads_ch, reference_ch)
    DEPTH_TABLE(MAP_READS.out.bam, reference_ch)
    MASKED_CONSENSUS(DEPTH_TABLE.out.depth, reference_ch, consensus_script_ch)

    FASTQ_QC.out.qc
        .join(DEPTH_TABLE.out.depth)
        .join(MASKED_CONSENSUS.out.consensus)
        .set { report_inputs_ch }

    HTML_REPORT(report_inputs_ch, report_script_ch)
}
