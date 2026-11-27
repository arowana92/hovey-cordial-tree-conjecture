# Uniform increments at a center with three branching neighbors

**Theorem.** Let a joint have exactly three neighbors with positive numbers of leaf children, and any number of additional direct leaves. Let $n$ count all vertices except the joint. There is a labeling modulo $n$ with the joint at zero, all free labels distinct, and all $n$ new weights distinct. Thus, for **every divisor $k$ of $n$**, the attachment preserves any prescribed $k$-cordial labeling at any vertex of any core, irrespective of its order. Each residue gains exactly $n/k$ occurrences on vertices and edges.

For a core of order divisible by $k$, the attachment extends cordially even when $k$ does not divide $n$. The uniform theorem contrasts with the exact obstructions at a joint with only two branching neighbors. [Two branching neighbors](two-branch-joint.md)

## A sufficient test with two moving populations

Give one of the three branch centers label zero. Let $A,B$ be the positive child populations at the other two, $T=A+B$, $H=n-T$, and $g=\gcd(A,B)$. Give their centers labels $x=B/g$, $y=-A/g$ modulo $n$. They are nonzero and distinct since $0<T/g<n$. They generate the cyclic group. A permutation of the free labels with $A$ shifts by $x$, $B$ shifts by $y$ and $H$ fixed positions realizes all required edges if $x,y$ stay fixed. Zero must then stay fixed as well: a nonzero shift there would send zero to an already fixed center. Use this fixed zero for the remaining center. Give its children and the ordinary leaves the other available fixed labels.

Use the [cyclic potential criterion](three-shifts.md#uniform-increments-for-two-branching-neighbors-at-all-composite-moduli). The three steps $y-x,-y,x$ cost $H,A,B$. Both centers can be fixed if the least cost of reaching $2(x-y)$ from zero is $2T$. Two copies of each of $-y,x$ do reach it at cost $2T$. For every step, multiplication of its displacement by $g$ gives its cost modulo $n$. Since $2T<2n$, any cheaper path must have cost $2T-n=T-H$. Thus a negative target or a positive target smaller than all three generators suffices. For target zero the only path of that cost is empty, so it suffices that $2(x-y)\ne0$.

## Choosing the zero center

Write the child counts in order $a\le b\le c$, and put $u=3+\ell\ge3$, where $\ell$ is the number of ordinary joint leaves. Thus $n=a+b+c+u$. First use $A=a,B=b$, leaving center $c$ at zero. Then $T-H=a+b-c-u<a$, the smallest cost. This works except possibly when $a+b=c+u$ and $g=1$. Indeed in the equality case $n=2T$ and the target displacement is $2T/g$, nonzero modulo $n$ if $g>1$.

In the remaining case set $s=c-b=a-u\ge0$. If $s=0$, the two equal populations $b,c$ may use centers $1,-1$. Use $b$ disjoint adjacent pairs in the ordinary interval $[2,n-2]$, assigning the smaller label in each pair to a child at $1$ and the larger to a child at $-1$. Their weights exchange labels in each pair. The interval has room because $n=2(a+b)$ and $a=u\ge3$. All other labels stay fixed.

Suppose $s>0$. Next use $A=a,B=c$, leaving center $b$ at zero. The only possible cheaper cost is now $2s$. Since $0<2s<2a$ and all positive costs are at least $a$, a cheaper path must use a single step of cost $a,c$ or $b+u$. It cannot cost $c=b+s$ since $s<a\le b$. Two numerical cases remain, in both of which we use $A=b,B=c$ instead.

1. If $2s=a$, then $a=2u$, $c=b+u$ and $\gcd(b,u)=1$. For the new choice the costs are $b,b+u,3u$ and the target cost is $2b-2u$. At most one of the first two costs fits. With neither, divisibility by $3u$ would give $u\mid 2b$. After subtracting either large cost, divisibility would give $u\mid b$. Both are impossible since $u\ge3$.
2. If $2s=b+u$, then $b=2a-3u$, $c=3a-4u$ and $a>3u$. The weak inequality follows from $a\le b$ and equality would violate $\gcd(a,b)=1$. Also $\gcd(a,u)=1$. The costs are $b,c,a+u$ and the target cost is $4a-8u$. At most one of $b,c$ fits. With neither large cost, or after subtracting $b$ or $c$ respectively, divisibility by $a+u$ would force $a+u$ to divide $12$, $7$ or $5$ respectively. This follows by subtracting multiples of $a+u$ and using $\gcd(a+u,u)=1$. But $a+u>4u\ge12$.

This exhausts the choices and proves the uniform theorem. Reduction modulo a divisor gives the uniform counts claimed, and translation puts the joint at its prescribed label.

## Any size on a core of order divisible by the modulus

When $n<k$, add twin leaves at one existing child's parent to reach $k$ free vertices. In the uniform construction every weight occurs once. If a dummy leaf carries the core's deficient weight, exchange its label with its real twin before restricting. The retained free labels and weights are distinct and the required weight survives.

When $n>k\ge6$, retain the three centers, one child at each, and enough other leaves to form a $k$-edge prefix. Give this prefix the uniform construction. Every omitted vertex now has its parent labeled. The ordinary leaf-batch lemma extends over all of them. For $k=3,4,5$, start with the three centers and $k-3$ other leaves. The prefix has at most two branching neighbors and admits the earlier full-block extension, after which the leaf batches apply. For $k=2$ alternately fill the deficient weight and avoid the surplus vertex label in connected order. For $k=1$ all counts are immediate. [Leaf-batch lemma](../counterexample-bound.md#removing-leaves)

The constructor tests the three choices of zero center using the short-path criterion. The verifier rebuilt each original edge and checked 91,520 complete permutations. Another 1,000 tests checked the histograms after reduction to divisors. [Construction and reproducible endpoint checks](three_branch_joint.py)

~~~sh
python3 -B -m research.census.three_branch_joint
~~~
