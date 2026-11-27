# A most-frequent label at the hub of a partially subdivided star

**Theorem.** Attach $b$ paths of length two and $l$ ordinary leaves to a hub. For every positive modulus $k$, the resulting tree has a cordial labeling with the hub in a most-frequent vertex class, with exactly one exception. At $k=4,b=2,l=0$, the middle of the five-vertex path cannot have a most-frequent label. The path itself is cordial.

The construction consequently extends over the hub of any cordially labeled tree of order one modulo $k$ when the old hub carries the unique surplus. Its label stays most frequent. The old histograms are a uniform contribution plus those of the singleton hub, so the same increments suffice. Modulus one is immediate. Ordinary cordiality of these subdivided stars was proved by the [unmarked construction](../hub/subdivided-stars.md).

**Matching consequence.** Start with one vertex and any collection of disjoint paths on **two or four vertices**. Join the chosen vertex by one edge to any vertex of each path. The resulting tree is $2m$-cordial at **every positive odd $m$**. The paths may meet their joining edges at endpoints or internal vertices, independently. In particular the number of branching vertices is unrestricted.

## Fewer than half a period of two-edge arms

Give the hub label zero. Write each arm as $(a,z)$ for intermediate label $a$ and tip label $z$, giving weights $a,a+z$. Suppose $2b<k$. For $b=2h$ use intermediate labels $\pm1,\dots,\pm h$. On $1\le j\le2h$ the permutation $j\mapsto2j\bmod(2h+1)$ has exactly those displacements. Put a tip at position $h+j$ with its displacement as its intermediate label. The free labels and weights both occupy $[-h,3h]$ with zero omitted.

For $b=2h+1$, first do the same on tip positions $h+1+j$ for the $2h$ opposite intermediate labels. Add the arm $(-h-1,h+1)$. Within $[-h-1,3h+1]$ the free vertices omit zero and the edges omit $h+1$. In either parity the containing interval has length $2b+1$. If $l<k-2b$, choose all $l$ direct leaf labels outside its residues. Every vertex of the whole tree and every edge respectively has a distinct label or weight. The hub is therefore in a most-frequent bin.

If $l\ge k-2b$, build a uniform first period from the $b$ arms and $k-2b$ direct leaves. For even $b$ use the displayed arm layout. For odd $b$ instead use intermediate labels $[-h,h]$ and place the tips on the next $b$ positions, doubling their indices modulo $b$. The displacements are exactly $[-h,h]$. In both cases the $2b$ distinct free labels equal the $2b$ distinct edge weights as sets. Use all their complementary residues on direct leaves. Each histogram has now gained one in every bin. Additional leaves can cycle through $1,\ldots,k-1,0$ in that order, keeping the hub most frequent.

## Removing full periods

For even $k\ne4$, $k/2$ two-edge arms have a uniform increment. At $k=2$ use $(0,1)$. At $k\ge6$ the [integer construction for regular branches](regular-joints.md#an-even-number-of-centers) supplies the block, including the odd-center case on the same page. Remove such blocks until $2b<k$.

Now take odd $k\ge3$ and put $h=(k-1)/2$. Remove groups of $k$ arms using $(j,j)$ for $j\in\mathbb Z_k$. If $b\ge h$ and a direct leaf is available, use a full period with $h$ arms and one direct leaf, as above. Repeat when possible. The only outstanding case has $h<b<k$ and no direct leaves.

For $k\ne3$ use the [nonzero-residue construction](two-site-arms.md#filling-the-nonzero-residue-classes) on the first $h$ arms. Together with the hub it makes the vertices uniform and the edges deficient at zero. For $r=b-h$ further arms, take $r$ entries of a full short row whose intermediate labels include zero, retaining the arm at intermediate zero. For odd $h$ the coincident-parent row has a centered interval of intermediate labels. For even $h$ the unit-difference row has intermediate interval $[1-h/2,h/2]$. Both contain zero, and all their vertex labels and edge weights are respectively distinct. The chosen arm uses vertex zero and fills the zero edge deficit. Thus the hub again belongs to a highest-frequency class. At $k=3$ the only remaining case is two arms, handled by $(1,2),(0,2)$.

## Four labels

Four direct leaves form a uniform period, as do four two-edge arms with pairs $(0,1),(0,3),(2,1),(2,3)$. Six two-edge arms also have a uniform labeling, and so do two arms with four direct leaves. The [small rows and checker](check_subdivided_star_mark.py) list both and the remaining cases $b=2,3$, $0\le l\le3$ except $(2,0)$.

For $b=2\bmod4$, $l=0\bmod4$, remove six arms if possible, otherwise two arms and four leaves when available. Outside the single claimed exception this leaves only uniform groups. In every other case reduce $b,l$ modulo four, using the short construction when $b<2$.

In the exception, a high hub would have the unique repeated label. Normalize it to zero. The four free labels and four weights would both be permutations. Subtracting their sums shows the two intermediate labels add to zero. They are distinct, so they must be 1 and 3. One tip then has label zero and repeats its parent's entering weight. This proves impossibility.

## Contracting the paths

Add one temporary mate at the joint. Every two-vertex path gives one matched pair. Every four-vertex path gives two matched pairs, regardless of where its joining edge meets the path. After contraction, the quotient is exactly a partially subdivided star with its temporary pair at the hub. At odd $m$, give the hub a most-frequent quotient label. Apply the [perfect-matching lift](../matching-expansion.md) and delete the temporary vertex. Its vertex label and its odd matching-edge weight both came from maximum-frequency bins. The histograms therefore stay balanced. This proves the all-orders matching consequence.

The checker tested the hub frequency and both histograms on 28,003 trees through modulus 60. It independently assigned the matching port parities and counted the actual vertices and edges after deletion on 13,773 expanded trees.

~~~bash
python3 -B -m research.census.check_subdivided_star_mark
~~~
