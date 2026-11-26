# Hovey’s cordial tree conjecture

**Work in progress.** This repository gives reproducible computer-assisted proofs that every finite tree is $k$-cordial for each modulus from 8 through 17. Hovey’s conjecture for every positive integer $k$ remains open. [Eight labels](research/eight/README.md) · [Nine through thirteen](research/rainbow/README.md) · [Fourteen through seventeen](research/rainbow/ordered-cut.md)

A vertex labeling takes values in the residues modulo $k$. Each edge receives the sum of its endpoint labels modulo $k$. Among vertices, every two residue counts must differ by at most one. The same condition holds independently among edges, including residues with count zero.

## Primary literature

- Hovey introduced the conjecture, proved the tree results for three through five labels, and gave a sufficient finite test using rooted forests. His caterpillar theorem includes the case of eight labels for that family. [Mark Hovey, *A-cordial graphs* (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)
- Driscoll, Krop and Nguyen proved the six-label case by choosing smaller families of rooted pieces and fitting their label and weight counts to the core. Their paper states Hovey’s finite test in Theorem 2.2. [*All trees are six-cordial* (2017)](https://www.ejgta.org/index.php/ejgta/article/view/231)
- Driscoll proved the seven-label case by splitting trees, listing local labelings and matching them to deficient weights or surplus vertex labels. [*All Trees are Seven-Cordial* (2019 preprint, version 2)](https://arxiv.org/abs/1909.12351)
- Youssef’s Theorem 4 shows that consecutive vertex labels and consecutive edge sums imply cordiality at every modulus. This relates the tree question to super edge-magic labelings. [*On k-cordial labelling* (2009)](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)
- Müyesser and Pokrovskiy discuss how their bounded-degree methods could approach Hovey’s conjecture when the modulus is sufficiently large relative to the degree bound. Section 6 describes the extra strengthening that such a proof would require. [*On the Graham–Sloane harmonious labelling conjecture* (2025 preprint, version 2)](https://arxiv.org/html/2509.05280v2#S6)

A related polynomial argument by Gnang and Williams concerns the order-equals-modulus base case. A check of its symmetrized term on the roots of unity gives zero when $n$ does not divide 4. A degree-dependent normalization gives an exact count of valid labelings. [Calculation and corrected polynomial stabilizer](research/orbit-polynomial.md) · [Gnang and Williams, version 1](https://arxiv.org/abs/2201.02240v1)

A primary-literature search on 26 November 2026 found these results and no earlier all-orders proof for eight labels. The eight-label argument here uses a finite attachment lemma and induction on tree order. The certificate verifies that lemma.

## General moduli

For every $\gamma>0$ and all sufficiently large $k$, if a counterexample exists then a smallest one has fewer than $k^{1+\gamma}$ vertices. This bound holds at unrestricted maximum degree. The proof embeds a tree in a larger cyclic group and prescribes omitted colors whose projections modulo $k$ are distinct. [Near-linear counterexample bound and verification](research/bounded-degree/projection.md)

For every fixed maximum degree $\Delta$, there is a threshold $k_0(\Delta)$ above which every tree of that maximum degree is $k$-cordial, with no restriction on its order. A bounded-degree auxiliary tree realizes the prescribed forest boundary weights, so the embedding lemma of Müyesser and Pokrovskiy applies directly. [Proof and checks](research/bounded-degree/README.md)

For fixed $k\ge 5$, a smallest counterexample, if one exists, has at most $k-2$ leaves and $3k^2-13k+3$ vertices. The proof combines Hall’s permutation theorem with explicit labelings of pendant paths and subdivided edges. [Counterexample size bound](research/counterexample-bound.md)

A second sufficient test uses rainbow labelings of forests on $k-1$ free vertices. Choosing a connected core that contains several original leaves reduces the number of forest shapes needed. For composite moduli, a prescribed star can fail the unrestricted version of this test by an explicit divisibility condition. [Rainbow forest reduction](research/rainbow/README.md) · [Pinned star obstruction](research/rainbow/pinned-star.md)

For every prime $p$, a star together with any number of singleton leaves admits the required rainbow extension with arbitrary prescribed parent labels, up to $p-1$ new vertices. The proof computes a signed count modulo $p$. It sharpens the minimum-counterexample bounds to $p-3$ leaves and, for $p\ge7$, $2p^2-10p+4$ vertices. [Prime-modulus extension and proof](research/rainbow/prime-star.md)

For every positive modulus $k$, attaching $k$ identical copies of an arbitrary rooted branch at one vertex preserves any cordial labeling of the core. If the branch has $n$ vertices, the construction adds exactly $n$ of each vertex label and each edge weight. [Repeated-branch theorem and construction](research/repeated-branches.md)

For every prime $p$, a forest on at most $p-1$ free vertices admits a rainbow extension if at most four edges join free vertices, with arbitrary prescribed external parent labels and any forbidden vertex label. A signed count and its first moments reduce all primes to a finite computation on 30 shapes. [Proof and reproducible checks](research/prime/README.md)

Starting with any tree of order at most thirteen, add arbitrarily many leaves at any one specified vertex. Every resulting tree is $k$-cordial for every positive $k$. Integer witnesses on 12,486 rooted cores and a periodic sequence of leaf labels give the large-modulus construction. [Proof for one attachment vertex](research/hub/README.md)

For every $k,s\ge2$, a prescribed cordial labeling modulo $k$ of a caterpillar on $sk$ vertices can fail to lift modulo $sk$. Summing one fiber of leaf weights forces its two parents to have the same lifted label. [Why lifting a fixed labeling can fail](research/cyclic-lifts.md)

For any fixed rooted core $H$, testing cordiality after adding arbitrarily many leaves at its root, for every modulus, reduces to a finite problem. In particular, failure of an explicit rational linear-algebra test produces ordinary counterexamples on exactly $p$ vertices for every sufficiently large prime $p$. [Equivalence, finite bound and exact search](research/hub/rational.md)

The large-modulus result also allows unbounded degrees. For any fixed $D\ge3$ and $\epsilon>0$ with $\epsilon<1$, every tree with total degree excess $\sum_v(\deg(v)-D)_+\le k^{1-\epsilon}$ is $k$-cordial for sufficiently large $k$. The proof cuts excess child edges and uses a matching to restore all original weights. [Unbounded-degree extension](research/bounded-degree/excess.md)

Attaching a two-edge path at the root of any fixed tree makes the resulting tree cordial for all sufficiently large moduli, even after adding arbitrarily many further leaves there. Another construction allows arbitrary mixtures of rooted branches of order at most sixteen and branches with level-wise uniform branching of any height. [Hub constructions and explicit modulus bounds](research/hub/branches.md)

Every star with any subset of its edges subdivided once is cordial for every positive modulus. The construction also covers certain paired branches of arbitrary sizes. For the entire radius-two family, it suffices at each modulus $k$ to check the trees of order exactly $k$. [Proof, high-degree lemma and label checks](research/hub/subdivided-stars.md)

At every even modulus $k=2s$, a radius-two tree is $k$-cordial if a center has degree at least $s-1$, for every tree order. A subgroup construction reduces the order-$2s$ proof to a permutation sum. Two explicit labelings handle the remaining fork-shaped exceptions. [Even-modulus theorem and subgroup criterion](research/hub/even-radius.md)

At every modulus, a radius-two tree is cordial if at most five neighbors of its center have children, or if their number is odd and at most 33. The child counts and number of ordinary hub leaves are arbitrary. [Integer construction, finite certificates and verification](research/hub/branch-levels.md)

For any fixed tree with at least three nonsingleton branches at a specified hub, every sufficiently large modulus works uniformly over all numbers of extra leaves at the hub. The edge sums around a cycle of branches use every nonzero vertex label once. Branch shapes and branching depths are unrestricted. [Proof, explicit bounds and checks](research/hub/cyclic-transfer.md)

Choose any two distinct vertices of an arbitrary finite tree. After adding sufficiently many leaves at each, the resulting tree is cordial at every modulus. The proof uses consecutive integer intervals and Hovey’s caterpillar theorem. The two leaf counts may grow independently. This also gives a finite decision for all leaf counts at the chosen hubs. [Two-hub construction and exact checks](research/hub/two-hubs.md)

For every core of order at most thirteen, arbitrary leaf counts at **two** specified vertices work at every modulus, including small counts at either hub. The independent coverage check verifies 31,820 marked-core witnesses and six residual one-hub cases. [Proof and reproducible certificate](research/hub/two-hubs-small.md)
