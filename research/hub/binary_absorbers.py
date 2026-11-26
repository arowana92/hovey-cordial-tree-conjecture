"""Verify and use rational pendant-tree certificates for ordinary endpoint sums."""

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
from math import gcd, lcm
from pathlib import Path
from random import Random

from research.hub.branches import coefficients, schedules

RESIDUAL = ("()", "(())", "((()))", "(()())", "((()()))", "((())())", "((()())())")
ARCHIVE = Path(__file__).with_name("binary-absorbers.jsonl")


def decode(code):
    stack = []
    children = []
    parents = []
    completed = []
    for token in code:
        if token == "(":
            if not stack and parents:
                raise ValueError("multiple roots")
            parents.append(stack[-1] if stack else -1)
            children.append([])
            stack.append(len(parents)-1)
        elif token == ")" and stack:
            node = stack.pop()
            parts = children[node]
            if parts != sorted(parts):
                raise ValueError("noncanonical child order")
            subtree = "(" + "".join(parts) + ")"
            if stack:
                children[stack[-1]].append(subtree)
            else:
                completed.append(subtree)
        else:
            raise ValueError("invalid shape")
    if stack or completed != [code]:
        raise ValueError("unclosed shape")
    return parents


def outside(a, b):
    # ar+b on 0 < r < 1, checked at both ends. An equality at one endpoint is fine.
    low, high = sorted((b, a+b))
    return ((high <= 0 and low < 0) or (low >= 1 and high > 1))


def verify_templates(parents, templates):
    exceptional = None
    fixed = set()
    for row in templates:
        if isinstance(row, dict):
            ratio = Fraction(row["ratio"])
            values = list(map(Fraction, row["labels"]))
            if (len(values) != len(parents) or len(set(values)) != len(values)
                    or values.count(1) != 1
                    or any(0 <= x < 1 for x in values)):
                raise ValueError("invalid special-ratio vertices")
            sums = [x+(ratio if p < 0 else values[p]) for x, p in zip(values, parents)]
            target = Counter(x for x in values if x != 1)
            target[0] += 1
            if Counter(sums) != target:
                raise ValueError("invalid special-ratio edge sums")
            fixed.add(ratio)
            continue

        forms = [tuple(map(Fraction, entry)) for entry in row]
        if (len(forms) != len(parents) or len(set(forms)) != len(forms)
                or forms.count((0, 1)) != 1
                or any(not outside(*v) for v in forms if v != (0, 1))):
            raise ValueError("invalid generic vertices")
        weights = []
        collisions = set()
        for i, ((a, b), p) in enumerate(zip(forms, parents)):
            c, d = (1, 0) if p < 0 else forms[p]
            weights.append((a+c, b+d))
            for c, d in forms[:i]:
                if a != c:
                    ratio = (d-b)/(a-c)
                    if 0 < ratio < 1:
                        collisions.add(ratio)
        target = Counter(v for v in forms if v != (0, 1))
        target[(0, 0)] += 1
        if Counter(weights) != target:
            raise ValueError("invalid generic edge sums")
        exceptional = collisions if exceptional is None else exceptional & collisions
    if exceptional is None or exceptional-fixed:
        raise ValueError("uncovered boundary ratio")


def labeling(core, attach, pendant, templates):
    """Label an arbitrary rooted core and attach the certified pendant tree."""
    if not 0 < attach < len(core):
        raise ValueError("the attachment must be different from the zero hub")
    labels = [None]*len(core)
    labels[0] = 0
    roots = [v for v, p in enumerate(core) if p == 0]
    for x, v in enumerate(roots, 1):
        labels[v] = x
    first = terminal = len(roots)+1
    for v, p in enumerate(core):
        if p > 0:
            labels[v] = terminal
            terminal += labels[p]
    near = labels[attach]
    for row in templates:
        if isinstance(row, dict):
            if Fraction(near, terminal) != Fraction(row["ratio"]):
                continue
            added = [terminal*Fraction(v) for v in row["labels"]]
        else:
            added = [near*Fraction(a)+terminal*Fraction(b) for a, b in row]
        if len(set(added)) == len(pendant) and set(added).isdisjoint(labels):
            break
    else:
        raise ValueError("no construction at this ratio")
    scale = lcm(*(v.denominator for v in added))
    full = [int(x*scale) for x in labels+added]
    parents = list(core)+[attach if p < 0 else len(core)+p for p in pendant]
    sums = [full[i]+full[p] for i,p in enumerate(parents) if i]
    target = Counter(full)
    target.subtract([first*scale])
    if len(set(full)) != len(full) or Counter(sums) != +target:
        raise ValueError("full-tree endpoint sums failed")
    return full


def verify():
    residual = set(RESIDUAL)
    candidates = {"("+"".join(parts)+")" for size in range(3)
                  for parts in combinations_with_replacement(sorted(residual), size)}
    records = {}
    for line in ARCHIVE.read_text().splitlines():
        code, templates = json.loads(line)
        if code in records:
            raise ValueError("duplicate record")
        records[code] = templates
    if not residual <= candidates or set(records) != candidates-residual:
        raise ValueError("incomplete binary transitions")

    for code in candidates:
        parents = decode(code)
        if len(parents) > 1 and not any(
                gcd(*coefficients(parents, order)[1]) == 1
                for order in schedules(parents, Random(17))):
            raise ValueError("small top-level branch has no certified coprime order")
    checks = 0
    for code, templates in records.items():
        parents = decode(code)
        verify_templates(parents, templates)
        for core in ((-1, 0), (-1, 0, 1), (-1, 0, 1, 2, 0, 4), (-1, 0, 0, 1, 3, 3, 2)):
            for attach in range(1, len(core)):
                labeling(core, attach, parents, templates)
                checks += 1
    print(f"{len(candidates)} binary transitions, {len(records)} pendant certificates, "
          f"{sum(map(len, records.values()))} rational templates, {checks} full labelings.")


if __name__ == "__main__":
    verify()
