# When a vertex cover has one prescribed label

**Theorem at every modulus.** Prescribe the same residue $a$ on a nonempty vertex cover $S$ of a tree of order $n$. Every cordial completion must assign $a$ to **every nonleaf**. Writing $F$ for the union of $S$ and the nonleaves, a completion exists exactly when $|F|\le\lceil n/k\rceil$ (for a singleton use $F=S$). Other labels can also be prescribed. Any prescription on $F$ must agree with $a$, and the remaining leaf labels need only pass the bin-capacity test below.

For instance, take a hub with $r\ge1$ two-edge arms and any number of direct leaves. Prescribe zero at the hub and all $r$ tips of the two-edge arms. Every middle vertex must also receive zero. These $r+1$ prescriptions extend exactly when $n\ge2rk+1$. For a single two-edge arm this gives an obstruction at orders eight and sixteen to prescribing the same 8-label at the hub and that tip. The tree itself is cordial.

## Components of a label class

Translate $a$ to zero, shifting all edge weights by $-2a$. Let $A$ be the zero vertices, $B$ their complement, $b$ the number of edges within $B$, and $h$ the number of those edges with opposite endpoint labels. The subgraph on $A$ is a forest. Its component count (zero if empty) is $|A|-|E(A)|$. Hence the difference between the zero vertex and edge counts is
$$
 V_0-E_0=|A|-|E(A)|-h
        =1+\sum_{v\in B}(d_v-1)-b-h .
$$
For balanced counts, $V_0-E_0\le\lceil n/k\rceil-\lfloor(n-1)/k\rfloor=1$. In particular
$$
                       \sum_{v\in B}(d_v-1)\le b+h\le2b .
$$
For a prescribed cover, $b=0$. On a nonsingleton tree every summand is nonnegative, so every nonzero vertex is a leaf. Conversely once all nonleaves and all of $S$ are zero, each nonzero leaf has a zero neighbor. This holds at order two as well since $S$ is a cover. Its weight is exactly its label. The resulting edge counts are the vertex counts minus one at zero.

With additional pins, count the already assigned vertices in bins $c_x$, counting each vertex of $F$ only once. Write $n=qk+r$ with $0\le r<k$. When $r=0$ require every $c_x\le q$. Otherwise require every $c_x\le q+1$ and
$$
               |\{a\}\cup\{x:c_x>q\}|\le r .
$$
Choose the $r$ high vertex bins to contain this union and fill the remaining slots with free leaves. The high bin at $a$ can lose one unit on the edge side after translating back. This proves both directions.

## A cover missing a few edges

If the vertices prescribed zero miss $j$ edges, then $b\le j$. Thus every vertex of degree greater than $2j+1$ is forced to be zero, and at most $2j$ nonleaves can have nonzero labels. The factor two is sharp: start with a tree of zero vertices, subdivide $j$ of its edges with adjacent pairs carrying $x,-x$ for some $x\ne0$, and keep the old vertices zero. Add direct leaves to an old vertex to fill a balanced vertex histogram with zero most frequent. The two new vertex contributions on each replaced edge are also its net edge contributions. The only uncovered edges are the $j$ central ones, and the degree surplus off zero equals $2j$. For $j=0$ this recovers the cover criterion.

These bounds also give a finite search for prescribed sets missing at most $j$ edges with work depending on $k,j$ apart from reading the tree and storing its label counts. Enumerate the labels on the at most $2j$ endpoints of uncovered edges. Every other vertex outside the prescribed set is adjacent only to zero vertices. For its nonleaf members, group by degree and decide the multiset of pairs (degree, nonzero label) to use, respecting group sizes and a total degree surplus of at most $2j$. Take all remaining nonleaves zero. An additional fixed label must be respected in these choices. After assigning the already fixed leaves, every remaining free leaf attaches at zero. Let $V^0,E^0$ count everything except these free leaves and their incident edges. Set $z_x=E^0_x-V^0_x$. The final vertex count $v_x$ lies in the integer interval
$$
 \max\{V^0_x,\lfloor n/k\rfloor,\lfloor(n-1)/k\rfloor-z_x\}
 \ \le v_x\le\
 \min\{\lceil n/k\rceil,\lceil(n-1)/k\rceil-z_x\}.
$$
The free leaves can fill the bins exactly when every interval is nonempty and the sums of the lower and upper endpoints bracket $n$.

## Reproduction

~~~sh
python3 -B -m research.census.check_cover_pins
~~~

The [constructor](cover_pins.py) fills the actual vertex bins. A [separate checker](check_cover_pins.py) enumerates full labelings on every rooted tree shape through six vertices at moduli two, three and four. It checks the off-zero degree sum and compares the exact completion test against 60,537 partial assignments with up to two additional pins.
