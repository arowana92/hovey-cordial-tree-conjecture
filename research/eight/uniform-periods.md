# Exact uniform increments at eight labels

**Theorem (computer-assisted).** Attach a rooted forest of $8q$ new vertices to any old tree, with each component root joined by one edge to any specified old vertex. Keep every old label. If $q\ge2$ and the forest has at most **eight rooted tips**, every vertex and edge residue can gain exactly $q$ occurrences. Old parent labels may agree or differ, and the old labeling is arbitrary. A rooted tip is a free vertex with no children.

Eight is the sharp tip limit for this universal assertion starting at sixteen vertices. Take a 15-vertex complete binary tree and a singleton, attached at old labels 0 and 1. The forest has nine tips. The sum of its entering and internal weights minus the sum of its vertex labels is the sum of the two boundary labels plus the sum of each free label times its number of children. This difference is odd, whereas equal increments to each vertex and edge histogram would give difference zero.

At every multiple of eight **from twenty-four onward**, the same conclusion holds with **nine rooted tips**. At sixteen vertices and up to nine tips the only failures consist of two full binary trees whose old parent labels have opposite parity. A full binary tree here has zero or two children at each vertex, including the one-vertex case.

With at most **three tips**, the conclusion holds already at $q=1$. In fact one can prescribe any parent-first order and obtain uniform increments on every successive block of eight vertices. For a single block the results below give a complete test with no tip limit, including an optional prescribed label at any one new vertex.

## Exactly eight new vertices

The free vertex labels must be a permutation of $0,\ldots,7$, and the eight entering weights, one per free vertex, must also be a permutation. Write $a_v$ for each free vertex's child count and $b_i$ for the boundary labels. The moment condition
$$
                     \gcd(8,a_v:v\in F)\mid\sum_i b_i
$$
is necessary by the same incidence sum. A colored forest is counted up to rooted isomorphism preserving the numerical boundary labels. The totals include the following complete breakdown.

| Components | Feasible | Fail the moment condition | Further failures |
|---:|---:|---:|---:|
| 1 | 920 | 0 | 0 |
| 2 | 5,752 | 224 | 56 |
| 3 | 16,704 | 0 | 0 |
| 4 | 25,642 | 1,840 | 208 |
| 5 | 30,240 | 0 | 0 |
| 6 | 21,228 | 3,168 | 156 |
| 7 | 13,728 | 0 | 0 |
| 8 | 810 | 5,625 | 0 |

Thus **every odd number of components works**, for all shapes and all parent labels. Of 126,301 colored forests, 115,024 admit a uniform extension. The 420 failures beyond the moment condition comprise 33 affine orbits on seven uncolored shapes. The table below names the shapes. A star is rooted at its center. A fork consists of a root with one child which in turn has two leaf children. A path is rooted at an end.

| Components in the forest | Further failing colorings |
|---|---:|
| Two forks | 4 |
| One fork and a three-leaf star | 16 |
| A five-leaf star and a two-vertex path | 16 |
| Two three-leaf stars | 20 |
| A three-leaf star, a two-vertex path and two singletons | 200 |
| Two two-leaf stars and two singletons | 8 |
| Two two-vertex paths and four singletons | 156 |

For at most three tips these shapes are unavailable. A forest of mass eight with at most three tips has a one-child vertex, since otherwise its order would be at most twice its tip count minus its number of components. Hence its moment condition is automatic. Each consecutive block in any parent-first order has at most as many tips as the original forest: its tips are incomparable ancestors of distinct original tips, since all vertices between two comparable block vertices must belong to the block.

**One common parent label.** Exactly four of the 286 rooted forest shapes fail at a common label. They are the fork and three-leaf star, the five-leaf star and two-vertex path, the two three-leaf stars, and the three-leaf star with a two-vertex path and two singletons. Equivalently these are exactly the nine-vertex trees, rooted at a specified vertex, on which the root cannot carry the surplus residue. Add the root at the common label. A surplus there leaves one copy of every residue in the free vertices and one of every weight on their edges. Translation permits any prescribed surplus value. For a specified second position, the catalog gives the exact feasible residues there as well.

