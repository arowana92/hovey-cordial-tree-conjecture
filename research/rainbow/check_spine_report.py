"""Reconcile a complete SPN2 stream audit with partition counts and retained files."""

import argparse
import hashlib
from pathlib import Path
import re

from spine_counts import totals


def check(k, shards, audit, retained):
    bases, eligible, assignments = totals(k)
    manifest = (audit / f"spine{k}.sha256").read_text().splitlines()
    if len(manifest) != shards or shards < 1:
        raise ValueError("unexpected manifest length")
    rows = 0
    byte_count = 0
    entries = {}
    for i, entry in enumerate(manifest):
        match = re.fullmatch(rf"([a-f0-9]{{64}})  spine{k}/{i}\.spn", entry)
        if match is None:
            raise ValueError(f"unexpected manifest entry for shard {i}")
        log = (audit / f"{i}.log").read_text().splitlines()
        expected_shapes = (bases + shards - 1 - i) // shards
        report = re.fullmatch(
            rf"shard {i}: {expected_shapes} shapes, (\d+) witnesses, full catalog {bases}", log[-1]
        )
        if report is None:
            raise ValueError(f"generator totals disagree for shard {i}")
        shard_rows = int(report[1])
        size = 5 + 12 * expected_shapes + (k - 1) * shard_rows
        entries[f"{i}.spn"] = size, match[1]
        rows += shard_rows
        byte_count += size

    expected = (f"k={k} rooted bases={bases} eligible forests={eligible} "
                f"base-only shapes={bases - eligible} witness rows={rows} "
                f"eligible boundary assignments={assignments}")
    if (audit / "verified.txt").read_text().strip() != expected:
        raise ValueError("native verifier disagrees with the generator or partition counts")
    for path in retained:
        size, expected_digest = entries[path.name]
        if path.stat().st_size != size:
            raise ValueError(f"wrong byte count for {path}")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                digest.update(block)
        if digest.hexdigest() != expected_digest:
            raise ValueError(f"digest mismatch for {path}")
    print(expected)
    print(f"{shards} shard reports, {byte_count} stream bytes, {len(retained)} retained files matched")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int, choices=range(5, 28))
    parser.add_argument("shards", type=int)
    parser.add_argument("audit", type=Path)
    parser.add_argument("retained", nargs="*", type=Path, help="retained shards named INDEX.spn")
    args = parser.parse_args()
    check(args.modulus, args.shards, args.audit, args.retained)
