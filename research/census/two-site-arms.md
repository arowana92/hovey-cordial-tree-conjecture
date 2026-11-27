# A leaf and two-edge paths at different sites, at every odd modulus

**Theorem.** Let $k$ be any positive odd integer. Fix any vertex labeling of any tree and choose two of its vertices $u,v$, which may coincide. Attach a leaf at $u$ and $(k-1)/2$ disjoint two-edge paths at $v$. The $k$ new vertices can use each residue modulo $k$ once, and so can the $k$ new edges. All old labels stay fixed. The leaf edge may have an arbitrary prescribed additive offset.

More generally one can attach a leaf and $b$ paths whenever $k\mid 2b+1$. After the first block, each additional group of $k$ paths can use $j$ on both vertices of path $j$ in coordinates with common parent zero. The two edge weights are $j$ and $2j$, so each bin gains two entries in both histograms.

In particular, **a smallest counterexample at any odd modulus $k\ge3$ has at most $(k-3)/2$ pendant two-edge paths at each vertex.** If there were $(k-1)/2$ such paths, remove them and any original leaf outside their joint and those paths. The theorem restores them on the smaller tree. If there is no such leaf, the tree consists of those paths and their joint. Its ordinary cordiality follows from the [partially subdivided star theorem](../hub/subdivided-stars.md). Paths themselves are also cordial.

## When the parent difference is a unit

Translate the common parent label to zero. Let $x$ be the effective parent label of the singleton, including its edge offset. Put $b=(k-1)/2$. Choose a set $I$ of $b$ intermediate labels and let $J$ be its complement. It suffices to permute $J$ with displacement multiset $I\uplus\{x\}$. For a slot $z$ with assigned displacement $d\in I$, use the arm $(d,z)$. Its weights are $d$ and $z+d$. At the slot for the extra displacement $x$, use the singleton label $z$. Thus the free labels and the added weights each use all of $I$ and $J$.

On the positions $0,\ldots,2h$, doubling modulo $2h+1$ is a permutation with integer displacements $[-h,h]$. The displacement of $j$ is $j$ up to $h$ and $j-(2h+1)$ thereafter.

- If $b=2h$, choose $I=[1-h,h]$ and $J=[h+1,3h+1]$ modulo $4h+1$. Double the indices of $J$ modulo $2h+1$. The extra displacement is $-h$, a unit.
- If $b=2h-1$, choose $I=[2-h,h]$ and $J=[h+1,3h]$ modulo $4h-1$. On indices $0\le j<b$, send $j$ to $1+(2j\bmod b)$. Send $b$ to zero. The first $b$ displacements cover $I$ and the last is $-b$, a unit.

Multiplication by a unit now gives any unit $x$. For $x=0$ and odd $b=2h-1$, take intermediate labels $[1-h,h-1]$ and double the indices on the next $b$ slots modulo $b$. The remaining slot supplies the singleton. For $x=0$ and even $b$, use the nonzero construction for modulus $1\bmod4$ below and label the singleton zero. Modulus one is immediate.

## Filling the nonzero residue classes

The auxiliary problem at odd $g$ is to cover each nonzero bin once, in both histograms, by $(g-1)/2$ two-edge paths with common parent zero.

For $g=4s+1$, put the tips at $s+j$ for $1\le j\le 2s$. On their indices use $j\mapsto 2j\bmod(2s+1)$. The displacements give the intermediate labels $\pm1,\ldots,\pm s$ and the images give the tip weights. This includes the empty block at $g=1$.

For $g\equiv3\pmod4$ and $7\le g\le51$, the [twelve explicit rows](two-site-arm-seeds.json) give the intermediate and tip labels. For every larger $g=11+4s$ we have $s\ge11$. Begin with this integer block.

| Intermediate | $-5$ | $1$ | $2$ | $5$ | $-3$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tip | $4$ | $3$ | $-4$ | $-2$ | $-1$ |

