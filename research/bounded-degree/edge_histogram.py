"""Construct a prescribed embedding core for tree and unicyclic edge histograms."""
from collections import Counter
from functools import reduce
from math import gcd

from check import adjacency
from check_excess import choose_variables, expression
from multiport import residue_sums
from partial_gap import build
from sparse_offsets import cap_tree, closed, edge, move_pairs


def construct(edges, opening, anchor, label, omitted, extra, rng, cap=3, offsets=None):
    ring = opening is not None
    k = len(edges) if ring else len(edges)+1
    graph = adjacency(k, edges)
    offsets = {edge(*pair): b % k for pair,b in (offsets or {}).items() if b % k}
    if ring and offsets:
        raise ValueError("ring spectra here use ordinary edge weights")
    if not ring and not omitted:
        raise ValueError("a tree must omit at least one edge weight")
    gap = None if ring else omitted[-1]
    paired = omitted if ring else omitted[:-1]
    if len(paired) != len(extra) or len(set(omitted)) != len(omitted):
        raise ValueError("wrong number of omissions or extras")
    if set(omitted) & set(extra) or any(not 0 <= x < k for x in [*omitted, *extra, label]):
        raise ValueError("invalid residues for the target histogram")
    protected = {anchor}
    if ring:
        opening = edge(*opening)
        if anchor not in opening:
            raise ValueError("anchor must be an endpoint of the opening")
        protected.update(opening)
    ends = [v for v, ns in enumerate(graph) if len(ns) == 1]
    movable = [v for v in ends if v != anchor]
    delta = (sum(extra) - sum(omitted) - sum(offsets.values())) % k
    correction = (k*(k-1)//2 - delta) % k
    coefficients = [len(ns)-1 for ns in graph]
    divisor = reduce(gcd, (c for v,c in enumerate(coefficients) if v != anchor), k)
    if (delta - coefficients[anchor]*label) % divisor:
        return None
    if (not ends and correction) or (len(ends) == 1 and not correction):
        return None
    if ring and len(ends) == 1 and len(graph[anchor]) != 2:
        raise ValueError("choose a cycle anchor away from the junction")
    if not ring and len(movable) == 1 and (correction-2*label) % k == 0:
        return None

    tree = [pair for pair in edges if edge(*pair) != opening]
    tree_graph = adjacency(k, tree)
    cuts, remaining = cap_tree(tree_graph, offsets, cap)
    fixed = protected | {v for pair in cuts for v in pair}
    reserved = [v for v in movable if v not in fixed][:2]
    site_degree = None
    modulus = 1
    reps = {}
    if len(reserved) == 2:
        # At least one bounded nonleaf degree is abundant in the asymptotic range.
        site_degree = Counter(len(ns) for ns in graph if 2 <= len(ns) <= cap).most_common(1)[0][0]
        modulus = gcd(k,site_degree-1)
        reps = {c % modulus: v for v,c in enumerate(coefficients) if v != anchor and c % modulus}
        fixed.update(reps.values())
        selected = []
    else:
        fixed.update(v for v, ns in enumerate(graph) if len(ns) != 2)
        selected = movable[:2]
        reserved = []
    blocked = closed(graph, fixed | set(reserved))
    donors = []
    for pair in tree:
        if len(donors) == len(paired):
            break
        a, b = edge(*pair)
        if a in blocked or b in blocked:
            continue
        donors.append((a, b))
        cuts.add((a, b))
        fixed.update((a, b))
        blocked.update(closed(graph, (a, b)))
        remaining[a].remove(b)
        remaining[b].remove(a)
    if len(donors) != len(paired):
        raise ValueError("insufficient remote edges")
    biases = offsets.copy()
    biases.update({pair: (q-p) % k for pair, q, p in zip(donors, paired, extra)})
    kept, sites, private, order = move_pairs(tree, tree_graph, remaining, cuts, fixed, reserved, site_degree)

    # Give the first donor end residue zero and the second its required pair sum.
    target = delta - coefficients[anchor]*label - sum(coefficients[b]*p for (_,b),p in zip(donors,extra))
    residues = dict(zip(reps.values(), residue_sums(modulus,reps,target)))
    special = set(selected)
    dependent = {b for a, b in donors}
    ordinary = fixed - private - special - dependent - {anchor}
    variables = [v for v in order if v in ordinary] + sorted(private)
    if len(special) == 2:
        variables.append(selected[0])
    forms = {v: expression((i, modulus), constant=residues.get(v,0)) for i, v in enumerate(variables)}
    forms[anchor] = expression(constant=label)
    for (a, b), value in zip(donors, extra):
        forms[b] = expression(*[(i, -c) for i, c in forms[a].items()], constant=value)
    if special:
        y = selected[-1]
        terms = [(i, (len(graph[v])-2)*c) for v, form in forms.items()
                 if len(graph[v]) != 2 for i, c in form.items()]
        forms[y] = expression(*terms, constant=correction)

    def weight(pair):
        a, b = pair
        return expression(*forms[a].items(), *forms[b].items(), constant=biases.get(edge(a,b), 0))

    for site, (pair, root) in sites.items():
        forms[site] = expression(*weight(pair).items(), *[(i,-c) for i,c in forms[root].items()])
    weights = [weight(pair) for pair in edges if set(pair) <= fixed]
    if not ring:
        weights.append(expression(constant=gap))
    evaluate = choose_variables(list(forms.values()), weights, k, rng)
    pins = {v: evaluate(f) for v, f in forms.items()}
    if ring:
        gap = evaluate(weight(opening))
    labels = build(kept, pins, gap, rng)
    assert labels is not None
    return (kept, opening, gap, pins, labels), donors, biases


def uniform_transfers(k, leaf_counts):
    """Return one (extra, omitted) pair per piece, with equal entries for no move."""
    s = k*(k-1)//2 % k
    delta = [s if leaves == 0 else (s+1) % k for leaves in leaf_counts]
    flexible = next((i for i, leaves in enumerate(leaf_counts) if leaves >= 2), None)
    one = [i for i, leaves in enumerate(leaf_counts) if leaves == 1]
    if flexible is not None:
        delta[flexible] = (delta[flexible] - sum(delta)) % k
    elif len(one) >= 2:
        a, b = one[-2:]
        remaining = (delta[a] + delta[b] - sum(delta)) % k
        delta[a] = next(v for v in range(k) if v != s and (remaining-v) % k != s)
        delta[b] = (remaining-delta[a]) % k
    elif one:
        i = one[0]
        delta[i] = (delta[i]-sum(delta)) % k
        if delta[i] == s:
            return None
    elif sum(delta) % k:
        return None
    moves = []
    previous = 0
    for difference in delta:
        current = (previous+difference) % k
        moves.append((current, previous))
        previous = current
    assert previous == 0
    return moves
