"""Count even and odd rainbow completions, with zero omitted as a vertex label."""

import argparse


def signed_count(k, parents):
    if k < 2 or len(parents) != k - 1 or any(not -k <= p < i for i, p in enumerate(parents)):
        raise ValueError("expected k-1 parents, each external or an earlier vertex")
    labels = []
    image = [None] * k
    counts = [0, 0]

    def visit(unused_labels, unused_weights):
        i = len(labels)
        if i == k - 1:
            missing, = unused_weights
            image[0] = missing
            inversions = sum(image[a] > image[b] for b in range(k) for a in range(b))
            counts[inversions % 2] += 1
            return
        p = parents[i]
        offset = -1 - p if p < 0 else labels[p]
        for x in unused_labels:
            w = (x + offset) % k
            if w in unused_weights:
                labels.append(x)
                image[x] = w
                visit(unused_labels - {x}, unused_weights - {w})
                labels.pop()

    visit(set(range(1, k)), set(range(k)))
    return tuple(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modulus", type=int)
    parser.add_argument("parents", type=int, nargs="+")
    args = parser.parse_args()
    even, odd = signed_count(args.modulus, args.parents)
    print(f"Even: {even}. Odd: {odd}. Signed count: {even - odd}.")
