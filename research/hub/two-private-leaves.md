# Two leaves at every original vertex

**Theorem.** For every sufficiently large modulus $k$ and every tree $H$ of order $h\ge k$, attaching at least two new leaves at each vertex of $H$ gives a $k$-cordial tree. Populations at different sites are independent. There is no degree restriction.

Some ranges hold at explicit moduli. The [breadth-first construction](breadth-first-leaves.md) covers $h=k$ and $h\ge2k$ for every $k$. Write the remaining orders as $h=k+r$, $0<r<k$. The proof below covers $2r\le k$ at **every odd modulus**, and $5r\ge4k$ at **every modulus**. Every odd $k\le33$ is covered for all $h\ge k$. The universal large-modulus threshold is existential.

## Completing a core with at most three edges per weight

Let $G=\mathbb Z_k$, $\sigma=\sum_{w\in G}w$, and let $X$ be the $t=k-r$ core labels occurring once. All other vertex labels must occur twice. Write $M_w$ for the old edge counts. Suppose
$$
\max M_w\le3,\qquad |\{w:M_w>0\}|\ge r,\qquad z=|\{w:M_w=3\}|<r.
$$
Assume also that $k$ is odd, or that $t$ is sufficiently large and $X$ contains two consecutive residues. Under these conditions, two leaves at each site suffice while preserving the core labeling.

