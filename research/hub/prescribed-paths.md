# Subdividing an edge with prescribed labels at both ends

Let an edge of a graph have endpoint labels $p,q$, possibly equal. Replace it by a path with $L$ internal vertices. For **every $L\ge76$** and every target $w$, there are distinct integer labels on those vertices, avoiding a prescribed finite set $F$ and $0,p,q$, such that the multiset of the $L+1$ actual edge sums is the multiset of internal labels together with $w$. The same holds in $\mathbb Z/k$ if
$$
k>360\bigl(|F\cup\{0,p,q\}|+L\bigr).
$$
The endpoints and target may be chosen independently, also at even or composite moduli.

## Four short identities

Starting at $p$, write a row $(a,b)$ for an internal label $ap+bt$. Each list below ends at the free parameter $t$. The sums along the list, including the first edge from $p$, permute the entries of the list as integer linear forms. This can be checked by adding consecutive rows, starting with $(1,0)$, and sorting. [Lean proof of the four permutations and of evaluation](PrescribedPaths.lean)

| Length | Rows in path order |
| --- | --- |
| 8 | $(1,-2),(-1,1),(2,-2),(-2,3),(0,-1),(1,-1),(-2,2),(0,1)$ |
| 9 | $(1,2),(2,2),(-4,-5),(3,4),(-1,-1),(2,3),(-2,-2),(-2,-3),(0,1)$ |
| 8, for an extreme integer endpoint | $(0,-2),(-1,1),(0,2),(-1,-1),(1,-1),(-1,3),(1,-2),(0,1)$ |
| 9, for an extreme integer endpoint | $(-1,2),(0,2),(1,-5),(-1,3),(0,-1),(-1,4),(1,-3),(0,-2),(0,1)$ |

At a zero endpoint one may also start with a single vertex $t$ whose incoming edge weighs $t$. Reserve two length-nine lists for the join. Subtract 18 and one more for each zero endpoint from $L$. The remainder $R$ is at least 56. Write $R=8i+9j$ by taking $j$ to be its remainder modulo 8. Indeed $8\lfloor R/8\rfloor\ge 8j$. There are at least two lists in this decomposition. Use one as preparation at each nonzero endpoint, or the singleton at a zero endpoint. Put the spare lists successively on the left, before its final preparation list. Equivalently, each side grows outward from its prescribed endpoint and the left can have more than one preparation list.

Choose the earlier left lists one at a time. In the final step let the left and right preparations end at $U,V$. Grow a generic nine-list from $U$ ending at $T$ and another from $V$ ending at $w-T$. Join the latter endpoints. Reading the whole right side in reverse preserves its edge sums. The joining edge supplies $w$.

To enforce distinctness, collect the $b\le36$ entries in the current step as affine forms in at most three parameters. Exclude equality with each of the $f$ forbidden values (including all previously used internal labels) and with each other. There are $bf+\binom b2<36(f+b)$ constraints. A preparation with a fixed nonzero parent has all terminal coefficients nonzero. In the generic lists, rows with the same terminal coefficient have first coefficients differing by one, so their difference is the nonzero parent up to sign. For an extreme integer preparation the first coefficients of such rows are distinct, which also suffices. Singleton preparations need no pair check.

Preparations on opposite sides use different parameters. Every vertex on the final two nine-lists has a nonzero coefficient of $T$, while the preparations have none. Within either final list the row pairs are distinct. Across the two lists the coefficients of $U$ and $V$ distinguish all comparisons except the pair of terminal rows, which has difference $2T-w$. Thus each exclusion is a nonzero constant or has a nonzero integer parameter coefficient of absolute value at most 10. A constant comparison at a fixed modular parent is already nonzero modulo $k$ by the generic row property.

Assign each nonconstant exclusion to its last nonzero parameter and choose the parameters in order. Over the integers it rules out at most one choice at that stage. Any consecutive interval of $36(f+b)$ values for each parameter suffices, including intervals with independently prescribed signs. Modulo $k$ each exclusion rules out at most 10 choices by the linear congruence criterion. Since $f+b\le |F\cup\{0,p,q\}|+L$, the asserted bound suffices. The choices keep each intermediate parent nonzero as required by the next list. [Executable construction](prescribed_paths.py)

