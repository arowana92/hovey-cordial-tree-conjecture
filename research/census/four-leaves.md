# Trees with at most four leaves

**Theorem.** Every finite tree with at most four leaves has a bijection from its vertices to the integers from 0 to $n-1$ under which the sums on its $n-1$ edges are consecutive. In particular every such tree is super edge-magic and is $k$-cordial for every positive integer $k$. One can reduce the same labeling modulo any $k$, since the frequencies of the residues of a consecutive interval differ by at most one.

For example, the three arms of length two at a common center give a small case where gluing at an extreme path label fails. Label the center 3 and the arms in outward order $(6,0),(5,2),(1,4)$. The edge sums are precisely $4,5,6,7,8,9$. The general proof assembles paths of arbitrary lengths and checks a finite list of such exceptions. [Integer certificates](four-leaf-certificates.json) · [Witness constructor](four_leaves.py)

Panpa, Imnang and Wasuanankul studied graceful labelings of spiders with up to five legs and gave $\alpha$-labelings for several of the building blocks used here. Meng's verification archive treats super edge-magic spiders with equal leg lengths, including the four-leg case. The theorem above allows unequal lengths and also covers trees with two branching vertices. [Panpa, Imnang and Wasuanankul (2025)](https://doi.org/10.1155/jama/5826777) · [Meng's equal-leg archive (2026)](https://zenodo.org/records/22652143)

## Two ways to join labeled trees

Use a bipartition with classes of sizes $A,B$. In each class assign ranks starting at 0, using every rank below the class size once. Require the edge rank sums to be exactly $0,\ldots,A+B-2$. Adding $A$ to all ranks in the second class produces the required ordinary vertex labeling. These ranks are also an equivalent description of an $\alpha$-labeling, by replacing the second-class rank $y$ by the ordinary graceful label $A+B-1-y$. Reflecting both rows of ranks around their midpoints preserves the rank property. A vertex of rank $x$ in a class of size $A$ has *deficiency* $A-1-x$.

Join two vertex-disjoint ranked trees $U,V$ by an edge $uv$, where $u\in U$. Align their bipartitions and increase the ranks in each class of $V$ by the size of the corresponding class in $U$. All ranks in the union now run consecutively in each class. The edge sums inside $U$ and $V$ occupy the intervals starting at 0 and $|U|$. The missing sum $|U|-1$ occurs on the join precisely when the deficiency at $u$ equals the original rank at $v$. This rule applies to a sequence of disjoint blocks joined consecutively. Earlier blocks add their total order to each subsequent bridge sum. A block may have just one vertex, and its two bridges may use the same vertex.

Alternatively, identify a vertex of maximum rank in $U$ with a vertex of rank zero in $V$. Align their classes and use offsets as before, decreasing the offset in the shared class by one. The shared ranks agree and all class ranks are used once. The sums inside $V$ now begin at $|U|-1$, immediately after the sums inside $U$.

## Paths with a specified rank

Rosa's path theorem allows rank zero at any prescribed vertex except the middle of the five-vertex path. Cattell studied prescribed labels on paths more generally. Here are constructive details for all path facts used below. A path's order always counts vertices. [Rosa, *Labeling snakes*](https://combinatorialpress.com/ars/vol3/) · [Cattell, *Graceful labellings of paths*](https://doi.org/10.1016/j.disc.2007.03.046) · [Ichishima et al., Theorem 4.1](https://repositori.udl.cat/bitstreams/5feb8d0f-e765-4fa4-8651-a92f42b3131f/download)

**Endpoint lemma.** A path on $n$ vertices can start at rank $h$ whenever $0\le h<\lceil n/2\rceil$ and either $h=0$ or $n\ne4h+1$. Its far endpoint then has deficiency $h$. Indeed, summing its edge rank sums gives twice the total of its vertex ranks minus the two endpoint ranks. Substitution of the two class sizes gives endpoint rank sum $\lceil n/2\rceil-1$, including on the singleton with its endpoint counted twice. For $n=4h+1>1$ this identity would force equal ranks at the distinct endpoints in the same class.

Write $W_n$ for the path with rank at position $i$ equal to $\lfloor i/2\rfloor$, starting at $i=0$. Its edge sums increase by one. For $h=0$ take $W_n$. Reflect ranks to assume $2h\le\lceil n/2\rceil-1$. Use induction on the order after this normalization.

- For $n=2m$ and $m=2h+1$, start with $W_{2h+1}$ in reverse order. Follow it with the $2h+1$ entries $2h-\lfloor i/2\rfloor$ for $0\le i\le2h$. The two portions have edge sums $0$ through $2h-1$ and $2h+1$ through $4h$, with bridge sum $2h$. The first portion uses ranks $0$ through $h$ in its first class and $0$ through $h-1$ in the second. The remaining entries fill both classes to $2h$.
- For $n=2m$ and $m\ge2h+2$, take $W_{2h+2}$ in reverse order. It starts at rank $h$ and ends at deficiency $h$. Join it by an edge to the smaller even path of order $2(m-h-1)$ starting at rank $h$. The latter class has size at least $h+1$.
- For $n=2m+1$, the hypotheses after normalization give $m\ge2h+1$ when $h>0$. The reverse of $W_{2h+1}$ starts at rank $h$ and ends at deficiency $h$. Join it to an even path of order $2(m-h)$ starting at rank $h$.

**Internal ranks.** Let $a\le b$ be the positive distances of a marked vertex from the two tips of a path. It can attain rank one except for $(a,b)=(1,1),(1,4),(4,4)$. More generally, for every $h\ge1$, every position on every path of order at least $12h+13$ can attain rank $h$.

For $a\ge4h+5$, put $u=2h+(a\bmod2)$, $v=b\bmod2$. Start with $W_{u+v+1}$, marked at position $u$, where its rank is $h$. Extend the left arm by $C=a-u$ vertices. This is an even path starting at the old left tip's deficiency $\lfloor(u+v)/2\rfloor$. The endpoint lemma applies since $C\ge2\lceil(u+v+1)/2\rceil$. Use the old tree as the first block, leaving its ranks unchanged. The old right tip initially had maximum rank. Its deficiency is now $C/2$ because both classes grew by $C/2$. Extend it by the even path with $D=b-v$ vertices starting at $C/2$. Here $D-C\ge 2h\ge2$, since rounding $b$ and $a$ down to even integers preserves their order.

For $a<4h+5$ and $b\ge a+4h+4$, put $v=2h+(b\bmod2)$. Start with the reversed $W_{a+v+1}$ marked at distance $v$ from the right. The right tip has rank zero and deficiency $\lfloor(a+v)/2\rfloor$. The remaining $b-v$ vertices form an even path of sufficient size by $b-v\ge 2\lfloor(a+v)/2\rfloor+2$. The omitted internal cases have order at most $12h+12$. Endpoints follow from the endpoint lemma. At $h=1$ exactly 64 pairs remain. The certificate gives rank rows for 61. Exhausting the permutations within the two classes excludes the other three.

For completeness the constructor also implements Rosa's rank-zero statement using four small rows. In the table, the mark is $u$ edges from the first tip, and the other tip is at distance $v$. Let $l,r$ be the two tip deficiencies.

| Parities of $a,b$ | $u,v$ | Seed rank row | $l,r$ | Lower bound on $a$ |
| --- | --- | --- | --- | ---: |
| odd, even | 1, 0 | 0 0 | 0, 0 | 3 |
| even, odd | 4, 1 | 1 2 2 0 0 1 | 1, 1 | 8 |
| odd, odd | 5, 1 | 1 2 3 1 0 0 2 | 2, 1 | 11 |
| even, even | 6, 2 | 1 2 4 3 2 0 0 1 3 | 3, 1 | 14 |

Extend first by $C=a-u$ at the left tip, then by $D=b-v$ at the right. The table ensures $C\ge2l+2$ and $D-C\ge2r+2$ in each parity class, so both even extensions exist. Below the listed threshold, use the reversed $W_{a+1}$ and append $b$ vertices at the marked tip starting at $\lfloor a/2\rfloor$. When the endpoint lemma does not supply this row, $a\le13$ and $b\le27$. Direct substitution leaves the midpoint $(2,2)$ and the twelve positive cases in the certificate.

## One branching vertex

Write $S(t_1,\ldots,t_m)$ for a spider with terminal paths of the given edge lengths. With three arms, choose two whose lengths are not both two. Their path has rank zero at the center, so reflect it and identify its center with the rank-zero endpoint of the third arm. Only $S(2,2,2)$ remains, covered by the example above.

With four arms and at most two of length two, split them into pairs so neither pair is $(2,2)$. The two paths have rank zero at the center. Reflect one and identify the centers. In the remaining case write the tree as $S(2,2,2,t)$. The certificate gives ranks on $S(2,2,2,5)$ with rank two at the tip of the long arm. Reflect it and append $t-5$ vertices at that tip, starting at rank two. This covers $t=5$ directly and all $t\ge10$ except 14. The certificate supplies ordinary integer labels for $t=1,2,3,4,6,7,8,9,14$.

## Two branching vertices

Let the centers be $u,v$ at distance $g\ge1$, with two terminal arms at each. If neither pair is $(2,2)$, give the two marked arm paths rank zero at the centers. Reflect the left path. Join them directly when $g=1$ and otherwise insert a block on the $g-1$ internal vertices of the connector. That path starts at zero and ends at deficiency zero. Both bridges satisfy the disjoint-block rule.

It remains to take left lengths $(2,2)$ and right lengths $c\le d$. The left center has rank one in $W_5$. First suppose we can present the right block with rank one at a vertex a distance $g$ from $u$.

- At $g=1$ join directly after reflecting the left block. Whenever $g-1\ge3$ and $g-1\ne5$, insert the path on $g-1$ vertices with initial rank one and final deficiency one.
- At $g=2$ or 6, absorb the internal connector into the left block, obtaining $S(2,2,j)$ for $j=1$ or 5. Its new tip has a certified rank one. Reflect this tree and join the right block by one edge.

Thus any right block presented at rank one works at every distance except three. The ordinary right arm path supplies such a block unless $(c,d)$ belongs to $E=\{(1,1),(1,4),(4,4)\}$. For each pair in $E$, the cases $g=1,4$ have direct integer witnesses. At every other $g$, absorb the connector vertex nearest $v$ into the right block $S(c,d,1)$. Its new tip has certified rank one. Its distance from $u$ is $g-1\ge1$ and differs from three, as required.

There remains $g=3$ for ordinary right arm paths. Absorb all three connector edges into $S(2,2,3)$. Its tip is $v$ and has a certified rank one in a class of size four. Its deficiency is two. If one free arm of length $c$ or $d$ supports endpoint rank one on that many vertices and the other supports endpoint rank two, take the three disjoint blocks in order. The first arm ends at deficiency one, the middle block receives the bridge at $v$ and sends the next bridge from the same $v$, and the last arm starts at rank two.

If $c=1$ or 2, absorb this arm into $S(2,2,3+c)$. The vertex $v$ at distance three from $u$ has a certified rank zero, so reflection permits the remaining arm of length $d$ to start at zero. Finally suppose $c,d\ge3$. Every length at least 10 supports both ranks, and every length at least 3 supports at least one. Testing lengths 3 through 9 leaves precisely $(3,3),(3,4),(3,9),(4,4),(4,9),(5,5),(9,9)$. Each has a direct integer witness.

For a nontrivial tree the sum of $\deg(v)-2$ over branching vertices is the number of leaves minus two. Thus the shapes handled above, together with paths, exhaust the theorem. The singleton uses label zero.

## Reproduction

From the repository root run

~~~sh
python3 -B -m research.census.check_four_leaves
lean research/census/FourLeafArithmetic.lean
~~~

The independent checker constructs the edges directly from the lengths, verifies all 105 certificate rows, and exhausts the four small negative marked-rank cases. For the spider records, number the center 0, then number each arm outward in the stated order. A double-fork record names $c,d,g$. Number the left block as $S(2,2,g)$, then number the two arms at its last tip in order $c,d$. The checker also verifies 6,441 endpoint constructions, 18,941 marked paths and 11,791 assembled trees. These sample counts test the implementation. The length inequalities and the shape classification establish the universal quantifiers. [Checker](check_four_leaves.py)

Lean 4.36 checks the two-ended path inequalities, the long-path bound, and the complete lists of exceptional connector and arm lengths. The graph constructions and the certificate checks are given above. [Lean arithmetic lemmas](FourLeafArithmetic.lean)
