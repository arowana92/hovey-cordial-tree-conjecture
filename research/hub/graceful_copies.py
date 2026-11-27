"""Two joined copies of a gracefully labeled tree, with separately ranked leaf counts."""


def expand(parents, graceful, join, even_counts, odd_counts):
    """Counts are in increasing order of the original graceful label."""
    n = len(parents)
    parity = [0]
    for p in parents[1:]:
        parity.append(1-parity[p])
    labels = [-g if parity[i] == copy else 1+g
              for copy in (0, 1) for i, g in enumerate(graceful)]
    edges = [(copy*n+i, copy*n+p) for copy in (0, 1)
             for i, p in enumerate(parents) if i]
    edges.append((join, join+n))
    owners = {label: i for i, label in enumerate(labels)}
    lo, hi = 1-n, n
    for bit, counts in enumerate((even_counts, odd_counts)):
        if len(counts) != n or any(a < b for a, b in zip(counts, counts[1:])) or counts[-1] < 0:
            raise ValueError("prefix counts must decrease weakly to a nonnegative value")
        for r, wanted in enumerate(counts, start=1):
            following = counts[r] if r < n else 0
            lower = r % 2 == bit
            for _ in range(wanted - following):
                start = lo-r if lower else hi+1
                highest = r if lower else r-1
                for i in range(r):
                    edges.append((owners[highest-2*i], len(labels)))
                    labels.append(start+i)
                if lower:
                    lo -= r
                else:
                    hi += r
    return edges, labels
