# Unrestricted leaves at the two copies of a zero-labeled vertex

**Diameter-five consequence.** Give two adjacent centers the same multiset of positive branch child counts. If each has at least three branch parents, arbitrary and independently chosen numbers of direct leaves at the two centers give a super edge-magic tree. For two branch parents per side the same conclusion holds when each center has at least one direct leaf. This complements the [independent branch size theorem](two-center-layers.md), which permits entirely different branch child counts on the two sides.

**General construction.** Let $g$ be a graceful labeling of a tree $H$ on $s$ vertices. Thus its vertex labels are $0,\ldots,s-1$ and its absolute edge differences are $1,\ldots,s-1$. Join two copies of $H$ by an edge at *any* two corresponding vertices. Arbitrary leaf counts can be added at the two copies of the vertex labeled zero, independently. The resulting tree admits consecutive integer vertex labels and consecutive integer edge sums. More generally, two decreasing lists of leaf populations are allowed as described below.

The undecorated construction is a consequence of Theorem 2.1 of Makadia, Kaneria, Andharia and Jadeja, who prove an $\alpha$-labeling for two joined copies of any bipartite graceful graph. We give the tree labels directly to locate the vertices for the additional leaves. [Primary paper](https://jaem.isikun.edu.tr/web/images/articles/vol.12.no.3/14.pdf)

Bipartition $H$. For each vertex of graceful label $i$, give its two copies the integers $-i$ and $1+i$. On the first copy choose $-i$ on one bipartition class and $1+i$ on the other, reversing these choices on the second copy. The vertices fill $[1-s,s]$. The new bridge weighs 1. For each edge of difference $e>0$, the two original edges weigh $1-e$ and $1+e$. All edges therefore fill $[2-s,s]$. The copies of the zero vertex have labels 0 and 1. A leaf at 0 can extend the upper ends of both intervals by one, and a leaf at 1 can extend the lower ends of both intervals by one. These operations can repeat in any order.

For the diameter-five application, start with just the branches on one side and root at the center. This tree has diameter four and center degree at least three. Van Bussel's characterization gives it a graceful labeling with zero at the center. Join its two copies at the centers, then add the two requested direct leaf populations. For two branches and a positive direct leaf count on each side, keep one direct leaf on each copy before applying the theorem, so the root degree is three. At most one nontrivial branch per side gives a caterpillar directly. [Van Bussel's paper](https://doi.org/10.1016/S0012-365X(03)00152-3) · [Author's thesis, Chapter 4](https://central.bac-lac.gc.ca/.item?app=Library&id=MQ53395&oclc_number=1006929582&op=pdf)

## Independent populations in graceful-label order

In the pair belonging to each graceful label $i$, designate the vertex with the even integer label and the one with the odd integer label. Give the successive even vertices any weakly decreasing sequence of nonnegative leaf counts in order $i=0,\ldots,s-1$. Do the same independently on the odd vertices. Some pairs can have leaves on just one member.

Indeed the pairs with $0\le i<r$ fill $[1-r,r]$. To add one leaf at just the even vertices of this interval, or just the odd ones, use the parity row of the [interval extension](two-center-layers.md#two-independently-extensible-lists-of-parents) with offset $m=1$. The lower parents are $r,r-2,\ldots,2-r$, the upper parents $r-1,r-3,\ldots,1-r$. The vertex and edge intervals retain the form $[L,U]$ and $[L+1,U]$ after every such extension. Taking successive differences of each population list proves the claim. These are integer constructions at all moduli. The undressed two-copy conclusion, for example, applies to any diameter-five half by Hrnčiar and Haviar's graceful labeling theorem. [Hrnčiar and Haviar](https://doi.org/10.1016/S0012-365X(00)00233-8)

The checker finds a graceful witness for every rooted shape through order eight, tests each possible bridge vertex, verifies the completed tree and leaf populations, then recomputes every integer edge sum. It checks 1,446 trees. The published graceful labeling theorems supply the existence statements for large halves. [Constructor](graceful_copies.py) · [Independent checker](check_graceful_copies.py)

~~~sh
python3 -B -m research.hub.check_graceful_copies
~~~
