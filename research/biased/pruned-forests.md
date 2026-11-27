# Choosing which ten vertices to restore

**Theorem.** At every odd prime $p\ge5$, a smallest noncordial tree of order $mp+s$, with $1\le s\le p$, must satisfy
$$
s\ge (p+13)/2.
$$
The same bound holds when the edges have independently prescribed additive offsets. At 29 the first remaining order residue is 21. A forest whose list coefficient vanishes can sometimes be replaced by a different forest in the same tree. Both choices leave a connected core.

## A connected core with prescribed component sizes

Let a tree have at least $q+2$ vertices, where $q\ge2$, and fix $1\le d\le q-1$. There is a connected induced subtree whose complement has $q$ vertices and either at least three components or exactly two components of sizes $d,q-d$.

Remove leaves one at a time, giving priority to the original leaves, until $q$ vertices are outside. If there were at least $q$ original leaves, the complement consists of $q$ singletons and satisfies the conclusion. Otherwise every original leaf lies outside. The core has at least two vertices, and each of its terminal vertices has an outside neighbor, since it was not an original leaf. Each outside component attaches to the core by exactly one edge. Thus at least two components exist.

If there are exactly two, the core is a path with one component attached at each end. To transfer one vertex of size from one component to the other, return the root of the shrinking component to the core and remove the core endpoint next to the growing component. Choose the shrinking component to have at least two vertices. The new core is connected. If the restored root had two or more children, the new complement has at least three components. If it had one, the retained core is again a path and the component sizes changed by one in the chosen direction. Repeat toward the prescribed pair. The difference from the target strictly decreases at each such exchange. [Constructive cut algorithm](pruned_forests.py)

## Ten-row coefficients and two root restorations

The [nine-row theorem](nine-row-lists.md) excludes order residues up to $(p+9)/2$. The arbitrary-offset case is already settled through 13. First take $p\ge29$ and $s=(p+11)/2$.

We seek a set of ten exterior vertices whose rooted forest certifies extension from the smaller cordial core. Its retained order is $mp+(p-9)/2$. There are $e=(p-11)/2$ high edge bins to avoid and $(p+9)/2=10+e$ available input residues. The uniform top coefficient with $r=10$ in the list polynomial therefore suffices. All prescribed boundary labels and edge offsets enter only lower-degree terms.

For each of the 1,842 rooted forests $H$ of order ten compute the rational uniform coefficient at $e=-11/2$. Denote its reduced numerator by $N(H)$. None is zero. The exponent transferred to a parent in the two-permutation formula is at most $\lfloor10^2/4\rfloor=25$. Every binomial denominator is therefore a unit at $p\ge29$, so the field coefficient vanishes exactly when $p$ divides $N(H)$.

Use the preceding cut with $q=12,d=5$. There are enough vertices since $s\ge20$. Return two component roots to the core one at a time, with the children of each returned root becoming component roots. For the initial forest $F$ take the gcd of all $N(H)$ obtainable this way. If $p$ does not divide this gcd, one choice of two restorations leaves a ten-vertex forest with nonzero coefficient. By minimality its enlarged core has a cordial labeling and the list lemma extends it to the whole tree. Different choices may use different core labelings.

The following integer computation covers all possible choices of $p$. Start with $|N(H)|$ at size ten and remove all factors of primes at most 23. For each eleven-vertex forest take the gcd of the entries obtained by returning one root. Repeat at size twelve. The counts include every unordered multiset of rooted components.

| Outside vertices | All rooted forests | Forests with at least two components and gcd greater than one |
| ---: | ---: | ---: |
| 11 | 4,766 | 26 |
| 12 | 12,486 | 16 |

At size twelve, fifteen surviving shapes have component sizes $1,11$ and one has component sizes $6,6$. The cut gives either at least three components or sizes $5,7$. Its gcd is therefore one. This excludes $s=(p+11)/2$ and proves the stated necessary condition. This argument chooses the core before applying induction and makes no assumption about the labeling obtained on it.

At $p=17,19,23$ a transfer factorial may be divisible by $p$. Evaluate the ten-row coefficients modulo $p$ at the actual nonnegative size $(p-11)/2$. Mark a forest as covered when its coefficient is nonzero, then mark a larger forest as covered when any root restoration reaches a covered forest. At twelve vertices the numbers of uncovered forests with two or more components are respectively 3, 3 and 1. All have component sizes $1,11$. The same cut at $5,7$ therefore proves the offset result at these primes as well. Even at 17 the critical residue is 14, so a core of at least two vertices survives the initial twelve removals.

## Reproduction

~~~sh
python3 -B -m research.biased.check_pruned_forests
~~~

The optional `--field` argument selects one of `rational`, `17`, `19` and `23` for a separate replay. Two exact expansions independently evaluate all ten-row coefficients. Forest enumeration by sorted component multisets is checked against leaf insertion at every vertex of a dummy-rooted tree. The gcd step consists only of restoring one root and deduplicating isomorphic choices. The checker also tests 53,201 connected cuts on actual trees, checking the sizes and connectivity of both sides. [Verification code](check_pruned_forests.py) · [Derivation of the signed coefficient](nine-row-lists.md#evaluating-a-forest-exactly)
