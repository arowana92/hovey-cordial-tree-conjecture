"""Generate and independently verify ranked SPN2 shards with restartable reports."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import fcntl
import hashlib
import os
from pathlib import Path
import re
import subprocess
import threading

from check_spine_report import check as check_final
from spine_counts import totals


def atomic_write(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def certificate(k, index, shards, generator, verifier, output):
    digest = hashlib.sha256()
    length = 0
    make = [generator, str(k), str(index), str(shards), "-", "--ranked-cover"]
    verify = [verifier, str(k), "--ranked-shard", str(index), str(shards), "/dev/stdin"]
    with (output / f"{index}.log").open("w") as log:
        with subprocess.Popen(make, stdout=subprocess.PIPE, stderr=log) as source:
            try:
                with subprocess.Popen(verify, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as sink:
                    try:
                        with sink.stdin:
                            for block in iter(lambda: source.stdout.read(1 << 20), b""):
                                sink.stdin.write(block)
                                digest.update(block)
                                length += len(block)
                        report = sink.stdout.read().decode().strip()
                        if sink.wait():
                            raise RuntimeError(f"verifier failed on shard {index}")
                    finally:
                        if sink.poll() is None:
                            sink.kill()
                if source.wait():
                    raise RuntimeError(f"generator failed on shard {index}")
            finally:
                source.stdout.close()
                if source.poll() is None:
                    source.kill()
    return f"{index}/{shards} k={k} {digest.hexdigest()} bytes={length} {report}\n"


def parse(row, k, index, shards, bases):
    match = re.fullmatch(rf"{index}/{shards} k={k} ([0-9a-f]{{64}}) bytes=(\d+) eligible=(\d+) "
                         r"base_only=(\d+) rows=(\d+) assignments=(\d+)\n", row)
    if not match:
        raise ValueError(f"invalid report for shard {index}")
    length, eligible, base_only, rows, assignments = map(int, match.groups()[1:])
    expected = (bases + shards - 1 - index) // shards
    if (eligible + base_only != expected or rows < expected or assignments < eligible
            or length != 5 + 12 * expected + (k - 1) * rows):
        raise ValueError(f"invalid counts for shard {index}")
    return match[1], eligible, base_only, rows, assignments


def run(k, shards, workers, generator, verifier, output):
    if not 5 <= k <= 27 or not 1 <= shards <= 2**31-1 or workers < 1:
        raise ValueError("invalid modulus, shard count or worker count")
    output.mkdir(parents=True, exist_ok=True)
    with (output / "run.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        signatures = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (generator, verifier)]
        configuration = f"ranked-shards-v1 {k} {shards} " + " ".join(signatures) + "\n"
        config = output / "configuration.txt"
        if config.exists():
            if config.read_text() != configuration:
                raise ValueError("this audit used different binaries, modulus or shard count")
        else:
            atomic_write(config, configuration)
        bases, expected_eligible, expected_inputs = totals(k)
        accepted = {}
        pending = []
        for i in range(shards):
            path = output / f"{i}.checked"
            if path.exists():
                accepted[i] = parse(path.read_text(), k, i, shards, bases)
            else:
                pending.append(i)
        print(f"{len(accepted)}/{shards} previously verified shards", flush=True)
        stopped = threading.Event()

        def worker(i):
            if stopped.is_set():
                return
            row = certificate(k, i, shards, generator, verifier, output)
            result = parse(row, k, i, shards, bases)
            atomic_write(output / f"{i}.checked", row)
            return result

        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs = {pool.submit(worker, i): i for i in pending}
            try:
                for job in as_completed(jobs):
                    accepted[jobs[job]] = job.result()
                    if len(accepted) % 16 == 0 or len(accepted) == shards:
                        print(f"{len(accepted)}/{shards} verified shards", flush=True)
            finally:
                stopped.set()
        eligible, base_only, rows, inputs = map(sum, list(zip(*accepted.values()))[1:])
        if (eligible, base_only, inputs) != (expected_eligible, bases-expected_eligible, expected_inputs):
            raise ValueError("shard reports disagree with independent partition counts")
        manifest = "".join(f"{accepted[i][0]}  spine{k}/{i}.spn\n" for i in range(shards))
        report = (f"k={k} rooted bases={bases} eligible forests={eligible} base-only shapes={base_only} "
                  f"witness rows={rows} eligible boundary assignments={inputs}\n")
        atomic_write(output / f"spine{k}.sha256", manifest)
        atomic_write(output / "verified.txt", report)
        check_final(k, shards, output, [])


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("modulus", type=int)
    cli.add_argument("shards", type=int)
    cli.add_argument("workers", type=int)
    cli.add_argument("generator", type=Path)
    cli.add_argument("verifier", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    run(args.modulus, args.shards, args.workers, args.generator.resolve(), args.verifier.resolve(), args.output)
