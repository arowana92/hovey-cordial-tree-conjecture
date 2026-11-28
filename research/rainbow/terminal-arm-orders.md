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
