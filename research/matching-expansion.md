# Doubling an odd modulus by contracting a perfect matching

**Theorem.** Let $M$ be a perfect matching of a finite tree $T$, and let $Q=T/M$ be the tree obtained by contracting all its edges. For every odd $m\ge1$, if $Q$ is $m$-cordial then $T$ is $2m$-cordial. The order of $Q$ is arbitrary and its labeling may repeat residues. At $|Q|=m$, this recovers the matching case of the [odd-quotient theorem](odd-quotient.md).

In particular, **every tree with a perfect matching is $k$-cordial at $k=22,26,30,34,38,42$**, by the all-tree results at the odd moduli through 21. At every modulus $k\equiv2\pmod4$, the result applies if $Q$ is a caterpillar or has diameter at most four. Consequently it applies to every tree of diameter at most six with a perfect matching. Indeed, lift a longest path of $Q$ to $T$. If $Q$ has at least two vertices, each terminal block has just one joining edge, and its second matching endpoint extends the lifted path by one edge at each end. Thus $\operatorname{diam}(Q)+2\le\operatorname{diam}(T)$. The single-block case is immediate. [Hovey's caterpillar theorem](https://doi.org/10.1016/0012-365X(91)90254-Y) · [Diameter-four theorem](hub/all-radius-two.md)

## The labeling

Give the two vertices of each matched pair opposite bits. Along every edge outside the matching give its endpoints equal bits. Start with either bit at one vertex and propagate along the unique paths of $T$. If the contracted vertex has label $x\in\mathbb Z_m$, put the two residues $2x$ and $2x+m$ modulo $2m$ on its vertices, according to their bits. Since $m$ is odd, each parity class receives a permuted copy of the vertex histogram of $Q$.

A matching edge has weight $4x+m$. This runs bijectively over the odd residues as $x$ runs over $\mathbb Z_m$, so the odd weights reproduce the vertex histogram. A joining edge between pairs with labels $x,y$ weighs $2(x+y)$ modulo $2m$, since its bits agree. The even weights therefore reproduce the edge histogram of $Q$.

Write $s=|Q|$. A balanced histogram of total $s$ on $m$ residues and one of total $s-1$ on $m$ residues have combined range at most one. If $s=am$, the first is constant $a$ and the second has counts $a-1,a$. If $s=am+r$ for $0<r<m$, both have counts in $\{a,a+1\}$. This proves the theorem at all orders.

## Equal stars in place of vertices

Let $t\ge2$. Replace each vertex of an $m$-cordial tree $Q$ by a star on $t$ vertices. Join the stars along the edges of $Q$, each time joining two centers or two leaves. Repeated use of any attachment vertex is allowed. For odd $m$, the result is $tm$-cordial, even when $t$ and $m$ share factors. In particular, adding $t-1$ leaves at every vertex of any $m$-cordial tree gives this conclusion at odd $m$.

Give the center digit zero and the leaves the nonzero digits modulo $t$. Order the stars outward from a root of $Q$. For each joining edge arrange that its digits are negatives of each other. A child star needs at most one prescribed leaf digit when its turn comes, so this is always possible. Choose representatives $R_a\in\mathbb Z_{tm}$ congruent to $a$ modulo $t$, with $R_0=0$ and $R_{-a}=-R_a$. Choose either sign pair freely. For the nonzero self-opposite digit at even $t$, use $R_{t/2}=tm/2$, which has the required digit because $m$ is odd.

In a star at quotient label $x$, put $tx+R_a$ on the vertex with digit $a$. Each vertex digit receives a copy of the quotient vertex histogram. For every nonzero digit $a$, the internal weight $2tx+R_a$ also gives a permuted copy of this histogram, since doubling permutes $\mathbb Z_m$. All joining edges weigh $t(x+y)$ and reproduce the quotient edge histogram in digit zero. Apply the same consecutive-totals argument as above. At $t=2$, either endpoint can serve as a center. The bits from the matching proof make every joining edge have like types. For comparison, the [repeated-product construction](repeated-product.md) allows more general pieces when the quotient has a bijective labeling at its order.

## Independent checks

The verifier builds the original edges from the specified attachment ports and computes full histograms, including unused residues. It checks the complete zero-digit row against the quotient edge counts, and each other row against the quotient vertex counts. Its 10,850 matching examples include all four ways to join each neighboring pair for every rooted quotient through five vertices at four odd moduli. The 3,696 star examples include repeated uses of one leaf, factors shared with the quotient modulus, and nonuniform quotient histograms. [Constructor](matching_expansion.py) · [Checker](check_matching_expansion.py)

~~~sh
python3 -B -m research.check_matching_expansion
~~~
