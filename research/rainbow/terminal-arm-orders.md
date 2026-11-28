# Depth-first orders on trees with long terminal arms

A terminal arm runs from an original leaf to the first vertex of degree at least three. Its length is its number of edges. Count its vertices from the leaf up to, and excluding, the branching vertex. Different arms are disjoint in this convention. Paths can be handled separately by the prescribed-order theorem for trees with few leaves.

**Theorem at 27 labels.** If a tree has at least four leaves and its four shortest terminal arms have total length at least 24, then every depth-first preorder admits one 27-cordial labeling on all its prefixes. Choose any root, any ordering of the children at each vertex, and any label at the root. In particular, six edges per terminal arm suffice, with unrestricted branching elsewhere and any number of leaves.

## What a preorder interval contains

Root a tree with at least three leaves anywhere. Let a consecutive interval of its preorder exclude the root. Its induced forest is oriented away from the root. Write $t$ for its order, $b$ for its number of rooted tips, and $a_1\le\cdots\le a_L$ for all original terminal-arm lengths. For $b\ge2$,

$$
                      t\ \ge\ 2+\sum_{j=1}^{b-2}a_j .
$$

In equality the forest consists of $b$ paths rooted at endpoints. Its first and last tips are singleton components.

Indeed, every tip except possibly the final interval vertex is an original rooted leaf. The next vertex after any nonleaf in preorder is its first child. Consider a tip strictly between the first and last tips. Unless the root is on its terminal arm, the arm is an unbranched downward path. The traversal visits the entire arm consecutively, ending at the tip. An earlier tip in the same interval lies outside the arm, so the whole arm belongs to the interval. If the root is on that arm, the segment from the root toward its leaf is either its first child subtree or its last. The leaf of this segment is therefore the first or last original rooted leaf in the entire preorder. In the last case it is the final vertex. In the first case no earlier interval tip can precede it. A root which is itself an original leaf is excluded from the interval.

This gives $b-2$ complete, disjoint arms and the two other tip vertices. In equality they account for every interval vertex. Each of those arms has its parent end outside the interval. Its branching parent could coincide with neither the first tip, an original leaf, nor the last tip, which occurs later. The two remaining vertices cannot be adjacent because the earlier is a rooted leaf. This proves the equality statement.

## Applying the interval bound

