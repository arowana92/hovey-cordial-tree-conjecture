# Every tree of diameter at most four is cordial at every modulus

**Theorem.** Every finite tree of diameter at most four has a bijective integer vertex labeling onto an interval for which the edge sums also form a consecutive interval without repetitions. In particular it is super edge-magic and is $k$-cordial for every positive integer $k$.

To obtain cordiality, reduce the two intervals modulo $k$. Each interval of length $m$ contains either $\lfloor m/k\rfloor$ or $\lceil m/k\rceil$ representatives of each residue, including residues with count zero. To obtain a super edge-magic labeling, first translate the vertex labels to $[1,n]$. The edge sums translate by twice the same constant. Assign the edge labels $n+1,\ldots,2n-1$ in decreasing order of edge sum, making every edge label plus its endpoint labels constant. For a tree with at least two vertices, taking $k=n-1$ also gives a harmonious labeling in the sense of Graham and Sloane. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf) · [Graham and Sloane](https://mathweb.ucsd.edu/~ronspubs/80_07_harmonious.pdf)

The proof is computer-assisted. Its infinite step uses the signed Langford existence theorem of Jordon and Mitchell. Six finite sets of initial labelings cover arbitrarily many branching neighbors. Smaller branch counts use explicit labelings. All witness checks use standard Python.

## 1. Removing the dependence on branch sizes

Root the tree at a vertex $o$ within distance two of every vertex. Let $c$ count the neighbors with at least one child, and let $t_1\ge\cdots\ge t_c\ge1$ be their child counts. Allow arbitrarily many other leaves adjacent to $o$. For $c\ge3$ we construct vertex labels $[L,U]$, edge sums $[L+1,U]$, and root label zero. Ordinary leaves at the root can then take consecutive labels above $U$, each equal to its edge sum.

If $c\le2$ the tree is a caterpillar. For completeness, list the edges along its spine, taking the leaves at each spine vertex between the incoming and outgoing spine edges. Consecutive edges share an endpoint, and each edge after the first introduces a new vertex. In each bipartition class, order the vertices by first appearance. Label the first class $0,\ldots,a-1$ and the second $a,\ldots,n-1$. At each step the shared endpoint stays fixed and the other endpoint advances by one within its class. The sums are consecutive. The isolated vertex is immediate.

Fix a list $P=(p_1,\ldots,p_c)$ of distinct nonzero parent labels, assigned in child-count order. Let $P_r$ denote its first $r$ entries. A layer of rank $r$ adds one child at each parent in $P_r$. The tree needs $e_r=t_r-t_{r+1}$ such layers, with $t_{c+1}=0$. A pair of lists $(p'_x)_{x=1}^l,(q_x)_{x=1}^u$ handles $m_r$ layers of rank $r$ if their multiset is $m_r$ copies of $P_r$ and
$$
\{x-p'_x\}=[0,l-1],\qquad \{x-q_x\}=[1,u].
$$
Use child $L-x$ at $p'_x$ and child $U+u+1-x$ at $q_x$. Their weights are exactly the new lower and upper ends of $[L-l+1,U+u]$. The vertex labels fill $[L-l,U+u]$.

Start by taking one full layer, available since $e_c\ge1$. From the remaining multiplicities take $e'_r\bmod m_r$ layers of each rank, where $e'_c=e_c-1$ and $e'_r=e_r$ otherwise. The resulting tree is called a seed. One valid labeling per residue tuple suffices since the remaining layers can be restored in groups of $m_r$. A seed witness lists the parent of each child in increasing order of its label. If $Q$ is the required multiset of child parents, its lower endpoint must be $L=-\sum_{q\in Q}q$, by subtracting the sum of edge weights from the sum of vertex labels. Its upper endpoint is $U=L+c+|Q|$. This determines the unused vertex labels and makes the witness check a direct recomputation of endpoint sums. [Small examples of the layer construction](even-layers.md)

## 2. A permutation on two symmetric integer intervals

**Lemma.** Given positive integers $d,s$ with $s\ge2d-1$, put $S=\pm[d,d+3s-1]$, where $\pm I=I\cup(-I)$. There is a permutation $\tau$ of $S$ such that its displacements $\tau(z)-z$ run through $S$ once each.

Put $A=[d,d+s-1]$ and $B=[d+s,d+3s-1]$. The signed Langford existence theorem gives a permutation $\pi$ of the length-$2s$ interval $B$ whose displacements are $\pm A$. In the signed-sequence notation, if positions $i<0<j$ carry the same symbol $a$, one has $i+j+a=0$. The correspondence $-i\mapsto j$ is a permutation of $[1,2s]$ with displacement $-a$. Translate both its domain and range to $B$. [Jordon and Mitchell, *Signed Langford sequences*](https://doi.org/10.1016/j.disc.2021.112719) · [Author's signed-sequence definition](https://www2.cms.math.ca/Events/summer21/abs/pdf/gd-hj.pdf)

For each $x\in B$ take the triple $(x,-\pi(x),\pi(x)-x)$. Its entries sum to zero. These triples partition $S$ since their three coordinates cover $B,-B,\pm A$, respectively. Within each triple $(u,v,w)$ set
$$
\tau(u)=-v,\qquad \tau(v)=-w,\qquad \tau(w)=-u.
$$
The images partition $-S=S$ and the displacements on the triple are $w,u,v$. This proves the lemma.

## 3. Enlarging a seed

The base degree $b$ will be one of $19,21,23,32,34,36$. Choose a seed at that degree and an even cutoff $D=2d>0$ and odd integer $h$. A label $x$ has speed $v(x)\in\{-1,0,1\}$. For even $x$ set $a=0$ and for odd $x$ set $a=h$. Define
$$
v(x)=
\begin{cases}
-1&x-a\le-D,\\
1&x-a\ge D,\\
0&\text{otherwise}.
\end{cases}
$$
For every old child $x$ at parent $p$, the witness satisfies $v(x)+v(p)=v(x+p)$. Let $s\ge D-1$ and $\Delta=6s$. Move each old label by $f(x)=x+\Delta v(x)$. Each old edge thus retains the correct endpoint sum after moving its weight by the same rule. This also holds at the hub since $f(0)=0$.

Consider either original interval $I=[L,U]$ or $I=[L+1,U]$. For $a=0,h$, the certificate checks that the portion of its parity class from $a-D+2$ through $a+D-2$ belongs to $I$. On that parity, $f$ fixes this central progression and moves the two outside progressions apart by $\Delta$ at each end. Hence $f$ is injective and its image in the interval enlarged by $\Delta$ at both ends omits exactly $a+2S$, with $S=\pm[d,d+3s-1]$. This includes the case of an initially empty outside progression, when the new entries start just beyond the old endpoint. The even and odd missing sets, $2S$ and $h+2S$, are disjoint. In coordinates $(x-a)/2$, the included central progression is $[1-d,d-1]$ and each new gap has length $3s$. Lean checks injectivity and the exact image on an arbitrary such interval. [Lean interval lemma](RadiusTwoIntervals.lean)

Give $o$ one new branching neighbor at each label in $2S$. Its hub edge has the same weight. For each $z\in S$ use child $h+2z$ at the new parent $2(\tau(z)-z)$. Its weight is $h+2\tau(z)$. The lemma uses each new parent exactly once and fills every missing odd label and weight exactly once. The resulting tree has $b+\Delta$ branching neighbors.

## 4. Ordering the enlarged parents and restoring all layers

Here it matters that arbitrary unequal child counts will be assigned to these parents. The required rank order can be extended systematically. For even $b$ take the entire parent list as active. For odd $b$ reserve the initial parent $1$ and take the rest as active. Write $E=b-(b\bmod2)$ for the even active length. Each of the six bases includes a permutation $\sigma$ of $[0,E-1]$ such that its displacements plus one are exactly the active labels.

For a lower band of length $r$, one may give child $L-r+i$ weight $L-r+1+\sigma(i)$, so the parent labels are the displacements plus one. For an upper band, the corresponding child and weight are $U+1+i$ and $U+1+\sigma(i)$, and the parents are the displacements themselves. Extend the active list from even length $r$ by appending $-r$. The permutation taking $i<r$ to $\sigma(i)+1$ and $r$ to zero gives an upper band. From odd length $r$, append $r+1$. Use the permutation taking zero to $r$ and $i+1$ to $\sigma(i)$ to obtain a lower band. Thus every new rank needs only one layer. If parent $1$ was reserved, put its single child in a lower band of length one. When the active band is also lower, concatenate the two lower bands by doing the two extensions successively.

These rules add successive even pairs $(-E,E+2),(-(E+2),E+4),\ldots$. In the base, the even parents of magnitude at least $D$ on the positive and negative sides are exactly $[D,E]$ and $-[D,E-2]$ in steps of two. The certificate checks these identities, $D\le E$, and that every odd parent is fixed by $f$. Therefore the ordered list extended by $\Delta$ places has precisely the parent set $f(P)\cup2S$. Indeed, the positive tail now ends at $E+\Delta$ and the negative tail at $-(E-2+\Delta)$. Beneath the cutoff the old even parents stay fixed.

All parents in any rank with $m_r>1$ are fixed by $f$. Thus the enlarged seed has one full layer together with exactly the prescribed residual short layers, even though some outer parent labels changed their position in child-count order. Assign the ordered parents to the branches and apply Section 1. This proves the enlargement for **every** set of positive branch sizes.

## 5. Coverage and reproducibility

For each residue class of $c$ modulo six, the table gives its base degree, the largest cutoff over its seed witnesses, and the first degree covered by Section 3. Each entry in the last row equals $b+6(D_{\max}-1)$.

| $c\bmod6$ | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Base degree $b$ | 36 | 19 | 32 | 21 | 34 | 23 |
| Largest cutoff | 18 | 18 | 20 | 20 | 16 | 22 |
| First expanded degree | 138 | 121 | 146 | 135 | 124 | 149 |

All smaller degrees in their respective residue classes are covered as follows. The consecutive-interval construction for six and 32 larger even degrees supplies 66 seeds. The direct archive supplies 330 seeds at 96 other degrees, together with the permutation lists for their ranks. The checker computes the exact set of required degrees and residue tuples. [Earlier even degrees](even-layers.md) · [Direct witnesses](radius-two-finite.jsonl.gz) · [Six expanding bases and their 24 seed witnesses](radius-two-frames.jsonl)

At $c=4$, the earlier construction reduces the layer counts to 150 profiles. In 113 of them the unused weight is already the interval minimum, and the restoration rules preserve this. In the other 37 profiles all retained counts are below four, so only rank-two layers could have been discarded. For each such profile the supplementary archive gives a rank-two band of multiplicity $m$ and a consecutive seed for each possible remainder of the actual rank-two count modulo $m$. The two parents used in the band are checked in every variant. Restore groups of $m$ rank-two layers. This covers all four-branch trees with consecutive edge sums, including arbitrary ordinary leaves at the root. [Four-branch reduction](branch-levels.md#four-nonleaf-neighbors) · [Replacement witnesses](four-consecutive.jsonl)

Run from the repository root using standard Python.

~~~sh
python3 -B -m research.hub.all_radius_two
~~~

To replay the separate interval proof with Lean 4.36, run the following command.

~~~sh
lean research/hub/RadiusTwoIntervals.lean
~~~

The verifier checks vertex-label sets, edge sums, parent multiplicities, band displacements, completeness of every residue table, speed compatibility, parity-interval endpoints, the outer parent lists and the active permutations. For each expanding witness it also reconstructs the entire enlarged seed at $s=D-1$. At this endpoint $s=2d-1$ is odd. The transpositions between $i$ and $s+(2i\bmod s)$ for $0\le i<s$ realize displacements $\pm[d,d+s-1]$ on $[0,2s-1]$. This gives a direct check of the expansion at the endpoint independent of the literature construction. The proof for all larger $s$ uses the published signed Langford theorem. [Independent certificate verifier](all_radius_two.py)

The finite and expanding archives are JSON lines, with gzip compression for the larger file. A direct record contains the parent list, one lower/upper band pair per rank, and the seed witnesses in lexicographic order of the remainder tuple. An expanding record also supplies the active permutation and gives each seed as a remainder tuple, cutoff, odd center and parent list for its children. These positive witnesses can be verified without reproducing a solver's search order.

Fresh expanding seeds can also be found using OR-Tools CP-SAT. The search takes the parent and band design, cutoff and center from the archive, then solves for all child assignments anew subject to the speed equation. It runs the same independent checks before printing the record. [Optional search](radius_two_search.py)

~~~sh
python3 -B -m research.hub.radius_two_search 19
~~~
