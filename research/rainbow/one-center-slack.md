# One center and arbitrary leaves at every modulus

**Theorem.** Fix a $k$-cordial labeling on a tree of order one modulo $k$. Add $n$ vertices by a forest in which at most one new vertex has children. The new center attaches to an old vertex, its children attach to it, and all other new vertices attach anywhere on the old tree. Every new edge may have its own prescribed additive offset. **If $n\ge k+1$, the old labeling always extends.** At a prime power $n=k$ also works. At every modulus with two distinct prime divisors there are ordinary, zero-offset attachments of size $k$ that fail. The last two assertions follow from the [one-period criterion](star-periods.md).

For an actual double star with independent offsets and freely chosen vertex labels this gives the exact last possible counterexample order. It is **$k+1$ at any modulus with two distinct prime divisors**, **$k$ at a composite prime power**, and there are **no failing orders at a prime**.

For a divisible-order core there is a related consequence. Any attachment with at most one new internal vertex works at every size: put the deficient edge weight on the center’s entering edge, then append independent leaves. With at most two new internal vertices and at least $k+2$ new vertices, first fill the deficiency at an internal root. The remaining forest fits the theorem above. If no new vertex has children, begin with any root.

## Preserving the surplus with one full period

Work with $k\ge2$ and translate the old surplus to zero. For an external row let its base shift be its old parent label plus its edge offset; for a child row let the base shift be its edge offset alone. The effective shift of a child adds the new center label $a$. The destination of each row is its source (its own vertex label) plus its effective shift. A whole period of $k$ rows with shifts summing to zero admits sources and destinations that are both permutations. One source can be assigned in advance by translating both permutations. [Hall (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

Write $c$ and $s$ for the number of children and singletons, so $c+s+1=n=k+r$. In a first period containing the center we may take any number of children
$$
\max(0,k-1-s)\le j\le\min(c,k-1).
$$
Whenever $j$ or $j+1$ is a unit modulo $k$, the [two congruences](star-periods.md#two-sufficient-congruences-for-arbitrary-boundary-colors-and-offsets) give a labeling of this period leaving a surplus core. Remaining leaves now have fixed effective shifts and can be appended in any number. Indeed, starting at a surplus core, up to $k-1$ independent rows can be padded to a zero-sum list of length $k$, with the surplus assigned to a dummy source. Their actual sources avoid that surplus and their weights differ. After $k-1$ rows, the next leaf fills the new deficient edge bin and restores a surplus core.

If the displayed interval includes an endpoint 0 or $k-1$, this suffices. Otherwise it is $[c-r,c]$. The candidates $j,j+1$ together cover $r+2$ consecutive integers. Every cyclic interval of length $\lfloor k/3\rfloor+2$ contains a unit. For $k\le5$ this follows by inspection. For $k=3m+1$ take $u=m$, for $k=3m+2$ take $u=m+1$, and for $k=3m$ take one of $m-1,m+1$ coprime to three. In the last case $\gcd(m\pm1,3m)=\gcd(m\pm1,3)$. In all cases $1,u,k-u,k-1$ are units, and successive gaps, including the wrap, are at most $m+2$. Thus this first-period construction applies whenever $r\ge\lfloor k/3\rfloor$.

## Repairing a missing source with one extra leaf

It remains to handle small positive $r$. In fact this second construction works whenever $3(r-1)<k$. Choose any $k$ rows including the center, prescribe its nonzero label $a=1$, and set all effective shifts accordingly, including those of the remaining leaves. Let $D$ be the sum of the shifts of the chosen $k$ rows and put $w=a+D$. Subtract $D$ from the center's shift. The resulting requests sum to zero, so obtain Hall permutations with the virtual center source fixed to $w$. Change its actual source to $a$ and restore $D$ to its shift. Every destination stays the same since $w-D=a$. The period's edge counts are uniform and its source histogram is $\mathbf1-e_w+e_a$.

Give one reserved leaf the missing source $w$. Together with the old surplus, the vertex counts now have distinct highs zero and $a$. This leaf contributes one extra edge weight $y$. The other $r-1$ leaves have known shifts. Pad those shifts to a zero-sum list and restrict Hall permutations to get distinct sources and distinct destinations. Translate them all together. For each of the $r-1$ rows at most three translations are forbidden: two would put its source at zero or $a$, and one would put its destination at $y$. When $3(r-1)<k$ there is a permissible translation. All final high bins are distinct in their respective histograms. If the first construction did not already apply, $1\le r<\lfloor k/3\rfloor$, so the inequality holds. Modulus one is immediate.

## Sharp orders for double stars with offsets

Take one center as a singleton old core and translate it to zero. The other center becomes the one free center of the theorem. Thus all double stars of order at least $k+2$ allow arbitrary offsets. At a prime power the same holds at order $k+1$. At a prime, the [prime star extension](prime-star.md) and its [independent-offset list version](../biased/star-lists.md) cover smaller orders by padding to a single rainbow period.

For a mixed-prime modulus take $k$ new vertices, with $c$ divisible by one prime factor and $c+1$ divisible by another. Put offset one on the edge between the centers and zero elsewhere. Once the old center is normalized to zero, these are exactly the effective shifts of the equal-parent one-period criterion with $p=1,b=0$. Neither congruence is soluble. At a composite prime power, the [order-$k$ double-star obstruction](../biased/README.md#reduction-to-one-order) uses a proper divisor $1<d<k$, $d-1$ leaves at one center and $k-1-d$ at the other, with the single nonzero offset on their joining edge. This proves the three asserted maxima.

## Reproduction

~~~sh
python3 -B -m research.rainbow.check_one_center
python3 -B -m research.rainbow.check_star_period
~~~

The first checker assembles and recounts the entire tree, including all old edges and all individual offsets. It tests every effective shift assignment with one spare row at moduli two and three, varied populations through modulus 45, and the exceptional child populations requiring the second construction at 60, 90, 105 and 210. In total it checks 348 exhaustive small inputs and 13,281 further whole trees, including 328 virtual-source repairs, and checks the unit-gap inequality through modulus 500. [Construction](star_period.py) · [Whole-tree verifier](check_one_center.py)
