# Two stars at arbitrary sites of a one-surplus core at prime powers

**Theorem.** Let $k=p^e$ be a prime power. Take a fixed cordial labeling of a tree of order one modulo $k$, with unique surplus vertex label $u$. Attach two stars of arbitrary positive orders by one edge from each center to any prescribed old vertex. At **odd prime powers**, the old labeling always extends. At **powers of two**, the only failure, up to exchanging the stars, has all three properties below.

- The stars have orders $1$ and $k-2$.
- The singleton attaches at a vertex labeled $u$.
- The other star attaches at a vertex whose label differs from $u$ by an odd residue.

Every successful input has a parent-first order of the new vertices and a single labeling cordial on every prefix. In particular every two-star attachment to a prescribed one-surplus core works at **27 labels**. Together with the [divisible-core theorem](two-star-moduli.md), every pair of stars extends from either starting order at every odd prime power. The statement concerns these particular forests.

## One full rainbow batch

Translate $u$ to zero. First suppose the two star orders $s,t$ have sum $k-1$. The new vertex labels must be the nonzero residues, and the $k-1$ new edge weights must be distinct. This also gives balance on every initial segment of any parent-first order. Equal sites, a site at zero, or a singleton are settled by the [equal-site and singleton constructions](two-star-surplus.md#two-intervals-supply-the-prime-construction) and the [exact surplus-site test](surplus-site.md). The latter gives exactly the stated exceptions when a site is zero. We now prove that distinct nonzero sites $a,b$ always work.

Write $m=\operatorname{ord}(a-b)$ and $H=\langle a-b\rangle$. We use second center $y=a$, first center $x=a+h$, and write $B$ for the first star's leaf labels. The required [histogram identity](two-star-surplus.md#a-quadratic-decision-procedure) simplifies to
$$
 (\tau^h-1)1_B=e_0+e_a-e_b-e_{a-b-(s-1)h},
 \qquad |B|=s-1,\quad B\cap\{0,a,a+h\}=\varnothing. \tag{1}
$$
Here $x$ must also be nonzero. Suppose $h$ generates a subgroup of order $M$ containing $a,b$, whose coordinates in units of $h$ are $A,C$. Choose two intervals of lengths $l,v$ immediately before $A,0$, respectively. With $r=s\bmod M$, require
$$
  l+v=r-1,\qquad 0\le l\le A-1,\qquad 0\le v\le M-A-2 .
$$
If $C$ is either starting position, the other starting position is $A-C-(s-1)$ modulo $M$. Thus (1) follows by telescoping. The interval bounds exclude all three forbidden labels. Fill the first star with $\lfloor s/M\rfloor$ whole outside cosets. Adding $h$ preserves each coset. The second star gets all remaining nonzero labels. All local intervals below use these bounds.

### Difference of order at least three

If $a\notin H$, then $b\notin H$. Put the smaller star first and take $h=a-b$, $B=\{b\}\cup\{-ih:1\le i\le(s-2)\bmod m\}$ before adding $\lfloor(s-2)/m\rfloor$ whole cosets disjoint from $H$ and $a+H$. The singleton $b=a-h$ avoids $a,a+h$ because $m\ge3$. The negative tail lies in $H$ and avoids zero. There is room for the cosets since $s\le(k-1)/2$ and $k/m\ge2$. The singleton translates to $a$ and the tail ends just before zero, giving (1). This argument works at arbitrary moduli.

Now let $a,b\in H$. If $1\le s\bmod m\le m-2$, solve the packet inside $H$ with that first star order. The difference of the two sites generates $H$, so the [unit-difference construction](two-star-surplus.md#two-intervals-supply-the-prime-construction) applies. Allocate whole outside cosets as leaves, since both local centers lie in $H$.

For either remaining remainder, one star order $D\in\{s,t\}$ is divisible by $m$. Take $M=p^{1+v_p(D)}$. Then $m<M\mid k$. Put $w=M/m\ge2$ and $r=s\bmod M$. The nonzero remainder of $D$ is a multiple of $M/p$, so both
$$
             r,\quad M-1-r\quad\text{are at least }M/p-1\ge w-1.
$$
These two residues are the local star orders and may be interchanged. We give the construction whenever their minimum is at least $w-1$.

If both are at least $w+1$, choose a generator $h$ of the order-$M$ subgroup with $wh=a-b$. Such generators exist by lifting units modulo $m$ to units modulo $M$. Then $C=A-w$, and $2w\le A\le M-w$ since the sites are distinct and nonzero. Use $l=w$, $v=r-1-w$ provided $A\le M-r+w-1$. If this fails, interchange the stars and use $-h$. The new first site has coordinate $M+w-A$, the new remainder is $M-1-r$, and the required inequality becomes $A\ge M-r$. This covers the other case.

If the smaller local order is $w-1$ or $w$, orient so $r=M-w$ or $M-w-1$. Choose $wh=b-a$. Hence $C=A+w<M$, since $a,b$ are nonzero multiples of $w$ and $b=0$ would be the only wrap at $A+w=M$. Take $v=M-A-w$ and $l=r-1-v$, which is $A-1$ or $A-2$. As $w\ge2$ and $A\ge w$, the bounds hold. The interval before zero starts at $C$.

### Antipodal nonzero sites

The remaining $m=2$ occurs at powers of two. Both sites generate the same subgroup of order $d\ge4$. Indeed, adding the unique element of order two preserves the order of every element of order at least four in a cyclic 2-group. If $1\le r=s\bmod d\le d-2$, take $M=d$, $w=1$. A local singleton is covered by the earlier construction. If $r=0$ or $d-1$, take $D\in\{s,t\}$ divisible by $d$ and put $M=2^{1+v_2(D)}$, $w=M/d$. Orient with first star of order $D$, so $r=M/2$. Here $r\ge w+1$ and $r\le M-w-1$.

In either case solve within the order-$M$ subgroup. For $w+1\le r\le M/2$ choose $wh=-b$. Now $C=M-w$, $A=M/2-w$. Take $v=w$ and $l=r-1-w$. For $M/2+1\le r\le M-w-1$ choose $wh=b$. Now $C=w$, $A=M/2+w$. Take $l=M/2$ and $v=r-1-M/2$. Both formulas meet the interval bounds and put a starting position at $C$. This finishes the prime-power proof for a full batch.

## Arbitrary sizes and prefixes

When $s+t<k-1$, pad at either center to reach $k-1$ and restrict the full construction. There are at least two possible padded splits and at most one exceptional split for fixed sites. When $s+t>k-1$, choose a first batch of $k-1$ containing both centers. If it succeeds, every remaining vertex is a leaf at a prescribed center. Starting from the resulting divisible-order tree, the next leaf can fill the deficient edge weight, and successive rainbow batches of leaves follow by [Hall's construction](../counterexample-bound.md#removing-leaves). Each prefix is cordial.

If every split containing both centers in the first batch is exceptional, the singleton at the zero site must have total order one and the other star has at least $k-1$ vertices. Indeed the allowed first-star interval is $[\max(1,k-1-t),\min(s,k-2)]$, and only an endpoint split can fail. Use the first $k-1$ vertices entirely in the other star. With site $b\ne0$, give its center label $b$ and take the remaining nonzero residues as leaves. Its new weights omit precisely $b$. Insert the postponed singleton next to fill the deficit and continue with leaves. Modulus two allows a single vertex in each rainbow batch and every attachment works there. This proves the theorem for all sizes.

## Verification

~~~sh
out=$(mktemp -d)
c++ -O3 -std=c++17 research/rainbow/check_surplus_pairs.cpp -o "$out/check"
python3 -B -m research.rainbow.check_surplus_prime_powers "$out/check"
~~~

The [constructor](surplus_prime_powers.py) builds the intervals and the parent-first order. The [checker](check_surplus_prime_powers.py) compares every ordered pair of sites and every full split at the composite prime powers through 49 with an [independent endpoint search](check_surplus_pairs.cpp). That search tries ordered centers and assigns each actual leaf to a star subject to the edge-weight exclusions. The checker includes literal leaf-subset enumeration at small moduli, tests larger prime powers through 1024, and joins general-size examples to a labeled old star, checking both histograms after each new vertex.
