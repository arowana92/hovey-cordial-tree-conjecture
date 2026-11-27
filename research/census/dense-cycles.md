# Cycles with prescribed holes at 26 and 27 labels

**Finite theorem.** For $k=26,27$ and every $1\le h\le6$, let $X,Y\subseteq\mathbb Z_k$ have size $h$. The complement of $X$ admits a cyclic ordering whose adjacent sums are precisely the complement of $Y$ **if and only if**
$$
\sum Y=2\sum X-S,\qquad S=\sum_{x\in\mathbb Z_k}x .
$$
This certifies the near-period forest-and-subdivision theorem explicitly at these two moduli for all six sizes. At 26 labels every attached forest of $h$ free vertices can be combined with $26-h$ subdivisions at any old edge, preserving any old labeling and increasing every count by one. At 27 labels the only exception to the corresponding assertion is a two-vertex path with the old edge weight twice the old path parent's label. These are ordinary endpoint sums.

Summing the cycle weights proves necessity. For sufficiency the generator visits each vertex-hole set up to $x\mapsto ux+t$ for units $u$. For each representative it searches every compatible weight-hole set. A translation of vertices translates weights by $2t$, so this reduction covers all actual pairs. The verifier checks the two sets in every cycle by recounting all its vertices and actual cyclic sums. It expands the vertex orbits and excludes duplicates. Independently, a subset recurrence counts the sets of each size and residue sum. Their counts give both the required coverage for each representative and the total number of compatible pairs.

| $k$ | Holes | Vertex orbits | Verified cycles | Compatible pairs before symmetry |
|---:|---:|---:|---:|---:|
| 26 | 1 | 1 | 1 | 26 |
| 26 | 2 | 3 | 39 | 4,225 |
| 26 | 3 | 10 | 1,000 | 260,000 |
| 26 | 4 | 57 | 32,604 | 8,551,400 |
| 26 | 5 | 218 | 551,540 | 166,423,400 |
| 26 | 6 | 767 | 6,800,222 | 2,041,219,180 |
| 27 | 1 | 1 | 1 | 27 |
| 27 | 2 | 3 | 39 | 4,563 |
| 27 | 3 | 9 | 977 | 316,881 |
| 27 | 4 | 44 | 28,600 | 11,407,500 |
| 27 | 5 | 176 | 526,240 | 241,382,700 |
| 27 | 6 | 634 | 6,950,820 | 3,245,256,396 |

## Restoring the forest

Let $c_i$ be the number of free children of vertex $i$. To get compatible holes we need distinct new labels $x_i$ and distinct entering weights $y_i$, with
$$
\sum_i(1-c_i)x_i=S+\sum_{\text{roots }j}p_j ,
$$
where $p_j$ are the old parent labels. The vertex holes of the cycle are the forest labels and its weight holes are the forest weights. If either old endpoint label is outside the vertex holes, traverse the certified cycle from that endpoint through a new copy of it, then recover the removed edge weight on the last edge. Orientation may be reversed. [Cycle insertion proof](two-leaf-padding.md)

If the forest has two or more terminals, reserve two of them and avoid one chosen old endpoint label throughout. Choose the other $h-2$ distinct labels in parent-first order, keeping their weights distinct. Each step excludes at most $2(h-3)+1$ choices. The two remaining labels are $z,R-z$ for a prescribed $R$. Avoiding the old endpoint and previous labels excludes at most $2(h-1)$ choices of $z$; avoiding the previous weights excludes at most $2(h-2)$. Avoiding the two final collisions costs at most four more choices. The total is at most $4h-2\le22<k$. This gives the required holes.

With one terminal the forest is a path. Let $p$ be its old parent; its tip label must be $T=p+S$. A single leaf is covered by the [one-leaf theorem](edge-padding.md). On a path of at least two vertices, first suppose one endpoint of the old edge differs from $T$. Avoid that endpoint and $T$ on the nontip vertices. Choose labels in path order, leaving the penultimate vertex and the tip for last. At the penultimate vertex, the two new weights differ because its predecessor is distinct from $T$. For a two-vertex path this uses $p\ne T$ at the even modulus. Avoiding old labels, the two reserved labels and the earlier weights on both new edges excludes at most $3h-4<k$ choices. The odd two-vertex case is treated below.

If both old endpoints equal $T$, arrange that the forest uses the weight $2T$. At the even modulus begin the path with $p$: this differs from $T$ and the first weight is $2p=2T$. At the odd modulus and length at least three, start with $p+1,p-1$ so the second weight is $2T$. For a three-vertex path at the odd modulus the final weight is $2p-1$, distinct from the first two. A two-vertex path at the even modulus gives $2p$ and $p+T$, also distinct. In other cases choose the remaining vertices by the preceding exclusions, ending at $T$. Now use the cycle with the smaller hole sets $X\setminus\{T\}$ and $Y\setminus\{2T\}$. Their moments still match. Starting at the old $T$ and coming back to it visits all the desired inserted labels; the cycle supplies the deleted edge weight $2T$.

For a two-vertex path at 27, translate $p$ to zero. The tip must be zero and the other label must be the deleted weight $a+b$, since its two forest edges have the same weight. Existence therefore requires $a+b\ne0$. For each of the 364 unordered endpoint assignments satisfying it, the finite path checker actually constructs the insertion and recounts the whole tree. There are 14 impossible assignments. [Whole-tree checks](check_dense_grafts.py)

## Consequences for tree order

At either modulus, subdividing any edge of an $n$-vertex tree by any number at least
$$
k\left\lceil(n-2)/6\right\rceil-(n-2)
$$
suffices. Peel batches of six outside the retained edge. An incomplete last batch of size two need only be used for a four-vertex star, where it consists of two leaves. The path base and the restoration of all batches are detailed in the [near-period argument](near-period.md#tree-consequences).

At 26 labels a smallest counterexample cannot have more than **19 consecutive internal degree-two vertices** on a bare path. Suppress twenty such vertices and delete six more by leaf removals avoiding the retained edge. The established order lower bound of 49 leaves room for this operation. Restoring both operations gives a uniform extension. At 27 labels the same proof bounds a bare run by **20** internal degree-two vertices.

## Reproduction

Run the following from the repository root in Bash. All streams together require about one GiB. The [hash manifest](dense-cycles.sha256) pins the output.

~~~bash
set -eu
out=$(mktemp -d)
src="$PWD/research/census"
c++ -O3 -std=c++17 "$src/dense_cycles.cpp" -o "$out/dense"
for k in 26 27; do
    for h in {1..6}; do
        "$out/dense" "$k" "$h" > "$out/dense-$k-$h.txt"
        python3 -B -m research.census.check_dense_cycles "$k" "$h" "$out/dense-$k-$h.txt"
    done
done
(cd "$out" && shasum -a 256 -c "$src/dense-cycles.sha256")
python3 -B -m research.census.check_dense_grafts "$out/dense"
~~~

The last checker reconstructs 719 complete trees and checks 19 normalized or sampled obstruction cases. The cycle-orbit verification is exhaustive. [Generator](dense_cycles.cpp) · [Independent catalog and cycle verifier](check_dense_cycles.py)
