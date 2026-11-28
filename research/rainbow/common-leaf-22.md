# A common parent color and one independently attached leaf at 27 labels

**Theorem (computer-assisted).** Fix a 27-cordial labeling on a core of order one modulo 27. Attach a forest of at most 22 vertices whose old parents all have the same color. Also attach one leaf at any old vertex. The coloring extends in such a way that every parent-first prefix of the additions is cordial. The extra leaf may have any prescribed edge offset, since this just changes its effective parent color.

**Counterexample restriction.** Suppose a smallest failure has order $27m+24$. No collection of whole branches at any vertex can total 22 vertices. To see this, remove such a collection at $v$. The remaining tree has at least two vertices, so one of its leaves differs from $v$. Remove that leaf as well. The smaller core is connected, contains $v$, and has order one modulo 27. The theorem restores both removals. A single edge side of order 23 is also excluded. Its root has 22 vertices in its child branches. Together with the [affine and divisible joins](../prime/four-deficits.md), this excludes all edge-side orders **22 through 27** at this residue.

The extension also holds at every multiple of 27 if the main forest's parents agree modulo 27. Translate the old surplus to zero. Lift the computed free labels from modulo 27 to the larger modulus. Distinct nonzero free labels and distinct new edge weights modulo 27 stay so after lifting.

## The two prescribed colors

Normalize the unique old surplus residue to zero. Removing it from consideration leaves equally frequent low vertex bins. All old edge bins have the same count. It suffices to supply distinct nonzero labels to the free vertices and distinct weights to the new edges. These conditions persist on every parent-first prefix.

Augment the main forest by a temporary root adjacent to each component root. With 22 main vertices this gives a 23-vertex tree. Let $f$ be an injective labeling of this tree with distinct edge weights. Write $r$ for the label of the temporary root, $V$ for the unused vertex residues, and $E$ for the unused edge weights. For a unit $u$ and $z\in V\cup\{r\}$, transform the labels by $y\mapsto u(y-z)$. Substitution of the old parents works when their common label is $a=u(r-z)$. All transformed main-forest labels avoid zero.

The extra leaf can take label $u(x-z)$ for any $x\in (V\cup\{r\})\setminus\{z\}$. Its effective old parent color $b$ gives a new weight outside the main weights precisely when some $w\in E$ satisfies
$$
                       b=u(w-x-z)\pmod {27}.
$$
Indeed, the unused weights of the transformed augmented tree are $u(w-2z)$, while the extra edge weighs $b+u(x-z)$. The freed dummy-root label may be used on the extra leaf. Padding a smaller main forest to 22 vertices and restricting its labels proves the smaller orders.

## Certificate and independent checks

At every marked vertex of every 23-vertex tree, the [generator](common_site_generate.cpp) covers all pairs $(a,b)$. Simultaneous multiplication by a unit splits the 729 pairs into 53 orbits. A witness row records only the original 23 labels. The [verifier](common_site_verify.cpp) parses the tree, checks its centroid and rank, and recomputes all vertex and edge residues. It applies each unit and translates the mark directly to 0, 1, 3 and 9. At each such joint color it tries the available nonzero leaf labels and tests all 27 effective parent colors. Scaling these four complete rows covers all 729 pairs.

The [manifest](common-leaf-22.sha256) covers **14,828,074** tree shapes with **244,575,215** witness rows and **248,622,316,758** literal choices of marked vertex and the two colors. The number of unrooted shapes is independently checked by rooted-tree multisets and dissymmetry. A [whole-tree replay](check_common_site.py) substitutes actual sites on a 28-vertex path and rebuilds both complete histograms. Four sampled exterior trees give 67,068 trees on 51 vertices, using every mark and every literal pair in each sample. The native verifier rejected both a repeated vertex color and an incomplete family of witness rows.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 "$r/common_site_generate.cpp" -o "$out/generate"
c++ -O3 -std=c++17 "$r/common_site_verify.cpp" -o "$out/verify"
python3 -B -m research.rainbow.check_common_site 23 --leaf --manifest "$r/common-leaf-22.sha256"
python3 -B -m research.rainbow.check_common_site 23 --leaf --run "$out/shards" --generator "$out/generate" --verifier "$out/verify" --shards 256 --workers 2
cmp "$out/shards/manifest.txt" "$r/common-leaf-22.sha256"
"$out/generate" 23 0 4096 --leaf > "$out/sample"
python3 -B -m research.rainbow.check_common_site 23 --leaf --replay "$out/sample"
~~~