Choose a set $Y$ of $t$ helper weights in $A=\{w:M_w<3\}$. Its size satisfies $0<t<|A|$. The possible sums of such sets have cardinality at least $|A|=k-z$. For $t=1$ or $t=|A|-1$ this follows directly. At intermediate cardinalities use the restricted-sum theorem of Girard, Griffiths and Hamidoune. Its exception needs a coset of an elementary 2-subgroup of size at least four, which cannot occur in a cyclic group. [Restricted-sum theorem](https://arxiv.org/abs/1110.1961)

Let $j=|\{w:M_w\ge2\}|$. Then
$$
j+z=h-1-|\{w:M_w>0\}|\le k-1.
$$
Consequently there is a choice of $Y$ for which $d=3\sigma-\sum_w wM_w-\sum Y$ has $M_d\le1$. Pair $-X$ with $Y$ so that their sums are distinct. At odd modulus this is the cyclic Snevily theorem. For large $t$ the transversal classification gives the same conclusion at even modulus. Consecutive elements of the proper subset $X$ rule out a coset of a proper subgroup, and the cyclic group has no large elementary 2-subgroup. [Dasgupta, Károlyi, Serra and Szegedy, Theorem 1](https://sites.math.duke.edu/~dasgupta/papers/finallatin.pdf) · [Müyesser and Pokrovskiy, Theorem 1.4](https://doi.org/10.1007/s00222-025-01328-x)

Each pair $(-x,y)$ requests one leaf with parent label $y-x$ and leaf label $x$. These shifts are distinct and every shift still has a second available leaf. All vertex bins now have size two. All edge bins have size at most three and bin $d$ has size at most two. Reserve one leaf at each shift. The [uniform-parent criterion](breadth-first-leaves.md#an-exact-criterion-with-uniform-parent-colors) completes these $k$ leaves to order $3k$ with deficient edge $d$. From this divisible order Hall's leaf extension adds the remaining leaves.

## Finding the core labeling

For $2r\le k$, number the vertices in breadth-first order, with children consecutive, starting at zero. Give each vertex its number modulo $k$. The integer weights $i+p_i$ are strictly increasing and lie in $[1,2h-3]$. Each residue occurs at most three times. Every third occurrence has $i+p_i\ge2k+1$, and $p_i<i$ implies $i\ge k+1$. Thus $z\le r-1$. The support has at least $(k+r-1-z)/2\ge k/2\ge r$ bins. The single labels form the consecutive interval $[r,k-1]$, of size $t\ge k/2$. Apply the preceding construction. The odd case also permits a singleton $X$.

For $k/2<r<4k/5$, take any connected prefix on $r+1$ vertices. Embed it as a rainbow tree in the sum-colored complete graph on the residues other than 0 and 1. The coloring is proper, and the order $r+1$ is at most $4k/5+1$. Thus the published almost-spanning rainbow tree theorem on $K_{k-2}$ applies at all sufficiently large $k$ with fixed positive slack. Let $u$ be any one prefix label. [Montgomery, Pokrovskiy and Sudakov, Theorem 1.1](https://doi.org/10.4171/JEMS/982)

The remaining $k-1$ vertices form a rooted forest with the actual prefix vertices as parents. Give them exactly $G\setminus\{u\}$, with every forest weight occurring at most twice, using the [prescribed-label forest construction](prescribed-forest-labels.md). The combined core has vertex bins of size one or two, maximum edge count three, and at least $r$ occupied weights from the prefix. Each triple weight uses two forest edges, so $z\le\lfloor(k-1)/2\rfloor<r$. The set $X$ of single labels contains 0 and 1 and has size $t>k/5$. The completion lemma applies at all sufficiently large moduli. This proof allows arbitrary boundary parents.

There is also an explicit finite range. If the prefix has an integer labeling with consecutive vertex labels $0,\ldots,r$ and consecutive edge sums, use that labeling and take $u=r$. The single set is now $X=[r,k-1]$. Kézdy and Snevily pair $-X=\{1,\ldots,t\}$ with the desired helper weights giving distinct shifts, since $2t\le k+1$. The same completion works at **every modulus** whenever such a prefix is available and $2r>k$. The integer census covers every prefix of order at most 27. In particular, joining the lower interval, this middle interval and the last fifth proves the two-leaf theorem for **every odd modulus through 33** and all $h\ge k$. [Integer tree census](../census/README.md) · [Kézdy and Snevily, Theorem 2.5](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Kezdy/kezdy.pdf)

## The last fifth at every modulus

For $5r\ge4k$ again use the breadth-first numbering of the entire core. Each old weight occurs at most four times. Write $Z=\{w:M_w=4\}$. A fourth occurrence has $i+p_i\ge3k+1$ and therefore $i\ge\lceil(3k+2)/2\rceil$. In particular
$$
2|Z|\le 2(k+r)-2\lceil(3k+2)/2\rceil\le r-t-2.
$$

Reserve **two** leaves at every shift. Each shift in $R=[0,r-1]$ still has at least two helper slots from its two original vertices. Assign the first $t-1$ missing inputs $r,\ldots,k-2$ in order, always using a shift in $R$ with a slot left and a weight of current count at most two. After $i$ helpers there are at most $\lfloor i/2\rfloor$ exhausted shifts and at most $(h-1+i)/3$ weights of count at least three. Together these exclude fewer than $k/10+2k/3<r$ shifts. Thus the only bins of count four are still those in $Z$.

For the last input $k-1$ vary the shift $s$ over $R$. Its weight $w=s+k-1$ varies injectively and the final deficient bin is $d=4\sigma-\sum(\text{previous weights})-w$. Avoid exhausted shifts, $w\in Z$, $d\in Z$, and $w=d$. The last equation excludes at most two shifts. In total at most
$$
\lfloor(t-1)/2\rfloor+2|Z|+2<r
$$
choices are excluded. The core and helpers now have two vertices per bin, at most four edges per bin, and fewer than four edges at $d$. The two reserved batches reach order $4k$ by the uniform-parent criterion. The remaining leaves can be added from that divisible order.

## Finite replay

The [constructor and physical-tree checker](two_private_leaves.py) searches directly for the restricted sum, the distinct shifts, and the small rainbow forests. It recounts vertex and endpoint-sum histograms including all zero bins. It verifies 1,263 lower-range constructions, 465 split-forest constructions and 33 upper-range constructions. They include every rooted ordered core through eight vertices for the covered parameter choices, and paths, stars and branching trees with independently varying populations at composite and prime moduli through 21. The split-forest examples in this checker use the earlier construction with a breadth-first $k$-vertex prefix and a rainbow suffix. The [prescribed-label checker](prescribed_forest_labels.py) also tests the argument above with a rainbow prefix of order $r+1$. The universal threshold comes from the embedding and matching theorems.

~~~bash
python3 -B -m research.hub.two_private_leaves
python3 -B -m research.hub.breadth_first_leaves
~~~
