# Every rooted tree has an integer certificate for adding leaves

**Theorem.** Let $H$ be any finite tree on $h$ vertices, with distinguished vertex $o$. Give $H$ the root $o$ and let $e=h-1-\deg(o)$. There are distinct integer vertex labels, with $x_o=0$, for which the endpoint sums use every vertex label exactly once except for one omitted label $s$. Their span is at most
$$
K=(2h+4)h2^e.
$$
Consequently, for every $k>K$, adjoining any number of leaves at $o$ gives a $k$-cordial tree. Also, adjoining at least $(h-1)K$ leaves at $o$ gives a tree cordial for **every** positive modulus. The labeling may depend on the modulus.

The proof below constructs the labels over the integers. No bound on degrees, depths, or numbers of branches is assumed.

## Finding the part to label last

Call a vertex with at least one child a support. A star rooted at its center admits the labels $0,1,\ldots,h-1$, omitting zero among the sums. Otherwise a hub neighbor is a support. If no vertex other than $o$ has two support children, such a neighbor has at most one support child, and the [anchor construction](branches.md) applies. Its initial magnitudes are at most $\deg(o)$, and each subsequent assignment at most doubles the maximum, including the delayed assignment of the anchor. There are $e$ such assignments, since the anchor replaces a child given its label initially. This gives span at most $2h2^e$.

In the remaining case choose a deepest vertex $P\ne o$ with at least two support children. From each support child follow the unique support child while there is one. The resulting chains end at supports whose children are all leaves.

- If some chain contains at least three supports, let $a,b,c$ be its last three, and choose one child $d$ of $c$. Retain the path $a,b,c,d$ as four distinguished sites. The rest of the subtrees at these sites consist of additional leaves at $a,b,c$. The parent of $a$ is the boundary vertex.
- Otherwise choose two chains. In each, use its first support and its support child if present, or its first support and any one of its leaf children if the chain has only one support. This gives arms $a,b$ and $c,d$ with common boundary $P$. All remaining descendants in the two arms are leaves attached directly to $a,b,c,d$.

Remove the four sites and their additional leaves temporarily. The boundary is a nonroot vertex in the remaining tree. All original neighbors of $o$ remain.

## Labeling the remaining tree

Label $o$ zero and its $D=\deg(o)$ neighbors $1,\ldots,D$. Put $Y=D+1$ and start a running integer at $Y$. Process every other remaining vertex in parent-before-child order. Give it the running integer, then increase the running integer by its parent's label. The assigned values strictly increase. Write $L$ for the final running integer and $p$ for the label of the boundary. All old labels are in $[0,L)$, with $0<p<L$ and $0<Y\le L$.

