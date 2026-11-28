# A prescribed vertex and an unused residue on every tree through order 25

**Theorem (computer-assisted).** In any tree of order at most 25, choose a vertex and two distinct residues $a,z\pmod{27}$. There is an injective labeling with distinct edge sums that assigns $a$ to the chosen vertex and never uses $z$.

**Extension.** A prescribed cordial core of order one modulo 27 extends across any rooted forest of at most **24 vertices** whose old parents all have one common label. One labeling works on every parent-first prefix. At a multiple of 27 the same conclusion holds for a core of order one modulo the larger modulus if the old parent labels agree modulo 27.

Normalize the surplus vertex residue to zero. Add a temporary root adjacent to the root of every component of the forest. If the common parent color is nonzero, prescribe it at the temporary root and leave zero unused. If the common color is zero, translate any injective rainbow labeling until the temporary root has that color. Delete the temporary root and substitute the actual old parents for its incidences. Each new weight is distinct and all new vertex labels are distinct, nonzero and different from the common parent color. The old vertex bins other than zero start equally low and all old edge bins start equal, proving the prefix assertion. At a multiple of 27, translate the surplus in the larger group first, reduce the old colors and lift any choice of new labels. Padding a smaller marked tree to order 25 by a pendant path and restricting proves the smaller orders. [Affine proof](common-site-27.md)

**Ordinary counterexample restriction.** In a smallest 27-label counterexample of order $27m+s$ with $m\ge1$ and $2\le s\le25$, no union of whole branches at a vertex can total $s-1$. Removing such a union leaves a smaller connected core of order one modulo 27. In particular, at residue 24 the prohibited union orders include **21, 22 and 23**. At residue 25 they include **22 and 24**. These restrictions allow arbitrary branch counts and branching within each component. [Independent pair at residue 24](common-pair-21.md) · [Independent pair at residue 25](common-pair-22.md)

## Witnesses and replay

For each marked vertex, the witness family contains an unused residue whose difference from the marked label has gcd 1, 3 or 9 with 27, separately for all three gcds. Multiplication by units supplies every nonzero difference and translation supplies the absolute choice of $z$. The search first uses ordinary injective rainbow rows. If an orbit is missing, it roots at the mark, fixes its label and reserves a specific unused color. The independent verifier checks the tree's canonical centroid encoding and rank, recomputes its edge weights, and explicitly tests the unit multiples of the differences. [Generator](common_site_generate.cpp) · [Verifier](common_site_verify.cpp)

All **104,636,890** unrooted 25-vertex trees passed. The **1,024** verified shards contain **1,367,975,727** witness rows. They cover **1,836,377,419,500** literal choices of tree, mark and two distinct prescribed residues. The manifest checker counts **70,629,900,750** normalized choices of tree, mark and common parent color, including zero. A separate recurrence with tree dissymmetry checks the number of shapes. Four complete shards, numbered 0, 137, 511 and 917, were regenerated with the combined public generator and checked against the hashes, totaling 408,738 trees and 5,343,545 rows. The whole-tree replay put the forests onto actual 28-vertex cores and tested 6,750 joins at ten sampled ranks, plus 675 joins at the last rank. Recounting both histograms checked all 178,200 nonempty restoration prefixes. [Manifest](common-site-24.sha256) · [Count and whole-tree checker](check_common_site.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 25 --manifest "$r/common-site-24.sha256"
python3 -B -m research.rainbow.check_common_site 25 --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --shards 1024 --workers 2
cmp "$out/shards/manifest.txt" "$r/common-site-24.sha256"
"$out/generate" 25 317 9500000 > "$out/sample"
python3 -B -m research.rainbow.check_common_site 25 --replay "$out/sample" --sample 10
~~~
