"""Generate, hash and independently audit every SPN2 shard using bounded disk space."""

import argparse
import errno
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess
import tempfile
import threading
import time


def run(k, shards, workers, generator, verifier, output, rank_bits=False):
    if workers < 1 or shards < 1 or not 5 <= k <= 26:
        raise ValueError("expected positive concurrency and shard count, and 5 <= k <= 26")
    output.mkdir()  # Preserve results of an earlier run.
    with tempfile.TemporaryDirectory(dir=output) as scratch:
        tmp = Path(scratch)
        pipes = [tmp / f"{i}.fifo" for i in range(shards)]
        for path in pipes:
            os.mkfifo(path)
        mode = "--rank-bits" if rank_bits else "--parallel"
        audit = subprocess.Popen([verifier, str(k), mode, str(workers), *pipes],
                                 stdout=subprocess.PIPE, text=True)
        stopped = threading.Event()

        def process(i):
            if stopped.is_set():
                return
            shard = tmp / f"{i}.spn"
            with (output / f"{i}.log").open("w") as log:
                subprocess.run([generator, str(k), str(i), str(shards), shard, "--ranked-cover"],
                               check=True, stdout=log, stderr=log)
            # The verifier opens its inputs on demand. Detect early reader exit,
            # including failures in a different worker, while waiting to connect.
            while not stopped.is_set():
                if audit.poll() is not None:
                    raise RuntimeError("verifier exited before opening all inputs")
                try:
                    fd = os.open(pipes[i], os.O_WRONLY | os.O_NONBLOCK)
                    break
                except OSError as error:
                    if error.errno != errno.ENXIO:
                        raise
                    time.sleep(0.1)
            else:
                return
            digest = hashlib.sha256()
            with os.fdopen(fd, "wb") as sink, shard.open("rb") as source:
                os.set_blocking(sink.fileno(), True)
                for block in iter(lambda: source.read(1 << 20), b""):
                    sink.write(block)
                    digest.update(block)
            shard.unlink()
            return digest.hexdigest()

        digests = [None] * shards
        with ThreadPoolExecutor(max_workers=workers) as pool:
            try:
                jobs = {pool.submit(process, i): i for i in range(shards)}
                for done, job in enumerate(as_completed(jobs), 1):
                    digests[jobs[job]] = job.result()
                    if done % 16 == 0 or done == shards:
                        print(f"{done}/{shards} streams delivered", flush=True)
                report, _ = audit.communicate()
                if audit.returncode:
                    raise RuntimeError(f"verifier exited with status {audit.returncode}")
            finally:
                stopped.set()
                if audit.poll() is None:
                    audit.kill()
                    audit.wait()
        manifest = "".join(f"{digest}  spine{k}/{i}.spn\n" for i, digest in enumerate(digests))
        (output / f"spine{k}.sha256").write_text(manifest)
        (output / "verified.txt").write_text(report)
        print(report, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int)
    parser.add_argument("shards", type=int)
    parser.add_argument("workers", type=int)
    parser.add_argument("generator", type=Path)
    parser.add_argument("verifier", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--rank-bits",action="store_true",help="use one global bit per rooted base")
    args = parser.parse_args()
    run(args.modulus, args.shards, args.workers, args.generator.resolve(),
        args.verifier.resolve(), args.output.resolve(), args.rank_bits)
