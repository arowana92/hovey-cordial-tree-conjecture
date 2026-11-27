# Replacing an edge by a chain of matched pairs

**Theorem.** Let $k=2m$ for odd $3\le m\le15$. Fix any labeled edge of any tree. Replace it by a chain of $jm$ pairs, $j\ge1$. Each incoming and outgoing link can use either site of its pair. There is a labeling preserving the two old endpoint labels and adding exactly $j$ to every vertex and edge count, **unless** all pairs are traversed between opposite sites and $j$ is odd. In that case the uniform increment is impossible. The old tree's order and labeling are unrestricted.

In particular at 26 labels any 13-pair chain containing a pendant vertex can be suppressed and restored. The conclusion concerns inserting a whole chain into a specified edge. A forest of pairs attached by single bridges has a [different extension theorem](../paired-forest.md).

## Closing the chain

Temporarily identify the old left endpoint with the last outgoing site, and omit the edge to the old right endpoint. The result is a ring of pairs. Its cycle contains one vertex from each pair and one extra vertex for each pair whose ports differ. Every pair with coincident ports supplies one pendant leaf. Write $P$ for the number of traversed pairs. The cycle thus has length $jm+P$. The ring has $2jm$ vertices and as many edges.

It suffices to give the ring a labeling with exactly $j$ copies of every residue in each histogram. Translate all labels together to make its last outgoing label the old left endpoint's label. Cutting the ring open now gives exactly the desired increments: its closing edge becomes the first entering edge with the same weight, and the edge from the last outgoing site to the right endpoint has exactly the removed weight. This construction allows the cyclic starting point to be chosen freely before the labels are translated.

If $P$ is even, [the pair parity construction](../paired-forest.md#replacing-an-edge-by-a-chain-of-pairs) works directly for every odd $m$. If the cycle length is odd, use Barrientos's odd-girth theorem. For completeness, delete the closing edge and use the remaining path as a caterpillar spine. Its two ends are in the same bipartition class $A$ of size $a$. Number the two classes by first appearance in the monotone spine-edge traversal and place $A$ first in the integer labeling. The ends have ranks $0,a-1$. The internal sums are consecutive from $a$ to $a+2jm-2$. The closing edge adds the preceding sum $a-1$. Both integer intervals have length $2jm$, so reduction modulo $2m$ gives the required counts. The same argument includes an ordinary odd cycle. [C. Barrientos, *On additive vertex labelings*, Theorem 3.1](https://www.ijc.or.id/index.php/ijc/article/download/121/83)

Together these two arguments cover **every even $j$**, for every odd $m$, since $jm+P$ is then odd when $P$ is odd. For odd $j$ and a nonbare ring choose the cyclic starting point to put a pair with a leaf in the first $m$ pairs. Label that block as its own ring using the one-period result below. Insert the remaining $(j-1)m$ pairs into its closing edge by the even-period construction. This reconstructs the full ring. Finally, if $j$ is odd and all pairs are traversed, the replacement is an ordinary path subdivision by $2jm$ vertices. The sum of all desired new vertex residues is $jm\bmod 2m$, whereas the net edge sum along a subdivision is twice the internal vertex sum. Uniformity would equate these unequal residues.

## One period and the independent count

The following finite computation handles even girth. At every even order from 10 through 30, every even cycle with a positive number of pendant leaves and at most one leaf per site has a bijective labeling with all edge sums distinct. At orders six and eight there are three exceptions. At six it is the four-cycle with leaves on opposite sites. At eight they are six-cycles with two leaves at distance one or three. The six-vertex exception cannot be a ring of matched pairs: its two leaf neighbors must match to their leaves and the remaining two vertices are nonadjacent. This completes the one-period proof for all the stated odd $m$.

| Order | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Even-cycle shapes | 2 | 4 | 7 | 14 | 26 | 53 | 110 | 237 | 526 | 1,205 | 2,808 | 6,666 | 16,023 |
| Missing labelings | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

For each even cycle length $c$, its $n-c$ leaves specify a binary word of length $c$ up to rotation and reflection. Fix one cycle label to zero by translation. If the cycle labels are $x_i$ and the leaf indicators are $b_i$, subtracting the sum of all vertex residues from the sum of all edge residues gives the necessary check $\sum_i(1+b_i)x_i=0\bmod n$. Backtracking on the cycle labels enforces this equation and rejects repeated weights, then labels the pendant sites. All positive claims have explicit witnesses.

The separate checker reconstructs each edge, checks both permutations, and independently excludes the three negative cases by trying all permutations fixing zero. It rules out duplicate shapes and uses Burnside's lemma for completeness: a rotation fixes a subset only when it is a union of its equal-length cycles, and a reflection allows its fixed sites and its two-element orbits. On the original trees the checker tests all single-period port patterns containing a leaf at every stated modulus, followed by longer random chains, with 44,381 exact increment checks. [Generator](cycle_pendants.cpp) · [Ring and substitution constructors](cycle_pendants.py) · [Independent checker](check_cycle_pendants.py) · [SHA-256 manifest](cycle-pendants.sha256)

~~~bash
set -e
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/cycle_pendants.cpp" -o "$out/generate"
for n in {6..30..2}; do "$out/generate" "$n" > "$out/cycle-$n.txt"; done
python3 -B -m research.census.check_cycle_pendants "$out"
(cd "$out" && shasum -a 256 -c "$src/cycle-pendants.sha256")
~~~

## Bounding the two-exposure case at 26

Suppose some tree with a matching missing at most two vertices is not 26-cordial. Choose a counterexample of minimum order **within this class**. Its order is $26q$, $q\ge2$, and its maximum matching has exactly two exposures, by the [matching-deficiency theorem](../near-matching.md) and the order-26 base. In any maximum matching contract all its pairs, keeping the two exposures as singleton vertices. Let $h$ be the number of pairs on the path between the two singletons, and let $s$ be the number off that path. Thus $h+s=13q-1$.

First $s\le12$. Otherwise remove 13 off-path pairs in child-before-parent order, rooting the off-path forest toward the path. The retained tree is connected and has a matching missing at most two vertices. Its smaller order is divisible by 26, so the [matched forest extension](../paired-forest.md) would restore all the removed pairs. This argument allows the removed forest to attach at several sites.

Mark every path pair supporting any off-path branch. Let $r$ be the number marked, so $r\le s$. A consecutive run of 13 unmarked pairs cannot occur. If any pair in the run has coincident ports, the chain theorem suppresses the 26 vertices and restores them to a smaller tree in the class. If all pairs are traversed, the run consists of 26 consecutive degree-two vertices on the original path. Their incident path edges yield consecutive component orders, so some cut has one side divisible by 26. At any cut in this run, the original exposures are on opposite sides. If a matching edge is cut, each side gains just one new exposure. Otherwise each side has just its single old exposure. Both sides are smaller trees in the class, and the [divisible-cut lemma](../divisible-cuts.md) joins their cordial labelings. The same reasoning applies even if the original exposed vertices are internal rather than leaves.

Hence $h\le r+12(r+1)$. Substitution gives $13q\le 13(r+1)+s$, so $q\le r+1\le13$. In particular **checking the twelve orders $52,78,\ldots,338$ would settle the entire two-exposure case at 26 labels**. At order $26q$ every maximum matching of a least counterexample in the class would have between $q-1$ and 12 distinct path pairs supporting off-path branches, with at most 12 off-path pairs in total. This conclusion applies without assuming all smaller unrestricted trees are cordial.
