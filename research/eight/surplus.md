# Exactly when an attachment preserves an eight-label surplus core

**Theorem.** Fix any 8-cordial labeling on a tree of order $8m+1$. Attach an arbitrary rooted forest, each component by one edge to a prescribed old vertex. The old labeling extends for **every forest size except possibly seven**. At size seven it extends except for exactly **42 colored forests**, or **11** up to multiplication by units after translating the old surplus to zero. The statement includes all old parent colors and coincidences. None of the exceptions gives an ordinary noncordial tree.

For a packet of one through seven new vertices, balance requires distinct new vertex labels avoiding the old surplus and distinct new edge weights, including all incoming edges. These conditions are also sufficient. The old edges are uniform and the surplus bin already has one more vertex than all others.

## The complete list at seven free vertices

Each exception consists of one new center with $c$ leaf children, together with $6-c$ singleton components. The middle column gives the colors of the old parents of the singletons. The right column gives the color of the old parent of the new center. Multiply every listed color by the same odd unit modulo eight to recover all cases. All colors here are relative to the old surplus.

| $c$ | Singleton parent colors | Center parent color |
|---:|:---|---:|
| 1 | 0, 0, 0, 0, 0 | 1 |
| 1 | 0, 0, 0, 4, 4 | 1 |
| 1 | 0, 4, 4, 4, 4 | 1 |
| 3 | 0, 0, 0 | 1 |
| 3 | 0, 0, 0 | 2 |
| 3 | 0, 0, 2 | 1 |
| 3 | 0, 2, 4 | 3 |
| 3 | 2, 2, 2 | 3 |
| 3 | 2, 2, 6 | 1 |
| 3 | 2, 4, 4 | 1 |
| 5 | 0 | 1 |

The [classification checker](surplus.py) starts at the empty forest and adds a leaf at every possible parent, including every boundary color. Sorting the parenthesis codes of child subtrees gives a complete isomorphism invariant. Every forest has a removable leaf. For each resulting parent array the checker lists all injections into the seven nonzero residues and intersects bit masks that exclude each pair of equal edge sums. An empty mask certifies that every injection fails. At sizes one through seven the numbers of distinct colored inputs are $8,44,200,814,3072,10996,37832$. Only the last size has failures. A second enumeration builds multisets of uncolored rooted trees, assigns boundary colors and searches labels one vertex at a time. Its 10,940 unit orbits at size seven give exactly the same raw cases and exceptions.

## Arbitrarily large attachments

Every forest on at least eight vertices has an ancestor-closed set of seven vertices outside the three exceptional **uncolored** shapes. If it has a path on three vertices from a component root, include these three; if two roots have children, include each with one child. Either choice already contains two vertices with children. Add available vertices until there are seven. If neither choice exists, the forest is all singletons or consists of one star with $c$ children and $s$ singletons. Seven singletons work whenever available. With the center included, the number of children in a seven-vertex initial set can take every value from $\max(0,6-s)$ through $\min(6,c)$. For $s+c\ge7$ this interval contains an even integer. Indeed, if neither 0 nor 6 is available then $s,c<6$ and the interval has at least two elements. All exceptional child counts are odd.

Use this ideal to reach a cordially labeled core of order divisible by eight. The [divisible-core attachment lemma](README.md#the-extension-lemma) then permits arbitrary further vertices, at most eight per batch, while retaining all earlier labels. This proves the stated classification for arbitrary forest size.

There is also a **second proof of ordinary eight-cordiality** using only the small packet classification above. Use strong induction. At order one modulo eight, remove a leaf (unless the tree is a singleton) and restore the unique deficient weight of the divisible tree. At any other order keep a connected core of order one modulo eight by removing $t=(n-1)\bmod8$ vertices, retaining a chosen original leaf in that core. This is always possible by growing the core from that leaf. For $t\le6$ the classification restores the vertices. For $t=7$, each exceptional exterior would have six tips, all leaves of the original tree, in addition to the retained leaf. Then delete seven original leaves instead. Their parents survive, and the all-singleton packet always extends the smaller core. This proves the induction also for orders through eight.

## A divisibility obstruction at every modulus

The earlier [pinned-star criterion](../rainbow/pinned-star.md) explains the rows whose singleton parents all carry the old surplus. Let $k\ge3$, choose $1\le c\le k-2$, and attach a new center with $c$ leaf children plus $k-2-c$ singleton leaves. The old core has order one modulo $k$ and surplus zero. If all singleton parents have label zero and the center's old parent has label $p$, then the old labeling extends **if and only if $\gcd(c+1,k)$ divides $p$**. At a prime modulus every $p$ works in this family.

Write $a\ne0$ for the center label and $B$ for the set of child labels. The singleton labels use the remaining nonzero residues and their weights equal their labels. The child weights $a+B$ must lie in $B\cup\{0,a\}$ and cannot equal $a$. They omit exactly one element of $B\cup\{0\}$, which summation shows to be $-ca$. The center edge must therefore weigh $a$ or $-ca$. This gives $p=0$ or $p=-(c+1)a$.

For $p=0$ choose $a=1$. Otherwise choose a solution of $(c+1)a=-p$. If $h$ is the order of $a$, write $c+1=qh+e$. In either case $1\le e<h$. Take $B\cup\{0\}$ to consist of $0,-a,\ldots,-(e-1)a$ and any $q$ complete cosets different from $\langle a\rangle$. There are enough cosets because $c+1\le k-1$. Then $a+B$ covers this set except for $-(e-1)a=-ca$. The required center edge and all singleton weights fit. This proves sufficiency.

## Arbitrary common singleton parent and prescribed center

There is an exact cyclic-interval test when the common singleton parent has any color $b$, even if the new center label $a\ne0$ is prescribed. Subtract $b$ from every prospective edge weight, put $d=a-b$, and let $h$ be the order of $d$. The singleton weights are again their own labels. Thus $d+B$ must lie in $B\cup\{0,a\}$, and the center requires the slot $p+d$ outside $d+B$.

On any $d$-orbit missing $0,a$, the selected child labels form the entire orbit or the empty set. In the other orbits they consist of a string of $l_0$ consecutive predecessors of 0 and a string of $l_a$ predecessors of $a$. Each string must stop before the previous hole, and strings of length zero are allowed. Indeed, from any selected child one can keep adding $d$ until reaching a hole; otherwise the whole orbit is selected. The two available center slots are consequently $-l_0d$ and $a-l_ad$. If the two holes have different orbits, both length caps are $h-1$. If $a=jd$ lies in the zero orbit with $1\le j<h$, the caps are $h-j-1$ and $j-1$, respectively.

Test each possible slot for $p+d$. It fixes its string length uniquely in $[0,h-1]$ by a linear congruence. Divide the remaining child count by $h$. The remainder gives the other string length and the quotient gives the number of full orbits needed. The caps and the available full orbits are necessary and sufficient. This includes $d=0$, where only zero-length strings are possible. Trying all $a\ne0$ handles a free center. The [constructor](surplus_grafts.py) implements the test and the arbitrary-size eight-label extension. The [whole-tree checker](check_surplus_grafts.py) tests 11,568 star inputs. It compares 9,828 prescribed-center instances against direct child-label subset enumeration, verifies the seven-vertex selection on all 286 forest shapes of order eight, and counts every actual edge in 522 complete grafts.

~~~sh
python3 -B -m research.eight.surplus
python3 -B -m research.eight.check_surplus_grafts
~~~
