# Replacing a prescribed edge with a path and one side branch

**Theorem (computer-assisted).** For every $4\le k\le63$, take an arbitrary edge $ab$ of an arbitrarily labeled $k$-cordial tree. Replace it by a path with $c\ge3$ new internal vertices and attach a pendant path with $k-c\ge1$ new vertices at any of these internal vertices. The labeling of all old vertices extends. This holds at **every old tree order** and with the original endpoint labels fixed.

For all even moduli in the range, every vertex and edge count can increase by one. For every odd $k$, an incidence identity rules out those simultaneous uniform increments. Two other constructions preserve cordiality at the certified odd moduli. In particular, the [order bound at 27 labels](ring-order.md) drops from 351 to **243 vertices**.

Closing the main path of $c$ free vertices makes a cycle of length $c$ with one pendant path, also called a tadpole or dragon. Write $J$ for the unique degree-three vertex and $Y$ for the tip. The odd-order obstruction for harmonious tadpoles also appears in the harmonious labeling literature. The proof below applies directly to the opened graph with prescribed old labels. [Seoud and Youssef, *Families of harmonious and non-harmonious graphs* (1999), bibliographic record](https://research.asu.edu.eg/handle/123456789/179938)

## Opening an edge

Number the cycle positions $0,\ldots,c-1$ with the pendant path at 0. Open any edge $uv$, orienting the replacement so $a$ joins $u$ and $b$ joins $v$. When the new label at $v$ equals the old label at $a$, the entering edge $au$ reproduces the closed edge $vu$ and $vb$ reproduces the deleted old sum $ab$. Thus the net edge increments are exactly the closed graph's histogram. Either port can serve this role by reversal.

Let $S$ be the sum of all residues. If the new vertex labels are bijective, the sum of the net edge increments in $\mathbb Z_k$ is
$$
             2S+x_J-x_Y .
$$
Indeed the entering edges and deleted edge cancel the contributions of the two old labels. The added incidences count each free label twice except for one extra at $J$ and one fewer at $Y$. Uniform edge increments would give $x_Y-x_J=S$. At odd $k$ this forces two distinct vertices to share a label. This obstruction is independent of the opening or any choice of port labels.

At even $k$ the checker verifies a harmonious labeling of each closed graph, with one exception. Translate the vertex labeling so a port has the required value and open the graph as above. At $(k,c)=(6,3)$, direct witnesses instead cover every cut and every pair of old labels up to translation. These witnesses give the same uniform increments.

## When the old edge counts have two levels

Write $G$ for the all-ones histogram. Seek vertex permutations for which the closed edge counts are $G+e_D-e_F$. For an anchor port $v$ at label $z$, translate it to zero. The resulting directed arc on residues is
$$
                        D-2z\ \longrightarrow\ F-2z .
$$
Include every unit multiple of the arc. Given an old endpoint label $a$, translating the anchored labels by $a$ translates every arc by $2a$. Strong connectivity is invariant under this translation. If the old edge counts have two levels, choose a walk from a low bin to a high bin. At its first crossing the duplicate is at a low bin and the omission at a high bin. Adding this witness leaves the two counts balanced. All vertex bins increase by one. The verifier demands a strongly connected graph at one or both endpoints of **each** opening. [Lean proof of the cut crossing and the frequency update](WeightTransfer.lean)

The generator groups residues by their gcd with $k$. For a unit-invariant set of arcs the vertices reachable from zero are a union of full unit orbits, and the same is true in the reversed graph. It can therefore track reachability from zero using only the orbit graph. The independent verifier expands every unit multiple and tests both reachability conditions on the actual residues.

## When the old edge counts are uniform

The old tree then has order one modulo $k$. Translate its unique surplus vertex label to zero. For odd $k$, a closed-graph labeling with vertex counts $G-e_0+e_R$ for $R\ne0$ and edge counts $G$ gives the desired extension if an anchor can match an old endpoint. The old surplus moves from zero to $R$. Multiplication by units permits any nonzero endpoint in the anchor's unit orbit. The checker requires every nonzero residue to be available at **each** port, since the endpoint with a nonzero label may be prescribed.

To find these labelings, remove $Y$ and biject the remaining vertices with the nonzero residues while keeping the remaining $k-1$ edge sums distinct. If $P$ is the neighbor of $Y$, the missing weight is $x_P-x_J$. Indeed the retained vertex labels sum to zero, and their incidence sum is $x_J-x_P$, including the case $J=P$. Restoring the tip at $-x_J$ supplies precisely the missing weight and repeats a nonzero vertex label.

If both old endpoints carry zero, the missing vertex residue prevents anchoring by equality. For every cut the certificate instead gives actual nonzero free labels with counts $G-e_0+e_R$. The free edges and the two entering edges together have counts $G+e_0$. Deleting the old edge of weight zero leaves net edge increments $G$. This covers the remaining boundary.

## Verification

There are 1,830 cycle and path length pairs and 41,480 choices of cycle edge in the indicated range. The [generator](one_leaf_period.cpp) emits 77,845 witness rows of vertex labels. The [independent verifier](check_one_leaf_period.py) rebuilds the graph, checks each labeling and its boundary coverage, then opens every cut on two actual labeled trees, recomputing every vertex and edge bin. The 82,960 replays include star and path cores and coincident endpoint labels. The [SHA-256 manifest](one-leaf-period.sha256) identifies all sixty witness streams.

~~~bash
set -e
src="$PWD/research/census"
out=$(mktemp -d)
c++ -std=c++17 -O3 "$src/one_leaf_period.cpp" -o "$out/generate"
for k in {4..63}; do
  "$out/generate" "$k" > "$out/one-leaf-$k.txt"
done
(cd "$out" && shasum -a 256 -c "$src/one-leaf-period.sha256")
python3 -B "$src/check_one_leaf_period.py" "$out"/one-leaf-*.txt
lean "$src/WeightTransfer.lean"
~~~
