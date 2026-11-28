# Two parent labels for the same pendant path

Let a labeled core have order one modulo $k$, and translate its surplus vertex label to zero. Attach a path of $k-1$ new vertices at its first vertex. A witness row is a permutation of the nonzero residues in path order. Which two distinct parent labels $b,c$ can use the **same** row?

**Theorem.** Write $S=\sum_{a\in\mathbb Z_k}a$. At all sufficiently large $k$, and separately at each $9\le k\le27$, a row starting at prescribed $x\ne0$ works for $b$ and $c$ exactly when
$$
                       z=x+S+b+c\ \notin\ \{0,x\}.
$$
The last path vertex must receive $z$. With the first label free, the sole condition is $S+b+c\ne0$. The free-first-label criterion also holds at every $3\le k\le8$. At eight, with the first label prescribed, the extra failures beyond the displayed test are exactly the unit multiples of $(x,b,c)=(2,1,7)$ with the pair unordered.

For other bounded-degree rooted trees at large moduli, every parent pair works when the first label is free. Prescribing it gives a sharp gcd criterion. [General tree proof and sharp star examples](tree-parent-pairs.md)

## Counting incidences and completing the path

The $k-2$ internal weights of a successful row are distinct. They omit exactly $x+b$ and $x+c$. Their sum is $S-2x-b-c$. Counting the same weights at their incident vertices gives $2S-x-z$. Equality forces the stated endpoint. Distinct nonzero path labels require $z\notin\{0,x\}$. If $x$ is free and $S+b+c\ne0$, choose $x$ outside $\{0,-S-b-c\}$.

For the converse at large $k$, use the path on $k-1$ vertices with vertex palette $G\setminus\{0\}$ and edge palette $G\setminus\{x+b,x+c\}$. Select both tips and six pairwise nonadjacent internal vertices away from the tips. Give the tips labels $x,z$. Choose the six other labels to make the sum of the eight marks equal to $S$. Choose four freely, then choose the last two with their prescribed sum. Avoiding the used labels and zero excludes only a bounded number of choices, and equality of the last two excludes at most two more. The marked subgraph has no edges. The marked degree-weighted sum is $2S-x-z$, exactly the sum of the edge palette. The marked vertices exhaust the degree-one class, and the degree-two class has at least six representatives both inside and outside. Lemma 4.9 of Müyesser and Pokrovskiy therefore extends the marks to a rainbow embedding with precisely these palettes. Restoring either parent supplies one of the two omitted weights. [Primary embedding lemma](https://arxiv.org/html/2509.05280v2#S4)

## The minimum number of preselected rows

With both endpoints $x,z$ fixed and distinct nonzero, let $h=z-x-S$. A parent $b$ is possible exactly when $2b\ne h$ in the regime of the fixed-first-label theorem. Its row also handles $h-b$. Each row handles exactly one pair, so the minimum number covering **all possible parents** is $(k-|\{b:2b=h\}|)/2$.

With only the first label fixed, it takes exactly $\lceil k/2\rceil$ rows to handle all parents in that regime. In the graph of possible parent pairs, at most two other vertices are forbidden to any vertex, since the two forbidden pair sums are $-S$ and $-S-x$. The minimum degree is at least $k-3$. A maximum matching leaves at most one unmatched vertex for $k\ge6$. Indeed, two unmatched vertices have no unmatched neighbors, and each matched edge can contribute at most two to their combined degree without yielding an augmenting path. Their combined degree is at most $k-2$, contradicting $2(k-3)>k-2$. A further edge covers a lone unmatched vertex. Each row handles at most two parents, proving optimality.

With neither endpoint prescribed, allow a stored row to be multiplied by any unit. Exactly $\lceil\tau(k)/2\rceil$ rows suffice, where $\tau(k)$ counts positive divisors. This holds at all sufficiently large $k$ and at every $3\le k\le27$, including the small moduli with extra fixed-endpoint exceptions. The units act transitively on the residues having any fixed gcd with $k$, and each row meets at most two such orbits. Two different orbits contain an allowed pair unless both are singletons with forbidden sum. The only possible missing edge is between the classes of zero and $k/2$ at even $k$. The resulting graph admits a matching leaving at most one class uncovered, which can be covered with one further edge. Indeed, any matching of the classes into pairs can avoid the one forbidden pair by re-pairing its endpoints with another pair, or with the unmatched class. For large primes a single stored path permutation therefore handles every parent after unit multiplication.

## Independent finite checks

The generator fixes the first and last labels, excludes the two missing weights and searches the remaining path positions. It writes one literal row per feasible input up to unit multiplication. The Python verifier recomputes every weight for each of the two actual parents, expands the unit orbits and compares coverage against the incidence condition. At orders three through eight it also checks **every permutation** directly to certify the exceptional triples. Across those six moduli there are 42 additional fixed-first-label failures. None removes a parent pair when the first label is free. [Generator](path_parent_pairs.cpp) · [Independent verifier](check_path_parent_pairs.py) · [Digests](path-parent-pairs.sha256)

~~~sh
set -e
src="$PWD/research/bounded-degree"
out=$(mktemp -d)
c++ -O3 -std=c++17 "$src/path_parent_pairs.cpp" -o "$out/generate"
for k in $(seq 3 27); do "$out/generate" "$k" > "$out/$k.txt"; done
(cd "$out" && shasum -a 256 -c "$src/path-parent-pairs.sha256")
python3 -B "$src/check_path_parent_pairs.py" "$out" 27
~~~