## Linear leaf bound for long subdivisions

Take any finite tree or connected unicyclic multigraph. Subdivide **each** original edge with at least 76 internal vertices, with independent choices of lengths. Let the resulting order be $N$. Adding at least **$830N$ leaves** at any chosen **original** vertex gives a super edge-magic graph and hence a cordial labeling at every modulus. The latter implication follows by reducing consecutive vertex labels and consecutive endpoint sums, translating the vertex labels if necessary. Loops and parallel edges in the coarse unicyclic graph give ordinary cycles and internally disjoint paths after subdivision.

Put the chosen site at zero, set $M=36N$, and give the other original vertices distinct labels in $[1,N]$. For a tree of original order at least two, give one of those other vertices $g=-10M$ instead. Assign the original edges distinct targets consisting of all original vertex labels in the unicyclic case, or all except $g$ in the tree case. For each edge apply the path construction avoiding all original and previously added labels. Now $f+b\le N$ throughout. Choose each parameter in $[1,M]$, except that the first terminal parameter at an endpoint $g$ is chosen in $[-M,-1]$ using the extreme list. The last terminal values $T,w-T$ lie in $[-M,M]$. All ordinary lists use parents of magnitude at most $M$, hence labels of magnitude at most $9M$.

In an extreme list the rows with first coefficient one have negative second coefficient. Their values are strictly above $g$. The other rows are also above $g$, and all rows are at most $13M$, by inspection of the two extreme lists. Thus the label span is at most $23M=828N$. All vertex labels are distinct. The edge sums are exactly the vertex labels with the minimum omitted in the tree case, and all vertex labels in the unicyclic case. Fill every hole in their integer interval by placing that label on a new leaf at the zero site. Fill upward for all remaining leaves. Both the vertex labels and the sums become consecutive intervals. The case of an original single-vertex tree follows by labeling the leaves consecutively. The [general quadratic leaf bound](quadratic-endpoint.md) also applies to unsubdivided trees.

## Preserving a labeled core

Let a coarse tree with at least one edge meet a prescribed labeled core in a single original joint. Prescribe labels modulo $k$ on **all** original vertices, consistent at the joint and pairwise distinct on the others. The joint may share a residue with another original vertex. Subdivide each coarse edge as above; let $N$ count the new vertices, excluding the joint, before any extra leaves. Choose an original site and attach any number $h$ of extra leaves there. If $k>360(N+3)$, both statements below hold.

* Any cordial labeling of a core whose order is divisible by $k$ extends, with the prescribed labels retained.
* If $k$ divides $N+h$, the construction can give uniform vertex and edge increments at any labeled core.

Translate vertex labels to put the chosen site at zero; weights translate by twice that amount. Let $S_0$ consist of the free original labels. For the second assertion take $S_0$ as the targets. For the first, replace one occurrence of any $g\in S_0$ by the core's deficient weight $d$ in the translated coordinates. These targets may form a multiset. Avoid all original labels and targets during the path construction. There are at most $N+3$ occupied or currently allocated values including zero. If $S$ is the set of the $N$ resulting free labels, the new weights are $S$ in the uniform case, or $S-\{g\}+\{d\}$ in multiset notation. The deficit of the old core cancels $d$, leaving a histogram equal to a constant plus the indicator of $S\setminus\{g\}$.

Label the extra leaves first from the complement of $S$, in any order. If leaves remain, repeat full permutations of the residues starting with $g$, stopping at the required length. Their actual edges have their vertex labels as weights in the translated coordinates. Both histograms stay balanced at each step in the deficit case. In the uniform case both increments have complete periods when $k\mid N+h$. Translate back to recover all prescribed labels.

The checker reconstructs the subdivided edges from the original incidence lists. It checks 279 bridges, 36 completed integer graphs (including coarse loops and parallel edges), and 15 modular attachments with full histograms. Lean covers the path table identities. The parameter avoidance, size bounds and attachment arguments are proved above. [Independent checker](check_prescribed_paths.py)

~~~sh
python3 -B -m research.hub.check_prescribed_paths
lean research/hub/PrescribedPaths.lean
~~~
