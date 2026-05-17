#!/usr/bin/env python3
import argparse


def read_fasta(path):
    name = None
    chunks = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    break
                name = line[1:].split()[0]
            else:
                chunks.append(line.upper())
    if name is None:
        raise SystemExit("Reference FASTA is empty")
    return name, "".join(chunks)


def read_depth(path):
    depth = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            chrom, pos, value = line.rstrip().split("\t")[:3]
            depth[int(pos)] = int(value)
    return depth


def wrap(seq, width=70):
    return "\n".join(seq[i : i + width] for i in range(0, len(seq), width))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", required=True)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--depth", required=True)
    parser.add_argument("--min-depth", type=int, default=1)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    _ref_name, reference = read_fasta(args.reference)
    depths = read_depth(args.depth)
    consensus = "".join(base if depths.get(i + 1, 0) >= args.min_depth else "N" for i, base in enumerate(reference))

    with open(args.out, "w", encoding="utf-8") as out:
        out.write(f">{args.sample}|masked_consensus|min_depth={args.min_depth}\n")
        out.write(wrap(consensus) + "\n")


if __name__ == "__main__":
    main()
