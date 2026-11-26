# Consecutive edge sums for radius-two trees with six or more branches

**Theorem.** Let every vertex of a tree be within distance two of a vertex $o$. Let $c$ be the number of neighbors of $o$ that themselves have children after rooting at $o$. If $c=6$, or if $c$ is even and $38\le c\le100$, the tree has an integer labeling whose vertex labels are $[L,U]$ and whose edge sums are $[L+1,U]$, each exactly once. The branch sizes and the number of ordinary leaves at $o$ are arbitrary.

Reduction of this single labeling gives a cordial labeling for every positive modulus. In a consecutive interval each residue appears either the quotient or the quotient plus one times upon division of its length by the modulus. Translating the vertices to $[1,n]$ also gives the consecutive edge sums that characterize a super edge-magic labeling. [Youssef, Theorem 4](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## Taking layers of children

Give $o$ label zero. Order the $c$ branching neighbors by decreasing child counts $t_1\ge\cdots\ge t_c\ge1$. Write $P_r$ for the first $r$ parent labels. There are $e_r=t_r-t_{r+1}$ layers consisting of one child at each parent in $P_r$, where $t_{c+1}=0$. Start the parent list with
$$
1,-1,3,-3,2,4.
$$
After an even length $r\ge6$, append $-r$. After an odd length $r\ge7$, append $r+1$. These labels are nonzero and pairwise distinct.

Suppose the vertex and edge intervals are $[L,U]$ and $[L+1,U]$. For a lower list $(p_1,\ldots,p_l)$ give parent $p_x$ the child $L-x$. For an upper list $(q_1,\ldots,q_u)$ give parent $q_x$ the child $U+u+1-x$. If the numbers $x-p_x$ permute $[0,l-1]$ and $x-q_x$ permute $[1,u]$, the new weights are exactly $[L-l+1,L]$ and $[U+1,U+u]$. The new intervals therefore have the same form. An empty list adds nothing.

| Rank | Layers used | Lower list | Upper list |
| --- | ---: | --- | --- |
| 1 | 1 | $1$ | |
| 2 | 1 | | $-1,1$ |
| 3 | 1 | $-1,1,3$ | |
| 4 | 1 | | $-3,-1,1,3$ |
| 5 | 2 | $1,-1,1,3$ | $-3,-3,2,2,-1,3$ |
| 6 | 1 | $1,-3,-1,2,4,3$ | |

These rows can be checked by subtraction. Together the two lists in each row use the required number of copies of each parent in $P_r$.

**Every higher rank can be added in a single layer.** A lower band of length $r$ is equivalent to a permutation $\sigma$ of $[0,r-1]$ with displacements $\sigma(i)-i$ equal to the parent labels minus one. Indeed, use child $L-r+i$ with weight $L-r+1+\sigma(i)$. An upper band similarly uses child $U+1+i$ with weight $U+1+\sigma(i)$, giving displacements equal to the parent labels.

At even $r$, start from a lower permutation $\sigma$ and set $\tau(i)=\sigma(i)+1$ for $i<r$, $\tau(r)=0$. Its displacements are the old parents together with $-r$, giving the next upper layer. At odd $r$, start from an upper permutation and set $\tau(0)=r$, $\tau(i+1)=\sigma(i)$ for $0\le i<r$. Adding one to its displacements gives the old parents together with $r+1$, giving the next lower layer. Each map is a permutation by inspection. The rank-six row supplies the base case.

## Two initial labelings suffice

Start with one rank-$c$ layer, which exists since $e_c\ge1$, and $b=e_5\bmod2$ rank-five layers. The hub and all $c$ parents are present. Set $D$ equal to the list $P_c$ with one additional copy of $P_5$ when $b=1$. The lower endpoint is $L=-\sum_{p\in D}p$ and $U=L+2c+5b$. Indeed, the difference between the total vertex-label sum and the total edge-weight sum in this initial tree must be $L$. The hub is zero and the parent label on each child edge contributes $-p$ to that difference.

For $c=6$ the following table specifies the parents of the children in **increasing order of the unused vertex labels** in $[L,U]$, after removing zero and the parent labels.

| $b$ | $[L,U]$ | Parents of children |
| --- | --- | --- |
| 0 | $[-6,6]$ | $2,3,4,-3,1,-1$ |
| 1 | $[-8,9]$ | $2,3,-1,3,-1,2,4,1,1,-3,-3$ |

For example, in the first row the unused vertex labels are $-6,-5,-4,-2,5,6$. Their edge sums are $-4,-2,0,-5,6,5$. Together with the six hub-edge sums these fill $[-5,6]$. In the second row the eleven child-edge sums are $-6,-4,-7,-2,-5,0,9,7,8,5,6$. Together with the hub-edge sums these fill $[-7,9]$.

For the remaining stated values of $c$, the archive gives the same two lists for each $c$. To verify one list, check its multiset against $D$, fill the interval with the children, and check that the union of the hub-edge sums and the child-edge sums covers $[L+1,U]$ without repetitions. [Initial labelings](even-layer-seeds.jsonl)

After removing the initial layers, the number of remaining rank-five layers is even. Add these in pairs and every other layer one at a time by the preceding rules. Finally give any ordinary leaves at $o$ the successive labels $U+1,U+2,\ldots$. Each is also its edge weight. This proves the theorem, with no search over branch sizes.

The permutation recurrence holds for all ranks. For a new even $c$, two valid initial labelings of the prescribed kind suffice to extend the theorem to that $c$. The archived range does not establish their existence for all $c$.

## Reproduction

Run from the repository root with standard Python. The checker verifies coverage of all 66 initial labelings, their child counts and every endpoint sum. It checks the displacement rules and also constructs 1,122 complete examples. The interval argument covers arbitrary child counts.

~~~sh
python3 -B -m research.hub.even_layers
~~~

The optional search uses OR-Tools CP-SAT. A Boolean variable chooses a parent for an unused integer vertex label. The model uses each target weight once and enforces the required parent multiplicities. Different runs can return different valid labelings. [Construction and checker](even_layers.py) · [Search](even_layer_search.py)

~~~sh
python3 -B -m research.hub.even_layer_search 6
~~~
