# Prescribing an edge-frequency change on a path with one side branch

**Theorem (computer-assisted).** Fix $7\le k\le54$. Replace an edge of any labeled tree by a path with $c\ge3$ new internal vertices, and attach a pendant path with $k-c\ge1$ more vertices at any of those internal vertices. Keep both old endpoint labels. Write $G$ for the vector of ones, $[w]$ for a unit in bin $w$, and $S=\sum_{x\in\mathbb Z_k}x$. For any $p,q\in\mathbb Z_k$ the new vertices can use every residue once with net edge increments
$$
                              G+[p]-[q]
$$
if and only if $p-q\ne S$. When $p=q$ the target is uniform. Thus odd moduli allow every nonzero one-bin transfer. Even moduli allow uniform increments and every transfer except between antipodal residues. The same criterion for all sufficiently large moduli follows from the [unicyclic frequency theorem](../bounded-degree/edge-histograms.md). The finite proof gives actual labelings and allows any old tree order.

## Opening and the eight-label case

Close the free main path to a cycle, giving a graph with a degree-three junction $J$ and tip $Y$. The sum of the net edge weights, including both entering edges and subtracting the deleted old edge, is $2S+x_J-x_Y$. Hence $p-q=S+x_J-x_Y$ and bijectivity forces the stated inequality on every opening.

Open a closed cycle edge $uv$ and attach $u,v$ respectively to old labels $a,b$. If $x_v=a$, the first entering weight replaces the closed weight, and the second replaces the old weight. The roles reverse when $x_u=b$. At $k=7$ and $10\le k\le54$ the certificates realize every allowed histogram with **any regular cycle vertex** fixed. Translate to put its label at zero, multiply by any unit and reflect the cycle about the junction. Translating back to the specified old label shifts both target bins by twice that label. Each cycle edge has a regular endpoint.

At eight and nine labels we also test the openings themselves. Normalize $a=0$ by translating old and free labels together. First enumerate closed labelings up to translation and try both anchors. Whenever that leaves a target uncovered, enumerate all permutations on the open graph and count its actual increments. For example, at $k=8$, take the five-cycle $0,1,2,3,4$ with the side path $0,5,6,7$ (these numbers index vertices). Open edge $2,3$ between old endpoints both labeled zero. The free labels in index order
$$
                         (0,1,7,2,4,5,3,6)
$$
give net frequencies $(1,2,1,0,1,1,1,1)$. Neither port can be fixed at zero in a closed witness for this target. Direct opening realizes it.

| $k$ | Missing targets at regular closed anchors | Opening inputs requiring direct tests | Impossible opening inputs | Total normalized opening inputs |
|---:|---:|---:|---:|---:|
| 4 | 8 | 48 | 40 | 108 |
| 5 | 44 | 160 | 112 | 700 |
| 6 | 44 | 270 | 102 | 1,800 |
| 7 | 0 | 0 | 0 | 5,292 |
| 8 | 16 | 16 | 0 | 9,800 |
| 9 | 2 | 0 | 0 | 21,384 |

The failures in this table concern a fixed opening, fixed old labels, and a prescribed frequency change. For example at four labels the triangle with a one-edge tail, cut from vertex zero to vertex one with both old endpoints zero, cannot duplicate zero and omit one. Ordinary cordial extensions at these small moduli are covered by the [one-leaf period theorem](one-leaf-period.md).

## Exact total changes using several replacements

Take $t\ge1$ pieces of the stated kind at prescribed edges. They can also be inserted successively, since the construction accepts any old labels. Require each to contribute one of the single-transfer histograms in the theorem. Prescribe their total increment as $tG+D$ where $D$ is an integer vector of sum zero. Let $P_x=(D_x)_+$, $B_x=(-D_x)_+$ and $h=\sum_x P_x$.

* For odd $k$ the exact test is $h\le t$, excluding $h=0,t=1$.
* For even $k$ the exact test is $h\le t$ and $B_x+P_{x+S}\le t$ for every $x$.

Indeed, a transfer draws one unit from its source and adds it to its target. At odd $k$ match the $h$ units of demand with the $h$ units of supply. Their supports are disjoint. Each arrow can be replaced by two through a third residue to increase the length by one. For zero demand begin with a two-arrow round trip, which can be lengthened in the same way.

At even $k$ take a maximum matching between units of supply and demand excluding the antipodal pairs. A set of supply units at two or more distinct residues sees the entire demand side. A set at residue $x$ sees $h-P_{x+S}$ demand units. By Hall's deficiency formula the number left unmatched on each side is $m=\max(0,\max_x(B_x+P_{x+S}-h))$. Match the remaining units arbitrarily and replace each forbidden arrow by two through a third residue. This uses at most $h+m$ pieces. Uniform pieces fill any spare positions. Conversely the gross supply at $x$ and gross arrivals at $x+S$ require disjoint pieces, since no single piece may do both. Hence $h+m$ is the exact minimum.

In particular two such pieces always permit uniform total increments, including at odd $k$. If some pieces are bare paths of $k$ internal vertices, their closed cycles permit exactly the one-bin differences $S$, by the [cycle construction](cycle-subdivision.md#an-even-hamilton-cycle-with-prescribed-repeated-weight). Uniform total increments with a bijection on each piece are possible for all bare pieces exactly when $tS=0$, for exactly one branched piece exactly when $tS\ne0$, and with two or more branched pieces in every case. The necessity follows by summing the individual differences even if the individual histograms are unrestricted. For sufficiency select allowed differences of sum zero and use each partial sum as the next target bin, so the transfers cancel. [Full telescoping argument](../bounded-degree/edge-histograms.md#several-edge-replacements-with-exactly-uniform-total-increments)

## Verification

The 46 [hashed witness streams](one-leaf-spectrum.sha256) contain 216,132 permutations. A [separate verifier](check_one_leaf_spectrum.py) recomputes all vertex labels and closed edge bins, then expands the symmetries and tests all 43,218,496 normalized regular-anchor targets. Together with the direct checks at eight and nine this covers 2,057,388,000 normalized opening targets from seven through 54. A separate enumeration compared the routing formulas above with sums of actual allowed steps in 159,254 cases.

~~~bash
set -eu
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/one_leaf_period.cpp" -o "$out/generate"
for k in 7 {10..54}; do
  "$out/generate" "$k" --spectrum > "$out/period-spectrum-$k.txt"
  python3 -B "$src/check_one_leaf_spectrum.py" --modulus "$k" --stream "$out/period-spectrum-$k.txt"
done
(cd "$out" && shasum -a 256 -c "$src/one-leaf-spectrum.sha256")
python3 -B "$src/check_one_leaf_spectrum.py" --failures "$out/small.txt"
echo "fd24d40ff96873b4c62ac37e0adb8ffdbbbc320cb09621bdead510b948ac9ecb  $out/small.txt" | shasum -a 256 -c -
python3 -B "$src/check_one_leaf_spectrum.py" --routing
~~~
