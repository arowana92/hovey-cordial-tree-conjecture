# A modular construction for a small rooted tree and arbitrary hub leaves

**Theorem.** Let $H$ be any tree of order $h$ with a specified root. For every integer $k>100(h+1)^{14}$, it has distinct labels in $\mathbb Z/k$, zero at the root, whose edge sums are exactly its vertex labels with one omitted. Consequently every number of extra leaves at this root gives a $k$-cordial tree. In particular, $13000\cdot100(h+1)^{14}$ extra leaves suffice at all positive moduli, allowing different labelings.

**Corollary.** For every sufficiently large $k$, any tree with all but at most $k^{1/15}$ of its leaves adjacent to one vertex is $k$-cordial. Its order and the lengths of its branches are unrestricted. The modulus may be prime or composite. This also gives the order-$k$ rainbow and order-$(k+1)$ harmonious labelings for this family.

The [ordinary integer construction](polynomial-hub.md) supplies an actual integer certificate. Here different moduli can give different edge-to-vertex correspondences. We keep the vertex and edge histograms $V,E$ of a growing subtree equal up to the missing root weight, $E=V-[0]$.

## A round using eight consecutive vertices

Suppose a set of new vertices has labeled parents, and a path of eight further vertices starts below a labeled nonzero parent $p$. All new vertices are distinct, and the path is taken from a separate child so none is an ancestor of another outside its own path. Each ordinary new vertex needs a label and an edge sum differing by its parent's label. Regard the latter as a prescribed jump in $\mathbb Z/k$.

Walk from zero with these jumps and erase each simple cycle when its endpoint first repeats on the current path. This partitions the steps into simple cycles and a simple residual path with the original endpoint. Assign each vertex the tail of its step. Any common translation within a piece preserves its jumps. A cycle can avoid a forbidden set $F$ by translation whenever its length times $|F|$ is less than $k$, since each tail and forbidden value forbid at most one translate.

Write $D$ for the sum of the prescribed jumps, excluding the eight path sites. If $D\ne0$, add the first of those sites as one more jump $p$, **last** in the walk. The residual endpoint is $e=D+p$. Denote the tail intercepts of the residual path by their unshifted positions. Translate each erased cycle so that its tails avoid the other tail intercepts, zero and $e$. There are at most $h+2$ forbidden intercepts at any such choice. All tail intercepts are now different, and none is $e$. The first path site's tail intercept $c$ is nonzero. If its step survived erasure, its tail was $D$ since it was the last step. If it belongs to a cycle, zero was reserved.

Use $X$ plus each assigned intercept as an actual vertex label. The net change of $E-V$ is $[X+e]-[X]$, also when the residual path is empty. The first path vertex now has label $X+c$. On the seven remaining sites, give the following labels in order:
$$
X+e,\quad -3X-c-2e,\quad 2X+c+e,\quad 2X+e,\quad
-X-e,\quad -2X-c-e,\quad 4X+c+2e .
$$
Starting from $X+c$, their edge sums are the third, sixth, fifth and seventh labels, then $X$, then the second and fourth labels. Thus this path cancels the histogram change. Its only slope-one label has intercept $e$, which all tails avoided. Its only repeated slope is two, and the intercept difference is $c\ne0$ in the group. All new labels with equal slope have different intercepts. [Lean verification of the actual sums and cancellation modulo every $k$](ModularLayer.lean)

