# Separate leaf lists when the shifts lie in a prime-order coset

Let $H$ be a subgroup of prime order $p$ of a finite abelian group $G$. Prescribe $r\ge1$ shifts $s_i$ in a single coset of $H$, with repetitions allowed. Give row $i$ a list $A_i\subseteq G$ of at least $r$ elements. If **at most $p-1$ lists have exactly $r$ elements**, there are distinct $x_i\in A_i$ with all $x_i+s_i$ distinct. In particular, one extra entry in each list suffices for any number of rows or shift values in that coset.

The allowance of $p-1$ shorter lists is sharp as a uniform bound. At $r=p$ give all rows the same list $H$. Use zero shifts except for one nonzero shift in $H$. Both the sources and the destinations would exhaust $H$, although their sums differ. Adding an outside option to even one of these lists makes the theorem applicable when $G$ contains such an option. [Earlier prime-size classification](prime-size-lists.md)

## Allocating the rows

Subtract a common shift to put all shifts in $H$. Distinct input cosets then give disjoint output cosets. Use induction on the number of remaining rows, writing $r$ for this number and calling a list *tight* when it has exactly $r$ elements. Choose a coset $C$ meeting some list. A row is *full* in $C$ if its list contains $C$.

For $h<p$ rows, each having at least $h$ choices in $C$, the prime list lemma supplies a placement. In coordinates on $H$ the top coefficient of the two Vandermondes is $\pm h!$, which is nonzero modulo $p$ and works for separate lists. For $p$ full rows, Hall's prescribed-differences theorem supplies a placement whenever their shifts sum to zero. [Separate-list proof](leaf-lists.md) · [Alon's grid argument](https://web.math.princeton.edu/~nalon/PDFS/alt2.pdf) · [Hall's theorem](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

* If fewer than $p$ rows are full, order the rows by decreasing number of options in $C$. Take the largest $h$ for which the first $h$ rows each have at least $h$ options there. Then $1\le h<p$. Place these rows in $C$ and exclude $C$ from every other list. Each remaining row loses at most $h$ entries, so only a previously tight row can be tight at the next stage.
* Otherwise, form a pool consisting of all full rows and all tight rows with exactly $p-1$ choices in $C$. If the pool has at least $2p-1$ members, Erdős–Ginzburg–Ziv supplies $p$ with shift sum zero. First find a full-coset placement by Hall. Each selected nonfull row misses just one source in $C$. At most $p-1$ selected rows are nonfull, so among the $p$ translations inside $H$ some translation avoids all their missing sources. Place these $p$ rows and exclude $C$. No remaining row loses more than $p$ entries, so the induction hypotheses persist. [Erdős, Ginzburg and Ziv (1961)](https://www.renyi.hu/~p_erdos/1961-25.pdf)
* If the pool has at most $2p-2$ members, place $p-1$ of them in $C$, including **every tight full row**. The pool has at least $p$ members and every selected row has at least $p-1$ options there. The prime list lemma applies. On excluding $C$, an unselected full row originally had at least $r+1$ entries, so it retains at least $r-(p-1)$. An unselected nonfull row loses at most $p-1$. The only rows that can now be tight are unselected full rows and unselected previously tight rows that lost exactly $p-1$ entries. All were in the pool, which has at most $(2p-2)-(p-1)=p-1$ members left.

Each step places at least one row and preserves both list-size conditions. The induction gives the promised assignment.

## Restoring leaves

In a cordial core of order $mk+h$ with $1\le h<k$, let $U$ be the $h$ high vertex residues and $W$ the $h-1$ high edge residues. For a leaf of effective shift $s_i$ its list is the complement of $U\cup(W-s_i)$. Thus $r$ leaves extend whenever their shifts lie in a prime-order coset and $2h+r\le k$. At $2h+r=k+1$ the same holds if at most $p-1$ leaves have $U\cap(W-s_i)=\varnothing$. Distinct sources and destinations outside the high bins increment only the low bins. [Frequency calculation](spare-lists.md)

For example, at 27 labels any cordial 29-vertex core admits 23 new leaves if the old parent colors are all congruent modulo nine. All three residues of the coset may occur with arbitrary multiplicities. This gives a family at order 52 with independently specified parents. The condition is on the given core labeling.

The cyclic-group constructor handles partial cosets, zero-sum blocks and translation around missing entries. An independent checker recounted 402,744 separate-list families at moduli four and six up to row reordering and common shift translation. It tested the sharp examples at primes two, three, five and seven and verified 17 repairs obtained by enlarging a single list. On 594 whole trees it counted actual vertex and edge frequencies, including 28 order-52 joins using all three shifts. Across the list and tree checks, 514 full placements included a row missing one option in the chosen coset. [Constructor](prime_coset_lists.py) · [Checker](check_prime_coset_lists.py)

~~~sh
python3 -B -m research.biased.check_prime_coset_lists
~~~
