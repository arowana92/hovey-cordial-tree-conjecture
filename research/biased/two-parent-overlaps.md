# Forcing overlaps for two leaf parents

**Theorem at 27 labels.** Suppose a smallest 27-cordiality counterexample has order $27m+s$. At $s=23,24,25$ the combined leaf count at its two busiest leaf parents is at most **16, 18, 20**, respectively. At $s=26,27$ the [unit-label argument](two-shift-holes.md#choosing-the-high-bins-on-the-smaller-tree) gives 23 and 25. All bounds concern freely chosen labelings of ordinary trees.

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
