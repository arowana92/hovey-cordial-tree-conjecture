# Extending a prescribed labeling across a two-level tree at its hub

Let a hub have $m\ge3$ branching neighbors. One has $e\ge1$ leaf children, and each other neighbor has $q\ge1$ leaf children. Any number $p$ of leaves can meet the hub directly. Write $n=m+e+(m-1)q+p$ for the number of vertices other than the hub.

**Theorem.** At every modulus $k$, a prescribed cordial labeling of a core of order divisible by $k$ extends across this tree at its hub. The size of the attachment and the joint label are arbitrary. If $k\mid n$, the attachment even extends any labeled core with exactly $n/k$ occurrences of each new vertex label and each new edge weight.

In fact, over the integers, one can label the hub zero and make the free labels and edge sums both fill the **same interval of length $n$**. A child of the center labeled zero is available to change one weight at a short attachment. The integer result also holds for an odd number of branching neighbors when all but one can be paired with equal populations within each pair. The populations can differ between pairs. Below, a center means a neighbor of the hub.

The result applies to prescribed core labels at composite as well as prime moduli. Ordinary cordiality for the separate diameter-four tree follows from the earlier integer theorem. [Diameter-four theorem](../hub/all-radius-two.md) · [Prime extensions](prime-joints.md)

## Odd numbers of centers

Assign the unpaired center zero. Sort the pairs by decreasing population and give pair $i$ the labels $i,-i$, for $1\le i\le a$. The centers fill $[-a,a]$ and each center's incoming edge weighs its own label. In any child layer the participating pairs are $1,\ldots,b$. There is a permutation of a length-$2b$ interval with displacements exactly $\pm1,\ldots,\pm b$. Indeed, alternate the smallest and largest unused positions in $[0,b-1]$. Follow that list by its reversal translated by $b$ and close it cyclically. Each difference magnitude from $1$ to $b-1$ appears in both directions and the two joins give $\pm b$.

Put these layer intervals successively above the centers. For a step $x\mapsto y$ put a child labeled $x$ at center $y-x$, so its weight is $y$. Append children of the zero center and ordinary leaves consecutively. This proves the integer assertion. [Interval construction](../hub/subdivided-stars.md)

## An even number of centers

Let $m\ge4$ be even and use the following set of center labels, whose sum is zero.
$$
P_m=\{0,1,2,-3\}\ \cup\ \{\pm j:4\le j\le m/2+1\}.
$$
The exceptional center receives zero. We first assign **one child at every center** so the free labels and weights fill the same integer interval.

For $m=4,6,\ldots,20$, the certificate lists one tip per center in increasing order of center label. To cover every even $m\ge22$, use the following eight-center seed. The centers are the top row and their tips the bottom row.

| $-5$ | $-4$ | $-3$ | $0$ | $1$ | $2$ | $4$ | $5$ |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $-1$ | $7$ | $9$ | $-2$ | $8$ | $6$ | $3$ | $-6$ |

