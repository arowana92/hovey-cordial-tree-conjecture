# Cordial growth through 26 labels

**Theorem.** For every $1\le k\le26$, each nonempty finite tree admits a connected vertex order and a single labeling that is $k$-cordial on **every prefix**. A specified leaf can be put in the final block, where blocks have $k$ vertices except possibly the last. The same assertions hold at 27 for [trees with at most twelve leaves](../census/leaf-profile-cuts.md) and at 28 through 30 for trees with at most eight leaves.

For the same labeling, any vertex in the first $\min(n,k)$-vertex block can start the order. Indeed, the vertices of that connected block have distinct labels and its edges have distinct sums. Reorder it in any connected fashion, then resume the existing order. At eight and nine the separate fixed-core theorem allows a starting vertex anywhere in the tree. At every composite modulus some specified connected orders obstruct prefix cordiality. [Prescribed start and prescribed-order obstructions](../eight/growth-orders.md)

## Keeping all the intermediate trees cordial

Write $n=mk+1+t$, $0\le t<k$. At order at most $k$, use the bijective rainbow base on an order-$k$ tree and restrict to the actual tree. Every connected order works on the restriction. For a larger tree proceed by induction on order.

If $t=0$, delete the marked leaf, or any leaf in the absence of a mark. Use a successful order and labeling of the smaller tree, and put the leaf last with the unique label that fills the deficient edge bin. If $t>0$, take the same cut as in the ordinary proof. When there are at least $t$ leaves one can delete $t$ of them together. Otherwise the leaf-centroid construction supplies a core of order $mk+1$ and a size-ordered exterior with at most $\lfloor2L/3\rfloor$ tips, where $L$ is the number of leaves. The required tests have been established in the stated ranges. The earlier contour tests allow arbitrary boundary colors and suffice as well. [Cut and leaf-batch proofs](README.md#why-the-hypotheses-suffice) · [Ordered-cut certificates](ordered-cut.md) · [Proofs and links through 26](../../README.md) · [Few-leaf certificates](few-leaves.md)

Apply induction to the core. If the mark is in it, the mark is still a leaf; its final block in this core consists of just that leaf. On the exterior take the rainbow labeling that the ordinary cut proof supplies for the actual boundary labels. The new vertex labels are distinct and avoid the core surplus, and the new edge weights are distinct. Put the exterior in any parent-first order. Every intermediate prefix adds some of these distinct labels to low vertex bins and adds distinct weights to uniform edge bins. Thus the same labeling works throughout. The final block contains the vertex at position $mk+1$ and all $t$ exterior vertices, so it contains the mark in either case. Induction within a leaf-limited class is valid because a connected subtree cannot have more leaves than the original tree, with singletons treated separately.

For the small moduli, one label is immediate. At 2, 3, 5 and 7 the theorem for **every** prescribed connected order allows the marked leaf to be placed last. At six and eight the small ordered certificates suffice. At four the only case beyond the leaf batch has two leaves and $t=3$, so one can take a three-vertex terminal path. For each normalized parent color $0,1,2,3$ a permutation of $1,2,3$ gives distinct entering weights, as also checked below. The order-four base consists of a path and a star: along the path use $0,2,1,3$, and on the star use zero at the center. [Small ordered certificates](../marked-leaves.md#reproduction) · [Prescribed orders at small primes](../near-matching.md#every-connected-prefix)

## Growing from a fixed site

Suppose the ordered forest test at modulus $k\ge2$ has been proved for $q$ tips on $k-1$ free vertices. Fix a cordial labeling of any nonempty core of order zero or one modulo $k$. Attach a forest of **arbitrary order** at one old vertex with at most $q$ tips in total. Some parent-first order of the new vertices keeps the fixed labeling cordial at every step. In particular $q=16$ works at [26 labels](twenty-six.md), $q=6$ at 27, and $q=5$ at 28, 29 and 30. Taking a single labeled vertex as the core gives a prescribed start when the tree rooted there has at most $q$ tips. A tree of at most $q+1$ leaves therefore admits any specified leaf as a start.

Induct on the number of new vertices. With no addition there is nothing to prove. Write $t=(n-1)\bmod k$ for the order $n$ after attaching the forest. If $t=0$, remove a new terminal vertex and return it last by filling the edge deficit. Otherwise $1\le t\le k-1$ and there are at least $t$ new vertices since the original core has order zero or one modulo $k$. Size-order the children at the attachment vertex and at every new vertex, and remove the last $t$ of this preorder. The remaining new forest is still attached at one site. Every one of its tips extends to a distinct original tip. Apply induction, then the ordered-cut certificate on the removed forest, padding a largest component if necessary. The terminal count and all boundary-run inequalities hold as in the ordinary proof. Append the resulting vertices in any parent-first order. The argument allows the traversal to be recomputed after each cut.

## Independent checks

The [constructor for marked trees](../marked_leaf.py) returns the growth order as well as the labeling. The [fixed-site constructor](site_growth.py) starts from the actual old vertex labels. A [separate replay](check_cut_growth.py) induces each prefix using the original edges, counts every residue including zeros, and checks connectedness. It checks 27,115 prefixes of 2,435 marked trees, together with 14,175 new prefixes in 350 fixed-core extensions. These finite replays test the implementation. The induction and the exhaustive forest certificates give the all-orders conclusions.

~~~sh
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -shared "$r/leaf_search.cpp" "$out/ref.o" -o "$out/solver.so"
python3 -B -m research.rainbow.check_cut_growth "$out/solver.so"
python3 -B -m research.check_marked_leaf
~~~
