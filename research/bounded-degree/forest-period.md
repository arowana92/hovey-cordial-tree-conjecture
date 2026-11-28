# Exact uniform increments from an attachment forest at every modulus

**Theorem.** Fix $D\ge3$ and $0<\epsilon<1$. Take a rooted forest $F$ on $n$ new vertices with $m$ components, each attached by one edge at a specified vertex of an arbitrarily labeled old tree. Let $b_i\in\mathbb Z_k$ be the old parent labels. At each new vertex $v$ let $a_v$ be its number of children. Suppose
$$
            m+\sum_v(a_v+1-D)_+\le n^{1-\epsilon}.
$$
For all sufficiently large $n$, simultaneously for **every divisor $k$ of $n$**, there is a labeling of $F$ adding exactly $n/k$ to every vertex bin and every edge bin if and only if
$$
                         \gcd(k,a_v:v\in F)\mid\sum_{i=1}^m b_i.
$$
All old labels are kept. The size threshold depends on $D,\epsilon$, uniformly in $k$, the old tree, the parent choices and the component sizes.

For example, any one-child vertex in $F$ suffices. Since $\sum a_v=n-m$, the displayed gcd divides $m$. Thus coprime $k,m$ also suffice, as does attachment at one common parent label, with any $m$ in the stated range. In particular, a smallest ordinary counterexample cannot have such a pendant forest with nonempty connected complement if any one of these conditions holds. One may remove the entire forest, label the smaller tree and restore it without changing either frequency difference. This cut may have arbitrarily many distinct attachment edges. The uniform-increment requirement applies to arbitrary old histograms.

## Necessity and projection

In the sum of the new weights, each new label is counted $a_v+1$ times, and the old parent labels enter once per component. If the two new histograms agree, subtracting their moments gives $\sum a_vx_v+\sum b_i=0\bmod k$. This proves necessity without a size or degree hypothesis. [Lean proof on actual rooted forests](ForestPeriod.lean)

It suffices to prove sufficiency at $k=n$. Indeed put $H=\gcd(n,a_v:v\in F)$. Choose integer representatives of the given parent labels modulo $k$. Changing one representative by $kt$ makes their sum zero modulo $H$ exactly when $\gcd(k,H)$ divides that sum. The step $k$ generates all multiples of $\gcd(k,H)$ modulo $H$, and $H/\gcd(k,H)$ divides $n/k$, so the required lift exists modulo $n$. External labels can be lifted separately even when components attach at the same old vertex, since their reductions agree. A permutation of all $n$ vertex residues with all $n$ weights distinct reduces to the required counts at modulus $k$.

## One full period

Work at modulus $k=n$. First suppose there are at least two nonroot terminals and a singleton component. Give its one vertex zero and delete it. The remaining forest has $k-1$ vertices, two free nonroot terminals, and must miss exactly the weight $b_i$ of the removed edge. The [forest spectrum theorem](forest-spectrum.md) applies. Its local test is automatic without pins. Its gcd test is precisely the stated condition, since the removed child count was zero.

Next suppose there is no singleton and at least three nonroot terminals. Choose a terminal $y$ with parent $v$. Reserve a label $u$ for $y$ and subtract $u$ from all new and boundary labels while constructing the witness. If $v$ is a root, choose $u$ different from its old parent label. Write $b_i'=b_i-u$. After deleting $y$, pin $v$ at a nonzero $x$ and prescribe missing weight $x$, so restoring $y$ with normalized label zero supplies it. Two other free nonroot terminals remain.

Put $h=\gcd(k,a_z:z\ne v)$ using the original forest. The new spectrum condition is
$$
                       a_vx+\sum b_i'\equiv0\pmod h.
$$
Deleting $y$ decreased $v$'s child count by one, while the missing weight contributes $x$. The coefficient gcd $\gcd(h,a_v)$ is the original divisor and divides $m$, so the congruence remains solvable after translating the boundary. An abundant positive child count less than $D$ occurs away from $v$, hence $h$ is bounded. Choose a solution $x\ne0$. If $v$ is internally adjacent to a component root other than itself, also avoid that root's boundary label. These exclusions are possible for large $k$. The only other potential forced comparison is between missing weight $x$ and the entering edge at $v$ when $v$ is a root; our choice of $u$ makes these distinct. Now apply the spectrum theorem and undo the translation. All weights and labels run through the group.

## The remaining shapes

