# Forcing overlaps for two leaf parents

**Theorem at 27 labels.** Suppose a smallest 27-cordiality counterexample has order $27m+s$. At $s=23,24,25$ the combined leaf count at its two busiest leaf parents is at most **16, 18, 20**, respectively. At $s=26,27$ the [unit-label argument](two-shift-holes.md#choosing-the-high-bins-on-the-smaller-tree) gives 23 and 25. The [finite strategy below](#a-stronger-finite-result-at-27-labels) further lowers the first four bounds. All bounds concern freely chosen labelings of ordinary trees.

The first three bounds use a general construction. Fix $k$, write $h=k+2-s$, and suppose $h\ge4$ and $r=2s-k-2=k-2h+2>0$. In a proposed smallest counterexample select $r$ original leaves at two parents $P,Q$. If their distance is at most $mk$, the retained tree has a connected subtree of order $mk+1$ containing both. Start with the path between them and grow it to that order. Label this subtree by minimality and translate its surplus to zero. Write $a,b$ for the two parent colors. If $h\ge5$, if $a=b$, or if $a-b$ has additive order different from five, the entire tree has a cordial labeling. Thus the distance test always applies when $5\nmid k$.

## Three additions to the core

The tree remaining after the leaf deletion has order $mk+h$. Add its other $h-1$ vertices to the labeled subtree in parent-first order. Write $X$ for the high vertex bins and $W$ for the high edge bins. After $i$ additions they have sizes $i+1,i$. For shift $a$, its two forbidden sets overlap in
$$
                         c_a=|(X+a)\cap W|
$$
pairs. Exactly $k-|X|-|W|+c_a$ pairs of this single shift remain available.

At a step with parent label $p$, subtract $p$ from the edge bins and put $Y=W-p$. The new vertex label $y$ must lie outside $X\cup Y$. After the addition, both sets acquire $y$ in these coordinates. Write $t=a-p$. If $t=0$, every allowed choice increases $c_a$. If $t\ne0$, an increase occurs when $y\in (X+t)\cup(Y-t)$. For $c_a=0$ such an increase is always possible. Otherwise $X+t$ would lie in $X$ and $Y-t$ in $Y$, since their intersections across the two sets are empty. Both sets would be invariant under the nonzero shift, whose order would divide both consecutive sizes. This is impossible. Use the first two steps to obtain $c_a,c_b\ge1$, preserving earlier overlaps. With equal colors this one overlap suffices.

For distinct colors, suppose both counts are still one at the third step. Then $|X|=3$ and $|Y|=2$. Call a shift blocked if no allowed $y$ increases its count. For any blocked $t\ne0$, the set $(Y-t)\setminus Y$ lies in $X$ and has size at most one, since $|X\cap(Y-t)|=1$. Write $Y=\{v,v+g\}$. The two translates of $Y$ must intersect, so a nonzero blocked shift belongs to $\{g,-g\}$.

Suppose both $g$ and $-g$ are blocked and distinct. The count-one condition and blockage give $v-g,v+2g\in X$ and $v,v+g\notin X$. In particular $X$ is not invariant under $g$. Also $(X+g)\setminus X\subseteq Y$, and its only possible member is $v$, because $v-g$ already accounts for the one overlap. Hence following $+g$ around its cycles, $X$ has just one nonempty consecutive run besides any entire cycles. The group element $g$ has order at least three, and all of $X$ has size three, so no entire cycle can accompany that run. Its last element is $v-g$. Likewise $(X-g)\setminus X=\{v+g\}$, so the first element is $v+2g$. A run of three then gives $v+4g=v-g$. It follows that $g$ has order five. The two original shifts differ by $2g$, also of order five. Thus one count can be raised to two at the third step unless the two shifts differ by an element of order five.

If both are blocked and $h\ge5$, make any allowed third addition. In the blocked configuration, $X$ consists of three elements of a coset of the order-five subgroup, and $Y$ consists of the remaining two elements of the same coset. The new label is outside it. Now the enlarged high vertex set $X'$ has three elements in that coset and one elsewhere. For *every* nonzero shift $t$, at least two elements of $X'+t$ lie outside $X'$. If $t$ is in the subgroup, it moves the singleton outside itself and does not preserve the three-element subset of a five-cycle. If $t$ is outside the subgroup, it moves three elements into a coset with at most one member of $X'$. At the fourth step this precludes blockage for any target with count one, since the shifted weight set can cover at most one of those elements. The zero shift can increase its count with any allowed addition. This handles the order-five exception whenever a fourth addition is available.

Complete any remaining additions greedily. At step $i\le h-2$ at most $2i+1<k$ labels are forbidden. Overlaps are monotone under these additions. At the final sets $k-|X|-|W|=r-1$. Thus each shift has a matching of size $r$, and at least one has size $r+1$ when the shifts differ. By the [single-edge exchange proof](two-shift-holes.md#proof-by-matchings), all intermediate multiplicities of the second shift occur in matchings of size $r$. Assign these pairs to the original leaves. All added labels and weights fill low bins. At equal shifts take any $r$ allowable pairs.

## A long path between the parents

For modulus 27, the [order-50 theorem](../census/order-fifty.md) ensures $m\ge1$. Suppose the two parents have distance at least $27m+1$ and combined leaf count at least $r=2s-29$. All $r$ selected leaves are outside the path between the parents. Apart from them, at most
$$
              (27m+s)-(27m+2)-r=27-s
$$
vertices are outside that path. For $s=23,24,25$ this is at most four. The path has at least 27 interior vertices. Choose a block of 27 consecutive interior positions. Assign each position weight one plus the total order of all off-path branches attached there. Its total weight is $27+e$ with $0\le e\le4$.

The prefix sums include zero and the total. Exactly $e$ integers are missing between them. The $e+1$ pairs $(i,i+27)$, $0\le i\le e$, have disjoint endpoints. One pair must survive intact, giving a contiguous piece of weight exactly 27 that includes all side branches at the chosen positions. It contains at least 23 path vertices. Cut both exterior path edges and replace the piece by one edge. The smaller tree is cordial by minimality. With zero side leaves, the odd-cycle subdivision restores the piece. With one side leaf use the [one-leaf period theorem](../census/one-leaf-period.md). With two through four side leaves use the [unicyclic replacement theorem](../census/few-leaf-rings.md). All apply with the retained endpoint labels. This excludes the long-distance case and proves the three bounds.

## Verification

The [checker](check_two_parent_overlaps.py) enumerates all three-element vertex sets and all two-element weight sets up to translation at moduli 6 through 22, 27 and 30. Across 346,042 normalized choices it finds 16 simultaneously blocked shift pairs. Every such pair has difference of order five, and it checks the fourth-step escape for every available third label. It separately builds labeled cores, regrows actual trees, finds the leaf labels by a cycle search, and recounts both histograms on 1,810 trees. The corridor check tries all 31,465 allocations of at most four off-path vertices to 27 positions.

~~~bash
python3 -B -m research.biased.check_two_parent_overlaps
~~~

## A stronger finite result at 27 labels

**Computer-assisted theorem.** At residues 23 through 27, the combined leaf count at the two busiest parents of a smallest counterexample is at most **14, 16, 19, 22 and 25**, respectively. In the first four columns a finite strategy labels the additional high bins on a core containing the two parents. The long-path argument above covers all other positions of the parents.

| Order residue $s$ | Leaves $r$ to restore | Core additions $H$ after order one | Required overlap $t$ | Verified states across four differences | Off-path vertices besides the $r$ leaves, in the long-distance case |
|---:|---:|---:|---:|---:|---:|
| 23 | 15 | 7 | 3 | 6,277,872 | at most 6 |
| 24 | 17 | 6 | 3 | 4,363,274 | at most 5 |
| 25 | 20 | 4 | 2 | 32,320 | at most 3 |
| 26 | 23 | 2 | 1 | 85 | at most 1 |

In each row $s=1+H+r$. Remove exactly $r$ leaves at the two parents. When their distance is at most $27m$, choose the initial labeled subtree of order $27m+1$ containing both, as above. Normalize the surplus to zero. Subtract the first parent color $a$ from all edge weights and scale vertex labels and the resulting edge weights by the same unit. The two shifts for the final leaves become zero and $\delta\in\{0,1,3,9\}$. Every effective parent of a new core vertex can have any of 27 values in these coordinates. Indeed, with scale $u$, parent label $P$ and new label $y$ in original coordinates, the scaled weight is $uy+u(P-a)$. Such parents can be among the vertices just added.

At the end of the $H$ additions, $|X|=H+1$, $|W|=H$, and $r=27-2H-1+t$. If the two overlaps reach $t$, each pure shift gives a matching of size $r$. If one reaches $t+1$, the exchange lemma supplies every multiplicity. Equal shifts only require the one overlap of size $t$. These sufficient overlaps persist if achieved early, so any unused labels and weights may complete the remaining steps. There are always available labels since $H\le7$.

There is one further accepting case **at the last step** for distinct shifts when both pure matchings have size exactly $r$. Look at the surviving edges of the two shifts. If the maximum matching has more than $r$ edges, use the exchange lemma. Otherwise both pure matchings are maximum. Every path component with an edge has odd order, since an even-order path would have a unique perfect matching and both pure matchings must attain that component's maximum. If $q$ intact cycles of length $2d$ remain, these cycles each supply either zero or $d$ shifted edges. All path components together supply any count between zero and $r-qd$. Thus every multiplicity works exactly when $q=0$ or $r-qd\ge d-1$.

In the long-distance case, each row leaves at most six off-path vertices beyond the removed leaves. The same prefix-sum proof gives a 27-vertex piece with at least 21 consecutive path vertices and at most six side leaves. The one-leaf period theorem and the ring census cited above restore every such piece. For residue 27, the earlier bound of 25 also follows from the total leaf count bound.

### Reproducing the strategy checks

The [generator](overlap_strategy.cpp) chooses one label for each next parent value. A binary record consists of two four-byte little-endian masks for $X,W$, followed by the 27 choices. Records are in increasing order of $X+2^{27}W$ with masks interpreted as integers. The [separate verifier](check_overlap_strategy.cpp) starts at $(\{0\},\varnothing)$, follows all 27 choices at every reachable state, and checks the two new residues and overlaps from their actual values. For the final matching test the generator sums maximum matching sizes of paths and cycles. The verifier starts with the full pure-zero matching and searches for an augmenting path by alternating shifted and identity edges. It counts intact cycles independently. It requires the next expected state at every record and exhausts the stream.

The [sixteen digests](overlap-strategies.sha256) cover **10,673,551** states and **288,185,877** parent choices. A separate [whole-tree replay](check_overlap_joins.py) reads the strategy at actual old vertices, using unit scalings and different first-parent colors. After the core is grown it computes the forbidden sets from the full histograms. It finds the leaf labels by a direct search along the residue cycles and checks all leaf multiplicities, recounting **3,792** complete trees. The verifier also rejects a corrupted label and an omitted state.

~~~bash
set -euo pipefail
out=$(mktemp -d)
b=research/biased
c++ -std=c++17 -O3 "$b/overlap_strategy.cpp" -o "$out/generate"
c++ -std=c++17 -O3 "$b/check_overlap_strategy.cpp" -o "$out/verify"
for H in 2 4 6 7; do
  t=$((H/2))
  for delta in 0 1 3 9; do
    stream="$out/overlap-$H-$t-$delta"
    "$out/generate" "$H" "$delta" "$t" "$stream"
    "$out/verify" "$H" "$delta" "$t" "$stream"
  done
done
(cd "$out" && shasum -a 256 -c "$OLDPWD/$b/overlap-strategies.sha256")
python3 -B -m research.biased.check_overlap_joins "$out"
~~~