For an interval of length at most 26 the hypothesis rules out seven or more tips. Six tips force equality with $t=26$. With at most five tips, the prescribed-boundary theorem gives distinct new labels avoiding any surplus residue and distinct edge weights including the entering edges. With six tips the independently prescribed path theorem gives the same conclusion. [Five-tip theorem](prescribed-five-tips-27.md) · [Six independent paths](../census/ring-order.md#terminal-paths-with-independently-prescribed-parents)

Starting from the chosen root label, take the next 26 vertices, or as many as remain. These distinct labels fill previously low vertex bins while the distinct weights start from uniform edge bins. Every initial segment is cordial. At divisible order the next vertex takes the unique label that fills the deficient edge bin. Repeat with the next interval. A short batch with at most five tips can be padded by extending a tip and restricted after labeling. The same proof preserves any fixed cordial prefix of order zero or one modulo 27 in the given preorder. It also allows arbitrary independent offsets on edges entering each batch from an earlier one.

The completed [six-tip independent-boundary theorem](prescribed-five-tips-27.md#six-tips-and-seven-leaf-lifts) also gives every preorder whenever the five shortest arms total at least 25. A batch with seven tips would require at least 27 vertices. This includes the case of five edges on every arm, which has the separate certificate proof below.

## Five edges on every terminal arm at 27

Every prescribed depth-first order still works when **every terminal arm has length at least five**. Seven tips in a batch would use at least $2+5\cdot5=27$ vertices. In a batch with six tips the four middle tips carry four disjoint pendant chains of at least five vertices. Extend any tip to pad the forest to 26 vertices. Delete the last four vertices from each of those four chains. This leaves a forest on ten vertices with six tips. Reversing the operation lists every possible padded forest needed in the proof.

The [checker](check_five_edge_arms.py) enumerates all such ten-vertex forests by adjoining a dummy root, and tries each choice of four tips. It independently enumerates their component orders and tip counts by partitions, allocating the four extensions by component. Both methods yield the same profiles. There are 2,437 possible padded shapes. With one or two roots the seven-tip results apply, with six roots all components are paths, and the ordered certificate handles the profiles for which all boundary choices are ordered. The other 653 candidate shapes occur in 120 profiles. The [supplementary certificates](five-edge-arm-profiles-27.sha256) test every shape in those profiles, including arbitrary colors on equal-sized components.

| Components | Profiles | Forests tested | Witness rows | Literal boundary assignments |
|---:|---:|---:|---:|---:|
| 3 | 27 | 232,720 | 42,929,375 | 4,580,627,760 |
| 4 | 56 | 21,781 | 29,445,794 | 11,575,316,421 |
| 5 | 37 | 644 | 5,194,086 | 9,240,696,108 |

The same fixed-core and entering-offset conclusions follow. For a full replay, use the generator, verifier and shared library built in the [independent-root reproduction](prescribed-five-tips-27.md#independent-checks-and-reproduction).

~~~bash
file=research/rainbow/five-edge-arm-profiles-27.sha256
awk -F '  ' '{print $3}' "$file" > "$out/arms.profiles"
python3 -B research/census/stream_leaf_profiles.py 27 "$out/arms.profiles" "$out/generate" "$out/verify" "$out/arms" --independent-roots --workers 2
cmp "$file" "$out/arms/manifest.txt"
python3 -B -m research.rainbow.check_five_edge_arms "$file" "$out/search.so"
~~~

The whole-tree check recounts 3,950 growth steps on 41 orders. One test places a six-tip batch with five components and a fork exactly at a block boundary.

## Arbitrarily large moduli

**Theorem.** Fix $0<\alpha,\beta<1$. At every sufficiently large modulus $k$, if all but at most $k^{1-\beta}$ terminal arms have length at least $k^\alpha$, every depth-first preorder has a single $k$-cordial labeling on all its prefixes. Both the tree order and the number and degrees of its branching vertices are unrestricted.

In an interval of at most $k-1$ vertices, at most $k^{1-\beta}$ of the complete middle arms can be short. At most $(k-1)/k^\alpha$ can be long. Thus $b\le 2+k^{1-\beta}+k^{1-\alpha}$. In a rooted forest with $c$ components and child counts $d_v$, summing $d_v-1$ gives

$$
                  c+\sum_v(d_v-1)_+=b .
$$

The degree in the forest counting one incoming edge is $1+d_v$. Hence its degree excess above three, plus $c$, is at most $b$. Padding by extending a tip keeps this bound. For large $k$ it is at most $k^{1-\min(\alpha,\beta)/2}$. The prescribed-boundary forest lemma now supplies the distinct labels and weights in every batch, and the same induction proves the theorem. Paths have at most two tips per interval and obey the same proof. [Degree-excess forest lemma](../bounded-degree/excess.md#forest-lemma) · [Müyesser and Pokrovskiy, Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4)

There is also a local consequence. In an ordinary counterexample at sufficiently large $k$, **every** depth-first preorder contains an interval of at most $k-1$ vertices containing more than $k^{1-\beta}$ complete terminal arms of length less than $k^\alpha$. Otherwise the same estimate would hold in every batch of that preorder. With arbitrary offsets on entering edges the proof is identical, since only the effective boundary labels change.

## Independent checks

The checker enumerates every plane rooted tree through order ten in preorder. It reconstructs the original unrooted arms and checks all 183,768 intervals with multiple tips on branching trees, including 42,635 equalities. On 121 larger depth-first orders it checks 428,311 intervals, including an explicit 26-vertex equality with six tips, then recounts the vertex and edge bins on 17,986 growth steps. On 41 of the orders it repeats the count with independent offsets on entering edges at 6,038 growth steps.

Run in Bash from the repository root.

~~~bash
set -eu
out=$(mktemp -d)
r=research/rainbow
c++ -O3 -std=c++17 -fPIC -Drainbow_witness=reference_witness -c "$r/search.cpp" -o "$out/ref.o"
c++ -O3 -std=c++17 -fPIC -shared "$r/leaf_search.cpp" "$out/ref.o" -o "$out/search.so"
python3 -B -m research.rainbow.check_terminal_arm_order "$out/search.so"
~~~
