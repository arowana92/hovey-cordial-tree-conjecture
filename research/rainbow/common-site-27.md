# Prescribing a marked vertex and an unused color modulo 27

**Theorem (computer-assisted).** On any tree with at most 23 vertices, choose a vertex and prescribe its label modulo 27. Choose a second, different residue that must remain unused. There is an injective vertex labeling meeting both prescriptions in which all edge sums are distinct.

**Common-parent extension.** On a prescribed cordial core of order one modulo 27, attach a forest of at most **22 new vertices**. All old parents must have the same label, but they may be different vertices. The labeling extends and is cordial on every parent-first prefix. All new labels avoid both the old surplus residue and the common parent label.

In particular, at order $27m+23$ a least counterexample cannot have **any collection of branches at one vertex totaling precisely 22 vertices**. Deleting such branches leaves a connected smaller core of order one modulo 27, and restoring them is a common-parent extension. This strengthens the [single-branch edge-cut exclusion](single-branches-27.md). At every multiple $k$ of 27, the same extension works on a prescribed core of order one modulo $k$ even when the old parents merely have congruent labels modulo 27. Normalize the old surplus to zero modulo $k$. Lift the free labels from their representatives modulo 27. Distinct free labels and weights modulo 27 lift to distinct residues modulo $k$, and the lifted free labels avoid the old surplus.

The [order-25 census](common-site-24.md) extends the marked-vertex theorem through order 25 and the common-parent forest bound through 24.

## From one tree labeling to many prescriptions

Let $f$ be an injective labeling with distinct edge sums, let $v$ be the mark and let $z$ be unused. Under $x\mapsto u(x-z)$ the unused residue becomes zero and the marked label becomes $u(f(v)-z)$. The units modulo 27 have three orbits on nonzero differences, with gcds 1, 3 and 9. A family of witnesses covering all three orbits at every vertex therefore realizes any prescribed nonzero mark with zero unused. Translation gives every pair of distinct prescribed residues.

For the common-parent application, add a temporary root to the forest adjacent to every component root, obtaining a tree. Prescribe the old parent label there and normalize the old surplus to zero. If the two labels differ, apply the theorem. If they coincide, translate any injective rainbow labeling of the augmented tree until its root is zero. In either case the new labels avoid zero and their weights are distinct. Substituting the actual old parent for every temporary-root incidence preserves its weight. The extension works on every parent-first prefix because the original edge counts are equal and the original vertex bins other than the surplus are equally low. For a smaller augmented tree, pad by a pendant path to order 23, retain the mark, then restrict.

## Independent checks and reproducibility

The [generator](common_site_generate.cpp) visits unrooted 23-vertex trees at their unique centroid. For each shape it emits a family of injective labelings and uses the missing vertex residues to track the three difference classes at every mark. The [verifier](common_site_verify.cpp) independently parses the tree, checks child ordering and the centroid bound, ranks its branches to exclude duplicates across shards, and recomputes all vertex and edge residues for each row. It explicitly multiplies each available mark-to-hole difference by every unit and requires coverage at every marked vertex. The mark-equals-surplus application is available from any row.

The [128 verified streams](common-site-22.sha256) cover **14,828,074 unrooted trees** and contain **116,963,408 witness rows**. Counting positions before automorphisms, they cover **9,208,233,954** marked-vertex and normalized parent-color inputs, including zero. A separate rooted-tree multiset recurrence and vertex/edge dissymmetry give the total number of unrooted trees independently of ranking. The [whole-tree replay](check_common_site.py) also translates literal rows, joins the components to a 28-vertex cordial star with the requested parent color, and checks both frequency lists after each insertion.

Each binary record starts with an eight-byte little-endian canonical tree word, followed by rows of 23 labels in preorder and a single byte 255. The generated streams can be discarded after verification. The manifest records the SHA-256 digest, shape count and row count for each rank stride.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 23 --manifest "$r/common-site-22.sha256"
python3 -B -m research.rainbow.check_common_site 23 --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --workers 2
cmp "$out/shards/manifest.txt" "$r/common-site-22.sha256"
"$out/generate" 23 0 1024 > "$out/sample"
python3 -B -m research.rainbow.check_common_site 23 --replay "$out/sample"
~~~