- **One nonroot terminal.** There is one path rooted at an endpoint and all other components are singletons. Write $S=\sum\mathbb Z_k$. Give the singleton vertices distinct labels $s_i$ and distinct weights $s_i+b_i$. The necessary far endpoint of the path is $z=S-\sum s_i+\sum_j b_j$, where the last sum includes the path's boundary. If there is a singleton, choose its last label also to ensure $z$ differs from all singleton labels. At most $O(m)$ first choices are excluded, with at most two from equality with the last label itself. Choose a fresh first path label $x\ne z$ so its entering weight differs from all singleton weights. The path's vertex palette omits just the singleton labels. Its internal edge palette omits their weights and the path's entering weight. Their sums satisfy $2\sum V-x-z=\sum C$. Pin the path ends and six mutually isolated degree-two positions away from them. Choose four of the six labels freely and the last two with the sum that makes the marks sum to $\sum V$. All but $O(m+1)$ choices work. The degree-weighted sum is consequently $\sum C$, and the degree-core embedding lemma completes the path.
- **Two nonroot terminals and two nonsingleton components, with no singletons.** Both components are endpoint-rooted paths. Join their far endpoints to make a spanning auxiliary path. For parent labels $b_1,b_2$, give the first root $x=S+b_2$ and the second root a fresh $y$ with $w=y+b_2\ne x+b_1$. Prescribe far endpoints with sum $x+b_1$ so their auxiliary edge supplies the first entering weight. The four labels must be distinct, and their induced edges must be distinct and avoid $w$. One can choose the first far label outside a bounded set: its mate is determined, and for large $k$ at most one original path has just two vertices. Each resulting equality excludes at most two choices unless it merely equates two already distinct vertices. The marked endpoint relation $2S-x-y=S-w$ gives the two moments after adding six ordinary positions as above. Remove the auxiliary edge and restore the two entering edges to fill all bins.
- **Two nonroot terminals and only one component.** The tree is not a path rooted at an endpoint. Apply the [root and missing-weight theorem](rooted-gap.md) with both normalized values zero. Its degree-excess hypothesis follows here. Translate the obtained labeling by the actual old parent label $b$. Now the entering edge supplies the missing weight $2b$.

A forest without nonroot terminals has $m=k$, excluded at large $k$. This exhausts the shapes. In the path cases the palettes occupy at least $k-O(m)$ positions, and each nonexhausted degree class has six representatives inside and outside the marks. The primary extension used here is [Müyesser and Pokrovskiy's Lemma 4.9](https://arxiv.org/html/2509.05280v2#S4).

## Finite checks and small exceptions

The [constructor](forest_period.py) gives the actual auxiliary tree, vertex and edge palettes, marks, and final translation. A [separate checker](check_forest_period.py) recomputes both degree-core moments, verifies the degree classes and compares every changed edge on the original forest with the auxiliary edges and missing colors. It accepted 270 one-period targets and detected five incompatible parent sums. It checked 1,263 projected targets, including ten that required changing a lift and were replayed through the full construction.

For two components, the [small exact search](../rainbow/check_two_periods.py) tests every forest through $k=10$, normalizing the two boundary labels to $0,\delta$. Their difference determines the input by translation. At $k=8$ the 96 shapes give 768 inputs. Of these 731 work, 28 fail the necessary congruence and nine further inputs fail. The nine occur on just four shapes. The table uses zero-based parent arrays with $-1$ for each root.

| Parents | Extra failing differences at eight |
| --- | --- |
| $(-1,0,-1,2,2,2,2,2)$ | $0,4$ |
| $(-1,0,0,0,-1,4,4,4)$ | $0,2,4,6$ |
| $(-1,0,0,0,-1,4,5,5)$ | $0,4$ |
| $(-1,0,1,1,-1,4,5,5)$ | $4$ |

For each shape the program searches internal rainbow permutations with the first root normalized to zero. The two unused weights determine the two possible parent differences up to translating the whole permutation. Each positive case is checked again on the actual edges. The additional negative cases are verified independently by searching with the actual parents fixed and the first root free. A rooted-tree partition recurrence checks the number of shapes. These failures concern exact uniform increments with the given parents. Ordinary eight-cordiality is [proved separately](../eight/README.md).

~~~sh
python3 -B research/bounded-degree/check_forest_period.py
python3 -B -m research.rainbow.check_two_periods
lean research/bounded-degree/ForestPeriod.lean
~~~