Both histograms fill $[-5,5]$ with zero omitted. To enlarge such an integer block on $[-r,r]$, use new intermediate labels $\pm[r+1,r+s]$. Put the $2s$ tips on $[r+s+1,r+3s]$. For $s\ge2r+1$ the signed Langford theorem gives a permutation of this tip interval with displacements exactly the new intermediate labels. Place each tip at the intermediate vertex carrying its displacement. The increments fill $[-r-s,r+3s]$ with the same omission. With $r=5$, reduction modulo its length $11+4s$ proves the claim. [Jordon and Mitchell, Theorems 3.1 and 3.2](https://doi.org/10.1016/j.disc.2021.112719)

Let $g=\gcd(x,k)$ with $x\ne0$, and first suppose $g\ne3$. In the subgroup of multiples of $g$, use the unit-difference block at $m=k/g$ with difference $x/g$, multiplying all its labels by $g$. For each arm $(a,z)$ from the nonzero construction at $g$, take $m$ arms
$$
(a+gj,\ z+gj),\qquad 0\le j<m .
$$
Their tip weights are $a+z+2gj$. Since $m$ is odd, the two vertex classes and the two weight classes each fill their respective fibers exactly. The nonzero classes modulo $g$ supply the complement of the subgroup. This also works when $g$ and $m$ share factors.

## Parent difference of gcd three

At $g=3$ the auxiliary problem has one path. Its tip weight could reproduce its tip label only if its intermediate label were zero. Instead treat the original modulus directly, scaling to effective parent difference three. Such scaling is possible because the units act transitively on residues with the same gcd. Explicitly, of the three lifts of $x/3$ modulo $k/3$, at least one is coprime to $k$.

| Radius $r$ | Singleton | Arms $(\text{intermediate},\text{tip})$ |
| ---: | ---: | --- |
| 3 | 0 | $(-2,1),\ (-3,3),\ (2,-1)$ |
| 4 | $-2$ | $(-3,1),\ (0,2),\ (-4,3),\ (4,-1)$ |

With singleton parent three, both free labels and weights fill $[-r,r]$. The same enlargement now gives a full block at $k=7+4s$ for $s\ge7$ and at $k=9+4s$ for $s\ge9$. The radius-four seed covers nine itself. Among odd multiples of three admitting a residue of gcd three, the remaining moduli are 15, 21, 27 and 33. Their explicit records in the seed file include every actual label. This finishes all odd moduli.

## Doubling by matched pairs

At modulus $2k$, replace every free vertex of the block by a matched pair. Choose the ports on each pair independently for each incidence. This attaches one pair at the first site and $(k-1)/2$ chains of two pairs at the second. The result adds one to **every** vertex and edge count at modulus $2k$. In particular, one pair and six double-pair chains work at every pair of old labels at modulus 26.

Apply the theorem modulo $k$ to the old labels at the two sites. Give both members of each new pair its prescribed low residue modulo $k$ and opposite parities. Orient the incoming endpoint to have the parity of its actual parent. Each entering weight is even with the low residue of its quotient edge. The matching weights are odd with low residues twice the quotient vertex labels. Both lists cover all $k$ low residues, proving the assertion. Translation of the normalized quotient restores the original low residues. [General matching lift](../matching-expansion.md)

## Verification

The [constructor](two_site_arms.py) implements the unit permutations, the subgroup construction and the arithmetic progressions of the signed Langford theorem. It takes linear time in the size of the output. The [independent checker](check_two_site_arms.py) counts the actual edges including both joining sites in 6,180 complete attachments, with examples through doubled modulus 131,070. It also checks both permutations of 2,394 signed Langford arrays. [Lean verification of the slot permutation and interval arithmetic](TwoSiteArms.lean)

~~~bash
python3 -B -m research.census.check_two_site_arms
lean research/census/TwoSiteArms.lean
~~~
