# A prescribed edge offset on every tree through order 25 modulo 27

**Theorem (computer-assisted).** In any tree with at most 25 vertices, mark an edge and add any prescribed residue modulo 27 to its endpoint sum. There is an injective vertex labeling in which all edge weights, including this adjusted weight, are distinct. The result holds at every multiple of 27 by reducing the offset and lifting the vertex labels. Smaller trees can be padded with pendant vertices to order 25 and their labels then restricted.

**Two-cut consequence.** A least 27-label counterexample of order $27m+s$, with $2\le s\le25$ and $m\ge1$, has no two disjoint sides cut off by single edges whose orders sum to $s$. In particular every 52-vertex tree with two such sides totaling 25 is 27-cordial. Examples include side orders 12 and 13, or 8 and 17, with arbitrary attachment points and branching. A single side of order 24 also suffices at residue 25. The complementary tree has a leaf other than its attachment vertex, giving a second side of order one. The direct proof at order 52 using a 24/28 split remains independent. [Single-side theorem](../census/side24-at-52.md)

For the proof take a cordial labeling of the connected middle component of order $27m$, and write $h$ for its deficient edge weight. Let $p,r$ be the labels at its two joining vertices. These vertices may coincide. Replace the entire middle by an edge between its exterior neighbors with offset $p+r-h$. The theorem labels this smaller tree on $s$ vertices. If its joining-edge endpoints receive $a,b$, translate the middle labels by $d=a+p-h$. The first joining edge now fills the translated deficit $h+2d$ and the other weighs $b+r+d=a+b+p+r-h$. The expansion adds exactly $m$ copies in each vertex and each edge bin. The same argument applies to a middle component of order divisible by any multiple of 27 when the smaller core labeling is available. [Expansion formula and chains of divisible pieces](one-offset-23.md)

## Completing the marked-edge census

For an injective rainbow row on an unadjusted tree, write $w$ for the weight at the mark and $z$ for an unused weight. Scaling by a unit $u$ permits the offset $u(z-w)$. Requiring a difference from every nonzero unit orbit at every edge therefore suffices. Modulo 27 these orbits have gcds 1, 3 and 9. Offset zero works from any row.

The generator first tries unprescribed rows. For a missing orbit, root the tree at one endpoint of the marked edge and process its other endpoint next. Set the endpoint labels to $0,a$ and reserve the weight $a+d$ where $d$ represents the required difference. The placement search avoids that weight as well as the marked weight $a$. A second search can exchange two labels while keeping the endpoints fixed, including exchanges with the unused labels. Every emitted row is indexed by the tree's original vertex order. The independent verifier recomputes all labels and endpoint sums, checks the canonical tree rank, and multiplies the available mark-to-hole differences by each unit. [Generator](../rainbow/common_site_generate.cpp) · [Verifier](../rainbow/common_site_verify.cpp)

The **1,024 verified shards** cover all **104,636,890** unrooted 25-vertex trees and contain **1,027,116,770** witness rows. They account for **67,804,704,720** literal tree, marked-edge and offset inputs. A separate rooted-tree recurrence with dissymmetry checks the total shape count. A combined build regenerated four full shards including the first and last, reproducing the published hashes and independent verifier totals for 408,738 trees and 4,011,920 rows. A whole-tree replay expanded ten sampled marked trees into 6,480 trees on 52 vertices and recounted both histograms. The last tree rank supplied another 648 joins, one for each of its 24 marks and 27 offsets. [Manifest](one-offset-25.sha256) · [Count and whole-tree checker](../rainbow/check_common_site.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 25 --edge --manifest research/biased/one-offset-25.sha256
python3 -B -m research.rainbow.check_common_site 25 --edge --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --shards 1024 --workers 2
cmp "$out/shards/manifest.txt" research/biased/one-offset-25.sha256
"$out/generate" 25 137 4096 --edge > "$out/sample"
python3 -B -m research.rainbow.check_common_site 25 --edge --replay "$out/sample" --sample 10
~~~
