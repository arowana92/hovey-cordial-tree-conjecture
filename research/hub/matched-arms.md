# Consecutive edge sums on two centers with two-edge arms

Join two centers by one edge. At the first attach $a$ paths of length two, and at the second attach $b$ paths of length two, using new vertices for every arm.

**Theorem.** If $a+b=2h$ and $\min(a,b)\ge\lfloor h/2\rfloor$, this tree is super edge-magic and $k$-cordial for every positive $k$. One integer labeling works at all moduli. In particular the two sides can have unequal numbers of arms, and both degrees are unbounded. For example, $(a,b)=(5,15)$ is covered. The family is a subfamily of the [diameter-five problem](diameter-five.md).

The central edge and the terminal edge on each arm form a perfect matching. Its contraction is a star. Luiz, Campos and Richter characterize a stronger type of graceful labeling using an $\alpha$-labeled contraction with balanced bipartition. A star with at least three leaves has bipartition sizes differing by at least two. The construction below uses sums in the original tree directly. Krisnawati and coauthors study subdivided double stars with an odd number of vertices inserted in the central edge. Here the centers are adjacent. [Luiz, Campos and Richter, Theorem 14 in the authors' manuscript](https://ic.unicamp.br/~reltech/2017/17-14.pdf) · [Published paper](https://doi.org/10.1016/j.dam.2019.05.004) · [Krisnawati et al.](https://doi.org/10.1155/2020/4285238)

## Assigning the arms

Set $m=2h+1$. Use the label pair $\{i,i+m\}$ on one matched edge for each $0\le i<m$. Reserve $i=h$ for the central edge, with the lower center labeled $h$. The matching sums $m+2i$ are all the odd integers in $[m,3m-2]$. We need the intervening even integers for the $2h$ edges that attach the arms.

For $1\le j\le h$, consider the two arm indices $i=h-j,h+j$. The joining edge weighs $h+i+dm$, where $d$ is the number of its endpoints using the upper member of their pair.

| Distance $j$ | Arm index | Upper endpoints $d$ | Joining weight | Allowed center |
| --- | --- | --- | --- | --- |
| odd | $h-j$ | 1 | $4h+1-j$ | either |
| odd | $h+j$ | 1 | $4h+1+j$ | either |
| even | $h-j$ | 2 | $6h+2-j$ | upper |
| even | $h+j$ | 0 | $2h+j$ | lower |

The odd-distance arms can use either center by putting their parent at the other level. Exactly $\lfloor h/2\rfloor$ arms are forced to each center. Assigning the rest freely realizes the stated populations.

For completeness put $u=\lfloor h/2\rfloor$ and $v=\lceil h/2\rceil$. In increasing order the **halves** of the joining weights comprise four intervals:
$$
[h+1,h+u],\quad [2h+1-v,2h],\quad [2h+1,2h+v],\quad [3h+1-u,3h].
$$
Since $u+v=h$, they partition $[h+1,3h]$. Thus every required even sum occurs exactly once. The vertices fill $[0,2m-1]$ and the edges fill $[m,3m-2]$. Reducing the two intervals gives cordial histograms at every modulus. [Youssef's consecutive-sums implication](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)

## An exact test for the same pair allocation on other trees

Let a perfect matching contract to an arbitrary tree $Q$ of odd order $m$. Suppose a permutation $f$ of $[0,m-1]$ on $Q$ has distinct edge sums modulo $m$. Translate $f$ so its missing sum is $-1$ modulo $m$, which is possible since doubling is invertible. Allocate $\{f(i),f(i)+m\}$ to the two vertices of pair $i$. We can decide in linear time whether some orientation of these pairs makes the integer edge sums consecutive, given the allocation.

The matching sums force the interval to be $[m,3m-2]$. For a quotient edge $ij$, let $z=f(i)+f(j)$ as an ordinary integer. Its weight must be the unique even integer in $[m+1,3m-3]$ congruent to $z$ modulo $m$. These $m-1$ possible targets represent every residue except $-1$ exactly once. The required number of upper endpoints is 1 if $z$ is odd, 0 if $z$ is even and $z\ge m+1$, and 2 otherwise. In the last case the unavailable value $z=m-1$ is excluded by the omitted residue.

Try each of the two orientations on the first pair. Traversing $Q$ from this pair, subtract the already assigned endpoint bit from the required number of upper endpoints. A result of zero or one fixes the other pair's orientation uniquely. Any other value rejects that initial choice. This proves necessity and sufficiency for the specified allocation. For the central star, the center index must be $h$, since twice the center index is its missing sum. Thus the population condition above is exact for this allocation. Other allocations may succeed outside its range.

## Reproduction

The Lean file verifies that each required even weight has a distinct arm index in range, that the endpoint levels give its exact integer sum, and that the two forced sets each have the claimed range. The Python checker independently rebuilds all 13,121 trees in the theorem through $h=160$ and checks their arm counts, labels and actual integer edge sums. On other small trees it exhausts all orientations for 3,056 fixed pair allocations. Of these, 2,575 pass and 481 fail the allocation, in agreement with the linear test. [Lean arithmetic](MatchedArms.lean) · [Constructor](matched_arms.py) · [Independent verifier](check_matched_arms.py)

~~~sh
lean research/hub/MatchedArms.lean
python3 -B -m research.hub.check_matched_arms
~~~
