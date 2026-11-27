"""Lift a cordial quotient labeling at an odd modulus to paired vertices or stars."""


def matching_labels(parents, quotient_labels, joins, modulus):
    """Pair i has vertices 2*i and 2*i+1. joins[i-1] gives parent and child ports."""
    flips = [0]
    for child, (left, right) in enumerate(joins, start=1):
        flips.append(flips[parents[child]] ^ left ^ right)
    return [(2 * label + modulus * (port ^ flip)) % (2 * modulus)
            for label, flip in zip(quotient_labels, flips) for port in (0, 1)]


def star_labels(parents, quotient_labels, joins, modulus, size):
    """Port 0 is the center. Each join must link two centers or two leaves."""
    period = modulus * size
    reps = [0] * size
    for digit in range(1, (size + 1) // 2):
        reps[digit], reps[-digit] = digit, -digit
    if size % 2 == 0:
        reps[size // 2] = period // 2
    digits = [list(range(size)) for _ in parents]
    for child, (left, right) in enumerate(joins, start=1):
        if (left == 0) != (right == 0):
            raise ValueError("a star join must have matching port types")
        wanted = -digits[parents[child]][left] % size
        digits[child][right], digits[child][wanted] = wanted, right
    return [(size * label + reps[digit]) % period
            for label, local in zip(quotient_labels, digits) for digit in local]
