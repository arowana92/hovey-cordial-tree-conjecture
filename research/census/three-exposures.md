# Every tree with matching deficiency at most three is 26-cordial

**Theorem.** Every finite tree with a matching missing at most three vertices admits a 26-cordial labeling. More generally, at order $26q-H$ with $0\le H\le13$, every tree of matching deficiency at most $H+2$ is 26-cordial. In particular a smallest unrestricted 26-label counterexample, whose possible orders have $0\le H\le5$, would require deficiency at least $H+4$. At order 47, every matching would miss at least nine vertices. [Order restrictions](../rainbow/short-forests.md)

## Deleting temporary mates from a forest

Let $m\in\{3,5,7,11,13\}$ and fix a $2m$-cordial labeling on a core of divisible order. Attach a forest $F$ by one bridge from each component to any core vertex. If $|F|-\nu(F)\le m$, the old labels extend. Here $|F|$ counts vertices. Equivalently, $F$ has independence number at most $m$, by the matching and vertex-cover equality for bipartite graphs.

Give each unmatched vertex a temporary leaf and match it to that leaf. The completed forest has $|F|-\nu(F)$ pairs. Apply one batch of the [matched forest construction](../paired-forest.md). Its first entering edge supplies the old deficit. The pairs receive distinct low residues modulo $m$, each in both parities. The matching weights are distinct and odd, and the later entering weights are distinct and even. Deleting the temporary leaves and their matching edges preserves distinctness of the retained vertex labels and of the weights after the first entering edge. That first edge is real. These facts suffice for both histograms to be balanced.

There is also a multiple-batch version with exactly one uncovered vertex when $|F|+1$ is a multiple of $2m$. Complete and label the forest in full batches. The final vertex histogram is uniform and the unique edge deficit is even. Deleting the single temporary leaf removes an odd weight, so the final two edge deficits are distinct. In both versions offsets on edges outside the matching are permitted as in the matched forest theorem.

## Choosing the two exposures to retain

