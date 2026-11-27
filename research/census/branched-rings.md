# One order remains for matching deficiency two at 26 labels

**Theorem.** If a tree with a matching missing at most two vertices fails to be 26-cordial, a smallest such tree has exactly **52 vertices**. In every maximum matching of that tree, the path between the two exposed vertices meets 13 through 18 matched pairs, with 7 through 12 further pairs off the path. Thus an order-52 test restricted to these trees would settle the entire matching-deficiency-two case. The unrestricted 26-label problem also includes trees of larger deficiency.

The additional finite ingredient is a substitution at a specified edge. Insert a chain of $13-b$ matched pairs between its two ends, and attach $b$ further matched pairs by single edges anywhere in the inserted tree, parent before child. For $1\le b\le6$, **every such insertion preserves the two endpoint labels and adds exactly one to each of the 26 vertex and edge counts**. The zero-branch case, including its pure-path exception, follows from the [paired chain theorem](cycle-pendants.md).

## Dividing the path into complete blocks

Choose a counterexample of minimum order among all trees with matching deficiency at most two. The [matching theorem](../near-matching.md) and the order-26 base require its order to be $26q$ with $q\ge2$ and its deficiency to be exactly two. Fix any maximum matching. Contract its pairs, and consider the path between the two exposed vertices. Write $h$ for the number of pairs on it and $s$ for the number off it. Hence $h+s=13q-1$. We have $s\le12$, since otherwise pruning 13 off-path pairs in child-before-parent order leaves a connected smaller tree in the class and the [matched forest theorem](../paired-forest.md) restores them.

Join the two exposed vertices by a temporary matching edge and regard them as a single distinguished pair. The path pairs and this extra pair now form a circular list. At each position include every off-path pair in the branches hanging there. A position with $w$ off-path pairs has mass $1+w$. The total mass is $13q$. This also assigns branches at either exposed vertex to the distinguished position.

Lay the positions on a circle of $13q$ unit intervals. Of the $13q$ integer boundaries, exactly $s$ lie strictly inside positions. As $s<13$, some residue modulo 13 contains no such boundary. Cut at **all** boundaries of that residue. The $q$ resulting blocks each have mass 13 and consist of whole positions. Exactly one contains the distinguished pair. Each other block is an ordinary two-ended subtree of the original tree, with one entering and one exiting edge. Its side branches are all internal to the block.

A block avoiding the distinguished pair cannot contain between one and six off-path pairs, by the substitution theorem below. Suppressing it leaves a smaller connected tree with the same two exposed vertices and a matching on the retained pairs. A block with no off-path pair is also impossible. If some pair's two ports coincide, the [chain substitution](cycle-pendants.md) works. Otherwise the block has 26 consecutive degree-two vertices. Cutting successive incident path edges gives consecutive component orders, one divisible by 26. Both sides have deficiency at most two, since each contains one original exposure and the cut destroys at most one matching edge. The [divisible-cut theorem](../divisible-cuts.md) joins the smaller cordial trees.

Consequently each of the $q-1$ ordinary blocks uses at least seven distinct off-path pairs. This gives $7(q-1)\le s\le12$, forcing $q=2$. Then $h=25-s$, proving the stated restrictions. The argument works for every maximum matching and every admissible residue for the cuts.

## Certifying the two-ended subtrees

Close the chain of pairs by joining the last outgoing site to the first incoming site. The resulting graph has 26 vertices and 26 edges. The $b$ off-path pairs can be grown one by one as pendant paths of length two attached at any existing vertex. Conversely, these operations produce every closed block needed in the proof. The cycle has length at least $13-b\ge7$.

Give the closed graph a bijection onto the residues with all 26 edge weights distinct. Translate all its labels until its last outgoing site has the label of the old left endpoint. Cutting the closing edge and attaching the chain makes its entering edge reproduce the closing weight, and the final link reproduces the removed edge weight. Thus the increments are uniform for every initial labeling.

| Off-path pairs $b$ | Graphs up to isomorphism | Verified bijections |
| ---: | ---: | ---: |
| 1 | 4,160 | 4,160 |
| 2 | 28,091 | 28,091 |
| 3 | 127,725 | 127,725 |
| 4 | 443,944 | 443,944 |
| 5 | 1,241,271 | 1,241,271 |
| 6 | 2,877,385 | 2,877,385 |

Each record represents the cycle by a list of rooted trees at its sites. Balanced parentheses encode each tree with its children in sorted order. Rotation and reflection select the least list. The [generator](branched_rings.py) starts with all port patterns and adds the pendant pairs. The [label search](branched_search.cpp) assigns internal vertices before leaves, pruning when the necessary moment $\sum_v(\deg v-1)f(v)=0\pmod{26}$ fails. Only explicit successful bijections are used.

The [independent verifier](check_branched_rings.cpp) reads each record, checks canonical form and strict ordering, reconstructs the 26 edges, and checks both permutations. It also determines which sites must match on the cycle. In a rooted decoration, a vertex with no child waiting for a mate needs its parent, while a vertex with one such child matches it. Two waiting children preclude a matching. The waiting cycle sites must occur in even runs between internally matched sites, or fill an even cycle. If $c$ is the cycle length and $o$ its number of waiting sites, precisely $c-o/2$ central pairs are required.

## Independent orbit count

Let $F_t$ count rooted trees on $2t+1$ vertices whose root is exposed and whose other vertices match internally. Let $M_t$ count perfectly matched rooted trees on $2t+2$ vertices. The children of a free root form a multiset of matched trees. A matched root instead has one free child and the same multiset of matched children. The child's odd order distinguishes it. Thus, writing $F(z)=\sum_t F_tz^t$ and $M(z)=\sum_t M_tz^t$,
$$
F(z)=\prod_{j\ge0}(1-z^{j+1})^{-M_j},\qquad M(z)=F(z)^2.
$$
These equations determine successive coefficients starting with $F_0=M_0=1$.

For a ring with $l=13-b$ central pairs, a nontraversed pair supplies one matched rooted tree, with generating function $M$. A traversed pair gives two ordered free sites, again counted by $F^2=M$. Reflection fixes every nontraversed symbol and exchanges the two free sites of a traversed symbol. The latter fixed symbols are counted by $F(z^2)$. If there is any nontraversed pair, the matching of the intervening free sites is forced. In an entirely free cycle there are two cyclic pairings. Count bracelets of all pair symbols, subtract bracelets using only traversed symbols, then add ordinary bracelets of $2l$ individual free sites. This counts the graphs themselves once each.

The [orbit calculation](branched_count.py) applies Burnside's lemma and takes the coefficient of $z^b$. A permutation orbit of length $d$ uses its symbol polynomial at $z^d$. A fixed site of a reflection allows only a reflection-fixed symbol. The six independent counts agree with all 4,722,576 checked records.

## Reproduction

Run from the repository root in Bash. The witness streams are regenerated locally. The manifest pins their exact bytes.

~~~bash
set -euo pipefail
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/branched_search.cpp" -o "$out/search"
c++ -O2 -std=c++17 "$src/check_branched_rings.cpp" -o "$out/check"
for b in {1..6}; do
    python3 -B "$src/branched_rings.py" 13 "$b" "$out/input"
    "$out/search" < "$out/input" > "$out/witness$b.txt"
    count=$("$out/check" "$b" < "$out/witness$b.txt")
    echo "$b $count" >> "$out/verified"
done
python3 -B "$src/branched_count.py" > "$out/expected"
diff -u "$out/expected" "$out/verified"
(cd "$out" && shasum -a 256 -c "$src/branched-rings.sha256")
~~~
