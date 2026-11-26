"""Construct normalized seeds and try their exact leaf-count completions."""

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import ceil

from .marked_leaf_blocks import complete
from .marked_leaf_geometry import at_target, child_label, geometry_seed, grow, steiner


def without(graph, omitted):
    return {v: neighbors-omitted for v, neighbors in graph.items() if v not in omitted}


def dominant_seed(graph, sites, counts, coordinate_limit):
    hull = steiner(graph, sites)
    o = max(sites, key=counts.__getitem__)
    q = next(v for v in sorted(hull) if len(hull[v]) == 1 and v != o)
    others = sorted(sites-{q, o})
    tree, labels, anchors = geometry_seed(without(hull, {q}), [o]+others[:2])
    parent, = hull[q]
    p = labels[parent]
    rest = sum(counts[v] for v in sites-{o})
    partial = sum(counts[v]*labels[v] for v in sites-{q})
    target = max(child_label(tree, anchors, p, 0), ceil(Fraction(rest-partial, counts[q])))
    if abs(target) > coordinate_limit:
        return None
    at_target(tree, anchors, p, 0, target)
    labels[q] = target
    grow(graph, tree, labels, anchors)
    return tree, labels, anchors


def adjustable_seed(graph, sites, counts, coordinate_limit):
    hull = steiner(graph, sites)
    x, y = sorted(v for v in hull if len(hull[v]) == 1)[:2]
    marked = sorted(sites-{x, y})[:3]
    tree, labels, anchors = geometry_seed(without(hull, {x, y}), marked)
    px = labels[next(iter(hull[x]))]
    py = labels[next(iter(hull[y]))]
    f = max(2, max(map(abs, labels.values())), 2-child_label(tree, anchors, px, 1),
            child_label(tree, anchors, py, 0))
    low, high = -f, f
    mx, my = counts[x], counts[y]
    partial = sum(labels[v]*counts[v] for v in sites-{x, y})
    target = Fraction(sum(counts[v] for v in sites), 2)
    moment = partial+mx*low+my*high
    if my <= mx:
        steps = max(0, ceil((moment-target)/mx))
        low -= steps
        high += round((target-moment+steps*mx)/my)
    else:
        steps = max(0, ceil((target-moment)/my))
        high += steps
        low -= round((moment+steps*my-target)/mx)
    if max(-low, high) > coordinate_limit:
        return None
    at_target(tree, anchors, px, 1, low)
    at_target(tree, anchors, py, 0, high)
    labels[x], labels[y] = low, high
    grow(graph, tree, labels, anchors)
    return tree, labels, anchors


def candidates(graph, counts, coordinate_limit):
    sites = sorted(v for v in graph if counts.get(v, 0) > 0)
    for size in range(3, len(sites)+1):
        for subset in combinations(sites, size):
            ranked = sorted(subset, key=counts.__getitem__, reverse=True)
            if size == 3:
                a, b, c = ranked
                order = [a, b, c] if 2*counts[a] >= 3*counts[b] else [c, b, a]
                yield geometry_seed(graph, order)
            elif size == 4:
                yield geometry_seed(graph, ranked, counts)
            else:
                for method in (dominant_seed, adjustable_seed):
                    seed = method(graph, set(subset), counts, coordinate_limit)
                    if seed is not None:
                        yield seed


def finish(seed, counts):
    tree, labels, anchors = seed
    remaining = Counter({p: counts.get(v, 0) for v, p in labels.items()})
    remaining.subtract(p for p, _ in tree.added)
    return complete(remaining, anchors)


def construct(graph, counts, coordinate_limit=None):
    """Return (seed, blocks), or None when the sufficient checks do not succeed."""
    if coordinate_limit is None:
        coordinate_limit = len(graph)+sum(counts.values())
    for seed in candidates(graph, counts, coordinate_limit):
        try:
            blocks = finish(seed, counts)
        except ValueError:
            continue
        return seed, blocks
    return None