Writing $V$ for the old vertex multiset and $[x]$ for one occurrence of $x$, the old edge multiset is
$$
V-[0]-[Y]+[L].
$$
The hub edges give their neighbors' labels. Every other edge gives the next running integer, including the final one. The formula also holds when there are no such edges and $Y=L$. This running-sum device is used in Ellingham's positive construction. [Ellingham, *Sum graphs from trees*, Section 2](https://math.vanderbilt.edu/ellingmn/paper/sgft/sgft-final-2p.pdf)

## Restoring the four sites and their leaves

Use the following labels and ordinary edge sums. For the path, list edges in order from its boundary. For the two arms, list the two edges of each arm starting at the boundary.

| Shape | Labels on $a,b,c,d$ | Edge sums in order |
|---|---|---|
| Path, $b$ positive | $-p-L,\ L,\ -L,\ -p$ | $-L,\ -p,\ 0,\ -p-L$ |
| Path, $c$ positive | $-p-L,\ -L,\ L,\ -p-2L$ | $-L,\ -p-2L,\ 0,\ -p-L$ |
| Two arms | $-p-L,\ L,\ -p,\ -L$ | $-L,\ -p,\ 0,\ -p-L$ |

All four labels are distinct and outside $[0,L)$. Their edge sums are the four labels with $L$ replaced by zero. Adding these contributions leaves exactly the gap $Y$ in the vertex multiset, including when $Y=L$.

On the path, choose the row that puts $+L$ at whichever of $b,c$ has fewer additional leaves. In the two arms, order them to put $+L$ at the end with fewer additional leaves. If the ends tie, put $a$ at the intermediate site with more additional leaves. Ties left by these rules can be broken either way.

Reserve one pair for each leaf of the $+L$ site, matching it with a distinct leaf of the $-L$ site. Every other new leaf has a negative parent. If any unpaired leaf remains, at least one has a parent of magnitude at least $L$. Unequal end counts leave a leaf at $-L$. With equal counts on the path, remaining leaves are at $a$; with equal counts on the arms, the tie rule guarantees at least one remaining leaf at $a$. Its magnitude is $p+L$.

Start with gap $g=Y$. Process that leaf first if one exists, assigning it $g-x_{\rm parent}$. Its edge fills the gap and its own label is the new gap. The first such label exceeds $L$, and every subsequent unpaired label strictly increases. Finally for each reserved pair choose $T$ one greater than the current maximum and give the two leaves $T$ at parent $+L$ and $T+L$ at parent $-L$. Their sums exchange the two labels, preserving the gap. This completes the construction.

Originally $Y\le h$. There are at most $e$ updates before reaching $L$, each at most doubling the running integer, so $L\le h2^e$. The most negative of the four labels exceeds or equals $-3L$. Each unpaired step advances the gap by at most $2L$, and a reserved pair advances the maximum by $L+1\le 2L$. At most $h$ such steps give a final maximum at most $(2h+1)L$. The stated span bound follows.

## Cordiality and finite exceptions

For $k$ greater than the actual span, reduce the integer certificate modulo $k$. Let $A$ be its set of vertex residues. Give new leaves successive entries of the repeating list consisting of all residues outside $A$, then $s$, then all residues in $A\setminus\{s\}$. Each hub edge uses its leaf's label. The first block fills empty bins in both histograms; the entry $s$ completes the edge histogram. The last block raises the remaining vertex bins to two and uses distinct edge bins. Every prefix is balanced, and a full period adds one to every bin. This works also for $h=1$.

For any $k$ with $h+m>(h-1)k$, an independent construction puts all $h$ old labels at zero. Choose balanced final vertex counts totaling $h+m$ with zero a most frequent residue. Its count is at least $h$, so leaves can fill all remaining slots. The edge histogram is the vertex histogram with one zero removed, hence balanced. This proves the second assertion of the theorem, including all $k\le K$.

**Finitely many counterexamples at bounded nonleaf count.** Fix $b$. There are only finitely many pairs $(T,k)$ up to isomorphism for which $T$ has at most $b$ nonleaf vertices and fails to be $k$-cordial. The exceptions can be enumerated effectively. More generally, on any core of fixed order $b$, a sufficiently large *single* population of incident added leaves suffices for all moduli, regardless of the other populations.

Indeed, for each core and set of attachment sites the [selected-site threshold](marked-leaf-threshold.md) covers the region with every selected population sufficiently large whenever there are at least two sites. On each remaining slice fix one of the finitely many smaller counts, absorb it into the core and recurse. This leaves finitely many fixed trees and one-site families. On each one-site family only $k\le K$ and $m<(h-1)K$ can fail. A fixed tree likewise has finitely many exceptional moduli by the integer theorem with $m=0$. The nonleaf vertices of a tree, if nonempty, induce a tree, and all remaining vertices are attached leaves, except for the separate orders one and two. Taking the finite union proves the claim. This also shows that along any sequence of counterexamples with $k\to\infty$ the number of nonleaf vertices must tend to infinity.

**An explicit necessary condition at each vertex.** Fix any $o$ of a possible counterexample and remove its adjacent leaves. If $e$ edges were not incident to $o$, the remaining order is at most $2e+1$, since each surviving neighbor of $o$ has at least one edge below it. The theorem, with the removed leaves restored, forces $k\le(4e+6)(2e+1)2^e$. It also bounds the number of removed leaves by the one-site population threshold when the trimmed order is greater than one. Thus a counterexample cannot have all but a bounded number of its edges at a single vertex as $k$ grows.

## Reproduction

The independent arithmetic checks reconstruct edge sums from the original parent lists and compare multiplicities. They cover all 7,813 rooted trees through order twelve, 750 prescribed leaf-count profiles, 1,810 larger trees of orders up to 200, and modular leaf periods at consecutive moduli. The Lean file verifies the template equations, disjoint ranges and the two ways to extend the gap. The structural argument and the bounded-nonleaf corollary are proved above. [Construction](universal_hub.py) · [Direct verifier](check_universal_hub.py) · [Lean identities](UniversalHub.lean)

~~~sh
python3 -B -m research.hub.check_universal_hub
lean research/hub/UniversalHub.lean
~~~

The threshold depends on the core and grows with its order. Hovey's conjecture across arbitrary cores and moduli remains open.
