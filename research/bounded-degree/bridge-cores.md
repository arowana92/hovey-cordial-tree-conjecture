# Bridges of every length between two prescribed divisible-order trees

**Theorem.** At every sufficiently large modulus $k$, take two independently $k$-cordially labeled trees, each of positive order divisible by $k$. Fix their port labels $a,b$ and denote their deficient weights by $D,E$. Join them by a path with $t$ new vertices. Write $S=\sum\mathbb Z_k$. All old labels extend exactly under the following conditions.

| $t$ | Condition, with label arithmetic modulo $k$ |
|---|---|
| 0 | $a+b\in\{D,E\}$ |
| 1 | $b-a=\pm(E-D)$ |
| 2 | The case $a=b$, $D=E=2a$ is excluded |
| $t\ge3$ | All cases, except that at even $k$ and $t=jk+1$ the integer $D+E-a-b+jS$ must be even |

The threshold is independent of the old trees, their degrees and $t$. At eight and nine the [finite bridge table](../eight/separated-pins.md#joining-two-independently-labeled-trees) already gives the complete result. At **every** modulus the [long-bridge construction](../census/long-bridge.md) supplies an explicit sufficient length and permits arbitrary old orders.

## Small bridges

The new vertices must have balanced counts. From the histogram of the $t+1$ path edges subtract one occurrence of each deficit. The result must be balanced of total $t-1$. The rows for zero or one new vertex follow. At $t=2$, putting $D,E$ on the two outside edges works unless $D-a=E-b$. Try the reverse assignment as well. If both fail, $D-E=a-b=b-a$. Instead put $D$ on the first edge and $E$ on the middle edge. The new vertices have labels $D-a,b$, distinct unless $D=a+b$. Interchanging $D,E$ forces $E=a+b$ too if this also fails. This gives precisely the excluded case. Translating it to $a=b=D=E=0$, two of $u,u+v,v$ would have to vanish at distinct internal labels $u,v$.

For **every modulus** and $3\le t<k$ with $k>4t-10+2\gcd(2,k)$ there is an elementary construction. Start the first $t-2$ vertices at $x=D-a$, greedily keeping vertices distinct and internal weights distinct. Each step excludes at most the previous vertex and weight counts combined. Let $c$ be the last prefix label, and put the last two labels $y,E-y$. They must both avoid the $t-2$ earlier labels and each other. The two remaining weights $c+y,b+E-y$ must avoid the $t-3$ earlier internal weights and each other. These restrictions exclude at most $2(t-2)+2(t-3)+2\gcd(2,k)$ choices of $y$. The first entering edge fills $D$, the last internal edge fills $E$, and all remaining weights are distinct. This covers $3\le t\le7$ at all sufficiently large $k$.

## Completing any shorter-than-period path

For $8\le t<k$, number the desired path $0,\ldots,t-1$. Extend it to a tree $U$ on $k$ vertices. Attach an additional leaf at position 5. When $k-t\ge2$, also attach a path of length $k-t-1$ at position 5. We will use a full bijection on $U$ with distinct internal sums, retaining only the original path.

Pin the following labels: $x=D-a$ at 0, $y$ at $t-1$, $u,E-u$ at positions 2 and 3, $z$ at 5 and $h=b+y-z$ at the extra leaf. Denote $L=b+y$. If there is a second extra arm, let $v$ be its tip label. The entering edge at 0 supplies $D$ and an internal edge supplies $E$. The other entering weight $L$ was the sum on a discarded edge. Once $U$ has distinct sums, the other $t-1$ contributions are distinct: they are the retained internal weights except $E$, together with $L$.

All non-degree-two positions of $U$ are pinned. Its full vertex sum is $S$ and its full edge sum must be $S-w$ for missing weight $w$. Counting incidences fixes
$$
 w=x+y+h-z-S\quad (k-t=1),\qquad
 w=x+y+h+v-2z-S\quad (k-t\ge2).
$$
Choose $y\ne x$ with $L\ne E$. Choose $u,E-u$ fresh and distinct. Choose $z,h$ fresh and distinct. With one extra leaf, exclude $w=E,L$ at this step. With two extra vertices, exclude $x+y+h-3z-S=0$, so $w\ne z+v$ whatever $v$ is. These restrictions exclude only boundedly many values: after substituting $h=L-z$ their nonconstant coefficients on $z$ have absolute value at most four. Finally choose a fresh $v$ if needed, avoid $w=E,L$ and, when its arm has length one, $z+v=E,L$. Thus the induced pinned sums are distinct and different from $w$. The displayed moment is exactly the empty-unpinned-moment case of the [partial embedding theorem](partial-gap.md). The degree cap is four and the pin count at most seven, so the same large-$k$ threshold works for every $t$. That theorem applies [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

## At least one period

First attach $t-k$ path vertices at $a$, preserving the first old labeling; a pendant path of every length extends a divisible core. Call its new tip label $z$, using $z=a$ at zero length. Temporarily join this enlarged first tree to the second by a single edge of weight $E$. Choose the second endpoint of the temporary edge at any required residue: every residue occurs in that tree. This fills its deficient bin, so the interim tree is cordial. [Pendant construction](../census/cycle-subdivision.md)

Remove the temporary edge and reconnect the two components at $z,b$ by a path on $k$ new vertices. The [distinct-port parity theorem](port-parity.md#one-and-two-ports) gives a compatible labeling except when $k$ is even, the interim edge counts are uniform, and $E-z-b-S$ is odd. The uniform case is exactly $t=jk+1$. The first pendant part then had $(j-1)k+1$ new vertices with some surplus $u$. It supplied $(j-1)$ copies of each edge weight plus $D$. Summing its path edges gives
$$
 z=a+(j-1)S+2u-D .
$$
Hence the port theorem's obstruction is precisely the claimed parity. Conversely on the final full bridge the sum of its weights must be $jS+D+E$ and also equals $a+b$ plus twice the internal-label sum. No labeling can evade that parity.

## Prescribing distant positions for large moduli

On a path, **any number of labels at mutual distances at least $2k+2$ may be prescribed**. The sole exception is even $k$, order $qk+1$, with both tips prescribed and their sum of parity different from $qS$. In the [path splitting proof](../census/long-bridge.md#many-prescribed-positions-on-a-path), use $t=r$ for order residue $r\ge3$, or $t=k+r$ for $r=0,1,2$. Align the first component to a multiple of $k$. Since $t\le k+2$, the distance suffices. Both sides are divisible, leaving the stated parity at the final join. This bound also works at eight and nine by their finite bridge tables.

Fix $0<\epsilon<1$. More generally take any tree with at most $l\le k^{1-\epsilon}$ leaves, with pins at mutual distances at least $2(l+1)(2k+1)+1$. Prescriptions extend whenever the order differs from one modulo $k$, the modulus is odd, or the tree has an unprescribed leaf. If every odd-degree vertex is prescribed and the order is $qk+1$ at even $k$, extension is equivalent to the sum of their labels having parity $qS$.

Indeed every connected subtree has at most $l$ leaves; each outward component beyond a new tip leads to a distinct original leaf. The degree excess above degree three is at most $l$ by the tree degree identity. For one pin, translate the ordinary labeling from the [degree-excess theorem](excess.md). With two or more pins their hull contains an internally unmarked, nonbranching segment of length at least half their separation, rounded up, by the [farthest branching vertex argument](../eight/separated-pins.md#cutting-a-tree-with-prescribed-labels). At most $l$ interior sites can branch outside the hull, since each such site has a distinct leaf in an outside component. If all clean runs had length at most $2k$, the segment would have at most $l+(l+1)2k$ interior sites. The separation gives a longer segment. A clean run of at least $2k+1\ge t+k-1$ permits an aligned bridge of the preceding size. Apply induction to its two divisible sides. An unprescribed leaf in the uniform-edge case can first be removed and restored. Otherwise the bridge parity, if tested, is the parity of the final sum at odd-degree vertices against $qS$, by incidence counting.

## Checks

~~~sh
python3 -B research/bounded-degree/check_bridge_cores.py
~~~

The [constructor](bridge_cores.py) gives actual elementary bridges and the labeled part of each auxiliary tree. The [independent checks](check_bridge_cores.py) recount 8,680 elementary bridges, verify all pinned sums, degree classes and both embedding moments on 540 auxiliary cores, and reconstruct 204 long-bridge core embeddings and 19 parity obstructions. The positive large-modulus conclusion uses the cited embedding theorem; these finite checks supply no numerical value of its threshold.
