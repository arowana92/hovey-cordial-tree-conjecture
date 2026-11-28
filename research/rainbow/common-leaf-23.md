# A 23-vertex forest and one independently attached leaf

**Theorem (computer-assisted).** Fix a 27-cordial labeling on a tree of order one modulo 27. Attach a forest of at most 23 vertices whose component roots all have the same effective old parent color. Attach one more leaf at any old vertex with any entering-edge offset. There is a single extension cordial on every parent-first prefix of the additions. This holds at every multiple of 27 when the main forest's effective parent colors agree modulo 27.

Use the [common-forest construction](common-leaf-22.md#the-two-prescribed-colors) with a temporary root and 23 free vertices. Normalize the old surplus to zero. In a rainbow labeling of the augmented 24-vertex tree, let $r$ label the root and let $V,E$ be its unused vertex and edge residues. For every pair of old effective colors $(a,b)$ the certificate gives a unit $u$, a choice $z\in V\cup\{r\}$ and an $x\in(V\cup\{r\})\setminus\{z\}$ such that $a=u(r-z)$ and $b=u(w-x-z)$ for some $w\in E$. Transform each main label $y$ to $u(y-z)$ and give the extra leaf $u(x-z)$. All free labels are distinct and nonzero and all new weights are distinct. Padding the main forest and restricting proves the assertion for smaller forests. At a multiple of 27, translate the old surplus to zero in that group, reduce the parent colors modulo 27, and lift each new label. Distinctness modulo 27 gives the two required distinctness conditions in the larger group.

**Ordinary tree consequence.** In a smallest 27-label counterexample of order $27m+25$ with $m\ge1$, no collection of whole branches at any vertex $v$ can total **23** vertices. Removing those branches leaves a tree with a leaf other than $v$. Removing that leaf as well gives an order-one core which is cordial by minimality. Restore the 23 vertices and the independent leaf using the theorem. The earlier two-site and common-site results exclude union sizes **22** and **24** at this same residue. [Two-vertex attachment](common-pair-22.md) · [Common-site attachment](common-site-24.md)

The [2,048 shard receipts](common-leaf-23.sha256) cover 39,299,897 unrooted trees, 1,092,010,734 witness rows and 687,590,997,912 literal choices of mark and two colors. The native verifier reconstructs the canonical rank, checks the labels and sums, and explicitly enumerates the old colors covered by each row. A separate count uses dissymmetry of rooted trees. Six sampled ranks gave 104,976 whole-tree joins with both histograms recomputed at order 52.

~~~bash
set -euo pipefail
r=research/rainbow
out=$(mktemp -d)
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generator"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verifier"
python3 -B -m research.rainbow.check_common_site 24 --leaf --manifest "$r/common-leaf-23.sha256"
python3 -B -m research.rainbow.check_common_site 24 --leaf --run "$out/shards" \
    --generator "$out/generator" --verifier "$out/verifier" --shards 2048 --workers 2
cmp "$out/shards/manifest.txt" "$r/common-leaf-23.sha256"
for rank in 0 120 49123 569008 1000003 39299896; do
    "$out/generator" 24 "$rank" 39299897 --leaf
done > "$out/examples"
python3 -B -m research.rainbow.check_common_site 24 --leaf --replay "$out/examples" --sample 6
~~~
