"""Cross-check ordinal verification, swapped streams and partial-run recovery."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
from tempfile import TemporaryDirectory

from stream_ranked_shards import run


def check(generator, verifier, tmp):
    k, stride = 8, 7
    audit = tmp / "audit"
    run(k, stride, 2, generator, verifier, audit)
    files = []
    for i in range(stride):
        path = tmp / f"{i}.spn"
        subprocess.run([generator, str(k), str(i), str(stride), path, "--ranked-cover"],
                       check=True, capture_output=True)
        expected = (audit / f"{i}.checked").read_text().split()[2]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        files.append(path)
    for options in ([], ["--rank-bits", "2"]):
        report = subprocess.check_output([verifier, str(k), *options, *files], text=True)
        assert report == (audit / "verified.txt").read_text()

    raw = files[0].read_bytes()
    header = raw[:5]
    start = 5
    records = []
    while start < len(raw):
        rows = struct.unpack_from("<I", raw, start+8)[0]
        end = start + 12 + (k-1)*rows
        records.append(raw[start:end])
        start = end
    assert start == len(raw) and len(records) > 2

    def probe(index, shards, data, error):
        path = tmp / "test.spn"
        path.write_bytes(data)
        p = subprocess.run([verifier, str(k), "--ranked-shard", str(index), str(shards), path],
                           capture_output=True, text=True)
        assert p.returncode == int(bool(error)) and p.stderr.strip() == error, (p, error)

    wrong = "wrong forest at shard position"
    probe(0, stride, files[1].read_bytes(), wrong)
    for modified in ([records[1], records[0], *records[2:]], [records[0], *records],
                     records[1:], [*records, records[0]]):
        probe(0, stride, header+b"".join(modified), wrong)
    probe(0, stride, header+b"".join(records[:-1]), "incomplete ranked shard")
    probe(0, stride, raw[:-1], "truncated record")
    probe(0, stride, raw[:17]+bytes([k])+raw[18:], "invalid packed vertex permutation")
    probe(115, 116, header, "")
    probe(114, 116, header, "incomplete ranked shard")

    manifest = (audit / "spine8.sha256").read_bytes()
    keep = [audit / f"{i}.checked" for i in range(stride) if i != 3]
    stamps = [p.stat().st_mtime_ns for p in keep]
    (audit / "3.checked").unlink()
    (audit / "3.log").write_text("interrupted\n")
    run(k, stride, 3, generator, verifier, audit)
    assert manifest == (audit / "spine8.sha256").read_bytes()
    assert [p.stat().st_mtime_ns for p in keep] == stamps
    print("Seven regenerated hashes and two full verifiers agree; nine faulty streams rejected.")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("generator", type=Path)
    cli.add_argument("verifier", type=Path)
    args = cli.parse_args()
    with TemporaryDirectory() as temp:
        check(args.generator.resolve(), args.verifier.resolve(), Path(temp))
