# Products of repeated labeled trees at shared factors

Let $Q$ be a tree of odd order $q\ge3$ with a bijection onto $\mathbb Z_q$ whose edge sums are distinct. Let $B$ be an $m$-cordial tree of any order with a fixed labeling $f$. Replace every vertex of $Q$ by a copy of $B$. For every quotient edge, join the two corresponding copies by one edge.

**Theorem.** If all the joining edges have endpoint $f$-labels summing to the same minimum-frequency internal weight $w\pmod m$, the resulting tree is $qm$-cordial. The moduli may share arbitrary factors. In particular one may use the same root $b$ for every attachment when $2f(b)=w$. If $|B|=m$ is odd, some such root exists for every bijective cordial labeling of $B$.

## Construction

Use indices $i\in\mathbb Z_q$ from the quotient labeling. For each $a\in\mathbb Z_m$ choose a representative $R_a\in\mathbb Z_{qm}$ so that $R_a+R_{w-a}=C$ is independent of $a$, for a fixed lift $C$ of $w$. To do this, partition low residues by the involution $a\mapsto w-a$. In a two-element orbit take one lift arbitrarily and define the other by subtraction. At a fixed point, starting with any representative $a$, solve $2t=(C-2a)/m\pmod q$ and use $a+mt$. Doubling is invertible modulo the odd number $q$.

Label $v$ in piece $i$ by $R_{f(v)}+mi\pmod{qm}$. For a fixed template vertex, its $q$ copies cover each lift of its low label exactly once. Thus the count at each full residue equals the template count at its low residue. For a fixed internal template edge $uv$, its copies weigh $R_{f(u)}+R_{f(v)}+2mi$. These likewise cover all lifts of its low weight once.

The quotient edges now have weights $C+m(i+j)$. They occupy $q-1$ different lifts of the same low weight $w$. Before adding these edges, every one of those lifts had minimum frequency. The final counts are balanced, including when all internal frequencies agreed. No relation between the orders of $Q$ and $B$ is needed.

If one root $b$ is used throughout, $C=2R_{f(b)}$. Denote the missing quotient weight by $z$ and take $i_0$ to be its half modulo $q$. The unused lift $C+mz$ is twice the full label at $b$ in copy $i_0$ and still has minimum frequency. Thus the rooted construction can be iterated. In particular, arbitrary finite iterated rooted products of odd-order trees with bijective cordial labelings have bijective cordial labelings at their product order, when each root is chosen at half the missing weight. This includes repeated factors of the same prime.

## Adding leaves at every vertex of a quotient

**Corollary.** For an odd-order quotient $Q$ as above, adding the same number $t\ge0$ of leaves at every vertex produces a tree cordial at *every positive multiple of $q$*. At $t=m-1$ the labeling is bijective at order $qm$. This covers the center-joined stars that obstruct the [prescribed path lift](path-quotient.md).

Here is an explicit version allowing unequal counts. Give center $i$ label $mi$. If it has $s_i-1$ leaves, give them the labels $mi+(j\bmod m)$ for $j=1,\ldots,s_i-1$, using remainders in $[0,m-1]$. The center and its leaves lie in the interval of $m$ residues beginning at $mi$, balanced within that interval. Their leaf edge weights lie in the interval beginning at $m(2i\bmod q)$, also balanced, with the first position a minimum. Every quotient edge $ij$ contributes $m(i+j)$, the first position of its midpoint's weight interval. Exactly one center $r$, twice whose index is the missing quotient weight, receives no such contribution.

It follows that the same formula works if all the $s_i$ lie in one closed interval between successive multiples of $m$, and all the $s_i-\mathbf1_{i=r}$ lie in another such interval. These conditions hold for every $m$ when all the $s_i$ agree. They also hold for every $m$ if all sizes are $s$ or $s+1$ and the omitted center has size $s+1$. These statements concern all multiples of $q$ for a fixed resulting tree.

## Verification

The checker reconstructs the entire graph and tests every full residue count. It checks 1,829 products with mixed attachment vertices, 1,466 rooted products with the specified minimum weight, 3,658 coronas with equal or varying counts, and four successive products ending at order 945.

~~~sh
python3 -B -m research.check_repeated_product
~~~
