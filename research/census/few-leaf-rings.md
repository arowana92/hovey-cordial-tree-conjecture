# Replacing an edge by a tree with a few side leaves

**Finite theorem.** For $11\le k\le30$, every simple connected unicyclic graph on $k$ vertices with two or three leaves has a bijection to $\mathbb Z_k$ whose $k$ edge sums are also a bijection. At even $k$ in this range the same holds with one leaf. At $k=26,27$ it also holds with four or five leaves. Pendant trees may have arbitrary shapes. The independent certificate checks cover 23,965,635 graphs.

| Number of leaves | Orders tested | Nonisomorphic graphs |
|---:|---|---:|
| 1 | Even orders from 12 to 30 | 180 |
| 2 | 11 through 30 | 20,240 |
| 3 | 11 through 30 | 603,596 |
| 4 | 26 and 27 | 2,093,931 |
| 5 | 26 and 27 | 21,247,688 |

These bijections are harmonious labelings of unicyclic graphs. Barrientos proves the odd-girth case for cycles with pendant edges, and Barrientos and Minion give constructions from trees with $\alpha$-labelings. The finite check here groups graphs by leaf count and allows branching in the attached trees. [Barrientos, Theorem 3.1](https://www.ijc.or.id/index.php/ijc/article/download/121/83) · [Barrientos and Minion, section 3](https://www.ejgta.org/index.php/ejgta/article/download/1200/pdf_184)

## Restoring a piece between two retained vertices

Let $uv$ be any cycle edge of a graph in the theorem. Replace an edge $ab$ of any labeled tree by the opened graph, attaching $a$ to $u$ and $v$ to $b$. Translate the graph labels until $v$ has the label of $a$. Translation permutes both lists of residues. The new edge $au$ has the former sum on $vu$, and $vb$ has the deleted sum on $ab$. Thus **every vertex and edge frequency increases by one**. A smaller cordial tree gives a cordial labeling of the restored tree at any old order and with either orientation of the ports.

Equivalently, remove two edges of a proposed smallest counterexample. Suppose the component between them has order $k$, its two boundary vertices are at distance at least two within the component, and the component contains $q$ original leaves. Closing the path between its boundary vertices by an edge makes a simple unicyclic graph with exactly $q$ leaves. For the values of $(k,q)$ above the piece is impossible in a minimum counterexample. Replacing it by a single edge between the retained endpoints gives a smaller tree to which the preceding construction applies.

With one side leaf the parity distinction is necessary. For any such period insertion, let the tip label be $y$ and the degree-three joint label $x$. Summing net edge weights by vertex incidence gives $2S+x-y$, where $S$ is the sum of all residues. Uniform edge increments require $y-x=S$. At odd $k$, $S=0$ and a bijection would give the same label to two different new vertices. With zero side leaves the direct cycle labels $0,1,\ldots,k-1$ work at odd $k$, since doubling permutes the residues.

## Odd numbers of sheets

For any connected $d$-sheeted graph cover of a bijectively labeled unicyclic graph of order $k$, **odd $d$ suffices** for a bijective vertex and edge labeling modulo $kd$ reducing to the original labels modulo $k$. Number sheets along a spanning tree so its matchings preserve the index $i$. The remaining matching is a single cycle on the sheets by connectedness, so a common renumbering makes it $i\mapsto i+1$ modulo $d$. For base label $x\in\{0,\ldots,k-1\}$ give sheet $i$ the label $x+ki$. On a base edge the low weight is fixed. The high digit runs through $2i+t$ modulo $d$, with fixed $t$ from the carry and a possible sheet shift. These high digits exhaust the fiber. Consequently opening any cycle edge of the cover gives a uniform insertion even when $k$ and $d$ have common factors. For even $d$, a labeling lifting the fixed low labels cannot have both bijections. The high digits on each intact edge fiber would have sum $d/2$ modulo $d$, whereas the two sums of endpoint high digits and the repeated carry add to zero. This argument concerns the graph with the closing edge present. [Related construction with prescribed offsets](../biased/cyclic-covers.md)

## Catalog completeness and reproduction

A cycle site carries an unordered rooted forest. The generator enumerates the children in sorted order and chooses the least cyclic list of sites among all rotations and reflections. The independent checker recursively parses every site, checks these order conventions, counts the graph's actual leaves and checks the two full permutations. It rejects duplicate shapes and compares totals **at each cycle length** to an independent Burnside count. For that count a rooted tree is either a single tip or a root over a nonempty forest. Taking multisets of $r$ available types of size $a$ and tip count $b$ multiplies the forest series by $(1-X^aY^b)^{-r}$. A cycle symmetry with site-orbit lengths $d_i$ fixes the coefficient of $X^{k-c}Y^q$ in $\prod_i F(X^{d_i},Y^{d_i})$, where $c$ is the cycle length and $F$ counts forests. Averaging over the $2c$ symmetries counts the bracelets.

On the first witness for each nonempty cycle-length class, the checker also tries every oriented cut edge and all differences of old endpoint labels. It counts the actual increments after subtracting the deleted edge, then checks complete three- and five-sheeted covers. [Generator](few_leaf_rings.py) · [Burnside count](count_few_leaf_rings.py) · [Independent verifier](check_few_leaf_rings.cpp) · [Stream hashes](few-leaf-rings.sha256)

Run from the repository root in Bash. A separate SSH checkout regenerated the first 52 streams, for one through four leaves, matching every hash and verifier total. For five leaves the independent checker verified 8,581,063 graphs at 26 and 12,666,625 at 27, matching the independent counts in all 39 nonempty cycle-length classes. The streams may be checked one at a time.

~~~bash
set -euo pipefail
src="$PWD/research/census"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/branched_search.cpp" -o "$out/search"
c++ -O3 -std=c++17 "$src/check_few_leaf_rings.cpp" -o "$out/check"
cd "$out"
while read -r digest name; do
    IFS=- read -r prefix k tail <<< "$name"
    q=${tail%.txt}
    python3 -B "$src/few_leaf_rings.py" "$k" "$q" | ./search "$k" > "$name"
    python3 -B "$src/count_few_leaf_rings.py" "$k" "$q" > counts.txt
    ./check "$k" "$q" counts.txt < "$name"
    echo "$digest  $name" | shasum -a 256 -c -
done < "$src/few-leaf-rings.sha256"
~~~
