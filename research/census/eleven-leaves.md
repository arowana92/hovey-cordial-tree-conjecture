# Every finite tree with at most eleven leaves is 27-cordial

**Theorem (computer-assisted).** Every finite tree with at most eleven leaves admits a 27-cordial labeling. In particular any counterexample at 27 labels must have at least twelve leaves. The unrestricted 27-label witness audit is in progress.

The [six-terminal theorem](../rainbow/few-leaves.md) already covers ten leaves and reduces any smallest failure among trees with at most thirteen leaves to order at most 54. The [short-forest theorem](../rainbow/twenty-one-free.md) covers all orders through 49. It suffices to treat trees with exactly eleven leaves and $50\le n\le54$. Write $t=n-28$. Every core of order 28 is already 27-cordial. Its unique surplus vertex residue can be translated to zero and its edge bins are uniform. Thus a forest of $t$ exterior vertices may be restored with distinct nonzero labels and distinct weights, including the edges from the core.

## Three branches at a leaf centroid

Choose a vertex $v$ for which every component of $T-v$ contains at most five original leaves. Such a vertex is obtained by walking toward a side containing more than half the leaves until none exists. Suppose some collection of components contains five leaves. Its complement contains six. Use as a seed $v$ and the side with the smaller total number of vertices. This seed has order at most $1+\lfloor(n-1)/2\rfloor\le28$ and contains at least five original leaves. From $v$ traverse the remaining branches in preorder, smaller child subtrees first, until the core has order 28. All exterior tips are original leaves and there are at most six. The boundary colors satisfy the [ordered-cut condition](../rainbow/ordered-cut.md#which-colored-forests-actually-occur). Pad the largest exterior component at a tip to order 26 in total and apply the six-terminal certificate.

If no collection contains five leaves, the branch leaf counts must be $3,4,4$. Indeed a part five is excluded. With a part four there can be no one, so the remaining parts are twos, threes and fours. A two and a three cannot coexist. The odd total forces at least one three and then $3x+4y=11$ gives one three and two fours. With no four and parts at most three, two and three cannot coexist. An all-ones-and-twos partition of eleven has a subcollection totaling five. A partition into ones and threes has either five ones or a three and two ones, since the count of ones is two modulo three. This exhausts the possibilities.

If one branch has at least $t$ vertices, the centroid and the other two branches give a seed of order at most 28 containing at least seven leaves. Otherwise write $a,b,c<t$ for the orders of the three-, four- and four-leaf branches, with $b\le c$. Each order is at most 25. We now enumerate the rooted branches explicitly. Equal-sized four-leaf branches may be tested in both orders.

## Sufficient cuts checked on each triple

1. **A seed and a preorder prefix.** Keep $v$ and a whole branch of size $s$ with $h$ leaves. Among the two remaining branches, enter a smaller one first and grow in size-ordered preorder. If its $(5-h)$-th leaf can be reached within $27-s$ visits, the resulting core has at least five original leaves. Finish the same traversal to order 28 and apply the six-terminal theorem. All ties in the prefix test may be optimized separately for the desired leaf. This argument uses a seed with a single boundary vertex.
2. **Removing the middle of two cuts.** Choose one downward subtree in each of two different branches. Suppose their orders add to $n-27$, they contain at least five leaves between them, and their parents are at distance at least two. The remaining middle piece has 27 vertices and three through six original leaves. Closing its two boundary vertices makes a simple unicyclic graph with those leaves. The [ring replacement theorem](few-leaf-rings.md) allows this piece to replace one edge of a smaller cordial tree while adding one to every bin. The distance is the sum of the two parent depths from $v$. For pruning, this includes keeping one whole branch of size $s$ and portions of the initial unbranched corridors of the other two. With corridor lengths $u,w$ (counting unary vertices), the central test is $2\le26-s\le u+w$.
3. **Six terminal paths.** If the six longest terminal arms have total length at least $t$, trim a total of $t$ vertices from them. Their lengths exclude the first branching vertex. The retained tree has order 28. The [independent six-path certificate](ring-order.md#terminal-paths-with-independently-prescribed-parents) restores all six paths with their actual parent labels.
4. **A complete side and a suffix on another side.** Choose a whole rooted subtree of size $s$ with $h$ leaves, and in another branch a rooted subtree with at least $z=t-s>0$ vertices. Delete the first subtree and the last $z$ vertices in size-ordered preorder of the second. Write $j$ for the number of tips in that suffix. Each exterior tip is an original leaf. The suffix has at most $j$ boundary runs and satisfies the ordered-cut inequalities. If $h+j\le6$ and $s+26-t\ge z+j$, append the first subtree after the suffix's components, padding it by $26-t$ vertices at one tip. Its size permits an arbitrary last boundary label. The six-terminal certificate restores the original forest by restriction. Both attachment parents survive. [Two-side pruning proof](pendant-order.md#removing-a-forest-with-few-tips)

These tests suffice at orders 50 through 53. For each remaining triple at 54, keep $v$ and the size-$c$ four-leaf branch. Visit the two other branches in size order, using canonical bracket order for ties, until reaching 28 vertices. The resulting exterior has exactly 26 vertices. Sort its components canonically. The ordered-cut proof applies because the initial seed is a union of whole branches at $v$.

## Exhaustive verification

The [structural enumerator](eleven_leaf_cuts.cpp) reads canonical bracket words for all 495,040 three- or four-leaf rooted branches of order at most 25. It decodes every vertex's actual depth, descendant subtree, terminal arm and preorder suffix. The [independent structural checker](check_eleven_leaf_cuts.cpp) builds all branches recursively as multisets of smaller trees and computes the same reductions from child data. Both enumerate the size triples and agree on every final forest word. No triples require new witnesses at orders 50–53. At 54, the 106,504 remaining branch triples give **1,785 distinct exterior forests**.

The [native witness verifier](../rainbow/spine_verify.cpp) checked 341,973 permutations, the actual edge sums, all boundary assignments and exact equality of the stream's shape set with the independently regenerated list. Each forest has three groups of boundary parents and permits all $27^3$ assignments. A [Python verifier](check_eleven_leaf_labels.py) independently rules out internal-edge collisions, entering-edge collisions with internal edges, and collisions between two entering edges by masking the offending triples. It recomputes the unit orbits of the literal triples and checks that every orbit has a witness for each forest. Both verifiers cover **35,134,155 boundary assignments**. Scaling a witness by a unit supplies the rest of its orbit. Since a least counterexample in this leaf class had to appear in the five tested orders, the theorem holds at every tree order.

## Reproduction

From the repository root, the following rebuilds the full proof. It needs a C++17 compiler and Python 3.8 or later.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/rainbow
c=research/census
c++ -O3 -std=c++17 "$c/eleven_leaf_cuts.cpp" -o "$out/cuts"
c++ -O3 -std=c++17 "$c/check_eleven_leaf_cuts.cpp" -o "$out/check-cuts"
"$out/cuts" "$out"
"$out/check-cuts" "$out"
c++ -O3 -std=c++17 -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 "$r/spine_generate.cpp" "$r/leaf_search.cpp" "$out/ref.o" -o "$out/generate"
c++ -O3 -std=c++17 -pthread "$r/spine_verify.cpp" -o "$out/verify"
"$out/generate" 27 0 1 "$out/proof.spn" --listed-cover < "$out/words-54"
"$out/verify" 27 --listed "$out/words-54" "$out/proof.spn"
python3 -B -m research.census.check_eleven_leaf_labels "$out/words-54" "$out/proof.spn"
echo "44c0696970d13362fd1aad964eac1d9bb24dfb76266f19d84a60144a015e66f1  $out/words-54" | shasum -a 256 -c -
echo "d6f1384368d7816daf18b1231a1650fbf2fe7a6d5fe8d4b0af126a55f7b61039  $out/proof.spn" | shasum -a 256 -c -
~~~
