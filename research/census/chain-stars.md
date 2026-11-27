# Chains of stars with monotone sizes and arbitrary joining leaves

**Theorem.** Take stars with positive leaf counts $a_0,\ldots,a_{q-1}$ in nondecreasing or nonincreasing order. For every consecutive pair join an arbitrarily specified leaf of each star by an edge. The two joins at an intermediate star may use the same leaf or different leaves. At every path length, the resulting tree admits a bijection onto $[0,N-1]$ with consecutive ordinary edge sums. The two bipartition classes also occupy consecutive intervals, so complementing the labels within the lower class gives an $\alpha$-labeling in the usual difference convention. In particular, the tree is cordial at every positive modulus.

When every intermediate star uses the same leaf for both joins the tree is a firecracker. Setiawan et al. proved a super edge-magic labeling for firecrackers with monotone star sizes. The construction below allows the two endpoints in every intermediate star to be specified independently, and gives an exact feasibility test for its block arrangement for an arbitrary sequence of sizes. [Setiawan et al., Theorem 3.2](https://ijc.or.id/index.php/ejgta/article/viewFile/1585/pdf_248)

## Local ranks

Reverse the path if necessary to make its sizes nondecreasing. Put leaves of even-indexed stars in the first global bipartition class and leaves of odd-indexed stars in the second. Each center goes in the opposite class. Let $A$ be the size of the first class. Allocate labels $[0,A-1]$ to that class and $[A,N-1]$ to the second, processing the stars in path order within each class. At each star its center gets the next available label in its class; its leaves fill the next $a_i$ labels of their class in some order. Number the available positions within a leaf block by ranks $0,\ldots,a_i-1$.

Let $P_i=\sum_{j<i}(a_j+1)$. The internal spoke sums of star $i$ fill
$$
[A+P_i,\ A+P_i+a_i-1].
$$
There is a single gap $A+P_i+a_i$ before the next star's interval. Suppose the two leaves on the join to star $i+1$ have local ranks $r,s$. The block of leaves at the second star starts one label after the center of the first in their common class. The joining sum is therefore $A+P_i+1+r+s$. It fills the gap exactly when
$$
r+s=a_i-1 .
$$

Choose an outgoing rank in star zero. At every subsequent star, its incoming rank is the complement of the previous outgoing rank in the previous block. It is available because $a_i\le a_{i+1}$. Reuse it if the joins share a leaf, and otherwise choose a different outgoing rank. Two distinct specified leaves guarantee at least two positions. Assign all unused ranks to the other leaves in any order. The sums now fill $[A,A+N-2]$. When converting to differences, $x\mapsto A-1-x$ on the lower class turns each sum $s$ into the positive difference $s-(A-1)$.

This argument also describes a gluing rule for general $\alpha$-labeled pieces in their sum convention. Put the ranks of each local bipartition class in a consecutive block, orienting successive pieces so the joining endpoints have opposite global colors. The edge sums within piece $i$ start at $A+P_i$ and cover $|V_i|-1$ positions. A joining edge fills its gap precisely when the two local ranks sum to one less than the size of the local class containing the outgoing endpoint.

## Testing any size sequence for this construction

Carry the set of feasible incoming ranks forward. At the first star every outgoing rank is possible. At a reused leaf keep exactly the incoming set. At distinct incoming and outgoing leaves, every outgoing rank is possible if there are at least two possible incoming ranks; if there is only one, exclude that one rank. Map each possible outgoing $r$ to $a_i-1-r$ and retain only values below $a_{i+1}$. By induction the next set is exactly the set attainable by the processed prefix. Backtracking from a surviving rank constructs labels for the original attachment leaves. Both directions of the path may be tried. A failure of this layout alone says nothing about other labelings.

The verifier compares this dynamic program with exhaustive independent permutations of all actual leaf ranks on 7,032 small size and attachment patterns, including nonmonotone inputs. It verifies the 5,130 successful forward labelings and 320 further monotone chains of up to 75 stars. The checks reconstruct the original joins, bipartition boundary, full integer vertex interval and every integer edge sum. [Constructor](chain_stars.py) · [Independent checks](check_chain_stars.py) · [Branching quotients](star-joins.md)

~~~sh
python3 -B -m research.census.check_chain_stars
~~~