The [catalog](period-pins.jsonl.gz) contains one record per affine orbit, encoded as a parent list, the number of vertex permutations that work, and eight bit masks. Bit $x$ of mask $i$ records whether position $i$ can receive residue $x$. A negative parent $-1-c$ represents an old parent of label $c$, and nonnegative parents are zero-based indices. Translating all colors and multiplying by an odd unit recovers every boundary assignment. The [lookup](period_pins.py) can also test any literal input and return an actual witness. For example, this pins the tip of a single eight-vertex path at 4, with old parent label zero.

~~~sh
python3 -B -m research.eight.period_pins --parents -1 0 1 2 3 4 5 6 --pin 7 4
~~~

## Sixteen new vertices and induction

The [cut generator](period_blocks.cpp) lists every rooted forest of order sixteen with up to eight tips and tries an ancestor-closed eight-vertex subset. The two induced forests may be labeled in order if each works for arbitrary boundary labels, or if all of its boundary vertices are the same and the shape works at a common label. For this test all the original old sites are treated as distinct. When restoring the second half, its components can also meet vertices in the first half.

Of **443,407** rooted forests, 443,251 admit such a cut. For the other 156 shapes the [direct certificate](period-16-direct.txt.gz) gives sixteen labels making both full histograms exactly two in each bin. Each distinct original component can have its own prescribed parent color. Normalizing the first to zero leaves only 730 inputs across the 156 shapes. The numbers of directly certified shapes at five, six, seven and eight tips are 1, 7, 28 and 120.

Now suppose $q\ge3$. Take the largest odd number $r$ no greater than the number of components. There are at most eight components, so $1\le r\le7$. If the number is odd, the chosen $r$ components contain the whole mass. If it is even, omit a smallest component. The other $r$ contain at least half the mass, hence at least eight vertices. Take a nonempty ancestor-closed subset in each chosen component, of combined size exactly eight. Start with their roots and add available children until reaching eight. The first block works because it has an odd number of components. Its complement has order at least sixteen and at most eight tips: any vertex remaining has all its original descendants remaining. Induction labels it at its now prescribed parents. Adding the two histogram increments proves the theorem.

## Nine tips

At order sixteen with exactly nine tips, seven vertices have children. If every child count is even, there are at least fourteen internal edges, and the number of components is even. There must then be two components and all seven positive child counts must be two. Conversely every such pair has gcd two, so opposite boundary parities preclude a uniform extension. There are 46 unordered full binary pairs of total order sixteen.

The cut and direct checks at sixteen [extend to all 108,692 nine-tip forests](period_blocks.py). An eight-vertex cut works on 108,385 shapes. On the remaining 307, the [labeling certificate](period-16-nine.txt.gz) covers all 10,042 normalized boundary assignments satisfying the moment condition. The other 184 assignments, four on each binary pair, have opposite parity. This proves necessity and sufficiency of the moment condition at order sixteen with up to nine tips.

At order twenty-four first take an ancestor-closed block of eight vertices with an odd number of components. To find it among at most nine components, select the largest one, three, five or seven components, taking the largest odd count at most seven available. These contain at least eight vertices: when eight or nine components are present, the seven largest contain at least $7/9$ of the mass. With an even count at most six the chosen components contain at least half the mass. Start at their roots and extend the block to size eight. It is universally labelable by the eight-vertex table.

Its complement now works unless it consists of two full binary components at distinct sites. In that case the complement has nine tips, hence uses every original tip. Reconstruct a possible original shape from the binary pair by adding back the eight removed vertices in reverse parent-first order. Each must parent a nonempty subset of the current roots, since every original tip is already present. The result has one or two components. There are only **2,070** possible shapes, including 1,656 connected ones. A [separate enumeration](nine_tip_period.py) instead lists each eight-vertex prefix with at most two tips and grafts the binary pair at all sites, requiring every prefix tip to gain a child. It recovers the identical set.

