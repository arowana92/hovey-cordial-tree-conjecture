# Polynomial span at a prescribed zero vertex

**Theorem.** For every rooted tree of order $h$, there are distinct integer vertex labels, zero at its root, whose ordinary endpoint sums use every vertex label exactly once except for one omitted label. Their span is at most
$$
P(h)=2^{20}(h+1)^{435}.
$$
The omitted label can lie inside the span. The theorem bounds the size of the integer labels even when both height and branching are unrestricted.

**Consequences.** At every modulus $k>P(h)$ any number of leaves may be added at the root. At every modulus simultaneously, $13000P(h)$ or more additional leaves suffice, allowing the labeling to depend on $k$. At all sufficiently large $k$, any tree with all but at most $k^{1/436}$ of its leaves adjacent to one vertex is $k$-cordial, with no restriction on total order. The exponent is absolute.

## A small labeled subtree with a shallow remainder

Write $[t]$ for one occurrence of $t$, and $V,E$ for the vertex and edge multisets. At height at most twelve, use the breadth-first integer construction of [the bounded-height bound](exceptional-moduli.md#all-moduli-at-bounded-branching-depth), with span at most $8(h+1)^{16}$. Assume greater height from now on.

Choose a deepest leaf and the ancestor eight edges above it. Within this descendant subtree look for a deepest fork with at least two children that are themselves parents. Below each such child the parents form a chain with only additional leaf children. If a chain contains three parents, take its last three $a,b,c$ and one leaf $d$ below $c$. If there is no fork, use the corresponding three parents on the path to the chosen deepest leaf. Otherwise, when all fork chains have at most two parents, take two arms $a,b$ and $c,d$ as in the [four-site construction](universal-hub.md#finding-the-part-to-label-last). Set aside these four sites together with their additional leaf children. The remaining tree $H'$ has a nonroot boundary vertex $w$ for the selected path or arms. Its descendant height is at most eight.

In $H'$ remove 432 simultaneous layers of nonroot leaves, stopping if only the root remains. Write $C$ for the residual tree and $u$ for its number of nonroot terminals. Each of these terminals has a separate downward path of 432 removed vertices. A nonroot vertex survives precisely when its original descendant height was at least 432. In $C$, mark the root and vertices of undirected degree different from two. Compress each segment between marks to a positive length congruent modulo twelve, retaining the first edge out of the root and then compressing any remaining portion to length at most twelve. There are at most $2u$ segments, each now of length at most thirteen. Include the first three vertices on each supplied downward path. The resulting tree has at most $29u$ edges. When $u=0$, use just the root.

Label the root zero and each other vertex $2h'+i$, where $h'=|H'|$ and $i$ is its positive breadth-first rank. For a nonroot parent the edge into a child of label $s$ has sum $t$ above every label. All these sums are distinct, since the child ranks increase and the parent ranks do not decrease. An edge with parent zero already has sum $s$. We will cancel each error $[t]-[s]$ using a block of fourteen consecutive new vertices.

Below a parent of label $p$, use the following seven arrivals to transfer $s$ to $t$:
$$
t,\ -p-2t,\ p+t,\ s+t,\ -t,\ -p-t,\ p+s+2t .
$$
The change to $E-V$ is $[s]-[t]$ by addition along the seven edges. Use this path twice, from $s$ to $z$ and from $z$ to $t$. The two constant arrivals are $t,-t$. Reserve all such values across all jobs. Among the other twelve arrivals the intercepts grouped by coefficient of $z$ are as follows. [Lean check of the seven-edge identity](../large-order/GapPath.lean)

| Coefficient | Intercepts |
|---|---|
| $1$ | $0,p,s,t$ |
| $-2$ | $-p,-p-s-2t,-p-s-t$ |
| $-1$ | $0,-p$ |
| $2$ | $p+s,p+s+t$ |
| $3$ | $p+s+2t$ |

Use slots after the first three vertices on each supplied path, leaving at least ten unused vertices at its end. Each path supplies 29 slots. For the first slot on each path use the error from the edge ending at the second of its three initially labeled sites. Thus $p$ is the third label, different from $0,s,t$. Later $p$ is fresh and outside all original labels and reserved targets. In all cases $s,t$ are positive and distinct. The intercepts within each row are therefore distinct. Each moving arrival rules out at most one integer $z$ per occupied or reserved value, fewer than or equal to $3h'$ such values altogether. Each pair of different slopes rules out at most one further $z$. With $W=100(h'+1)$, choose $z$ among the $W$ integers immediately above $\lfloor-(p+s+2t)/3\rfloor$. At most $36h'+91<W$ are excluded. Both constant arrivals are fresh because all targets were originally reserved and their positive magnitudes were distinct. The last arrival $p+s+3z+2t$ has absolute value at most $3W$. Each first parent has magnitude at most $3h'$, so this bounds the parent of every block. Substitution in the table bounds every arrival in magnitude by $4096(h'+1)$.

Restore the compressed lengths using the [twelve-vertex subdivision](long-branches.md#a-short-core-with-arbitrarily-elongated-edges). Each edge to be expanded has endpoints $p,q$ among the original positive labels. Take the two parameters $j,4j$, with $1\le j\le W$. In the [twelve rows](../large_order_subdivision.py) all parameter slopes are nonzero. Different parameter coefficient pairs give different slopes, since their differences have entries of magnitude at most two. Equal slopes have constant differences among $\pm p,\pm q,\pm(p+q)$, all nonzero. At most $12h'+66<W$ choices collide with occupied labels or one another. Repeat inside the edge with endpoints $j,4j$ for each further subdivision. Thus all endpoints used as parameters are bounded by $4W$ and all new labels by $4096(h'+1)$. Each insertion adds the same multiset to $E$ and $V$. The subtree now contains $C$, is closed under taking ancestors in $H'$, and has distinct labels with $E=V-[0]$. Every nonroot vertex in it has descendant height at least ten in $H'$. In particular the boundary $w$ is still unlabeled. The remaining vertices are within 432 downward edges of the labeled subtree.

## Completing the integer labels

Let $B=4096(h+1)$. For every unlabeled vertex just below the seed, form a jump equal to its parent's label. Negate the entire seed if the sum $S$ of the jumps is negative. Arrange the jumps in nondecreasing order and walk from zero with these steps. Whenever a position repeats in the current path, excise the resulting simple cycle, preserving its assigned steps. The remaining path is simple and ends at $S$. If $S=0$, it is empty. If $S>0$, its endpoint exceeds all earlier positions, since all nonpositive jumps occurred first and zero steps produce separate cycles.

Assign to each first-layer vertex the tail of its step, translating all steps of each cycle or of the residual path by a common integer for that piece. Its edge sum is the translated head. Place the cycles above $B$ in successive disjoint integer intervals. Finally translate the path by $Y$ so its minimum position is one above the preceding intervals. For an empty path choose $Y$ one above them. All assigned labels are distinct and positive. The terminal $L_1=Y+S$ exceeds every label, and the change in $E-V$ is $[L_1]-[Y]$. The sum of the unshifted spans of all the pieces is at most the sum of absolute jump sizes, at most $hB$. There are at most $h+1$ pieces, so both $Y,L_1\le8(h+1)(B+1)$.

For each subsequent level give each vertex the running label $L$, starting at $L_1$, then add its positive parent label to $L$. Each level multiplies the running bound by at most $h+1$. After at most 431 further levels the histograms satisfy
$$
E=V-[0]-[Y]+[L],\qquad B<p<L,\qquad Y\le L ,
$$
where $p$ is the boundary's label. All negative old labels have magnitude at most $B$, and $L$ is strictly greater than every old label.

Restore the four sites with the following labels in order. For the path put $+L$ at the site with fewer extra leaves among $b,c$. For the two arms put it at the end with fewer leaves, breaking a tie by giving $a$ the larger intermediate leaf count.

| Shape | Four vertex labels |
|---|---|
| Path, $b$ positive | $-p-L,L,-L,-p$ |
| Path, $c$ positive | $-p-L,-L,L,-p-2L$ |
| Two arms | $-p-L,L,-p,-L$ |

These labels are distinct and fresh, since $p>B$. Their sums replace $L$ by zero, leaving gap $Y$. Pair every remaining leaf at $+L$ with one at $-L$. All unpaired leaves have negative parents. If any remain, one parent has label at most $-L$, by the choice of the positive site and tie order. Process the most negative first. Give each leaf the current gap minus its parent, so the first label exceeds $L$ and subsequent labels strictly increase. At paired leaves use $T,T+L$ with $T$ one above the current maximum. Their sums exchange the labels. This proves the required histogram identity. The final span is at most $(3h+5)L$. Using the bound on $L_1$ and the number of levels gives the stated $P(h)$. [Four-site identities in Lean](UniversalHub.lean)

## Consequences for cordiality

For $k$ above the actual span, reduce modulo $k$, writing $A$ for the set of vertex residues and $g$ for the omitted weight. Periodically give added leaves all residues outside $A$, then $g$, then all residues in $A$ except $g$. Each prefix balances both histograms. For $k\le P(h)$ use the [one-site degree theorem](../large-order/gap-path.md), since $13000P(h)\ge13000k$. This gives the two uniform leaf-population claims.

Let $H$ now have $a$ nonroot terminals and any additional leaves at its root. The singleton is immediate. Compress its segments between the root, branches and terminals to their original length when at most fourteen, and otherwise to their congruent length in $[3,14]$ modulo twelve. The resulting order is at most $28a+1$. When $a\le k^{1/436}$, the polynomial span is at most $2^{20}(28a+2)^{435}=o(k)$ uniformly as $k$ tends to infinity. For original order $h<k/20$, restore the compressed portions by the injective modular subdivision lemma, since $k>12h+132$ for large $k$. Each segment to be expanded has at least three edges with at most one zero sum and with only the root possibly a zero endpoint, at its upper end. There is an edge eligible for the lemma. At orders $k/20\le h\le k$ the established positive-density theorem applies with $\epsilon=1/2$. For $h>k$ use the preceding prefix induction, since each prefix has at most $a$ nonroot terminals. This proves the assertion at every tree order, including $k$ and $k+1$. [Subdivision, positive-density theorem and induction](long-branches.md) · [Müyesser and Pokrovskiy, primary embedding results](https://arxiv.org/html/2509.05280v2#S3.SS1)

There is also a sharper bound in the [exceptional-moduli argument](exceptional-moduli.md). In each of the $O(a+1)$ compressed prefixes, multiply the $O((a+1)^2)$ nonzero absolute vertex-label differences from this theorem. Each difference has logarithm $O(\log(2+a))$. The resulting product $N_H$ has $\log N_H=O((a+1)^3\log(2+a))$. If $k$ does not divide this product, all the prefix labelings stay injective. The same prime-counting argument therefore supplies a prime $p=O((a+1)^3\log(2+a))$ all of whose positive multiples work for every leaf population.

## Reproduction

Run from the repository root. The checker recomputes ordinary edge sums from the original parents, checks distinctness, and audits the partly labeled subtree separately. It covers every rooted shape through order eleven, all three deep fringe choices, a 5,680-vertex host, 75 further random trees, 3,906 signed jump lists and every prefix of two periods at eight consecutive moduli. These finite checks exercise the construction. The arguments above establish the bounds for unbounded order. [Constructor](polynomial_hub.py) · [Independent edge and histogram checks](check_polynomial_hub.py)

~~~sh
python3 -B -m research.hub.check_polynomial_hub
~~~
