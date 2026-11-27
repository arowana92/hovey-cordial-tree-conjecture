"""Enumerate possible orders of a minimum tree after pruning terminal paths."""
from functools import lru_cache


def branch_tables(s, threshold, max_leaves, small_cap=None, count=4):
    k, limit, run = 26, 546, 19
    bound = s-2
    budget = bound-count*threshold
    full = (1 << (limit+1))-1

    def merge(target, source):
        for cost, bits in source.items():
            target[cost] = target.get(cost, 0) | bits

    @lru_cache(maxsize=4096)
    def sums(a, b):
        result = 0
        while b:
            low = b & -b
            result |= a << (low.bit_length()-1)
            b -= low
        return result & full

    def combine(target, first, rest):
        for a, left in first.items():
            for b, right in rest.items():
                if a+b <= budget:
                    target[a+b] = target.get(a+b, 0) | sums(left, right)

    def attach(target, children, arms, mass):
        extra = max(0, mass-arms*threshold)
        for cost, bits in children.items():
            if extra+cost <= budget:
                new_cost = extra+cost
                target[new_cost] = target.get(new_cost, 0) | ((bits << (1+mass)) & full)

    # A row includes its parent connector. Its key counts arm excess, and
    # bit n means a branch of order n survives the tests.
    rows = [[{} for _ in range(run+1)] for _ in range(bound+1)]
    any_connector = [{} for _ in rows]
    forest = [{} for _ in rows]
    safe = [sum(1 << n for n in range(1, limit+1)
                if all((n+i)%k not in (0,s%k) for i in range(length+1)))
            for length in range(run+1)]

    arm_cap = run+1 if small_cap is None else min(run+1, small_cap)
    for leaves in range(2, max_leaves+1):
        for split in range(2, leaves-1):
            rest = any_connector[leaves-split].copy()
            merge(rest, forest[leaves-split])
            combine(forest[leaves], any_connector[split], rest)

        # All cases independent of the parent connector's length.
        common = {}
        for arms in range(leaves+1):
            for mass in range(arms, min(bound, arms*arm_cap)+1):
                attach(common, forest[leaves-arms], arms, mass)
                if arms >= 2 and arms < leaves:
                    attach(common, any_connector[leaves-arms], arms, mass)
                if arms == leaves and arms > 2:
                    attach(common, {0:1}, arms, mass)

        for length in range(run+1):
            branch = common.copy()
            if leaves == 2:
                for mass in range(2, min(bound,2*arm_cap,25-length)+1):
                    attach(branch, {0:1}, 2, mass)
            for mass in range(1, min(bound,arm_cap)+1):
                for child in rows[leaves-1][:max(0,25-mass-length)]:
                    attach(branch, child, 1, mass)

            for cost,bits in branch.items():
                surviving = ((bits & safe[length]) << length) & full
                if small_cap is not None and leaves <= 6:
                    cap = small_cap if leaves <= 3 else bound
                    surviving &= (1 << (cap+1))-1
                if surviving:
                    rows[leaves][length][cost] = surviving
            merge(any_connector[leaves], rows[leaves][length])

    return rows, attach, sums


def orders(s, threshold, count=4):
    k, limit, run = 26, 546, 19
    bound = s-2
    rows, attach, _ = branch_tables(s, threshold, bound, count=count)
    final = {}
    for leaves in range(2, bound+1):
        # Root at an endpoint of the branching skeleton, with one child
        # and at least two terminal arms.
        for arms in range(2, leaves-1):
            for mass in range(arms, min(bound, arms*(run+1))+1):
                for length,child in enumerate(rows[leaves-arms]):
                    if arms != 2 or mass+length <= 25:
                        attach(final, child, arms, mass)
    result = 0
    for bits in final.values():
        result |= bits
    return {n for n in range(49, limit+1) if n%k==s%k and result & (1 << n)}


def allowed_orders(s):
    # The fourth longest terminal arm has some length in this range.
    return set().union(*(orders(s, z) for z in range(1,(s-2)//4+1)))


if __name__ == '__main__':
    for s in range(23,27):
        possibilities = sorted(allowed_orders(s))
        print(s, possibilities, flush=True)
