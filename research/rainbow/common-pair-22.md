# A 22-vertex forest and a separate pair at 27 labels

**Theorem (computer-assisted).** Give a tree of order one modulo 27 any 27-cordial labeling. Attach a rooted forest of at most 22 vertices whose old parents have one common color. At a second, independently prescribed parent color, attach either a path of two new vertices by an end or two new leaves. The two leaves can have different old parents of that color. There is an extension that stays cordial along every parent-first ordering of the additions.

**Consequence.** In a smallest 27-label counterexample of order $27m+25$ with $m\ge1$, no union of branches at any vertex has 22 vertices. No edge has a side of any order from **22 through 27**. In particular, if a 52-vertex counterexample exists, it has a unique centroid and every branch there has at most 21 vertices.

To prove the restriction, remove a union of order 22 at its joint $v$ and root the retained tree at $v$. A deepest vertex with children has only leaf children. If it has at least two, remove two of them. If it has one, remove it and its child. In the latter case it differs from $v$ because the retained tree has more than two vertices. The core still contains $v$ and has order $27m+1$. Label it by minimality and use the theorem to restore the two attachments. A side of order 22 is itself such a union. In a side of order 23, the child branches at its entering root form such a union. A side of order 24 can be paired with a leaf outside it, by the [two-cut theorem](../biased/one-offset-25.md). The [affine and divisible joins](../prime/four-deficits.md) exclude orders 25 through 27. At order 52 each centroid branch has at most 26 vertices and two centroids would give a 26/26 split. [Order-52 leaf bound](../census/order-fifty-two.md)

## Certificate

Normalize the surplus residue of the old core to zero. Add a temporary root to the 22-vertex forest, joining it to all component roots. The [verifier](common_site_verify.cpp) checks injective rainbow rows on the resulting 23-vertex tree. For each possible mark (the temporary root) and old color $a$, it tries affine images under units that put $a$ at the mark and leave zero available after deleting the mark. Let $S$ be the unused nonzero labels after the deletion. Let $D$ be the weights missing from the augmented tree; replacing its marked vertex by old parents of color $a$ preserves every weight.

For two leaves at old color $b$, a row works if two distinct $x,y\in S$ have $b+x,b+y\in D$. For a path, it suffices that $b+x,x+y$ are distinct and in $D$, with $x$ on the entering vertex. The checker tests all $b$ at each mark, separately for both shapes. It tests $a=0,1,3,9$, since every residue modulo 27 is a unit multiple of one of these and unit scaling carries all endpoint sums along. Every addition gives a distinct nonzero label and a distinct new weight. Any parent-first prefix therefore preserves cordiality. Padding a smaller main forest by temporary leaves and restricting the labeling proves the result for every smaller size. The extension lifts to a core of order one modulo any multiple of 27 whenever the first parents agree modulo 27 and the two leaf parents agree modulo 27. Normalize the surplus in the larger group, reduce the old colors, and choose arbitrary lifts of the new labels. [Affine formulas](common-pair-21.md)

The **384 independently checked shards** exhaust **14,828,074** unrooted trees on 23 vertices. They contain **718,182,472** witness rows and cover **497,244,633,516** choices of tree, mark, two colors and attachment shape. The ranker enumerates branch multisets at the unique centroid at this odd order. The verifier decodes trees and recovers their expected ranks. A separate rooted-tree count with dissymmetry checks the total. For three ranks, the [generator](common_site_generate.cpp) obtained the remaining witnesses by rerooting its search. Regenerating ranks 7,203,851, 14,146,186 and 14,379,276 individually gave 50, 47 and 45 checked rows. The combined public generator and verifier also regenerated five complete shards, including the shards of those three ranks, matching every hash and count. A separate Python replay built **134,136** trees on 52 vertices from four sampled augmented trees and counted all vertex labels and endpoint sums directly. [Shard hashes](common-pair-22.sha256) · [Count and whole-tree replay](check_common_site.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 23 --pair --manifest "$r/common-pair-22.sha256"
python3 -B -m research.rainbow.check_common_site 23 --pair --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --shards 384 --workers 2
cmp "$out/shards/manifest.txt" "$r/common-pair-22.sha256"
"$out/generate" 23 717 3000000 --pair > "$out/sample"
python3 -B -m research.rainbow.check_common_site 23 --pair --replay "$out/sample" --sample 4
~~~