When $D=0$, the original jumps decompose entirely into cycles. Translate these to avoid the old vertices and one another. Use just the first seven path sites for the neutral transfer with source and target both $X$, under parent $p$. In path order their labels are
$$
X,\quad -p-2X,\quad p+X,\quad 2X,\quad -X,\quad -p-X,\quad p+3X .
$$
The net change is zero. The two pairs with equal slopes have intercept difference $p\ne0$. Leave the eighth site available. [Seven-edge transfer](../large-order/gap-path.md#transferring-a-missing-weight)

At either step, consider the old fixed labels as having slope zero. For different slopes $a,b$, equality excludes at most $|a-b|$ values of $X$ modulo $k$, by the linear congruence formula, even when the difference is a nonunit. Here $|a-b|\le7$. With at most $h$ vertices, a common choice avoids all collisions. This proves the round directly in the cyclic group.

## Stopping with at most twelve levels

For height at most four the [breadth-first integer bound](exceptional-moduli.md#all-moduli-at-bounded-branching-depth) gives span at most $8(h+1)^8$. Otherwise start at an ancestor four edges above a deepest leaf and apply the [four-site rule](polynomial-hub.md#a-small-labeled-subtree-with-a-shallow-remainder) within its descendant subtree. A fork with two support children gives two arms or three consecutive supports and a leaf. With no fork the last three supports on the original path and the deepest leaf suffice. The boundary $w$ is nonroot and its descendant height is at most four.

Temporarily withhold $w$ and its entire descendant subtree. Label the root zero and its eligible children with distinct nonzero residues. This gives $E=V-[0]$. While some available child of the labeled subtree begins a downward path of eight eligible unlabeled vertices, use such a path. The other available children form the prescribed jump list for the round. The parent of the path is nonzero, since every eligible child of the root was already assigned. Each round adds at least seven vertices and keeps the labeled tree closed under ancestors. At termination every eligible vertex is within seven downward edges of a labeled ancestor. Restoring access to $w$ adds at most one edge to reach $w$ and four below it, so every unassigned vertex is within twelve edges of the labeled subtree.

Set aside only the four special sites and their extra leaf children now. For the first layer of all other unassigned vertices, decompose the parent jumps as before. Let $e$ be the residual endpoint. Translate cycle intercepts disjointly from one another, the residual tails and $e$. Assign $X$ plus each tail intercept. Every first-layer form has slope one, and the terminal form $L=X+e$ is distinct from them. The edge histogram is now $V-[0]-[X]+[L]$.

In each later level assign the current $L$ to each child, then add its parent's form to $L$. All such parents have positive slope. The terminal slope strictly increases at each assignment, so the new forms are distinct. The first assignment of the second level uses the reserved endpoint intercept. After at most eleven such levels the terminal slope is at most $A=(h+1)^{11}$, since each level multiplies it by at most $h+1$. The boundary's form $p$ has positive slope at most that of $L$, and it differs from $L$ even if their slopes agree. Intercepts throughout these computations are residues, and slopes are ordinary integers.

Restore the four sites by the [path and two-arm table](universal-hub.md#restoring-the-four-sites-and-their-leaves), with these forms $p,L$. Their negative slopes separate all negative arrivals from the old positive or zero slopes. The forms $-p,-L$ are distinct because $p,L$ are. The other negative forms $-p-L$ and, where used, $-p-2L$ have strictly smaller slopes. The positive arrival $L$ is fresh. The four edges leave gap $X$. Pair the extra leaves at $+L$ with as many leaves at $-L$, using the table's ordering rule. If there are unpaired leaves, choose one whose parent's negative slope has magnitude at least the slope of $L$ first. Assign each unpaired leaf the current gap minus its parent. Its new slope first exceeds the slope of $L$ and then strictly increases. For a paired pair choose $T$ of slope one above the highest current slope, and use $T,T+L$ in that order at $+L,-L$. The edge sums exchange their labels. This gives a single omitted vertex form and distinct forms everywhere.

All final slope magnitudes are at most $7(h+1)A$: the four-site magnitudes are at most $3A$, each unpaired step costs at most $3A$, and each pair raises the maximum by at most $A+1$. Equal slopes have distinct intercepts modulo $k$, including for the originally fixed vertices. Across at most $h(h-1)/2$ different-slope pairs, fewer than $100(h+1)^{14}$ choices of $X$ are forbidden. Specialization gives the desired distinct residues and exact edge multiset.

## Arbitrary populations and branch lengths

For the first population assertion add leaves in periods, filling the complement of the vertex set, then its omitted weight, then its other labels. For smaller $k$ use the [one-site bound of $13000k$ leaves](../large-order/gap-path.md). For the corollary delete the extra leaves at the hub, and write $a$ for the remaining nonroot terminals. Compress core segments to order at most $28a+1$. The new bound is $100(28a+2)^{14}=o(k)$ when $a\le k^{1/15}$. For core order below $k/20$, restore long segments by the twelve-vertex subdivision lemma. For core order between $k/20$ and $k$, apply the positive-density embedding theorem with exponent $1/2$. For larger cores the prefix induction uses the same bound on nonroot terminals. These are exactly the three steps of the [arbitrary-order argument](polynomial-hub.md#consequences-for-cordiality). [Path and matching hypotheses](long-branches.md)

## Reproduction

The Python checker reconstructs edge residues from the input parent arrays. It checks every rooted shape through order thirteen at modulus $65536$, all three outcomes for the last prescribed jump, 15,624 modular walks, 240 larger trees and moduli, and five wide suffixes with large slopes. The Lean file verifies the seven residual edge sums, their multiset cancellation and reduction modulo $k$. The size bounds, termination and tree induction are proved above. [Constructor](modular_injection.py) · [Independent checks](check_modular_injection.py)

~~~sh
python3 -B -m research.hub.check_modular_injection
lean research/hub/ModularLayer.lean
~~~
