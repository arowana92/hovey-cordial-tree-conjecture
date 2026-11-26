# The exact prime-modulus spectrum for two attachment vertices

Fix a tree $H$ of order $h\ge2$ and two distinct vertices $a,b$. At $k\ge h$, adjoin $k-h-t$ leaves to $a$ and $t$ leaves to $b$, for $0\le t\le k-h$. The set of pairs $(k,t)$ admitting a cordial labeling in which the two hub labels differ by a unit is effectively definable in Presburger arithmetic. At prime $k$, this is the exact set admitting an ordinary cordial labeling. It gives an effective ultimately periodic set of candidate moduli whose intersection with the primes is exactly the set of primes at which some distribution fails.

For any modulus the unit assumption permits simultaneous translation and multiplication by a unit to set $a=0,b=1$. At order $k$, all vertices receive distinct labels, so the assumption is automatic over a prime field.

## One blocked weight in each gap

List the core labels as $0=x_0<x_1=1<\cdots<x_{h-1}<k$, and put $x_h=k$. Represent edge residues in $[1,k]$, representing zero by $k$. Mark the $h-1$ core edge weights and the one weight to be missing as blocked targets.

**Gap criterion.** A fixed core assignment extends exactly when each interval $(x_i,x_{i+1}]$ contains one blocked target $z_i$, with
$$
t=\sum_{i=0}^{h-1}(x_{i+1}-z_i).
$$
In particular the core weights must be distinct. Every free vertex slot in a gap can reach only that gap's edge positions, by a shift of zero or one. There is one fewer vertex slot than edge position there. The blocked target separates leaves labeled $x_i+1,\ldots,z_i-1$ at $a$ from those labeled $z_i,\ldots,x_{i+1}-1$ at $b$. This gives both necessity and sufficiency: as the assigned labels increase, distinct weights obtained by shifts zero or one must also strictly increase. The last gap includes the possible wrap from $k-1$ to weight zero.

## Projecting the inequalities

Enumerate the orders of the $h-2$ unpinned core vertices and the assignments of the core edges and missing weight to the $h$ gaps. For an edge $uv$, its slot $y$ satisfies either $y=x_u+x_v$ or $y+k=x_u+x_v$, with $1\le y\le k$ and the appropriate gap inequalities. The missing weight is forced as an ordinary integer by
$$
w=k+\sum_{v\in H}x_v-\sum_{e\in H}y_e-t .
$$
Require it to lie in its assigned gap as well. Each case uses linear integer inequalities, finite disjunctions, and existential quantifiers over core labels and edge slots. Projecting onto $(k,t)$ gives the asserted effective description. Taking the complement in $k\ge h$, $0\le t\le k-h$, then projecting onto $k$, gives an effectively semilinear subset of the nonnegative integers, hence an ultimately periodic set. [Ginsburg and Spanier, *Semigroups, Presburger Formulas, and Languages*](https://www.csa.iisc.ac.in/~deepakd/atc-common/ginsburg-spanier-PJM-1966.pdf)

For each arithmetic progression in its periodic tail, a residue coprime to the period gives infinitely many primes by Dirichlet's theorem. All possible primes in the other progressions divide the period and can be checked individually. At $k<h$, checking leaf counts below $k$ at each hub suffices because a batch of $k$ leaves at either hub can take all residues. At $k\ge h$, the order-$k$ tests decide the ordinary all-orders family at prime $k$. A smaller tree can be extended to order $k$ and its labeling restricted. In a larger tree retain $H$ and enough leaves to reach order $k$. Add one further leaf to supply the missing weight, then apply the [Hall leaf extension](../counterexample-bound.md#removing-leaves) to the remaining leaves at the two already labeled hubs. In contrast, the [two-hub interval theorem](two-hubs.md) gives a finite all-moduli decision for the same fixed family without a unit condition.

## An infinite obstruction to prescribing the difference

Take the path $b,a,u,v$ and put all $k-4$ additional leaves at $b$. A unit difference between $a,b$ is impossible for every even $k\ge4$. With $a=0,b=1,u=x,v=y$, the leaves at $b$ occupy every edge weight outside $\{1,2,x+1,y+1\}$ modulo $k$. The three core weights $1,x,x+y$ must be distinct members of this set. Thus $x=2$ or $x=y+1$. At $x=2$, the third weight can only be $3$ or $y+1$, requiring $y=1$ or $2=1$. At $x=y+1$, it can only be 2 or $x+1$, the latter again requiring $y=1$. The remaining equation $2y=1$ fails at even $k$. For odd $k\ge5$, $y=(k+1)/2$, $x=y+1$ give a witness. The underlying trees are caterpillars and have ordinary cordial labelings at every modulus.

The program computes the excluded set in the parameter plane using the Integer Set Library. On this four-vertex core it gives exactly $t=k-4$ with even $k\ge4$, also checking every other split. The separate finite check runs through full vertex permutations at each split. [Integer Set Library manual](https://libisl.sourceforge.io/user.html)

~~~sh
# Optional dependency for symbolic projection, tested with Python 3.11.
python3 -m pip install 'islpy==2026.2.2'
python3 -B -m research.hub.two_hub_spectrum --hubs 0 3 -- -1 0 1 0
python3 -B -m research.hub.two_hub_spectrum --check
~~~
