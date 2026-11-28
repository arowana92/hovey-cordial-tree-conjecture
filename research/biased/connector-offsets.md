# An offset on the connector of a subdivided double star

**Theorem.** At every prime power $k\ge4$, let two nonleaf vertices be joined by a path of length two, with all remaining vertices leaves at its endpoints. On either edge of the connecting path prescribe any additive offset. At every tree order there is a labeling cordial on every prefix of a suitable connected order. The two endpoint degrees can be arbitrarily large.

Equivalently for ordinary cordiality, that chosen edge can be replaced by any chain of trees of orders divisible by $k$, each supplied with an ordinary $k$-cordial labeling and two arbitrary attachment vertices. The aggregate effective offset can be prescribed on the edge before restoring the chain. The conclusion for the expanded tree concerns its final counts. [Expansion identity](period-chains.md)

**Two independent connector offsets.** At those prime powers one may in fact prescribe offsets on both $UA$ and $AB$ independently, prescribe the label at $A$, and start the growth order there. This follows from the earlier two-star fixed-core theorem. Normalize $A$ to zero. The two components of $T-A$ are both nontrivial stars. Attach their centers to the two effective boundary colors on a surrogate one-surplus star, and replace that surrogate by $A$ when reading the labeling. The only exceptional two-star shape at a power of two has a singleton component. At an odd prime power there are no exceptions. Consequently one may insert arbitrary chains of cordially labeled divisible pieces on **both** connecting edges. The single-offset calculation below also gives necessary conditions at moduli with distinct prime factors. [Two-star theorem](../rainbow/surplus-prime-powers.md) · [Surrogate-core equivalence](one-edge-exceptions.md#allowing-independent-offsets-on-all-edges-at-one-vertex)

## Exact test at every modulus on one period

Take the order to be $k$. Name the three consecutive vertices $U,A,B$, put offset $d$ on $UA$, and let $t$ be the degree of $B$, counting its neighbor $A$. The construction has $t-1$ pendant leaves at $B$ and $k-t-2$ at $U$. Allow $1\le t\le k-2$. Normalize the label of $U$ to zero.

Test each possible nonzero label $b$ of $B$. Let $h$ be its additive order and write $t=qh+j$ with $0\le j<h$. This $b$ works if and only if $j\ne h-1$ and one of the two residues
$$
                     b-d,\qquad -tb-d
$$
belongs to $\{-b,-2b,\ldots,-jb\}$ or, when $q>0$, lies outside $\langle b\rangle$. The first set is empty for $j=0$.

Indeed, the labels form a bijection. Write $X$ for the $t$ labels of the neighbors of $B$, including the connector label $a$ at $A$. The pendant leaves at $U$ use every residue outside $\{0,b\}\cup X$. Their weights equal their labels. The $t$ weights $b+X$ avoid $b$ and must therefore lie in $\{0\}\cup X$. On any coset of $\langle b\rangle$ away from zero, closure under adding $b$ forces all or none of its elements into $X$. On the subgroup itself, starting at any selected element and advancing by $b$ must lead to zero through selected elements. This gives a consecutive string of negative multiples ending at $-b$. Its length is at most $h-2$, since $b$ is already used at $B$. Thus $X$ consists of the displayed $j$ elements and $q$ whole nonzero cosets. There are enough such cosets because $t\le k-2$. Any prescribed label outside the subgroup can be included when $q>0$.

After assigning the edges incident to $B$, the only remaining slots for $a+d$ are $b$ and $-tb$. For $j>0$, the translate of the string fills zero and leaves $-jb=-tb$ unused. For $j=0$ the whole cosets are unchanged and zero is unused. This proves necessity and gives the actual labels whenever the test passes.

## Why every prime power works

Assume $t\ge2$ and $k=p^e$. Offset zero works with $b=1$ and $a=-t$. If the additive order of $d$ exceeds $t+1$, take $b=-d$. Then $j=t$, and $-tb-d=-(t-1)b$ is in the string. Otherwise suppose $d\ne0$ and let $h$ be the smallest power of $p$ strictly greater than $t+1$. It divides $k$. Put $r=h/\operatorname{ord}(d)$. Then $2\le r\le h/p\le t+1$. In a cyclic group there is a $b$ of order $h$ with $rb=d$. Here $j=t<h-1$, and $b-d=-(r-1)b$ lies in the string. This covers every offset.

Below order $k$, pad one of the two leaf populations to order $k$ and restrict the rainbow labeling. Above order $k$, retain a connected core of exactly $k$ vertices containing $U,A,B$ and at least one pendant leaf of $B$. All omitted vertices are leaves of the retained core. From divisible order add one leaf with the label that fills the deficient weight. From order one modulo $k$, the leaf-extension theorem labels up to $k-1$ leaves with distinct nonsurplus labels and distinct weights. Repeat these steps as necessary. Parent-first growth inside the initial rainbow core and within every batch keeps every prefix cordial. The proof also permits arbitrary offsets on the omitted leaves by adding each to its parent color. [Leaf extension](../counterexample-bound.md#removing-leaves)

## Composite moduli with obstructions

For $k=2p$ with $p\ge5$ an odd prime and $2\le t\le k-2$, the **only** failure is $d=p$ with $t\le p-2$. In this range every other nonzero offset has order at least $p>t+1$ and works by $b=-d$. To test $d=p$, a label $b$ of order two has no admissible slot for $a$. A label $b$ of order $p$ has $q=0$, and both candidate slots lie outside its subgroup. A label of order $2p$ gives $d=pb$ and neither candidate lies in the length-$t$ string. When $t\ge p-1$, take a unit $b$. As $b$ varies, coefficients $-1,2,p$ suffice to realize all three nonzero gcd classes. Coefficient $-1$ is allowed by $t\ge2$ and $2,p$ both belong to $[2,t+1]$.

More generally, for even $k$ and $d=k/2$, at $t=2$ the test succeeds exactly when $3\mid k$ or $4\mid k$. At $t=3$ it succeeds exactly when $3\mid k$ or $8\mid k$. To see this, an odd order $h$ can work only with $h\le t$ and $j\ne h-1$, since $d$ is outside the subgroup. For even $h=2s$, one has $d=sb$. Order two fails, and for $s\ge2$ the candidate slots work exactly when $s-1\le j\le2s-2$. Substituting $t=2,3$ gives the divisibility tests. At ten labels these are the two additional exceptional marked trees beyond the double stars. [Complete small-modulus classification](one-edge-exceptions.md)

The [checker and witness construction](connector_offsets.py) directly chose the actual neighbors of the far hub as a subset through modulus 14. All 803 literal comparisons agreed with the orbit criterion. Through modulus 100 it evaluated 328,248 inputs, reconstructed 326,225 full labeled trees and recounted every ordinary and adjusted weight. A separate two-connector replay rebuilt 1,650 ordinary trees after inserting a full star on each connector, checking 43,540 adjusted growth prefixes before expansion.

~~~bash
python3 -B -m research.biased.connector_offsets
~~~
