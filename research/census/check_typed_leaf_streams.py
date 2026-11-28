"""Compare the component-type stream with two complete independent enumerations."""
import argparse
from collections import defaultdict
from pathlib import Path
from struct import unpack_from
import subprocess
from tempfile import TemporaryDirectory

from research.rainbow.check_spine_samples import direct, parse


def records(file):
    data = file.read_bytes()
    k = data[4]
    short = data[:4] == b"SPN3"
    mass, ptr = (data[5], 6) if short else (k-1, 5)
    assert data[:4] in (b"SPN2", b"SPN3")
    while ptr < len(data):
        word, count = unpack_from("<QI", data, ptr)
        end = ptr + 12 + count * mass
        assert end <= len(data)
        parents, roots, sizes, active = parse(k, word, mass)
        parts = tuple(sorted((s, sum(v not in parents for v in range(r, r+s))) for r, s in zip(roots, sizes)))
        yield parts, word, data[ptr+12:end], (parents, roots, sizes, active)
        ptr = end


def check(generator, verifier, temp, mass):
    k = 8
    origin = temp / "all"
    mode = ["--cover"] if mass == k-1 else ["--short", str(mass), "4"]
    def generate(path, flags):
        subprocess.run([generator, str(k), "0", "1", path, *flags], check=True, stdout=subprocess.DEVNULL)
    generate(origin, mode)
    expected = defaultdict(dict)
    stems = defaultdict(dict)
    for parts, word, data, shape in records(origin):
        if shape[-1]:
            expected[parts][word] = data
            parents, roots, _, _ = shape
            if len(roots) == 1 and parts[0][1] >= 2:
                branch = next(v for v in range(mass) if parents.count(v)>1)
                roots = [v for v,p in enumerate(parents) if p == branch]
                children = tuple(sorted((b-a, sum(v not in parents for v in range(a,b)))
                                        for a,b in zip(roots, roots[1:]+[mass])))
                stems[branch+1,children][word] = data
    cases = trees = assignments = 0
    for parts, group in expected.items():
        file = temp / "slice"
        flags = ["--typed", *(f"{s},{h}" for s, h in parts)]
        generate(file, flags)
        cmd = [verifier, str(k), flags[0], file, *flags[1:]]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        found = {}
        for actual, word, data, shape in records(file):
            assert actual == parts and word not in found
            found[word] = data
            assignments += direct(k, *shape, data)
        assert found == group
        if mass < k-1:
            generate(file, ["--typed-restarts", *flags[1:]])
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            replay = set()
            for actual, word, data, shape in records(file):
                assert actual == parts and word not in replay
                replay.add(word)
                direct(k, *shape, data)
            assert replay == group.keys()
        original = file.read_bytes()
        header = 6 if mass < k-1 else 5
        faults = [original[:header], original[:-1], original + original[header:],
                  original[:header+12] + bytes([0]) + original[header+13:]]
        for corrupt in faults:
            file.write_bytes(corrupt)
            assert subprocess.run(cmd, capture_output=True).returncode != 0
        cases += 1
        trees += len(group)
    for (stem, children), group in stems.items():
        file = temp / "rooted"
        spec = [f"stem={stem}", *(f"{s},{h}" for s,h in children)]
        generate(file, ["--typed", *spec])
        subprocess.run([verifier, str(k), "--typed", file, *spec], check=True, stdout=subprocess.DEVNULL)
        found = {word:data for _,word,data,_ in records(file)}
        assert found == group
        # The whole-tree description has a different component decomposition.
        wrong = [f"{mass},1"]
        assert subprocess.run([verifier,str(k),"--typed",file,*wrong], capture_output=True).returncode != 0
    return cases, trees, assignments, sum(map(len,stems.values()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generator", type=Path)
    parser.add_argument("verifier", type=Path)
    args = parser.parse_args()
    with TemporaryDirectory() as temp:
        for mass in (6, 7):
            counts = check(args.generator.resolve(), args.verifier.resolve(), Path(temp), mass)
            print(f"k=8 free={mass} profiles={counts[0]} forests={counts[1]} inputs={counts[2]} corruptions rejected={4*counts[0]} rooted stem records={counts[3]}")


if __name__ == "__main__":
    main()
