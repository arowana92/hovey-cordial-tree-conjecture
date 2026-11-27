"""Check that a compiled SPN2 verifier rejects seven distinct certificate faults."""

import argparse
from pathlib import Path
import struct
import subprocess
import tempfile


def check(verifier, shard, compact=False):
    with shard.open("rb") as f:
        header = f.read(5)
        if header[:4]!=b"SPN2":
            raise ValueError("expected an SPN2 witness file")
        k = header[-1]
        while record := f.read(12):
            _,count = struct.unpack("<QI",record)
            payload = f.read((k-1)*count)
            if len(payload)!=(k-1)*count:
                raise ValueError("truncated source shard")
            if count>1:
                break
        else:
            raise ValueError("need a shard containing a nontrivial cover")
    complete = record+payload
    cases = [
        ("incomplete catalog",complete,"incomplete rooted-tree catalog"),
        ("repeated forest",complete+complete,"repeated forest rank" if compact else "repeated forest"),
        ("vertex residue",record+bytes([k])+payload[1:],"invalid packed vertex permutation"),
        ("truncation",complete[:-1],"truncated record"),
        ("empty cover",record[:8]+bytes(4),"invalid packed count"),
        ("partial cover",record[:8]+struct.pack("<I",1)+payload[:k-1],"incomplete packed coverage"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/"altered.spn"
        for name,rows,reason in cases:
            path.write_bytes(header+rows)
            options = ["--rank-bits","1"] if compact else []
            result = subprocess.run([verifier,str(k),*options,path],capture_output=True,text=True)
            if result.returncode!=1 or result.stderr.strip()!=reason:
                raise AssertionError(f"{name}: {result.returncode}, {result.stderr!r}")
            print(f"Rejected {name} ({reason}).")

        path.write_bytes(header+complete)
        mode = "--rank-bits" if compact else "--parallel"
        result = subprocess.run([verifier,str(k),mode,"2",path,path],capture_output=True,text=True)
        reason = "repeated forest rank" if compact else "repeated forest across shards"
        if result.returncode!=1 or result.stderr.strip()!=reason:
            raise AssertionError(f"cross-file duplication: {result.returncode}, {result.stderr!r}")
        print(f"Rejected cross-file duplication ({reason}).")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verifier",type=Path)
    parser.add_argument("shard",type=Path)
    parser.add_argument("--rank-bits",action="store_true")
    args = parser.parse_args()
    check(args.verifier.resolve(),args.shard,args.rank_bits)
