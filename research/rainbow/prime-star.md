# A star extension for every prime modulus

**Theorem.** Let $p$ be prime and let a rooted forest have at most $p-1$ free vertices. Suppose at most one free vertex has children, and each component root has an external parent of arbitrary prescribed label in $\mathbb F_p$. For every forbidden residue $u$, the free vertices have distinct labels avoiding $u$ and all the new edge weights are distinct.

The external parent labels of the singleton components can vary independently. The [divisibility obstruction](pinned-star.md) supplies composite-modulus examples in the same family.

Pad a nonempty smaller forest by singleton components to reach $r=p-1$ free vertices. A witness restricts to the original forest. Translating the boundary and free labels lets us take $u=0$. The empty forest is immediate.

## A signed count independent of the boundary modulo p

The next argument applies to *any* rooted forest on $r=p-1$ free vertices. Number them from 1 to $r$, put $D=\mathbb F_p^\times$, and let $y_i$ be the edge sum from free vertex $i$ to its parent. For a bijection $x$ of the vertices onto $D$ with distinct weights $y_i$, let $m$ be its missing weight. Assign the labeling the sign of the permutation $0\mapsto m$, $x_i\mapsto y_i$ of the field. Denote the sum of these signs by $N$.

**Lemma.** The residue of $N$ modulo $p$ is independent of all prescribed boundary labels.

Write $V(z)=\prod_{i<j}(z_j-z_i)$. The polynomial $P(x)=V(x)V(y)$ has total degree at most $r(r-1)$. The coefficient $C$ of $\prod_i x_i^{r-1}$ is independent of the prescribed boundary labels, since selecting a constant boundary term lowers total degree. Put $Q(z)=\prod_{v\in D}(z-v)$. The finite-grid coefficient formula gives
$$
C=\sum_{x\in D^r}\frac{P(x)}{\prod_i Q'(x_i)}.
$$
For completeness, univariate Lagrange interpolation yields $\sum_{v\in D}v^e/Q'(v)=0$ for $0\le e<r-1$ and gives 1 for $e=r-1$. On a monomial of total degree at most $r(r-1)$ other than the target, at least one exponent is less than $r-1$. Multiplying the univariate sums proves the formula. [Schauz, *Algebraically Solvable Problems*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/734)

Only bijective $x$ with distinct $y_i$ contribute. The denominator is then a fixed nonzero field element, as is $V(x)^2$. Adjoining 0 to the front of $x$ multiplies its Vandermonde by $\prod_{v\in D}v$. Adjoining $m$ to $y$ multiplies its Vandermonde by the same factor, since the $y_i-m$ enumerate $D$. The two enlarged tuples are permutations of the entire field. Thus $V(y)/V(x)$ is exactly the sign assigned above. It follows that $C$ is a fixed nonzero factor times $N$ in the field. This proves the lemma.

## Evaluating the star

Specialize every boundary label to zero. Let the nontrivial component have center label $a\ne0$ and $j$ leaves with label set $A$. If all components are singletons, mark one as center and take $j=0$. The center and all singleton vertices contribute their own labels as weights. For the weights to be distinct, the shifted leaf labels must satisfy $a+A\subseteq A\cup\{0\}$. This condition is sufficient as well, since translation is injective.

Addition by $a$ is one cycle of length $p$. Starting at any member of $A$, its successive translates must stay in $A$ until they reach 0. Consequently $A$ is precisely $\{-a,-2a,\ldots,-ja\}$. This set works, since $j\le p-2$. The permutation defining the sign fixes the center and every singleton label and cycles the $j+1$ residues in $A\cup\{0\}$. Hence its sign is $(-1)^j$. There are $p-1$ choices of $a$, $j!$ orders of the star leaves and $(p-2-j)!$ orders of the singleton vertices. We obtain
$$
N=(p-1)(-1)^j j!(p-2-j)! \quad\text{at zero boundary.}
$$
None of the factors vanishes modulo $p$. The lemma gives a nonzero signed count modulo $p$ at every boundary assignment, so at least one rainbow labeling exists. This proves the theorem.

## Consequence for minimum counterexamples

Write $t=(n-1)\bmod p$ for a minimum counterexample of order $n$ and $L$ for its number of leaves. The leaf argument gives $t>0$ and $L<t$. If $L=t-1$, first remove all $L$ original leaves. The remaining tree has at least two vertices, since $n\ge t+1$. Remove one of its leaves as well. Exactly $t$ vertices have been removed, the core is connected, and the added forest consists of a star and singleton leaves. By minimality the core, of order $1\bmod p$, has a cordial labeling with uniform edge counts and a unique surplus vertex label. Apply the theorem with that surplus residue forbidden. The extension is cordial. We conclude
$$
L\le t-2\le p-3.
$$

For odd $p$, subdividing an edge by $p$ vertices adds one to every vertex and edge count. Starting at an endpoint labeled $a$, insert the labels $a+1,\ldots,a+p$ before the other endpoint. The first $p$ weights are $2a+2i+1$ for $0\le i<p$, which run through the group. The last edge retains the original weight. Thus a path between branching vertices in a minimum counterexample has length at most $p$. Each pendant path has length at most $p-1$ by the earlier pendant-path extension. If $p\ge7$, suppressing degree-two vertices and counting the remaining edges now gives
$$
n\le 1+L(p-1)+(L-3)p \le 2p^2-10p+4.
$$

The suppression count uses at most $L-3$ internal segments. [Degree count](../counterexample-bound.md#counting-the-remaining-vertices)

## Where the coefficient test runs out

At $p=11$, take five singleton components and two stars with one and two leaves respectively. With every boundary label zero there are 12,000 positive and 38,400 negative labelings. The signed count is $-26{,}400$, divisible by 11. Thus nonvanishing of this single coefficient cannot certify every forest, even for primes. The count itself exhibits many rainbow labelings at this boundary.

To reproduce the exact enumeration independently of the polynomial argument, run from the repository root

```sh
python3 research/rainbow/signed_count.py 11 -1 0 -1 2 2 -1 -1 -1 -1 -1
```
