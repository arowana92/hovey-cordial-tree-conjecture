# Cordial growth from a chosen root at large moduli

**Theorem.** Fix an integer $D\ge3$ and $0<\epsilon<1$. For all sufficiently large $k$, take any finite tree $T$ and choose any starting vertex. Write $E_D(T)=\sum_v(\deg_T(v)-D)_+$. Allow an edge $uv$ to have weight $x_u+x_v+\delta_{uv}$ modulo $k$, where all but $b$ of the offsets have one common value. If
$$
                      E_D(T)+b\le k^{1-\epsilon},
$$
one labeling is cordial on **every prefix** of the depth-first preorder from the chosen vertex with child subtrees visited in nondecreasing order of size. Ties may be fixed in advance. The starting vertex may be assigned any label. The tree order is unrestricted.

**Prescribed-order corollary.** If $T$ has $L$ leaves and $L+b\le k^{1-\epsilon}$, **every prescribed connected order** works. In particular this holds with ordinary sums on all trees with at most $k^{1-\epsilon}$ leaves. For every composite $k$ some prescribed orders on unrestricted trees are impossible. [Explicit examples](../eight/growth-orders.md#a-prescribed-order-at-every-composite-modulus)

We prove a more local statement covering trees with arbitrarily many exceptional edges or high-degree vertices overall. All estimates below are uniform in the tree and offsets for fixed $D,\epsilon$. The external asymptotic input is the bounded-degree embedding lemma of Müyesser and Pokrovskiy. [Primary preprint, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

## A bijective rainbow base with sparse offsets

First let $T$ have exactly $k$ vertices with $E_D(T)+b\le k^{1-\eta}$ for fixed $0<\eta<1$. Subtracting the common offset permutes the edge palette, so take it to be zero. We construct a bijection to $G=\mathbb Z_k$ with $k-1$ distinct adjusted edge weights.

Cut all nonzero-offset edges. While a degree exceeds $D$, cut one more edge at that vertex. Each such extra cut decreases the remaining excess by at least one. There are $c\le E_D(T)+b$ cuts, called the main cuts. Mark their endpoints. If at least two original leaves are still unmarked, reserve two of them. Otherwise mark all original leaves and branching vertices and designate two distinct original leaves for use below. In this second case there are at most $2c+1$ leaves and at most that many branching vertices, by the degree sum. Both cases use $O(c+1)$ marks.

For each main cut choose a distinct ordinary edge as its private partner. Choose the private edges to form an induced matching whose endpoints are outside the closed neighborhoods of the current marks and reserved leaves in $T$. This is possible greedily. The sum of degrees of the original vertices of degree greater than $D$ is at most $(D+1)E_D(T)$. Hence the closed neighborhood of the initial exclusions has $O_D(c+E_D(T)+1)$ vertices and is incident with at most that many edges up to a factor depending on $D$. Each private choice has bounded-degree endpoints and the same bound applies after all $c$ choices. In particular only $o(k)$ of the $k-1$ edges need be excluded. Add the private endpoints to the marks and cut all private edges.

The result has $2c+1$ components. Away from the closed neighborhoods of all marks and reserved leaves select an independent set of $\Omega_D(k)$ sites in the original tree. Indeed only $o(k)$ vertices are excluded and every eligible vertex has original degree at most $D$. Sort the components in decreasing order of their numbers of sites, with the first called the principal component. Root the **original** tree anywhere in that component. Each nonprincipal component now has a unique entering cut with child $r$ in that component. Working down the sorted list, attach $r$ to a fresh site in an earlier component. For the $j$-th such attachment the first $j$ components have at least $j\Omega_D(k)/(2c+1)$ sites, while only $j-1$ have been used. The new graph $U$ is a tree of maximum degree at most $D+2$. Each component attaches to an earlier component once. Every newly used site and every cut endpoint is prescribed below.

Put an independent variable $X_v$ at each marked original vertex. Suppose a main cut $uv$ with child $v$ and offset $\delta$ is paired to a private cut $st$ with child $t$. At the site reconnecting $v$ prescribe $X_s+X_t-X_v$. At the site reconnecting $t$ prescribe $X_u+X_v+\delta-X_t$. The two new ordinary edge sums equal the two original adjusted weights in opposite order. Thus the entire weight multiset agrees for any assignment respecting the site prescriptions. The induced edge sums on all prescribed positions in $U$ are precisely the adjusted weights of the original edges between marked original vertices. Sites were independent and had no original neighbor among those marks.

**Distinct labels and weights.** Let $M=c+1$. There are $O(M)$ prescribed labels and $O(M)$ induced weights, the latter because the original marked subgraph is a forest. No two induced weights have the same unordered pair of variables. Assign the main variables in parent-before-child order of the original tree, then the private variables, then the two designated original leaves if present. Enforce inequalities between pairs of labels and between pairs of weights at the last surviving variable of each difference.

For labels, the coefficient vectors on a private pair $s,t$ that use either variable are $e_s,e_t,e_s+e_t,-e_t$. Each occurs once and its support is disjoint from the private variables of other pairs. Every comparison involving a site therefore retains a private variable. Each private variable occurs in only constantly many label expressions. Each designated leaf also occurs in constantly many expressions, since it is incident with at most one main cut. The remaining comparisons are between individual main labels. Consequently any variable decides at most $O(M)$ label comparisons.

For weights, each private variable occurs only in its own private edge among the marked original edges. Each designated leaf occurs in at most one edge. Comparisons involving any of these variables are therefore decided among them, with $O(M)$ tests per variable. Among the other edges a parent precedes its child, and a vertex is the child of at most one edge. Its turn decides at most $O(M)$ comparisons. A nonzero coefficient in any of these comparisons has absolute value at most two and excludes at most two residues. Thus greedy assignment has room at every step.

**Choosing the missing weight.** Put $S=\sum_{x\in G}x$ and let $P$ be all prescribed positions of $U$. With two reserved leaves, both remain unpinned leaves in $U$. After assigning the pins, choose $w$ so that
$$
       -w-\sum_{v\in P}(d_U(v)-1)x_v
       \quad\text{is divisible by}\quad
       g=\gcd(k,d_U(v)-1:v\notin P).
$$
Some unpinned vertex has degree between two and $D+2$, because $\sum_v(d_U(v)-1)=k-2$ and $|P|=o(k)$. Hence $g\le D+1$. The permitted class contains $k/g$ values and only $O(M)$ induced weights have to be avoided.

In the other case every unpinned vertex of $U$ has degree two. Define
$$
             w=-S-\sum_v(d_T(v)-2)X_v-\sum_e\delta_e .
$$
Only marked variables occur. Include $w$ versus each induced edge weight in the greedy assignment. Each of the two designated leaves has coefficient $+1$ in $w$. A single original edge omits at least one of them since $k>2$. The last surviving designated leaf has coefficient $+1$, so each comparison excludes just one value at its step. These $O(M)$ new tests are compatible with the preceding bounds, even when a branching coefficient in $w$ is large. For any completion of the labels, equality of the two full edge multisets gives $\sum_v(d_U(v)-2)x_v=\sum_v(d_T(v)-2)x_v+\sum_e\delta_e$. Both degree corrections are already determined by pinned labels.

In both cases the pins are injective and all induced weights are distinct and avoid $w$. The [partial-labeling theorem](partial-gap.md) now applies to $U$ with missing weight $w$. In the first case its two-leaf gcd condition holds by construction. In the second its non-degree-two positions are exhausted and its required moment is exactly the equation defining $w$. Its bounded-degree hypothesis holds for $D+2$, and $|P|=O_D(k^{1-\eta}+1)\le k^{1-\eta/2}$ for large $k$. The resulting bijection retains every pin. Restoring the original edges gives the required bijection and distinct adjusted weights on $T$.

## A whole growth order

A connected order starts at one vertex and adds one vertex adjacent to the previous prefix at every step. Number the positions starting at one. At position $mk+1$ with $m>0$, the previous prefix has uniform vertex counts and one deficient edge weight. Give this vertex the unique label producing that weight on its entering edge, including its given offset. At position one choose its label freely. The prefix now has uniform edge counts and one surplus vertex residue $u$.

Take the next $t\le k-1$ vertices up to the next block boundary or the end of the order. Their induced forest $F$ has $q$ components, with one edge to the old prefix from the root of each. Translate all old labels temporarily by $-u$. Join these roots to a dummy vertex, retaining internal offsets. On a dummy edge use the actual translated old parent label plus the original edge offset. Pad the resulting tree of order $t+1$ to order $k$ by extending a terminal vertex along an ordinary path. For $t=0$ no extension is required. For $t>0$ one may first subtract any common offset from all the original edges under consideration.

If $b_F$ is the number of internal edges of $F$ exceptional relative to that common offset, this auxiliary tree has at most $b_F+q$ exceptional edges. Its excess is at most $E_D(F)+2q$. Each root gains one incident edge, the dummy has degree $q$, and the padding from a rooted terminal creates no excess. Thus the base lemma applies whenever $E_D(F)+b_F+3q\le k^{1-\eta}$ for some fixed $\eta>0$ and all sufficiently large $k$. This **local condition on each block** suffices for the prescribed order. Translate the auxiliary bijection by minus its dummy label. The exterior labels are distinct and nonzero and its internal and entering weights are all distinct. Restoring $u$ adds $u$ to every new vertex label and the same constant to all new weights, accounting also for the common offset. Every initial segment of the block therefore adds distinct labels to low vertex bins and distinct weights to uniform edge bins. This proves cordiality throughout.

For size-ordered preorder, a block of $t$ vertices is an initial interval of the remaining preorder after its starting cut. The suffix components occur in groups according to their old parents, from deepest to shallowest. At a change of parent, each component of the next group has full order strictly larger than the entire previous mass. To see this, the child subtree on the route to the cut contains all earlier components and a visited vertex, and was visited before the new siblings. If the interval touches $a$ parent groups, the first $a-1$ are fully included. Their mass is at least $2^{a-1}-1$ by doubling, and at least one vertex of the final group is present. Hence $2^{a-1}\le t$, even when the final component is only partly traversed. There are at most $D(1+\log_2 t)+E_D(T)$ entering edges, by summing degrees at these distinct parents. This bounds $q$. In addition, $E_D(F)\le E_D(T)$ and $b_F\le b$. The local condition follows with $\eta=\epsilon/2$ for large $k$. [Lean proof of the interval bound](../rainbow/OrderedCut.lean)

In an arbitrary connected order, the component roots are incomparable in the tree rooted at the start. A descendant leaf from each gives $q\le L$ for any nonempty block. The identity $\sum_{d_v\ge3}(d_v-2)=L-2$ gives $E_D(F)\le L$ for trees of order at least two. The same local condition proves the prescribed-order corollary. A singleton is immediate.

## Reproduction

~~~sh
python3 -B research/bounded-degree/check_sparse_offsets.py
lean research/rainbow/OrderedCut.lean
~~~

The [constructor](sparse_offsets.py) builds the cuts, sites, pinned affine labels, missing weight and embedding core. The [independent checks](check_sparse_offsets.py) verify the changed-edge multisets, both embedding moments and degree-class conditions on 84 trees, including adjacent offset edges, adjacent high-degree vertices and paths with both end edges biased. They check 1,609,843 actual preorder intervals, all normalized offset choices on two four-vertex shapes at moduli 5 through 8, and 1,980 actual prefixes across several successive blocks. The asymptotic passage from a small embedding core to a full base bijection uses the primary embedding lemma above.
