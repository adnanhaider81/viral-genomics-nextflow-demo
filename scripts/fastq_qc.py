#!/usr/bin/env python3
import argparse


def read_fastq(path):
    with open(path, "r", encoding="utf-8") as handle:
        while True:
            name = handle.readline().rstrip()
            if not name:
                break
            seq = handle.readline().rstrip()
            plus = handle.readline().rstrip()
            qual = handle.readline().rstrip()
            if not (name.startswith("@") and plus.startswith("+")):
                raise SystemExit(f"Malformed FASTQ record near {name!r}")
            yield name[1:], seq, qual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", required=True)
    parser.add_argument("--fastq", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    read_count = 0
    total_bases = 0
    total_quality = 0

    for _name, seq, qual in read_fastq(args.fastq):
        read_count += 1
        total_bases += len(seq)
        total_quality += sum(ord(char) - 33 for char in qual)

    mean_length = total_bases / read_count if read_count else 0
    mean_quality = total_quality / total_bases if total_bases else 0

    with open(args.out, "w", encoding="utf-8") as out:
        out.write("sample\treads\tbases\tmean_read_length\tmean_base_quality\n")
        out.write(f"{args.sample}\t{read_count}\t{total_bases}\t{mean_length:.2f}\t{mean_quality:.2f}\n")


if __name__ == "__main__":
    main()
