# Prescribed connected orders at 27 labels

**Theorem (computer-assisted).** For every tree with at most six leaves, and for every prescribed vertex order with connected prefixes, there is one 27-cordial labeling on every prefix in that order. This also holds for a tree with seven leaves if the order starts at a leaf.

More generally, start with any fixed 27-cordial labeling on a nonempty core of order zero or one modulo 27. Attach a forest with at most six rooted tips **at any old vertices**. Every prescribed parent-first order admits an extension cordial throughout that order. The entering edges may carry arbitrary independent additive offsets. There is no bound on the order of the core or the forest.

## An exact finite test for the fixed-core property

For general $k\ge2$, consider every rooted forest on $k-1$ vertices with at most $q$ tips. Assign any residue to the old parent of each component, independently. Require distinct nonzero vertex labels and distinct new edge sums, counting every entering edge. This finite test is necessary and sufficient for the fixed-core, prescribed-order conclusion with $q$ tips at modulus $k$.

For necessity take a star on $k+1$ vertices, with center zero and the leaves carrying all $k$ residues once. Attach each root at a leaf of its prescribed color. The starting surplus is zero and its edge counts are uniform. Cordiality after the last of the $k-1$ additions forces exactly the required labeling.

For sufficiency, from a divisible-order prefix the next vertex has a unique label that fills the deficient edge weight. It creates one surplus vertex residue $h$. From a prefix of order one modulo $k$, take the next $k-1$ vertices of the prescribed order, or all that remain. The edges they induce form a rooted forest with an edge from each root to an earlier parent. Its tips are incomparable under ancestry. A path from one batch vertex to any descendant in the same batch is entirely within the batch. Consequently distinct tips extend to distinct tips of the original attached forest. The test applies after translating $h$ to zero. Pad a short batch by lengthening a tip, then restrict. Distinct labels avoiding $h$ and distinct weights preserve both histograms on every intermediate prefix. Repeat from divisible order. From a singleton core, rooting at a leaf reduces the rooted tip count by one when the tree has at least two vertices. [Earlier prescribed-block construction](../near-matching.md#every-connected-prefix)

The proof only needs each non-forced batch to have at most $q$ tips. The entire tree may have more. Each edge whose parent lies in an earlier batch can carry its own prescribed offset, since that offset adds to its effective parent color. In particular an arbitrary assignment of offsets on the edges incident to the first vertex works under the stated leaf bounds.

## Exhausting the independent boundary colors at 27

A partition count gives **2,831,426** forests on 26 vertices with at most five tips and **9,191,299,338** literal parent-color assignments. The following cases cover them.

* A single component passes the [seven-tip test](seven-tip-27.md). With two unequal orders every color pair is ordered. The equal split is covered by the [independent two-root certificate](two-rooted-trees.md#the-first-block).
* When every component has one tip, the forest consists of paths. The [independent path certificates](../census/ring-order.md#terminal-paths-with-independently-prescribed-parents) cover up to six components.
* Write the component orders as $s_1\le\cdots\le s_j$. If $s_i\ge s_1+\cdots+s_{i-1}+i-1$ for every $i$, every assignment satisfies the sharp ordered-cut test. The seven-tip certificate again suffices.
* The remaining profiles have three or four components and at least one fork. The new streams use a separate input color for every component, including equal-sized or identical components.

| Total tips | Supplementary profiles | Forests | Witness rows | Literal assignments |
|---:|---:|---:|---:|---:|
| 4 | 61 | 1,431 | 264,411 | 28,166,373 |
| 5 | 459 | 39,094 | 14,479,676 | 3,946,480,866 |

The [four-tip](independent-four-tips-27.sha256) and [five-tip](independent-five-tips-27.sha256) manifests include a SHA-256 digest for each uncompressed stream. A partition recurrence checks the full supplementary profile set and its counts. The native verifier checks each canonical topology and every emitted permutation. It reconstructs all entering colors that give unused, pairwise distinct weights, and checks coverage under multiplication by units modulo 27.

## Marked leaves and a consequence at 54 labels

Let $Q$ have at most five leaves and $S$ vertices, and put $r=1+((S-1)\bmod27)$. Any specified set of at most $r$ leaves can simultaneously have **distinct most-frequent labels**. Place the marks last in a connected order. Each of the earlier full blocks uses every residue once, and the final block has $r$ distinct vertex labels. With six leaves the same statement holds for at most five marks, since an unmarked leaf can start the order. The one- and two-vertex cases allow either available order directly.

Now let $T$ have at most six leaves, maximum matching size $\nu$, deficiency $d=|T|-2\nu$ and $S=|T|-\nu$. Then $T$ is **54-cordial whenever $d\le1+((S-1)\bmod27)$**. In particular this covers every such tree whose order is outside the residues $-3,-2,-1,0,1,2,3$ modulo 54.

For a nonsingleton, root at a leaf and retain one child edge at each nonterminal vertex. The resulting disjoint paths end at distinct rooted tips, at most five in total. Matching along each path proves $d\le5$. Move all exposed vertices to leaves by alternating-path exchanges. Add a mate to each exposed leaf and contract the resulting perfect matching. Extending terminal paths and contracting edges leaves at most six leaves in the quotient. The $d$ extra pairs are marked pendant quotient vertices, so the preceding result puts them in distinct most-frequent bins. Lift the quotient labeling and delete the added mates by the [matching construction](../near-matching.md#completing-and-lifting-a-maximum-matching). This proves the criterion. If $d>r$, then $|T|=2S-d\equiv 2r-d\pmod {54}$, with $1\le r<d\le5$, giving the stated residue restriction. The restriction describes the reach of this construction.

## Six tips and seven-leaf lifts

The additional independent-boundary census at six tips is complete. Altogether the finite test covers **23,665,913** rooted forests of order 26 with at most six tips and **333,471,617,685** literal boundary assignments. The earlier cases above handle up to five tips. With exactly six tips, a single component, two components, all-path forests, and profiles admitting every ordered change already have certificates. The remaining profiles have three, four or five components.

| Components | Additional profiles | Forests | Witness rows | Literal assignments |
|---:|---:|---:|---:|---:|
| 3 | 173 | 401,597 | 74,157,119 | 7,904,633,751 |
| 4 | 677 | 119,061 | 161,143,209 | 63,273,896,901 |
| 5 | 609 | 8,351 | 67,535,362 | 119,827,722,357 |

The [1,459 profiles](independent-six-tips-27.sha256) exhaust the supplementary partition list. The verifier checks all 302,835,690 rows on their actual forests and expands the permissible entering colors, including independent colors on identical components. The block proof above now gives the prescribed-order theorem through six rooted tips at all orders. A tree with seven leaves has six rooted tips when started at a leaf.

The same matching argument gives **54-cordiality for every tree with at most seven leaves whenever $d\le1+((S-1)\bmod27)$**, with $d=|T|-2\nu$ and $S=|T|-\nu$ as above. In particular it suffices that the order lie outside $-4,-3,\ldots,4$ modulo 54. Rooting at a leaf gives a covering by at most six disjoint paths, hence $d\le6$. The quotient has at most seven leaves. If it has seven, at most six are marked, so an unmarked leaf can start the prescribed order. Otherwise every order works. The exposed pairs can therefore occupy the last $d$ positions in distinct most-frequent residues whenever $d$ fits in the final block. When it does not fit, $2r-d$ ranges from $-4$ to $4$.

There is also a condition independent of the number of leaves. At 27 labels every depth-first preorder works if the **five shortest terminal arms have total length at least 25**. Indeed, a 26-vertex batch with at least seven tips would contain five complete intermediate arms and two other tip vertices, requiring at least 27 vertices. All batches therefore have at most six tips. With fewer than five leaves every connected order already works. [Preorder interval bound](terminal-arm-orders.md#what-a-preorder-interval-contains)

A fresh build reproduced 90 supplementary stream hashes, covering 740 forests, 407,403 rows and 459,794,880 literal assignments. Separate whole-tree checks reconstructed 255 joins at specified boundary colors and recounted 6,630 prefixes. They also checked 630 prescribed growth orders and 14,706 prefixes on larger trees and 479 actual 54-label lifts, including a seven-arm tree of deficiency six.

## Independent checks and reproduction

The [Python checker](check_prescribed_forest_order.py) enumerates the required profiles by partitions. On three branching forests it expands units and spare edge weights to test all 570,807 literal boundary inputs. It builds 201 of the corresponding whole trees and recounts 5,226 prefixes. For each sample it also rejects a stream generated only for ordered boundary changes. On larger trees it replays 525 prescribed growth orders and 11,991 prefixes, including offsets on edges crossing batches. Finally it counts both original histograms modulo 54 on 403 trees with matching deficiencies zero through five.

Run from the repository root in Bash. The exhaustive native replay stores only per-profile receipts.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
c++ -O3 -std=c++17 -fPIC -shared "$r/leaf_search.cpp" "$out/ref.o" -o "$out/search.so"
for h in four five six; do
  file="$r/independent-$h-tips-27.sha256"
  awk -F '  ' '{print $3}' "$file" > "$out/$h.profiles"
  python3 -B research/census/stream_leaf_profiles.py 27 "$out/$h.profiles" "$out/generate" "$out/verify" "$out/$h" --independent-roots --workers 2
  cmp "$file" "$out/$h/manifest.txt"
done
python3 -B -m research.rainbow.check_prescribed_forest_order "$r"/independent-{four,five}-tips-27.sha256 --samples "$out/generate" "$out/verify" --growth "$out/search.so"
python3 -B -m research.rainbow.check_prescribed_forest_order "$r"/independent-{four,five,six}-tips-27.sha256 --tips 6 --samples "$out/generate" "$out/verify" --growth "$out/search.so"
~~~

The exhaustive tests and the block proof give the six-tip theorem for all orders. Ordinary 27-cordiality for unrestricted trees remains open.
