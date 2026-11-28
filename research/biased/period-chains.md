# Repeated cut residues on a path in a smallest counterexample

**Theorem.** Fix $k\ge2$, and let $T$ be a smallest ordinary non-$k$-cordial tree, if one exists. Orient any path from its first vertex to its last. At each edge of the path record, modulo $k$, the order of the component containing the first vertex after cutting that edge. Each residue occurs at most $2^{\Omega(k)}$ times, where $\Omega(k)$ counts the prime factors with multiplicity. This also holds for a least failure within trees with a specified upper bound on their number of leaves.

At a prime $p\ge7$, write $s=|T|\bmod p$ and $F=\{-1,0,1,s-1,s,s+1\}\subseteq\mathbb Z_p$. Then
$$
      \operatorname{diam}(T)\le 2(p-|F|)+2,\qquad |T|\le p(p-4).
$$
For instance, a smallest counterexample at 29 labels has at most **725 vertices**, and at 31 labels at most **837**. The result bounds the order to be tested and does not settle either modulus.

## Compressing consecutive pieces

Suppose $t+1$ edges occur along the path with the same recorded residue. Cut them all. Between successive cuts lie $t$ disjoint connected trees $P_i$, each of positive order $q_i k$ and with two incident cut edges. Branches extending off the path stay in their respective components. Each $P_i$ is smaller and therefore has a cordial labeling. Denote its port labels by $a_i,b_i$ and its deficient edge weight by $h_i$. The two ports may coincide. Write $c_i=a_i+b_i-h_i$.

If $\sum_{i=l}^r u_i c_i=0$ for units $u_i\bmod k$, replace these consecutive pieces by a single ordinary edge. The smaller tree has a cordial labeling. Restore the pieces in order. Starting at the old label $x$, multiply the labels of the next piece by $u_i$ and translate by $x+u_i(a_i-h_i)$. Its first joining edge fills its translated deficit. Its vertices and its internal edges together with the joining edge each contribute $q_i$ copies of every residue to their respective histograms. Its outgoing label is $x+u_i c_i$. After the last piece the outgoing label is the original $x$, so the final joining edge has the weight of the replaced edge. The reconstructed tree is cordial. Replacing a two-port piece by an edge preserves the degrees of all outside vertices. Both the smaller tree and each isolated piece have at most the original number of leaves. [Single-piece expansion](sparse-path-offsets.md#compressing-a-tree-between-two-ports)

The required interval always exists for $t\ge2^{\Omega(k)}$. This is the consecutive unit-weighted zero-sum theorem of Mondal, Paul and Paul. For a direct construction, give each coefficient one parity bit for each exact valuation $j<a$ at each prime power $p^a\parallel k$. A term of valuation at least $a$ contributes zero there. Among $2^{\Omega(k)}+1$ prefix parity vectors two coincide. On the intervening interval, pair terms of equal valuation separately at each prime power. Two such terms are unit multiples of one another, so their locally scaled sum can be made zero. The Chinese remainder theorem combines the local unit choices for each term. This proves the path assertion. The arithmetic threshold is sharp for fixed coefficients. Indeed, set $S_1$ empty and $S_k=(pS_{k/p},1,pS_{k/p})$ for any $p\mid k$. An interval containing the central 1 cannot cancel modulo $p$. An interval in either half would cancel after division by $p$ in the shorter sequence. Actual given piece labelings can realize any such word. Take a $k$-vertex star labeled by all residues with center zero, entry at the center and exit labeled $c_i$. [Mondal, Paul and Paul, Theorem 3.8](https://arxiv.org/pdf/2203.02665)

## Bounds at primes

Take a diameter path. Its first and last edges are pendant. At every other edge both sides have at least two vertices, and the prime cut theorem excludes all residues in $F$. Each remaining residue occurs at most twice by the path theorem. This proves the diameter bound, including when entries of $F$ coincide. [Prime cut theorem](../prime/deficit-cut.md)

Write $n=mp+s$ now with $1\le s\le p$ and let $L$ be the number of leaves. The divisible-cut and leaf-deletion bounds give $n\le p(L-1)$ and $L\le s-2$. If $s<p$, these already give $n\le p(p-4)$. If $s=p$, the diameter is at most $2p-4$. A center is therefore at distance at most $p-2$ from every vertex. Its paths to the $L$ leaves cover the tree, so $n\le 1+L(p-2)\le1+(p-2)^2$. Rounding down to a multiple of $p$ gives $p(p-4)$ for $p\ge7$. [Divisible-cut and leaf bounds](../divisible-cuts.md)

For pieces on different edges, a separate [packing inequality](period-edges.md) gives $3m<2\lceil(n-1)/p\rceil$ for $m$ disjoint two-port pieces in a smallest prime counterexample of order $n$.

## Testing a given interval

Scale each fixed piece independently by a unit. To test whether their total effective offset can be a prescribed $z$, work at every $p^a\parallel k$. Truncate valuations at $a$, let $j$ be the least valuation among the $c_i$, and let $m$ be its multiplicity. Require $p^j\mid z$. If $j=a$, there is no further condition at this prime. The remaining conditions depend on the prime.

* At $p=2$, $z/2^j$ must have the parity of $m$.
* At odd $p$ with $m=1$, require $p\nmid z/p^j$.
* At odd $p$ with $m\ge2$, every multiple of $p^j$ is attainable.

To see sufficiency, divide by $p^j$. Each of the $m$ least terms can be made any unit modulo $p^{a-j}$. At odd $p$, the sum of two nonzero field elements can take every value. At $p=2$, every unit reduces to one. First meet the required residue modulo $p$, then adjust a single unit by a multiple of $p$ to attain the exact residue modulo $p^{a-j}$. The remaining higher-valuation terms may be kept fixed. Lift each chosen multiplier locally to a unit and combine the choices by the Chinese remainder theorem.

The [checker](check_period_chains.py) compared the criterion with direct sumsets for 10,809 multisets at moduli through 64. It also checked 136,076 complete coefficient words at their threshold and all intervals of the displayed extremal words through modulus 64. It independently constructed 1,175 complete trees by expanding selected intervals with 3,886 pieces of one, two or three periods, including 120 coincident-port pieces. All original vertex and edge bins increased by the required amounts.

~~~sh
python3 -B -m research.biased.check_period_chains
~~~