Both intervals are $[-6,9]$. Put $s=(m-8)/2\ge7$. Move each integer $x\le-4$ down by $s$ and each $x\ge4$ up by $s$. For each old center $a$ and tip $x$, the signed movements at $a,x$ sum to the movement at $a+x$, as direct substitution in the table shows. Both stretched intervals leave the same holes $\pm[4,3+s]$. Put the new centers in those holes. The resulting center set is $P_m$. Use the next $2s$ consecutive integers as tips. The signed Langford theorem gives a permutation of this tip interval with displacements $\pm[4,3+s]$. Attaching each tip to its displacement supplies all missing weights. The theorem in general gives displacements $\pm[d,d+s-1]$ on a length-$2s$ interval whenever $s\ge2d-1$. [Jordon and Mitchell, *Signed Langford sequences*](https://doi.org/10.1016/j.disc.2021.112719) · [Lean proof of the stretched interval image](../hub/RadiusTwoIntervals.lean)

**Adding layers.** For every even $m\ge8$ there is an integer permutation of $[0,m-2]$ with displacement set $P_m\setminus\{0\}$. The certificate gives its values in source order for $8\le m\le28$. For $m\ge30$, concatenate the seven positions for $m=8$ with a signed Langford permutation of defect six and order $(m-8)/2\ge11$. Its displacements fill exactly the remaining pairs $\pm[6,m/2+1]$. Use $q-1$ such consecutive layers above the seed. Every nonzero center now has $q$ children. Append $e-1$ additional children at zero and all $p$ direct leaves.

At $m=4,6$ the certificate gives permutations realizing *two* and *three* copies of every nonzero center as displacements. Every $q-1\ge2$ is a sum of twos and threes. For $q=1$ the one-tip seed suffices. For $q=2$ the certificate gives a separate initial interval with one tip at zero and two at each nonzero center. In each case the additional children at zero and ordinary leaves extend the common interval. This proves the integer theorem for every population.

For comparison, when exactly two centers have $q$ children each and there are no direct leaves, uniform increments modulo $n=2(q+1)$ exist exactly when $q$ is even. In a uniform block zero must be a center, since a zero tip would repeat its parent's incoming weight. The other center translates its tip set into itself, requiring its additive order to divide $q$. The earlier two-center theorem gives the converse and extends the core with its prescribed deficit at *every* modulus in all these cases. With a direct leaf and two equal populations, assign the centers $1,-1$, reserve zero for an ordinary leaf and use the paired layers. Thus for equal positive populations the precise exceptions to uniformity at the full modulus are the two-center, odd-population cases without direct leaves. [Two-center theorem](two-branch-joint.md)

## Prefixes and arbitrary moduli

When $m\le K\le n$, take a connected prefix of exactly $K$ edges containing all centers. We show that it can be chosen with the same integer interval property. Retain direct leaves only if needed after taking all tips. Write $t$ for the retained tip count.

For odd $m$, let the pair capacities sum to $A$ and the unpaired capacity be $e$. Retain $b=\min(A,\lfloor t/2\rfloor)$ pairs of tips across the paired centers, respecting their capacities, and $t-2b$ tips at the unpaired center. This last count is at most $e$ because $e\ge1$ and $t\le 2A+e$. Taking the largest pairs first preserves the nested layers. Zero retained tips at a center are allowed.

For even $m$, if $t>(m-1)q$, keep all $q$ children at the $m-1$ ordinary centers and $t-(m-1)q$ at the exceptional one. The even construction applies. Otherwise leave the exceptional center temporarily childless. On the remaining odd number of centers use the preceding rule with unpaired capacity $q$. The unused exceptional center itself takes the next upper integer as an ordinary leaf of the prefix. Every original vertex outside each prefix is now a leaf at a vertex of the prefix.

If $k\mid n$, reduction of the complete interval labeling gives uniform increments. Translating all labels to the actual joint adds a constant to every free vertex and twice that constant to every new weight, preserving uniformity. For arbitrary $k$, normalize the joint to zero and let $d$ be the normalized core's deficient weight.

* If $n<k$, the complete common interval is injective modulo $k$. When it misses $d$, relabel one tip at the zero center by $d$. Its vertex label and weight both become $d$. The free labels and new weights are distinct, with $d$ among the weights, as required.
* If $m\le k\le n$, use the $k$-edge prefix. Its increments are uniform, the order is again divisible by $k$, and every remaining vertex is a leaf with a labeled parent.
* If $m>k$, add the largest multiple of $k$ of the centers, using every residue once per batch. If $r=m\bmod k>0$, add the last $r$ centers and $k-r$ children of the centers already present in a single batch with labeled parents. Those earlier centers have at least $k$ children. All remaining vertices have labeled parents.

At a core of divisible order, any batch of at most $k$ vertices with already labeled parents can be added. Give the first vertex a label supplying the deficient weight. Hall's partial permutation lemma assigns the rest distinct labels avoiding that first label, and distinct new weights. A full batch returns to divisible order. This completes the extension at every modulus. [Leaf batch proof](../counterexample-bound.md#removing-leaves)

## Reproduction

The certificate uses nine one-tip seeds, eleven one-layer permutations, four multiple-layer permutations and two short seeds. For the short seeds the tips are grouped by increasing center label. The program reads the tables and finds the required signed Langford permutations by finite exact cover. The independent checker reconstructs the original vertices and edges, checks both integer intervals on 54,004 prefixes, and checks the final modular histograms for 10,531 prescribed core extensions. The histogram tests include translating the joint, supplying a missing weight, crossing several batches, and all zero bins. Five exhaustive two-center comparisons test the boundary of the uniform result. [Finite data](regular-joint-seeds.jsonl) · [Construction](regular_joint.py) · [Independent checker](check_regular_joint.py)

The leaf batch implementation uses Hall's two-request exchange. Starting with the identity permutation, it installs one requested displacement per round while preserving the others already installed. Hall proves that each exchange visits at most $k-2$ occupied rows, giving quadratic time for a full permutation. The checker tests every zero-sum request multiset through modulus 10 in shuffled order and 502 larger inputs through modulus 512. [Hall's original proof, §2](https://doi.org/10.1090/S0002-9939-1952-0050579-7) · [Implementation](../large_order_hall_pools.py)

~~~sh
python3 -B -m research.census.check_regular_joint
lean research/hub/RadiusTwoIntervals.lean
~~~
