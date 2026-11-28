# Prescribing both a root label and the missing edge color

Fix $D\ge3$, $0<\epsilon<1$, and take $k$ sufficiently large. Let $U$ be a tree on $k$ vertices with total excess $\sum_v(d_U(v)-D)_+\le k^{1-\epsilon}$. Prescribe a label $a$ at an arbitrary root $r$, and require a bijection onto $G=\mathbb Z_k$ whose $k-1$ edge sums are precisely $G\setminus\{w\}$. Write $S=\sum G$ and $b=w-2a$.

**Theorem.** If $U$ is a path rooted at one of its tips, the prescription is possible exactly when $S+b\ne0$. In every other case it is possible exactly when
$$
                        h=\gcd(k, d_U(v)-1:v\ne r)\quad\text{divides } b .
$$
There is no degree restriction on the root beyond the total excess bound. If $U$ has at most $k^{1-\epsilon}$ leaves then its excess above three satisfies the hypothesis and it has many ordinary degree-two nonroot vertices. In that case every root and missing-color prescription works except for the stated path exception. In particular the gap $w=2a$ always works outside the odd path rooted at its tip.

Müyesser and Pokrovskiy characterize existence of a harmonious labeling for large bounded-degree trees over abelian groups and give an embedding lemma with prescribed vertex and color sets. We use that lemma to keep a designated root fixed and to realize a specified omitted color, also allowing polynomially sublinear total degree excess. [Primary theorem and applications](https://arxiv.org/html/2509.05280v2#S1) · [Prescribed tree embedding](https://arxiv.org/html/2509.05280v2#S4)

## Necessity and the path

Translate all vertex labels by $-a$. The root must now have label zero and the missing weight is $b$. Subtract the sum of the vertex labels from the sum of the edge weights to obtain
$$
                     \sum_{v\ne r}(d_U(v)-1)x_v=-b.
$$
This proves the divisibility condition. For a path with root at a tip and other endpoint $y$, summing edge weights also gives $2S-x_y=S-b$. Thus $x_y=S+b$ must differ from zero. Conversely fix the two nonadjacent endpoints at these values. Add six isolated ordinary positions to the marks and choose their labels so the marks sum to $S$. The degree-weighted sum is then $2S-x_y=S-b$. There are no induced edges on these marks and every degree class is exhausted or has six representatives inside and outside. Lemma 4.9 supplies the requested labeling.

## Preserving the root through degree redistribution

In every remaining case there are two leaves $p,q$ other than $r$. Reserve them for the final vertex sum. Some fixed degree $2\le d\le D$ occurs $\Omega_D(k)$ times: degrees greater than $D$ contribute only $O_D(k^{1-\epsilon})$ to $\sum(d_U-1)=k-2$. Set $g=\gcd(k,d-1)$. For each nonzero residue of $d_U(v)-1\pmod g$ occurring at a nonroot vertex, mark one representative. Give $r$ its fixed zero. Protect the two reserved leaf edges.

Use the [degree redistribution](sparse-incidence.md#distributing-the-high-degrees) rooted at $r$, retaining at most $D-1$ children per vertex and prioritizing both protected edges. Including the root costs at most one cut beyond the total excess. Make the five additional disjoint cuts away from all protected positions. There are $O_D(k^{1-\epsilon}+1)$ cuts and base marks. Choose sites from the frequent original degree $d$, outside the closed neighborhoods of all marks and reserved leaves in the capped forest. There are still $\Omega_D(k)$ available. Match component roots to nonincident cut edges as before. For a wire at root $j$ paired to the cut $uv$ its site label is $X_u+X_v-X_j$. The resulting bounded-degree tree $A$ has the same formal multiset of changed edge weights. The two reserved leaves remain unmarked leaves and many original degree-$d$ vertices are untouched.

Set the independent base variables to zero modulo $g$ except at the representatives. Their residues can arrange
$$
                \sum_{v\text{ marked}}(d_U(v)-1)x_v=-b\pmod g .
$$
Indeed the coefficient gcd with $g$ of the representatives is $h$: an unaffected nonroot of degree $d$ exists. Each new site has coefficient $d-1=0\pmod g$. The fixed root contributes zero.

Lift the variables from their assigned residue classes. After fixing $X_r=0$, each wire-site form still differs from every base label and from the other sites. A negative component-root variable is unique to its site. If this negative variable is the prescribed root, the two positive cut endpoints are distinct nonroot variables and give a distinct two-variable form. For an original edge at the root its sum has a single nonroot variable. Other original edges have two distinct variables. Thus all induced edge forms are distinct, including after replacement by the matched wires, and each differs formally from the constant omitted color $b$.

Order the unpinned variables in original parent-before-child order. In the edge list each variable is latest only at its own parent edge. In the vertex list it is latest in boundedly many forms: its own label, the single site using its cut edge as positive child, and its possible single role as negative component root. A positive parent of a cut has its child later, since the original tree is rooted at the fixed zero. Thus comparisons between forms with different latest variables cost $O_D(k^{1-\epsilon}+1)$ tests per variable. There are only that many same-latest pairs in total, including those whose latest variable cancels. Every nonconstant difference has coefficients of absolute value at most two. Each congruence excludes at most two lifts at its last surviving variable, whereas there are $k/g$ available. This gives distinct marked labels and distinct induced edge sums avoiding $b$.

On these marks the coefficient sum in $A$ equals that in $U$, since every cut and its matched wire have the same weight. Enlarge the marks with the reserved leaves to a degree core of $A$. Choose the additional ordinary labels zero modulo $g$ while maintaining distinctness and avoiding $b$ on edges. Two isolated unaffected degree-$d$ positions with a prescribed pair sum correct $\sum(d_A-1)x$ to $-b$ modulo $k$. The two reserved leaves then correct the unweighted sum to $S$. Neither changes the corrected coefficient sum. Each step excludes only $O_D(k^{1-\epsilon}+1)$ choices, including the omitted weight. The resulting marked degree-weighted sum is $S-b$. Lemma 4.9 gives the bijection with precisely the target colors, extending all pins. Restore the original cut edges to conclude.

The degree-excess restriction matters. At odd $k$ take a $k$-vertex star rooted at a leaf and prescribe $a=w=0$. The missing color of a bijectively labeled star is twice its center label, which would force that center to zero as well. Its displayed gcd is one. This obstruction is to the root prescription.

## Splitting a vertex without a bound on its outside degree

Choose any vertex $v$ in an arbitrarily labeled old tree. Attach $U$ by the edge $vr$ and move any subset of edges formerly at $v$ to $r$, retaining their opposite endpoints. With $a=x_v$, use the rooted prescription $w=2a$. Every moved edge retains its weight, the new edge $vr$ has weight $2a$, and the internal edges of $U$ have all remaining weights. Every vertex and edge bin gains one. This works independently of the old order, labels and number of moved branches, except for the odd endpoint-rooted path case.

Consequently, at sufficiently large $k$, no smallest counterexample can contain such an excess-bounded part of order $k$ with **all edges to the outside meeting one vertex of the part**, however many outside edges there are. Remove the part and choose one outside attachment vertex $v$. Reconnect the other outside components at $v$. Label the smaller tree by minimality and use the construction to restore it. In the exceptional path case there is already a pendant path of $k-1$ edges starting at $r$ and ending at the other tip. This exceeds the [terminal path bound](../counterexample-bound.md#shortening-paths) for a smallest counterexample.

## Verification

~~~sh
python3 -B research/bounded-degree/check_rooted_gap.py
~~~

The [constructor](rooted_gap.py) computes the prescribed quotient residues and both embedding moments. The [independent checker](check_rooted_gap.py) verifies 411 successful targets by reconstructing the original edge changes, the root label, omitted weight, degree classes and moments. It also checks 39 gcd or endpoint obstructions. The original maximum degrees reach 30.

At eight labels the checker tries all $7!$ nonroot permutations for each of the 115 rooted tree shapes. Of the 920 root-zero and omitted-weight prescriptions, 778 are feasible. There are 96 failures beyond the general necessary gcd and endpoint tests. Precisely 95 of the 115 shapes can have both root and omitted weight zero. One failure is the tree rooted at 0 with parent list $(-1,0,1,2,2,0,5,5)$. These are failures of the stronger prescribed labeling; every eight-vertex tree is 8-cordial.
