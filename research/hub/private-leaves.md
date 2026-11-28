# Leaves at almost every vertex of a tree of order close to the modulus

**Theorem.** There are absolute constants $\delta>0$ and $k_0$ with the following property. For $k\ge k_0$ let $H$ be any tree with $(1-\delta)k\le |H|\le(1+\delta)k$. Attach leaves at at least $(1-\delta)k$ different vertices of $H$. The resulting tree is $k$-cordial. Each occupied site can have any positive number of added leaves. The degrees in $H$ are unrestricted.

**Corollary for larger trees.** For all sufficiently large $k$, if $|H|$ is any positive multiple of $k$, attaching at least one leaf at every vertex of $H$ gives a $k$-cordial tree. For exactly one new leaf per vertex, the [two-period construction below](#adding-two-copies-of-every-residue) also covers specified ranges of $|H|\bmod k$.

## Matching the increments of three histograms

Fix a tentative labeling $f$ of the original vertices. Write $V_f,W_f$ for its multisets of vertex labels and edge weights, and $S$ for the multiset of parent labels of the new leaves, one occurrence per leaf. Given desired final multisets $V,W$, put $X=V-V_f$ and $Y=W-W_f$, requiring nonnegative multiplicities. A partition of $X,S,-Y$ into zero-sum triples assigns each new leaf an input label and produces the prescribed histograms. In particular the necessary sum identity is
$$
\sum Y=\sum X+\sum S.
$$

For three multisets of length $r$, let $E$ be the sum of their three excesses over their respective support sizes. For sufficiently large cyclic groups the identity suffices if $r-E\ge(1-c)k$ for an absolute $c>0$. This is the cyclic near-full-set result of Müyesser and Pokrovskiy, followed by the elementary operation that matches one occurrence of a repeated value until all three shores are sets. [Primary matching theorem and the linear bound after Problem 7.4](https://doi.org/10.1007/s00222-025-01328-x) · [Multiset proof and explicit bound at 27](../biased/four-hole-matchings.md#from-sets-to-prescribed-repeated-labels)

Choose a small constant $\eta>0$ relative to $c$, then $0<\delta<\eta$. All constants in the estimates below are absolute. A histogram of size $k+O(\eta k)$ that equals one outside $O(\eta k)$ bins has support $k-O(\eta k)$. Three such histograms meet the matching bound when $\eta$ is sufficiently small.

## Labeling the original tree

Write $h=|H|$, $r$ for the number of new leaves and $n=h+r$. For $n>2k$, retain exactly $2k-h$ new leaves at as many distinct parents as possible. At least $(1-\delta)k$ different parents are retained. After proving this order-$2k$ subtree cordial, the other leaves can be attached in batches. From a divisible order, use the first leaf to fill the deficient weight. From an order one modulo $k$, Hall's prescribed-differences lemma allows up to $k-1$ leaves at already present parents. Repeat from the next divisible order. [Hall's theorem and the leaf extension](../counterexample-bound.md#removing-leaves)

It remains to consider $2k-2\delta k\le n\le2k$. Take a connected subtree of $H$ on $\lfloor(1-2\eta)k\rfloor$ vertices. Embed it injectively with distinct sums in the sum-colored complete graph on $\mathbb Z_k$. This is the almost-spanning rainbow tree theorem with a fixed positive slack and sufficiently large $k$. Add the remaining $O(\eta k)$ vertices in parent-first order. For each, avoid doubly occupied vertex bins and values producing a doubly occupied edge weight. At every step there are only $O(\eta k)$ such exclusions. This gives a labeling with both old histograms bounded by two and equal to one except at $O(\eta k)$ bins. The many distinct parent sites now give $k-O(\eta k)$ different shifts, since only $O(\eta k)$ core labels have two copies. [Montgomery, Pokrovskiy and Sudakov, Theorems 1.1 and 1.5](https://doi.org/10.4171/JEMS/982)

Put $t=2k-n$. The final vertex bins should be two except at $t$ distinct residues $A$ of count one. The final edge bins should be two except at $t+1$ distinct residues $B$ of count one. Neither low set may meet bins already doubled on its own side. The required identity is
$$
\sum B=\sum A+\sum V_f-\sum W_f-\sum S.
$$

For $t\ge1$, choose any admissible $A$, then $t-1$ distinct admissible members of $B$. The remaining two members must have a specified sum $q$. There are $k$ ordered pairs $(x,q-x)$. At most twice the number of excluded residues meet the excluded set, and at most two have equal entries. Since $t\le2\delta k$, an admissible pair exists. The multisets $X,Y,S$ now meet the matching bound, proving cordiality.

For $t=0$, the unique low edge weight is forced to be $d=\sum V_f-\sum W_f-\sum S$. We adjust a single label so that $W_f(d)\le1$. Choose an occupied parent $v$ of total degree between two and eight in the enlarged tree, whose neighbors in $H$ have distinct labels. The sum of degrees over $H$ is $2(h-1)+r=3k+O(\eta k)$, so linearly many occupied sites have degree at most eight. A pair of equal-labeled core vertices has at most one common neighbor in a tree. There are only $O(\eta k)$ such pairs, proving existence of $v$.

Erase its label and its incident core weights. As the new label $x$ varies, $d=C+(1-\deg_T v)x$ for a fixed $C$. Avoid old doubled vertex bins, choices making any incident core edge hit an unaffected doubled weight, and choices making $d$ equal an unaffected doubled weight. Each excluded residue in the last test forbids at most seven values of $x$. Also exclude $d=x+f(w)$ for each core neighbor $w$, eliminating at most eight choices per neighbor. Here multiplication by a nonzero integer $a$ in $\mathbb Z_k$ has fibers of size at most $|a|$. All exclusions together cost $O(\eta k)+O(1)<k$. The new incident weights are mutually distinct. Thus both core histograms still have maximum two, the forced bin is admissible, and changing this bounded-degree vertex preserves the near-full support of $S$. The multiset matching finishes the divisible order.

## Adding two copies of every residue

Let $F$ be a rooted forest of exactly $k$ ordinary vertices. Each root has an entering edge with a prescribed old parent label, with $O(\log k)$ distinct old labels in total and a fixed implied constant. Give every ordinary vertex one private leaf. For all sufficiently large $k$, these $2k$ vertices and their $2k$ edges, including the entering edges, can supply **two copies of every vertex label and every edge weight** while all old labels are retained.

Choose a parent-first prefix of $\lfloor(1-2\eta)k\rfloor$ ordinary vertices. Give it distinct labels and distinct weights including its entering edges, using the prescribed-subtree version of the almost-spanning rainbow theorem. For the boundary reduction, identify equal old parent labels into one hub for each distinct value, join these hubs to an auxiliary center, and prescribe the resulting rainbow star. Its $O(\log k)$ vertices lie below the prescribed-subtree bound. Discard this star after embedding. Add the remaining ordinary vertices one at a time as above, avoiding doubled vertex and weight bins. [Prescribed-subtree theorem and hub construction](../rainbow/pinned-prefix.md)

Write $c_i$ for the number of ordinary children of vertex $i$. The necessary sum condition for increments exactly two on both sides reduces to
$$
\sum_{i\in F}(c_i+1) f(i)+\sum_{\text{roots }i} b_i=0.
$$
Here $b_i$ is the old label on the entering edge. Indeed, subtract the ordinary vertex sum from the ordinary edge sum including the entering edges, then add the private-leaf parent sum. This gives the displayed left side, which must vanish since the final edge and vertex histograms agree. [Lean identity for the underlying forest weights](../bounded-degree/ForestPeriod.lean)

Choose an ordinary terminal $v$. Select a second vertex $w$ different from and nonadjacent to $v$, with at most three ordinary children and distinct labels at its ordinary neighbors and its entering parent if present. There are linearly many vertices with at most three children. Two equal free labels can create a neighbor collision at at most one vertex of the forest. A collision between an old parent and a free child can occur at only $O(\log k)$ roots, since each boundary label occurs on at most two free vertices and every free child has a single parent. The terminal has at most one ordinary neighbor to exclude.

Erase the two labels and the affected ordinary weights. Write $y=f(w)$ and set $f(v)=D-(1+c_w)y$ to enforce the identity. Avoid the old doubled bins for both vertex labels and for all new incident weights. At $w$ the new weights are mutually distinct by the choice of its neighbors. Also avoid equality of the two new labels or of the terminal's one incident weight with any new weight at $w$. The latter equations have coefficient $2+c_w$. The coefficients of $y$ in the exclusions have nonzero absolute value at most five, so $O(\eta k)+O(1)$ choices are excluded. The resulting ordinary histograms have maximum two and nearly full support. The three multisets needed for the private leaves have size $k$, nearly full support, and the correct sum. Match them to obtain the two exact uniform increments.

The same proof gives a cut usable in an arbitrary tree. Let the forest have $h=(1\pm\delta)k$ ordinary vertices and $2k-h$ additional leaves at at least $(1-\delta)k$ ordinary parents. Suppose some ordinary terminal $v$ has **exactly one** of these additional leaves. Keep the logarithmic bound on the number of boundary labels. The two uniform increments still exist, even when other ordinary vertices have several additional leaves or none. In the identity replace $c_i+1$ by $c_i+\ell_i$, where $\ell_i$ counts additional children. The coefficient at $v$ is one. Since $\sum_i(c_i+\ell_i)\le2k$, linearly many occupied sites have coefficient between one and eight. Choose $w$ among them with the same neighbor and separation conditions. All fiber sizes in the exclusions are then at most nine. The ordinary histograms and the shift multiset still have nearly full support. This proves the cut assertion and excludes such a removable piece with a connected nonempty remainder in any smallest counterexample at a sufficiently large modulus.

For the corollary, root $H$ and remove the last $k$ ordinary vertices in a preorder visiting child subtrees by nondecreasing size, recomputing the traversal on the retained tree at each cut. Every suffix forest attaches to the retained tree at $O(\log k)$ different parents by the size-doubling inequality. For the initial $k$-vertex block give its root one fictitious entering edge. Removing that edge from the uniform construction gives a cordial tree on $2k$ vertices. Restore each suffix with its private leaves. Once the order is divisible, any further leaves can be added by the batches above. [Ordered cut and doubling bound](../rainbow/ordered-cut.md)

More generally, for exactly one private leaf at every site write $|H|=qk+s$ with $1\le s<k$. The same cuts reduce to a corona with $s$ ordinary vertices. If $(1-\delta)k\le s<k$, the first theorem applies to it. For each fixed $\epsilon>0$, if $2s\le(1-\epsilon)k$, the almost-spanning theorem gives this entire initial tree a rainbow injective labeling for sufficiently large $k$. Small initial trees can be padded by leaves before the embedding. In either range the restored two-period blocks preserve cordiality.

## Finite checks of the constructions

A separate test reconstructs both target histograms on ordinary trees and tests the two-variable sum repair on forests attached to an actual path containing every possible boundary label. At modulus 27 it uses the independently certified four-hole matching bound whenever its hypotheses hold. It checks 396 whole trees of orders 52 through 54, including 137 with a one-vertex repair, and 308 uniform attachments. In 44 of the attachments, 26 ordinary vertices carry 28 new leaves. The large-modulus conclusions follow from the two cited embedding and matching results with fixed slack. [Finite checker](check_private_leaves.py)

~~~bash
set -euo pipefail
out=$(mktemp -d)
c++ -std=c++17 -O3 research/biased/four_hole_matchings.cpp -o "$out/generate"
python3 -B -m research.hub.check_private_leaves "$out/generate"
~~~
