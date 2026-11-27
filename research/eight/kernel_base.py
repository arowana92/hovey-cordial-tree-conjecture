"""Emit compact base witnesses and small kernel-reduction proofs for order eight."""
import gzip
import json
from math import factorial
from pathlib import Path
import sys

from .lean_tables import normalize


def base_words():
    canonical = {}
    with gzip.open(Path(__file__).with_name("certificate.jsonl.gz"),"rt") as rows:
        for line in rows:
            kind,parents,witnesses = json.loads(line)
            if kind != "base":
                continue
            key,perm = normalize([0]+[8+p for p in parents[1:]])
            labels = [0]*8
            for j,x in enumerate(witnesses[0]):
                labels[perm[j]] = x
            canonical[key] = labels
    words = []
    for idx in range(factorial(7)):
        parents = [idx//factorial(i)%(i+1) for i in range(7)]
        key,perm = normalize([0]+[8+p for p in parents])
        labels = [canonical[key][i] for i in perm]
        weights = {(labels[j+1]+labels[p])%8 for j,p in enumerate(parents)}
        gap, = set(range(8))-weights
        words.append(sum(x<<(3*i) for i,x in enumerate(labels+[gap])))
    return words


def write_tables(directory):
    words = base_words()
    width = 16
    chunks = [sum(w<<(27*i) for i,w in enumerate(words[j:j+width]))
              for j in range(0,len(words),width)]

    def lookup(lo,hi):
        if hi==lo+1:
            return str(chunks[lo])
        mid = (lo+hi)//2
        return f"(if b < {mid} then {lookup(lo,mid)} else {lookup(mid,hi)})"

    directory.mkdir(parents=True,exist_ok=True)
    with (directory/"BaseRows.lean").open("w") as file:
        print("import research.eight.BaseCheck\nnamespace Cordial.Eight.Kernel",file=file)
        print("private def chunk (b : Nat) : Nat := "+lookup(0,len(chunks)),file=file)
        print("def row (j : Nat) := (chunk (j/16) >>> ((j%16)*27)) % 134217728",file=file)
        print("set_option maxHeartbeats 0",file=file)

        def certify(lo,hi):
            name = f"valid_{lo}_{hi}"
            if hi-lo<=width:
                proof = (f"member (lo:={lo}) (n:={hi-lo}) "
                         f"(by decide +kernel : batch row {lo} {hi-lo} = true)")
            else:
                mid = (lo+hi)//2
                proof = f"ranges {certify(lo,mid)} {certify(mid,hi)}"
            print(f"private theorem {name} : ∀ i, {lo} ≤ i → i < {hi} → "
                  f"ok row i = true := {proof}",file=file)
            return name

        complete = certify(0,len(words))
        print(f"theorem base : Cordial.BaseTest 8 := ofRows row "
              f"(fun i hi => {complete} i (Nat.zero_le _) hi)",file=file)
        print("end Cordial.Eight.Kernel\n#print axioms Cordial.Eight.Kernel.base",file=file)


if __name__=="__main__":
    write_tables(Path(sys.argv[1]))
