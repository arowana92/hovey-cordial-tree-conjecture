# Five omitted residues in a matching at 27 labels

**Theorem (computer-assisted).** Three subsets of $\mathbb Z_{27}$ of the same size $m\ge22$ admit a partition into zero-sum triples, one entry from each set, exactly when their sums add to zero. More generally this holds for three multisets of common size $m$ whenever $m-\sum_i(m-|\operatorname{supp}M_i|)\ge22$.

For $m=22$ the verifier checked all **247,768,822** normalized orbits. Every set has a unique translate of sum zero since 22 is invertible modulo 27. The three centering translations sum to zero on compatible inputs. The complements are the $\binom{27}{5}/27=2,990$ five-element sets of sum zero. Multiplying all three sets by a common unit and permuting their order preserves zero-sum triples. Before taking these symmetries and translations there are $2,990^3\cdot27^2=19,486,825,371,000$ ordered compatible inputs. The multiset and larger-set assertions follow by [deleting one compatible triple at a time](four-hole-matchings.md#from-sets-to-prescribed-repeated-labels). This improves the explicit threshold at 27 in the finite matching question of Müyesser and Pokrovskiy. [Problem 7.4 in the primary paper](https://doi.org/10.1007/s00222-025-01328-x)

## Ordinary trees near two periods

Let $L$ count the leaves of a tree and $P$ their different parents. Each of the following rows guarantees 27-cordiality.

| Order | Leaves | Required parents |
| ---: | :--- | :--- |
| 52 | 21, 22 or 23 | $P\ge21$ |
| 53 | 22, 23 or 24 | $P\ge22$ |
| 54 | 23, 24 or 25 | $P\ge23$ |

In particular a 52-vertex counterexample with 23 leaves would have **eight through twenty** different parents. [Lower bound on the parent count](seven-shift-lists-27.md)

Delete the exterior leaves to leave a tree $H$ of order $27+h$. Call their parent sites active. Every leaf of $H$ is active. In the table $2\le h\le4$. Prune $h-1$ vertices one leaf at a time to leave a connected 28-vertex subtree $D$. When at least two vertices are pruned, the first two can be different original leaves of $H$. Label $D$ cordially using the [known order-28 result](../census/order-fifty-one.md). Its weights are uniform and a single vertex residue $u$ occurs twice. Write $j$ for the number of pruned active sites. There are at least $28-P+j-2$ singly occurring labels on inactive vertices of $D$. Restoring a vertex with one of these labels doubles that vertex bin. Require its new edge weight to differ from the previously doubled weights. For the rows at orders 52 and 53 the initial pool has more than $2(h-2)$ choices in every case, using $j\ge\min(2,h-1)$ and $P\le L$. Indeed, at the closest case $h=4$ one has $P\le22$, hence at least six choices. Each addition excludes at most $h-2$ already used labels and $h-2$ used weights. The resulting cordial core has shift excess $e=L-|\operatorname{supp}S|\le L-P+1$, since only $u$ could occur at two active vertices. Thus $h+e\le5$. At these orders $L<27-h$, so the [fixed-core padding argument](four-hole-matchings.md#leaves-on-a-fixed-cordial-core) with $b=22$ restores all leaves.

At order 54 the final missing edge residue also matters. Choose the first pruned vertex $v$ to be a leaf of $H$ with a single exterior child if possible. When $L-P\le1$ at least one such leaf exists. Otherwise the only new case is $(L,P)=(25,23)$, and $v$ has $1\le c\le3$ children. Restore $v$ last. Before $v$, choose labels for returning active sites from the singly occurring labels at inactive sites of $D$. For returning inactive sites, use singly occurring labels at active sites of $D$. In both pools avoid earlier choices and previously doubled weights. There are at most two additions before $v$. When there are two, $P=L=23$ and $j\ge2$, so the smaller pool of inactive-site labels has at least five entries. When there is one, $P\le24$ and $j=2$, giving at least four. The active-site pool has at least $P-j-2\ge18$ entries.

Just before $v$, denote the high vertex and weight sets by $U_0,W_0$, its parent's label by $p$, and the exterior shifts other than those contributed by $v$ by $S_0$. For a low vertex label $a$ at $v$ the new weight is $p+a$, and the required missing residue is
$$
z=\sum U_0-\sum W_0-p-\sum S_0-ca .
$$
Exclude choices giving $p+a\in W_0$, $z\in W_0$, or $z=p+a$. For $c=1$ this excludes at most $2(h-2)+1$ values because 2 is invertible. For $c>1$ we have $h=2$, so $W_0$ is empty and at most $\gcd(c+1,27)\le3$ values are excluded.

If both copies of $u$ are active in $D$, all $28-P+j$ inactive sites there have singly occurring labels. Earlier active additions use exactly $j-1$ of those labels. The remaining $29-P$ choices exceed the exclusions in each row, and keep the shift excess at most $L-P+1$. If at most one copy of $u$ is active in $D$, the active sites before $v$ have distinct labels. Any low residue at $v$ creates at most one duplicated active-site label, and there are $27-(h-1)$ low choices. This gives $h+e\le5$ and $z$ outside the final high weights. The full-size fixed-core criterion restores the leaves.

## One fewer parent when the stripped tree has few leaves

**Theorem.** Delete all leaves of $T$ once and call the resulting tree $H$. A vertex of $H$ is active if it bore a deleted leaf. In each row below, the stated number of distinct parents suffices when $H$ has at most seven leaves.

| Order of $T$ | Leaves of $T$ | Required parents |
| ---: | :--- | :--- |
| 52 | 21, 22 or 23 | $P\ge20$ |
| 53 | 22, 23 or 24 | $P\ge21$ |
| 54 | 23, 24 or 25 | $P\ge22$ |

At orders 52 and 53 there are two further criteria at the same parent bound. Write $|H|=27+h$, $h\in\{2,3,4\}$. It suffices that an inactive vertex belong to the side of an edge of $H$ of order at most $h$, as the endpoint incident to that edge. Also, when $h\ge3$ it suffices that $H$ have at most **eight** leaves. In particular a 52-vertex counterexample with exactly twenty leaf parents and 21 or 22 leaves would have at least nine leaves after stripping.

It suffices to consider exactly the indicated $P$, since the higher values are covered above. First consider orders 52 and 53. We seek a connected 28-vertex subtree $D$ with a cordial labeling whose unique surplus label $u$ occurs at some inactive vertex. If $D$ has an inactive leaf, delete that leaf, give its 27-vertex complement a rainbow bijection, and restore the leaf using the missing weight. The restored leaf carries the surplus. The small-side criterion supplies such a $D$ by taking the inactive endpoint and any connected 27 vertices in the opposite side containing its neighbor.

If $D$ has at most seven leaves, select any inactive vertex $v$ in $D$, available since $P<28$. Start with $v$ and restore the forest $D-v$ at that one site. The 27 new vertices have at most seven rooted tips. The common-site period theorem adds each label and each weight exactly once, putting the surplus at $v$. If $H$ itself has at most seven leaves, pruning to any connected $D$ preserves this upper bound. [Common-site period at 27](../bounded-degree/prescribed-pair.md)

Suppose $H$ has eight leaves and $h\ge3$. If a terminal path from a leaf to its first branching vertex has length at most $h-1$, remove its vertices up to but excluding the branching vertex. This reduces the leaf count to seven. Finish pruning to order 28. Otherwise the first $h$ vertices along each of the eight paths are disjoint, and each is the endpoint of a pendant side of order at most $h$. There are $8h>P$ such vertices, so one is inactive. This proves the eight-leaf assertion.

Let $j$ of the $h-1$ pruned vertices be active. In $D$ there are at least $28-P+j-2$ single labels at inactive sites and at least $P-j-2$ at active sites. At least one pruned vertex is an original leaf of $H$, hence active. Both pools have more than $2(h-2)$ members. Restore the pruned vertices parent-first. At an active site use a single label from the inactive pool, and at an inactive site use a single label from the active pool. Avoid any label already used in restoration and any choice repeating a newly doubled edge weight. Each exclusion costs at most $h-2$ choices. Thus the restored core is cordial and its $P$ active sites have **distinct** labels. The shift excess for the exterior leaves is $L-P$, where $L$ is their number. At order $n$ one has
$$
h+L-P=n-27-P=5.
$$
The five-hole theorem and the [fixed-core padding argument](four-hole-matchings.md#leaves-on-a-fixed-cordial-core) restore all the actual leaves.

### The final missing weight at order 54

Here $P=22$. Assume $H$ has at most seven leaves. First prune a leaf $w$ of $H$, to be restored last, with as few exterior children as possible among such leaves. Let their number be $c$. When $h=4$ there is only one extra exterior child beyond one per active site, so $c=1$. For $h=3$ there are two extras and $c\le2$. For $h=2$ the crude bound $c\le4$ suffices. Prune another $h-2$ vertices arbitrarily to reach $D$.

We can arrange that the two surplus vertices in $D$ are **one active and one inactive**. At most $j\le3$ inactive vertices are leaves of $D$, since each such leaf has a disjoint pruned branch containing an active leaf of $H$. Thus at least $(28-P+j)-j=6$ inactive vertices are internal in $D$. If $D$ has two or three leaves, its maximum degree is at most three. The radius-two ball about an inactive internal vertex has at most ten vertices, while at least $P-j-3\ge16$ active vertices are internal. Choose a distant active internal vertex, leaving two or three leaves outside the pair.

If $D$ has four through seven leaves, at least one is active. Some active leaf has distance at least three from some inactive internal vertex. Otherwise the inactive internal vertices are all in the closed neighborhood of the parent of every active leaf. Closed neighborhoods of distinct vertices in a tree intersect in at most two vertices. Thus all active leaves have the same parent $p$. At least five inactive internal neighbors of $p$ would then have distinct branches beyond them ending in inactive leaves, contradicting the bound of three. With the distant pair chosen, three through six leaves lie outside it. The [finite prescribed-pair theorem](../bounded-degree/prescribed-pair.md) at distance at least three supplies the desired simultaneous surplus labels in both cases.

Use the opposite-site pools as before until only $w$ remains. Each doubled label currently occurs at an active vertex, and the 21 already present active sites have distinct labels. Thus the six residues absent at those sites are all low vertex labels. Choosing any of them at $w$ also preserves distinctness of the active labels. Let $p$ be its parent's label and write $W_0$ for the $h-2$ previously doubled weights. For a proposed label $x$, the last doubled weight would be $p+x$ and the forced final deficient weight has the form $z=C-cx$. This follows by substituting the last vertex and edge and the $c$ copies of its shift into $z=\sum U-\sum W-\sum S$.

Avoid $p+x\in W_0$, $z\in W_0$ and $z=p+x$. The number of excluded choices is at most
$$
(h-2)(1+\gcd(c,27))+\gcd(c+1,27).
$$
For $h=4,c=1$ this is five. For $h=3,c\le2$ it is at most five. For $h=2,c\le4$ it is at most three. One of the six choices places $z$ outside the final high weights. The fixed-core criterion now applies at full size with $h+L-P=5$.

The [whole-tree checker](check_stripped_core_parents.py) uses 975 matching orbits and constructs 976 trees at the three new parent thresholds. It includes inactive leaves and inactive internal sites, restored paths with inactive intermediate vertices, and final sites with up to four exterior children. It recomputes the leaf and parent counts and all vertex and edge frequencies from the physical tree. With the five-hole generator built below, run

~~~bash
python3 -B -m research.biased.check_stripped_core_parents "$out/generate"
~~~

## Reproduction

The generator writes the three centered-complement indices and 22 assigned vertex labels per row. The independent verifier recomputes the complementary sets and checks every endpoint sum and each used residue. For each shard it combines strict canonical order with an independent orbit count from the unit permutations' cycles. The [176 shard receipts](five-hole-matchings.sha256) cover every possible first index. To regenerate all witnesses with bounded scratch space, run the following from the repository root in Bash.

~~~bash
set -euo pipefail
out=$(mktemp -d)
r=research/biased
c++ -std=c++17 -O3 -DOMITTED_RESIDUES=5 "$r/four_hole_matchings.cpp" -o "$out/generate"
python3 -B -m research.biased.check_four_hole_matchings --holes 5 --manifest "$r/five-hole-matchings.sha256"
while read -r _ interval _; do
    lo=${interval%..*}
    hi=${interval#*..}
    "$out/generate" "$lo" "$hi" | python3 -B -m research.biased.check_four_hole_matchings \
        --holes 5 --low "$lo" --high "$hi"
done < "$r/five-hole-matchings.sha256" > "$out/actual"
cmp "$out/actual" "$r/five-hole-matchings.sha256"
python3 -B -m research.biased.check_four_hole_trees "$out/generate" --holes 5
~~~

The tree replay inverts the centering translations, common unit and shore permutation. It verifies actual endpoint-sum histograms on 2,733 trees, including 720 with controlled core labels at orders 52 and 53 and 480 with the gap tuned at order 54. It also checks 270 multiset instances and 27 forced collisions for fixed labelings. The universal matching assertion uses the full census.