For **all 2,070 shapes**, the checker finds an alternative ancestor-closed eight-vertex subset. It verifies that the first block works at its actual boundary sites and that the remaining sixteen vertices either have a shape other than a full binary pair or have both roots at one site. In the latter case their old parent labels agree. This proves the assertion at twenty-four for arbitrary old labels. At each larger multiple of eight use the odd-component first block again and apply induction to its complement, which retains at most nine tips.

## Verification

For all 5,287 affine representatives at size eight, the [permutation test](period_pins.py) starts with every one of the $8!$ assignments and intersects bit masks excluding each pairwise edge collision. A [second verifier](check_period_pins.py) assigns actual labels consecutively, checks every entering sum as it goes and reproduces both the solution count and every pin mask. It independently generates every colored shape by one-leaf insertion and requires the recorded affine orbits to cover that set without any overlap.

At size sixteen the [independent verifier](period_blocks.py) parses and canonicalizes every full rooted forest, rejects repeated shapes and checks each tip count against a rooted-tree multiset recurrence (adjoin one common root to count the forests). It checks the ancestry of every proposed cut, determines its actual boundary sites and compares both induced forests with the eight-vertex catalog. For the direct witnesses it recomputes all sixteen weights and requires complete normalized boundary coverage.

~~~bash
set -euo pipefail
out=$(mktemp -d)
python3 -B -m research.eight.period_pins --catalog "$out/eight.gz"
gzip -dc "$out/eight.gz" | shasum -a 256
python3 -B -m research.eight.check_period_pins "$out/eight.gz"
python3 -B -m research.eight.period_blocks --catalog "$out/eight.gz" --flags > "$out/flags"
c++ -O3 -std=c++17 research/eight/period_blocks.cpp -o "$out/generate"
"$out/generate" "$out/flags" > "$out/cuts"
python3 -B -m research.eight.period_blocks --catalog "$out/eight.gz" --cuts "$out/cuts"
python3 -B -m research.eight.period_blocks --cuts "$out/cuts" --generate-direct > "$out/direct"
gzip -dc research/eight/period-16-direct.txt.gz | cmp - "$out/direct"
shasum -a 256 "$out/cuts" "$out/direct"
~~~

The uncompressed SHA-256 digests are `0a77a8c87cdb8a9d40e9c4594b7f86f2f09d8500245568401512ad4b77ca934b` for the eight-vertex catalog, `056bab63a06605ecc0f3ddce930995d1fb7b90cb88d1a901b6b74c1902ed4100` for the cut stream and `018d75009aead75c87afab373342e83aae18d89d508ffd6d13300cd7bc732556` for the direct rows. These exact-increment results strengthen the attachment theory at eight. The [ordinary eight-label theorem](README.md) and [extension across arbitrary attachments to a surplus core](surplus.md) have separate proofs.


To reproduce the nine-tip classification and the twenty-four-vertex reduction with the same generator and flags, run the following additional commands.

~~~bash
"$out/generate" "$out/flags" --nine-tips > "$out/nine.cuts"
python3 -B -m research.eight.period_blocks --cuts "$out/nine.cuts" --nine-tips
python3 -B -m research.eight.period_blocks --cuts "$out/nine.cuts" --nine-tips --generate-direct > "$out/nine.direct"
gzip -dc research/eight/period-16-nine.txt.gz | cmp - "$out/nine.direct"
shasum -a 256 "$out/nine.cuts" "$out/nine.direct"
python3 -B -m research.eight.nine_tip_period
~~~

The nine-tip cut stream has SHA-256 `c977f5cdcb46ad8fb0dd6b81c0b0fc073e58abf83d4becbb40af3b3119658f65`. The direct rows have SHA-256 `cd547ad8a925a191bac70fda3f815e710855368bb54c2f92ee1f3cd06016f25e`.
