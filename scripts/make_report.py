#!/usr/bin/env python3
import argparse
import html


def read_qc(path):
    with open(path, "r", encoding="utf-8") as handle:
        header = handle.readline().rstrip().split("\t")
        values = handle.readline().rstrip().split("\t")
    return dict(zip(header, values))


def depth_summary(path):
    values = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            values.append(int(line.rstrip().split("\t")[2]))
    covered = sum(1 for value in values if value > 0)
    return {
        "positions": len(values),
        "covered": covered,
        "mean_depth": sum(values) / len(values) if values else 0,
        "breadth": 100 * covered / len(values) if values else 0,
    }


def read_consensus(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.startswith(">"):
                chunks.append(line.strip())
    seq = "".join(chunks)
    return {"length": len(seq), "masked_bases": seq.count("N")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", required=True)
    parser.add_argument("--qc", required=True)
    parser.add_argument("--depth", required=True)
    parser.add_argument("--consensus", required=True)
    parser.add_argument("--out-html", required=True)
    parser.add_argument("--out-qmd", required=True)
    args = parser.parse_args()

    qc = read_qc(args.qc)
    depth = depth_summary(args.depth)
    consensus = read_consensus(args.consensus)

    report_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(args.sample)} viral genomics report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #14213d; }}
    table {{ border-collapse: collapse; width: min(760px, 100%); }}
    th, td {{ border: 1px solid #d8deea; padding: 0.65rem; text-align: left; }}
    th {{ background: #eef5ff; }}
  </style>
</head>
<body>
  <h1>{html.escape(args.sample)} viral genomics report</h1>
  <p>Demo report generated from synthetic FASTQ, mapping, depth, and consensus outputs.</p>
  <table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Reads</td><td>{html.escape(qc.get("reads", "NA"))}</td></tr>
    <tr><td>Bases</td><td>{html.escape(qc.get("bases", "NA"))}</td></tr>
    <tr><td>Mean read length</td><td>{html.escape(qc.get("mean_read_length", "NA"))}</td></tr>
    <tr><td>Mean base quality</td><td>{html.escape(qc.get("mean_base_quality", "NA"))}</td></tr>
    <tr><td>Reference positions</td><td>{depth["positions"]}</td></tr>
    <tr><td>Covered positions</td><td>{depth["covered"]}</td></tr>
    <tr><td>Breadth</td><td>{depth["breadth"]:.1f}%</td></tr>
    <tr><td>Mean depth</td><td>{depth["mean_depth"]:.2f}</td></tr>
    <tr><td>Consensus length</td><td>{consensus["length"]}</td></tr>
    <tr><td>Masked bases</td><td>{consensus["masked_bases"]}</td></tr>
  </table>
</body>
</html>
"""
    report_qmd = f"""---
title: "{args.sample} viral genomics report"
format: html
---

## Summary

Demo report generated from synthetic FASTQ, mapping, depth, and consensus outputs.

| Metric | Value |
|---|---:|
| Reads | {qc.get("reads", "NA")} |
| Bases | {qc.get("bases", "NA")} |
| Mean read length | {qc.get("mean_read_length", "NA")} |
| Mean base quality | {qc.get("mean_base_quality", "NA")} |
| Reference positions | {depth["positions"]} |
| Covered positions | {depth["covered"]} |
| Breadth | {depth["breadth"]:.1f}% |
| Mean depth | {depth["mean_depth"]:.2f} |
| Consensus length | {consensus["length"]} |
| Masked bases | {consensus["masked_bases"]} |
"""
    with open(args.out_html, "w", encoding="utf-8") as out:
        out.write(report_html)
    with open(args.out_qmd, "w", encoding="utf-8") as out:
        out.write(report_qmd)


if __name__ == "__main__":
    main()
