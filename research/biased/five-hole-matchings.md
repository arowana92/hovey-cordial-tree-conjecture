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
