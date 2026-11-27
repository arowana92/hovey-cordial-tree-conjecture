# An exact obstruction for prime-size leaf lists

Let $p$ be an odd prime and $k=2p$. Give each of $p$ rows its own list $A_i$ of at least $p$ residues, and prescribe shifts $b_i$. We seek distinct inputs $x_i\in A_i$ with distinct outputs $x_i+b_i$ modulo $k$.

**Theorem.** An assignment fails to exist exactly when all three conditions hold.

1. The shifts have a common parity $e\in\{0,1\}$.
2. All lists equal one and the same parity class.
3. $\sum_i (b_i-e)/2\ne0\pmod p$.

For example, $p-1$ zero shifts and one shift of 2 fail on the common even list. Changing one of the lists to include an odd input removes the obstruction.

## Mixed shift parities

Write $v$ for the number of odd shifts. When $0<v<p$, the [two-Vandermonde coefficient](twice-prime-power-lists.md#reduction-of-the-coefficient), reduced modulo $p$ and up to sign, is
$$
v!(p-v)!\binom{(p-1)/2}{\lfloor v/2\rfloor}.
$$
Every factor is nonzero in $\mathbb F_p$. The complex coefficient is therefore nonzero, and interpolation gives the assignment on the original independent lists.

## Shifts in one coset

More generally, take a finite abelian group $G$, a subgroup $H$ of prime order $p$, and $p$ shifts lying in $b_0+H$. On independent lists of size at least $p$, the sole obstruction is that every list equals the same $H$-coset and $\sum_i(b_i-b_0)\ne0$ in $H$. The proof applies also to $p=2$.

First consider $r<p$ rows and lists of size at least $r$. If we assign each row to an input coset, different input cosets give disjoint output cosets since all shifts induce the same translation on $G/H$. Within a single pair of cosets choose coordinates in $H\simeq\mathbb F_p$. The [prime list theorem](leaf-lists.md#prime-and-composite-moduli) solves any $h<p$ rows in that input coset when each has at least $h$ entries there.

To allocate the rows, pick a coset containing some listed entry. Sort the rows by decreasing number $t_i$ of entries there. Set $h=\max\{j:t_j\ge j\}$. Allocate the first $h$ rows to this coset. Each has at least $h$ choices there, and every other row has at most $h$ entries there. On deleting this coset, the remaining $r-h$ rows have at least $r-h$ choices apiece. Induction on the number of rows finishes the allocation.

For $r=p$, if the union meets multiple cosets, shrink the lists to size $p$ retaining two entries from different cosets in the union. Pick a coset containing one of these entries. Now $1\le h<p$, since at least one row is not contained in the chosen coset. Both resulting groups have fewer than $p$ rows, so the preceding argument applies.

Finally, if all entries lie in a single input coset, every list is that entire coset. Translate the inputs into $H$ and the outputs back by the input origin plus $b_0$. Both sets must exhaust $H$, so their sums agree. Conversely, Hall's prescribed-differences theorem for finite abelian groups realizes any zero-sum sequence of $|H|$ elements as the differences between two enumerations of $H$. Pair these differences with their respective rows. Taking $G=\mathbb Z_{2p}$ and $H$ the even residues gives conditions 2 and 3 above when the shifts have common parity. [M. Hall, *A combinatorial problem on abelian groups* (1952)](https://doi.org/10.1090/S0002-9939-1952-0050579-7)

## Larger batches and the 26-label frontier

For $k=2p^a$, the same projected coefficients also apply to some batches of $r\ge p$ rows. When $r$ is odd or $v$ is even, the size-$r$ independent lists suffice if both parity multiplicities are less than $p$. Indeed, $r\le2p-2$ and both factorials and the half-sized binomial coefficient are nonzero modulo $p$. For even $r$ and odd $v$, the modified coefficient permits both multiplicities to be at most $p$. Its two factorials have arguments $v-1,r-v-1$, and its binomial has upper index $r/2-1<p$. Here one marked list must have at least $r+1$ entries, with $r-1$ sufficient in one row of opposite shift parity. [Coefficient derivation](twice-prime-power-lists.md#reduction-of-the-coefficient)

At 26 labels, suppose a least counterexample has order $26m+21$ and at least 15 leaves. Delete any 15 original leaves. Every cordial labeling of the remaining core must give at most two leaf-parent shifts in the less frequent parity, counted over these 15 attachments. Indeed the core has six high vertex bins and five high edge bins, leaving at least $26-6-5=15$ choices per leaf. With both parities occurring at least three times each, neither multiplicity exceeds 12. The odd batch with $p=13$ would restore the tree. This restricts core labelings at the first residue left by the [short-forest certificates](../rainbow/short-forests.md).

## Reproduction

The checker uses direct backtracking on inputs and outputs for all 288,000 shift-normalized size-three list instances at modulus six. It also checks random and deliberately obstructed examples at larger moduli, and tests the lifted coefficients by exact cyclotomic traces.

~~~sh
python3 -B -m research.biased.check_parity_boundary
~~~
