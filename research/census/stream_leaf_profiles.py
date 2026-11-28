"""Generate, hash and independently verify one stream per component profile."""
import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess


def audit(k, parts, generator, verifier, restarts, two_roots=False):
    name = " ".join(parts)
    mode = "--typed-restarts" if restarts else "--typed"
    if two_roots:
        mode = "--two-roots"
    make = [generator,str(k),"0","1","-",mode,*parts]
    check = [verifier,str(k),"--two-roots" if two_roots else "--typed","/dev/stdin",*parts]
    digest = hashlib.sha256()
    # Generator progress at every 100,000 records can go straight to the job log.
    with subprocess.Popen(make,stdout=subprocess.PIPE) as source:
        with subprocess.Popen(check,stdin=subprocess.PIPE,stdout=subprocess.PIPE) as sink:
            try:
                for block in iter(lambda: source.stdout.read(1048576), b""):
                    sink.stdin.write(block)
                    digest.update(block)
                sink.stdin.close()
                report = sink.stdout.read().decode().strip()
                if sink.wait() or source.wait():
                    raise RuntimeError(f"failed profile {name}")
            finally:
                source.stdout.close()
                if source.poll() is None:
                    source.terminate()
                if sink.poll() is None:
                    sink.terminate()
    match = re.fullmatch(r"forests=(\d+) rows=(\d+) assignments=(\d+)",report)
    if not match:
        raise ValueError(f"invalid verifier report for {name}: {report}")
    return digest.hexdigest()+"  "+report+"  "+name+"\n"


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("modulus",type=int)
    cli.add_argument("profiles",type=Path)
    cli.add_argument("generator",type=Path)
    cli.add_argument("verifier",type=Path)
    cli.add_argument("output",type=Path)
    cli.add_argument("--workers",type=int,default=1)
    cli.add_argument("--restarts",action="store_true",help="use bounded restarts in the short-forest search")
    cli.add_argument("--two-roots",action="store_true",help="allow arbitrary independent colors at two roots")
    args = cli.parse_args()
    lines = args.profiles.read_text().splitlines()
    if not lines or len(lines) != len(set(lines)) or args.workers < 1:
        raise ValueError("expected distinct profiles and positive worker count")
    args.output.mkdir()
    def worker(i):
        row = audit(args.modulus,lines[i].split(),args.generator.resolve(),args.verifier.resolve(),args.restarts,args.two_roots)
        (args.output/f"{i}.checked").write_text(row)
        return row
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(worker,range(len(lines))))
    (args.output/"manifest.txt").write_text("".join(rows))
    print(f"Accepted all {len(rows)} profiles",flush=True)


if __name__ == "__main__":
    main()
