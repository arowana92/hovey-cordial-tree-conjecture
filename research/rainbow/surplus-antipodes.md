# Antipodal obstructions on a one-surplus core

**Theorem.** Let $k=2n$, and normalize the unique surplus vertex label of a fixed old core to zero. Attach a star of order $s$ at a vertex labeled zero and a star of order $k-1-s$ at a vertex labeled $n$, where $1\le s\le k-2$. The core extends exactly when some divisor $m\ge3$ of $k$ satisfies one of the following conditions, writing $r=s\bmod m$ in $[0,m-1]$.

| Order $m$ | Condition |
|---|---|
| Even | $m/2-1\le r\le m-2$ |
| Odd | $s\ge m$ and $r\le m-2$ |

In particular at $k=2p$ for an odd prime $p$, extension fails exactly for $1\le s\le p-2$. At **26 labels** this gives all star orders **1 through 11** at the surplus vertex when the other parent is its antipode. A star core of order $k+1$, centered at zero with leaves labeled by every residue once, realizes these prescriptions. Attach the new centers to leaves labeled zero and $n$. The resulting tree is a caterpillar and is ordinarily cordial at every modulus. The obstruction certifies failure to extend that particular labeling.

Here the nonzero parent has order $d=2$. In the [general surplus-site theorem](surplus-site.md), odd $m$ fall in the first row, and even $m>2$ give the threshold $m/2-1$. The row for $m=d=2$ has no allowed residue. This proves the stated specialization.

## All old parent labels at twice an odd prime

At $k=2p$, $p$ an odd prime, the complete list of obstructed pairs of stars on $k-1$ vertices consists of these two families, allowing exchange of the stars.

1. A singleton is attached at the surplus and the other star's parent differs from the surplus by an odd residue.
2. The parents are the surplus and its antipode, and the order of the star at the surplus is at most $p-2$.

The first family is exactly the [pinned-star divisibility obstruction](pinned-star.md) for one singleton, since $\gcd(k-2,k)=2$. The second follows from the divisor table, whose only candidates here are $p,2p$. At $p=3$ the independent literal search checks every input directly. In what follows assume $p\ge5$ and use coordinates with surplus zero.

Equal parents and distinct nonzero parents whose difference is a unit are covered by the [interval constructions](two-star-surplus.md#two-intervals-supply-the-prime-construction). A singleton at one of two distinct nonzero parents is covered there too. If just one parent has nonzero residue $c\ne p$, orient its star first and write $j$ for its order. For even $c$ choose a unit step putting $c$ at position $k-2$; for odd $c$ choose a unit putting it at $k-3$. These are in the respective unit orbits since $p\ge5$. Put all $j-1$ first leaves immediately before that position in step coordinates. The other parent at zero is the start of the empty interval before zero. This works for $j\le k-2$ in the even case and $j\le k-3$ in the odd case. The remaining odd case is family 1.

It remains to consider two distinct nonzero parents $a,b$ and stars of orders at least two. When $a-b$ is even, let $h=a-b$, of order $p$, and take the smaller star first, $s\le p-1$. If both parents are odd, set $y=a,x=a+h$ and use the leaf set
$$
                         \{b\}\ \cup\ \{-h,-2h,\ldots,-(s-2)h\}.
$$
The isolated label $b=a-h$ lies in the odd coset, distinct from the centers since $p\ge3$. The other leaves lie in the even subgroup. Their translate differences telescope exactly as in the two-interval construction.

If both parents are even and $s\le p-2$, first use the prime theorem inside the even subgroup with stars of orders $s,p-1-s$. Give every label of the odd coset to the second star as extra leaves. Its even center translates that whole coset onto itself, so all added weights are new. If $s=p-1$, the orders are $p-1,p$. Choose the unit $h$ with $2h=a-b$. In its coordinates $A=a/h$ is even and at least four, since $A=2$ would give $b=0$. Use the two intervals with $l=2$, $r=s-3$, whenever $A\le k-s+1$. The other parent is at $A-2$. In the opposite orientation with step $-h$, the first parent is at $k+2-A$, so that orientation works whenever $A\ge t+1=k-s$. Both star orders are at least three.

Finally suppose the parents differ by $p$. Exactly one of them is odd, hence a unit since both are nonzero. Put the star at the even parent first, of order $e$. If $e\le p$, choose a unit step putting the odd parent at $-1$. The even parent is now $A=p-1$. Take $l=e-2$, $r=1$. For $e\ge p+1$, put the odd parent at $1$, so $A=p+1$, and use $l=p$, $r=e-1-p$. These choices obey the interval bounds and place the other parent at one of the starts. This exhausts the possible differences modulo $2p$.

The [independent endpoint search and reproduction commands](two-star-surplus.md#verification) check the classifications without using the divisor test to decide any input.
