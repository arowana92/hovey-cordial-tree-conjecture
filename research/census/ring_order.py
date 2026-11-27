"""Upper bounds from six-tip pruning, terminal arm lengths, and edge substitution."""

from functools import lru_cache


def largest(k, s, threshold, paths=5):
    mass = s-2
    run = k-7
    max_tips = mass-7
    budget = mass-paths*threshold
    limit = k*(k-3)  # the divisible-cut theorem
    # Keep one bit per exact order and cost. Two legitimate intermediate orders
    # fit below a stride even when added without first checking the global limit.
    stride = 2*(limit+1)
    repeat = sum(1 << (cost*stride) for cost in range(budget+1))
    full = (1 << ((budget+1)*stride))-1
    safe = []
    for corridor in range(run+1):
        allowed = sum(1 << n for n in range(1, limit+1)
                      if all((n+i) % k not in (0, s%k) for i in range(corridor+1)))
        safe.append(repeat*allowed)

    @lru_cache(4096)
    def combine(first, second):
        result = 0
        while second:
            low = second & -second
            result |= first << (low.bit_length()-1)
            second -= low
        return result & full

    def branches(cap):
        rows = [[0]*(run+1) for _ in range(max_tips+1)]
        single = [0]*(max_tips+1)
        arm_cap = min(run+1, cap)
        group_limit = repeat*((1 << (mass+1))-1)

        @lru_cache(None)
        def side_forest(leaves, largest):
            if leaves == 0:
                return 1
            largest = min(largest, leaves)
            if largest == 1:
                # All directions of the side forest are terminal arms.
                result = 0
                for w in range(leaves, min(mass, leaves*arm_cap)+1):
                    cost = max(0, w-leaves*threshold)
                    if cost <= budget:
                        result |= 1 << (w+stride*cost)
                return result
            result = side_forest(leaves, largest-1)
            result |= combine(single[largest], side_forest(leaves-largest, largest))
            return result & group_limit if leaves <= 6 else result

        profile = [[None]*(run+1) for _ in range(max_tips+1)]
        for tips in range(2, max_tips+1):
            # pending[e] contains base orders admissible up to outer length e.
            pending = {}
            def bins(tag):
                if tag not in pending:
                    pending[tag]=[0]*(run+1)
                return pending[tag]
            for largest in range(1, tips):
                side_tips = tips-largest
                can_open = side_tips <= 4 and (side_tips >= 2 or k%2 == 0)
                if largest == 1:
                    # The continuation goes to an original leaf. Enumerate the
                    # longest arm and every possible total of the other arms.
                    for d in range(1, arm_cap+1):
                        for w in range(side_tips, min(mass-d, side_tips*d)+1):
                            cost = max(0, w+d-tips*threshold)
                            last = k-1-w-d if can_open and w <= k-3 else run
                            if last >= 0 and cost <= budget:
                                bins((side_tips,w,d-1) if side_tips<=3 else (4,0,0))[min(last,run)] |= 1 << (1+w+d+stride*cost)
                    continue

                choices = side_forest(side_tips, largest)
                while choices:
                    bit = choices & -choices
                    choices -= bit
                    cost, w = divmod(bit.bit_length()-1, stride)
                    for g, child in enumerate(rows[largest]):
                        last = k-2-w-g if can_open and w <= k-3 else run
                        if last < 0:
                            continue
                        last = min(last,run)
                        shift = 1+w+stride*cost
                        if side_tips >= 4:
                            bins((4,0,0))[last] |= child << shift
                            continue
                        regular, high, short = profile[largest][g][side_tips-1]
                        t = k-2-g-w
                        fmax = min(t,k-3-w)
                        common = regular | high[max(0,fmax+1)]
                        target = bins((side_tips,w,g))
                        # The contribution for e is decreasing with e. A bin at
                        # e also contributes to all shorter exterior corridors.
                        previous = None
                        for e in range(last,-1,-1):
                            choice = common | short[max(0,t-e)]
                            if choice != previous:
                                target[e] |= choice << shift
                                previous = choice

            for e in range(run+1):
                profile[tips][e] = [[0,[0]*(k+1),[0]*(2*k+1)] for _ in range(3)]
            for (q,w,g), by_end in pending.items():
                allowed = 0
                for e in reversed(range(run+1)):
                    allowed |= by_end[e]
                    states = ((allowed & safe[e]) << e) & full
                    if tips <= 6:
                        side_cap = cap if tips <= 3 else mass
                        states &= repeat*((1 << (side_cap+1))-1)
                    if not states:
                        continue
                    rows[tips][e] |= states
                    for r,filters in enumerate(profile[tips][e],1):
                        if r+q>4 or w>k-3:
                            filters[0] |= states
                        else:
                            filters[1][w] |= states
                            filters[2][w+g+1] |= states
            for e, filters in enumerate(profile[tips]):
                single[tips] |= rows[tips][e]
                for regular, high, short in filters:
                    for i in reversed(range(k)): high[i] |= high[i+1]
                    for i in range(2*k): short[i+1] |= short[i]
        side_forest.cache_clear()
        return rows

    first_large = s+1-k//2
    pairs = [(first_large-1, first_large-1)]
    pairs.extend((a, mass-a) for a in range(first_large, mass+1))
    tables = {cap: branches(cap) for cap in {v for pair in pairs for v in pair}}
    orders = 0
    for a, b in pairs:
        for left in range(7, mass-6):
            for right in range(7, mass-left+1):
                for e in range(run+1):
                    orders |= combine(tables[a][left][e] >> e, tables[b][right][e])
    return max(n for n in range(s, limit+1, k) if n <= 1+6*mass or (orders >> n) & repeat)


if __name__ == "__main__":
    for modulus in (26,27):
        for residue in range(23,modulus+1):
            print(modulus, residue, max(largest(modulus, residue, z)
                  for z in range(1,(residue-2)//5+1)), flush=True)
