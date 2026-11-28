# Two attachment vertices and one prescribed edge offset modulo 27

**Theorem (computer-assisted).** Let a tree have at most six leaves. At every order, one can prescribe an additive offset on any one edge modulo 27 and choose a single labeling and a connected vertex order such that every prefix is cordial, counting the offset whenever the edge is present. All other edges use the ordinary endpoint sum.

## A certificate on 27 vertices

Fix an order-27 tree in this class and two vertices $v,w$, possibly equal. In a bijective labeling $f$ with distinct edge sums, let $h$ be the missing sum. Put $c=f(v)+f(w)-h$. Every such pair has at least one of the following properties.

* Some labeling gives $c=0$.
* For every nonzero residue $d$, some labeling gives $c=d$.

When $vw$ is an edge, $f(v)+f(w)$ occurs, so only the second alternative is possible. Given a nonzero offset $b$ at that edge, choose $c=-b$. Its adjusted weight becomes $h$, different from every other weight. For offset zero take any certified row. Padding a smaller tree by extending a leaf with a path preserves its leaf count and the marked edge. Restricting gives distinct labels and weights on the original tree. Every connected prefix of such a labeling is cordial.

| Leaves | Unrooted trees | Bijective witness rows |
| ---: | ---: | ---: |
| 2 | 1 | 37 |
| 3 | 56 | 2,123 |
| 4 | 2,013 | 76,530 |
| 5 | 35,271 | 1,338,905 |
| 6 | 359,304 | 13,637,910 |
| Total | 396,645 | 15,055,505 |

There are 378 unordered port pairs per tree, counting coincident ports. The [100-shard manifest](period-ports-six.sha256) covers 149,931,810 choices of tree and port pair. Its columns give leaf count, tree and row counts, first and last tree words, and SHA-256 of the binary witness stream. The [generator](../rainbow/common_site_generate.cpp) records ordinary bijections until the coefficient zero or all three nonzero unit orbits have appeared at each pair. The [verifier](../rainbow/common_site_verify.cpp) reparses each tree, checks all labels and endpoint sums, and explicitly expands the unit multiples of each coefficient. It requires canonical ordering of the branches, a centroid root, the specified leaf count and strictly increasing tree words. The [census checker](period_port_census.py) checks disjoint shard ranges and independently counts the required trees. An odd-order tree has a unique centroid. At order 27 its branches form a multiset of rooted trees of orders at most 13 and total order 26. Multiplying their multiset generating functions by order and tip count gives the counts above.

## Keeping the marked edge during growth

More generally let $k\ge2$. Suppose the one-edge rainbow assertion holds at order $k$ for trees with at most $L$ leaves, and the ordered-cut forest extension holds through $k-1$ vertices for forests with at most $L-1$ rooted tips. Then the one-edge prefix assertion holds at every order for these trees.

For $n>k$ write $n=mk+1+t$ with $0\le t<k$. If $t=0$, delete a leaf other than a marked endpoint. Such a leaf exists since a tree on at least three vertices has two leaves and an edge meets at most one of them. Label the smaller tree inductively, then append the leaf with the label that fills the unique deficient edge bin. Its vertex bins had equal counts.

If $t>0$, delete the marked edge temporarily. Choose an original leaf on its smaller side (either side in a tie), and root the original tree there. Such a leaf exists even when that side is a singleton. The subtree beyond the mark has size at least $\lceil n/2\rceil>t$, since $n\ge k+1+t$ and $t<k$. Visit child subtrees in nondecreasing size in depth-first preorder. The far endpoint and all its descendants form a contiguous segment, so its first vertex occurs by position $n-t$. The first $n-t$ vertices contain both marked endpoints. The remaining $t$ vertices are an ordered-cut forest whose tips are original leaves other than the root. The smaller connected core has at most $L$ leaves, so induction supplies a prefix labeling with the specified offset. Its edge bins are now uniform and its vertex bins have a unique surplus. The forest certificate at those actual boundary colors extends the labeling in parent-first order. Every prefix remains cordial. The [ordered-cut inequalities](../rainbow/ordered-cut.md) and the [seven-tip forest theorem at 27](../rainbow/seven-tip-27.md) supply the extension used here.

## Ordinary trees obtained by inserting pieces

* In a core of **any order with at most six leaves**, replace one edge by any chain of trees of positive orders divisible by 27. Each inserted tree may have arbitrary ports and branching, provided it admits an ordinary 27-cordial labeling. The successive pieces have a total effective offset. Prescribe that offset on the core edge, then expand it. Each inserted period adds one to every vertex and edge bin. [Expansion identity](period-chains.md)
* In a core of **at most 27 vertices with any number of leaves**, replace any number of edges with chains of order-27 trees from the certificate. All of these expanded trees are 27-cordial. Start with a rainbow labeling of the core, available from the [integer census](../census/README.md). If all pieces of a chain can give zero, retain its original weight. Otherwise at least one piece gives all 26 nonzero offsets. Fix the others, leaving at least 26 possible total offsets for that chain. Assign the remaining chains distinct final weights in turn. At each step at most 25 weights are already in use. [Small-core insertion lemma](period-edges.md)
* In particular, suppose a tree on **53 or 54 vertices** has a connected 27-vertex piece incident to exactly two outside edges. The entire tree is 27-cordial if the piece has at most six leaves, or if suppressing it to one edge leaves a tree with at most six leaves. For the second case the piece itself has an ordinary rainbow labeling by the integer census. At 80 or 81 vertices two disjoint certified 27-vertex pieces, each incident to two outside edges, suffice. Adjacent pieces form one chain on suppression.

## Reproduction

Run from the repository root in Bash. Each shard is generated, verified independently and hashed. Only the short receipts need to persist.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/gen"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/check"
python3 -B -m research.biased.period_port_census 2 3 4 5 6 --run "$out/six" \
    --generator "$out/gen" --verifier "$out/check" --workers 2
cmp "$out/six/manifest.txt" research/biased/period-ports-six.sha256
python3 -B -m research.biased.period_port_census 2 3 4 5 6 --sample 1 | "$out/gen" --ports > "$out/examples"
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -shared "$r/leaf_search.cpp" "$out/ref.o" -o "$out/search.so"
python3 -B -m research.biased.check_period_ports "$out/examples" --growth-library "$out/search.so"
~~~

The [whole-tree checker](check_period_ports.py) built and recounted 96,390 ordinary trees of orders 53 and 54, including every port pair in the sampled shapes. It also checked all 3,510 single-edge adjustments in those shapes and 11,620 actual connected prefixes on 180 adjusted trees of orders 28 through 109. The all-orders statements follow from the finite certificate and the growth and insertion proofs.