Write $d=|T|-2\nu(T)$. Choose a maximum matching with every exposure an original leaf, using [alternating exchanges](../near-matching.md#completing-and-lifting-a-maximum-matching). Contract its pairs, leaving the exposures as singleton leaves. In this quotient a path between two exposures meets $h$ pair vertices. Its two singletons and the original vertices of those $h$ pairs form a connected subtree. Avoiding the other exposed leaves, grow that subtree to include any desired number of whole pairs between $h$ and $\nu(T)$.

First take $d=3$. The [prefix and matching theorem](../near-matching.md) covers every order except $1$ and $-1$ modulo 26. At order $1$ modulo 26, remove one exposed leaf. The [two-exposure theorem](two-exposures.md) labels the divisible core, and the leaf can return with the weight of its edge equal to the unique deficit.

At order $26q-1$ there are $13q-2$ pairs. If some two exposures leave at least 12 pairs outside their path, grow their core to include $13q-14$ pairs. It then has order $26(q-1)$ and deficiency at most two. The exterior has 12 pairs and one uncovered vertex. The preceding forest lemma restores its 25 vertices.

The three exposures have a median pair. Let $h_i$ count the pairs strictly between the median and exposure $i$, and let $s$ count all pairs off the three arms and median. Thus $h_1+h_2+h_3+s=13q-3$. The path between the other two exposures leaves $h_i+s$ pairs outside. For $q\ge3$ some $h_i+s\ge12$, by summing the three inequalities. The order-25 base is known. It remains to treat order 51 with $h_i+s\le11$ for all $i$. Here
$$
h_1+h_2+h_3+s=23,\qquad s\le5,\qquad h_i+h_j\ge12\quad(i\ne j).
$$

## Two terminal pieces at order 51

Choose any two arms. Starting at each tip and walking inward, count the pairs on its arm together with their entire side branches. A position with $w$ side pairs adds $1+w$. For arm $i$ let $A_i=h_i+s_i$ be its full mass, with $s_i$ side pairs attached along the arm. The attainable prefix masses include 0 and $A_i$ and omit precisely $s_i$ integers in between. Neither exposed tip has side branches.

Since $A_i,A_j\le11$, there are $A_i+A_j-11$ integer solutions of $x+y=12$ with $0\le x\le A_i$ and $0\le y\le A_j$. At most $s_i+s_j$ solutions use an omitted mass. The difference is $h_i+h_j-11\ge1$. Choose an attainable split. Take the two tip pieces, their side branches and their exposed vertices. These give two singly attached components with 12 pairs and two exposures, hence 26 vertices. Let $b$ be the number of side pairs in these pieces.

The remaining core is a 25-vertex tree with 12 pairs and one exposure. Complete its matching by one temporary leaf. The contracted 13-vertex tree has a bijective 13-cordial labeling. The [matching lift](../matching-expansion.md) gives a bijective 26-cordial labeling with distinct low residues on different pairs. Remove the temporary leaf. One old missing weight is even, the removed weight is odd, and all retained vertex labels are distinct.

If $1\le b\le5$, the two core parents lie in different pairs. Indeed, if both cuts reached the median, they would take both complete arms, giving $12=h_i+h_j+s_i+s_j$ and hence $b=0$. The parent labels therefore differ modulo 13. Join the two exposed tips by a temporary matching edge and join the two boundary sites by a closing edge. This is one of the [certified branched rings with two specified edges](two-exposures.md#blocks-with-one-to-five-off-path-pairs). Its first joining construction adds **one to every vertex and edge count** and works on a core of any order. It restores the original tree.

If $b=0$, the two pieces are the unbranched arms described below. The core has a nonuniform edge histogram, so the arm theorem applies even if the parents coincide. This completes the proof at 51 and hence at every order for deficiency three.

## Two arms on a prescribed core

Take two terminal paths of matched pairs with twelve pairs between them in total and with one further exposed vertex at each tip. The two arms can be attached at arbitrary parents of a fixed 26-cordial core whenever its edge histogram is nonuniform. More precisely, both histograms can receive a uniform increment of one except precisely when every pair has coincident ports and the two parent labels have opposite parities.

To check uniform increments, give the free vertices a bijection with distinct internal weights. If the arm roots have labels $a,b$ and the missing weights are $u,v$, the normalized differences of parent labels covered by this row are the unit multiples of $u-v-a+b$ and $v-u-a+b$. The affine translation realizing these choices was [proved and checked in Lean](two-exposures.md#joining-at-two-labeled-parents). The independent checker verifies all four unit orbits for every nonzero port pattern. For the all-coincident pattern it verifies both even orbits. Interchanging the arms reduces the descriptions to $7\cdot2^{12}$.

For the exceptional case, a uniform increment is impossible by parity. Summing the new edge weights and subtracting the sum of the new vertex labels gives the sum of the two parent labels plus twice the sum of the twelve arm sites with coincident ports. This cannot vanish when the parent parities differ.

Instead use increments of one everywhere except two at residue $x$ and zero at residue $y$. Regard each attainable choice as an arrow $x\to y$. For each of the seven splits, normalize the first parent to zero by translation and the difference to 1 or 13 by a unit. The [checker](check_three_exposures.py) builds the graph of arrows from **literal histograms** and verifies reachability between every ordered pair of residues. For a nonuniform cordial edge histogram, some arrow starts in the nonempty set of low bins and ends outside it. This transfer is exactly what restores balance. The free vertex increment is uniform. Translation and unit scaling permute the bins, preserving this argument for the original parents.

## Higher deficiencies at orders just below a multiple

Suppose $2\le H\le13$ and $d=H+2$ at order $26q-H$. Orders below 26 are already covered, so take $q\ge2$. Choose any four of the exposed leaves in the contracted tree. Their minimal connecting subtree has four leaves and at most $\nu=13q-H-1$ other vertices, all paired. A tour in cyclic depth-first leaf order uses each edge twice. Its four paths thus have total length at most $2(\nu+3)$. A shortest one, meeting $h$ pairs, has length $h+1$, whence $2h\le\nu+1$. This gives $h\le13q-14$.

Grow this two-exposure subtree to $13q-14$ pairs, leaving every other exposure outside. The connected core has order $26(q-1)$ and deficiency at most two. The exterior has $13-H$ pairs and $H$ exposures, so exactly 13 completed pairs. The forest lemma restores it. For $d\le H$ the earlier prefix bound applies since $H+d\le26$. The parity of the tree order supplies the remaining step between the two cases. For $H=0,1$ use the two- and three-exposure theorems. This proves the stated range and counterexample restriction.

## Verification

The arm search emits 105,738 bijections for uniform increments. Direct calculation of 131,040 transformed histograms verifies the exceptional transfers. An independent enumeration checks all 60,458 sorted tripod mass profiles and every attainable split of each pair of arms. Further checks include 900 forest extensions with temporary mates. With the earlier ring streams available, the whole-tree checker verifies 112 actual trees on 51 vertices, including 91 of matching deficiency three. [Search](paired_arms.cpp) · [Independent verifier](check_three_exposures.py) · [Lean bounds for the exposure paths](ExposureHull.lean) · [Stream hashes](three-exposures.sha256)

~~~bash
set -e
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/paired_arms.cpp" -o "$out/arms"
"$out/arms" --neutral > "$out/neutral-arms.txt"
"$out/arms" --sample-combs > "$out/transfer-arms.txt"
python3 -B -m research.census.check_three_exposures "$out"
(cd "$out" && shasum -a 256 -c "$src/three-exposures.sha256")
lean "$src/ExposureHull.lean"
~~~

Pass the output directory of the [two-exposure replay](two-exposures.md#reproduction) as an additional `--ring-directory` argument for the branched whole-tree checks.
