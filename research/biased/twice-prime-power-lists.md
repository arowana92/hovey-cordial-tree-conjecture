# Leaf lists at twice an odd prime power

**Theorem.** Let $k=2p^a$ with $p$ an odd prime and $a\ge1$. Give $r<p$ leaves arbitrary shifts $b_i$ modulo $k$ and a separate list of allowed vertex residues for each leaf. If $r$ is odd, lists of size $r$ suffice to choose distinct labels $x_i$ whose shifted values $x_i+b_i$ are also distinct. For even $r$, size $r$ still suffices when an even number of shifts are odd. In the remaining parity case, one extra entry in any one list suffices. A row of opposite shift parity may then have only $r-1$ entries.

**Consequence.** A smallest ordinary counterexample at 26 labels would have to have order $26m+s$ with $17\le s\le26$. At $s=17$ it would have five or six leaves. More generally, for every $k=2p^a$ with $p\ge7$, its order residue is at least $k/2+4$. These results concern arbitrary tree order.

## Reduction of the coefficient

Represent residues by the complex $k$th roots of unity. If $\alpha_i$ represents $b_i$, the shifted value of $X_i$ is $\alpha_iX_i$. The coefficient of $\prod X_i^{r-1}$ in the product of the two Vandermondes, one on the inputs and one on these outputs, is up to sign
$$
P(\alpha)=\sum_{\pi}\prod_i\alpha_i^{\pi(i)}
$$
where the exponent assignments permute $0,\ldots,r-1$. A nonzero value proves the list conclusion by finite-grid interpolation over $\mathbb C$. This is the permanent method of Dasgupta, Károlyi, Serra and Szegedy. Feng, Sun and Xiang give related results for common lists and repeated shifts at groups whose least prime divisor exceeds the row count. [Transversals of additive Latin squares](https://services.math.duke.edu/~dasgupta/papers/finallatin.pdf) · [Feng, Sun and Xiang](https://bpb-us-w2.wpmucdn.com/sites.udel.edu/dist/a/6387/files/2017/08/FSXPublVersion-2lyt73t.pdf) · [Grid coefficient argument](leaf-lists.md)

Take a primitive $p^a$th root $\xi$ and use $-\xi$ as the primitive $k$th root. There is a ring map $\mathbb Z[\xi]\to\mathbb F_p$ taking $\xi$ to 1, since $\Phi_{p^a}(1)=p$. It sends $\alpha_i$ to $(-1)^{b_i}$. Let $v$ be the number of odd shifts. Under this map the permanent becomes
$$
(r-v)!v!\,[z^v](1+z)^{\lceil r/2\rceil}(1-z)^{\lfloor r/2\rfloor}.
$$
Indeed choose the exponent positions assigned to the odd rows, then order each of the two row sets. If $r=2h+1$, the polynomial is $(1+z)(1-z^2)^h$, whose coefficient at $v$ is $(-1)^{\lfloor v/2\rfloor}\binom h{\lfloor v/2\rfloor}$. For $r=2h$ it is $(1-z^2)^h$, with the same formula for even $v$. All the indicated factorials and binomial coefficients are nonzero modulo $p$ when $r<p$. This proves nonvanishing in characteristic zero even if every original shift is different.

For even $r=2h$ and odd $v$, give row $i$ a list of size at least $r+1$ and choose any opposite-parity row $j$. Both parities occur. Use the same product of Vandermondes, changing the target powers at $i,j$ from $r-1$ to $r,r-2$, respectively. If the second determinant assigns exponents $e_1,\ldots,e_r$, the complementary exponents in the first determinant must now swap the entries at $i,j$. This is possible exactly when $e_i=e_j+1$. Every surviving term has the same permutation-sign factor, the negative of the original common sign.

Set $e_j=m$ for $0\le m\le r-2$. The remaining exponents include $h-1$ even and $h-1$ odd positions. The number of remaining odd rows is $v-1$, which is even. Up to a sign independent of $m$, the contribution of the two marked rows is $(-1)^m$. The sum of these signs is 1. Thus the coefficient after specialization, up to an overall sign, is
$$
(v-1)!(r-v-1)!\binom{h-1}{(v-1)/2}.
$$
It is nonzero modulo $p$. Interpolation requires only $r-1$ entries at $j$ and $r$ on the other unmarked rows. For size $r$ alone, at each odd $v$ there are bad instances. Use $v$ shifts equal to $p^a$ and all others zero, on a common list consisting of $r/2$ pairs $\{x,x+p^a\}$. Within a pair the two assigned shifts must agree to avoid an output collision, so the number of shifted entries must be even.

## Order and leaf count

Write a minimum counterexample order as $mk+s$, $1\le s\le k$, and let $L$ count its leaves. The [leaf-deletion lemma](../counterexample-bound.md#removing-leaves) gives $L<s-1$. Take the largest odd $r$ with $r\le L$ and $r<p$. After deleting $r$ leaves the core has $u=s-r\ge2$ high vertex bins and $u-1$ high edge bins. The lists on the deleted leaves have at least $k-2u+1=2r-(2s-k)+1$ entries each. Thus $2s-k\le r+1$ would restore the tree. Since $2s-k$ is even and $r$ odd, the conclusion is
$$
2s-k\ge r+3.
$$
This bound in terms of $L$ also applies to minimum counterexamples with prescribed offsets, since the effective shifts already include them. For ordinary trees the [four-leaf theorem](../census/four-leaves.md) gives $L\ge5$, so $p\ge7$ implies $r\ge5$. At $k=26$ and $s=17$, seven leaves would permit $r=7$ and force $2s-k\ge10$, contradicting $2s-k=8$.

## Adding other large prime factors

The same list theorem holds at $k=2p^a M$ if every prime dividing $M$ exceeds $r!$ and is different from $2,p$. To see this, consider any sum of at most $r!$ roots of unity of order dividing $k$. For a prime power $q^b$ exactly dividing $M$, expand in a primitive $q^b$th root over the cyclotomic field of the coprime remaining order. The minimal polynomial is $\Phi_{q^b}$ by the cyclotomic degree formula. If the sum vanishes, the coefficients at the $q$ exponents in each class modulo $q^{b-1}$ all agree, by divisibility by $\Phi_{q^b}=1+X^{q^{b-1}}+\cdots+X^{(q-1)q^{b-1}}$ in degrees below $q^b$. At least one exponent in each class is empty because $q>r!$, so all coefficients vanish. Setting the $q$-part to one preserves vanishing. Iterate over $M$.

For lists of size $r$, the permanent has exactly $r!$ summands and its specialization to the $2p^a$ part was proved nonzero above. The mixed-exponent coefficient has at most $r!$ terms as well, and the same specialization argument applies. In the sharpness example replace $p^a$ by $k/2$. In particular the ordinary bound $s\ge k/2+4$ also holds for these extended moduli when $p\ge7$ and all prime factors of $M$ exceed $5!=120$, by taking $r=5$.

## Reproduction

~~~sh
python3 -B -m research.biased.check_twice_prime_power
~~~

The checker expands projected permanents directly by exponent permutations, then tests original complex permanents exactly by summing their squared magnitudes over all primitive roots using Ramanujan sums. It also searches for assignments on separate lists, tests the parity obstructions, and recounts both histograms on trees at the excluded residue. [Independent checks](check_twice_prime_power.py)
