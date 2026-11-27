"""Bound a minimum 26-label counterexample using cuts at two pendant components."""
from .arm_order_bounds import branch_tables


def largest_order(s, threshold):
    mass_bound = s-2
    excess_budget = mass_bound-4*threshold
    # If a large branch of order a exists, the opposite half has cap t-a-1.
    # Padding the large branch to a full 25-vertex test permits a >= t-11.
    first_large = s-12
    cap_pairs = [(first_large-1, first_large-1)]
    cap_pairs.extend((a, mass_bound-a) for a in range(first_large, mass_bound+1))
    caps = {c for pair in cap_pairs for c in pair}
    tables = {}
    for cap in sorted(caps):
        tables[cap], _, sum_orders = branch_tables(s, threshold, mass_bound-7, cap)

    attainable = 0
    for cap_left, cap_right in cap_pairs:
        for left in range(7, mass_bound-6):
            for right in range(7, mass_bound-left+1):
                for length in range(20):
                    for spent, first in tables[cap_left][left][length].items():
                        for other, second in tables[cap_right][right][length].items():
                            if spent+other <= excess_budget:
                                # Both entries include the interior of their common corridor.
                                attainable |= sum_orders(first >> length, second)
    # Without an edge with at least seven leaves on each side, six groups suffice.
    coarse = 1+6*mass_bound
    return max(n for n in range(s,547,26) if n <= coarse or (attainable >> n) & 1)


if __name__ == '__main__':
    for residue in range(23,27):
        print(residue, max(largest_order(residue,z)
                           for z in range(1,(residue-2)//4+1)), flush=True)
