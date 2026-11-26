# Hovey’s cordial tree conjecture

**Work in progress.** This repository gives reproducible computer-assisted proofs that every finite tree is 8-, 9-, 10-, 11- and 12-cordial. Hovey’s conjecture for every positive integer $k$ remains open. [Eight-label proof](research/eight/README.md) · [Proofs and certificates for nine through twelve labels](research/rainbow/README.md)

A vertex labeling takes values in the residues modulo $k$. Each edge receives the sum of its endpoint labels modulo $k$. Among vertices, every two residue counts must differ by at most one. The same condition holds independently among edges, including residues with count zero.

## Primary literature

- Hovey introduced the conjecture, proved the tree results for three through five labels, and gave a sufficient finite test using rooted forests. His caterpillar theorem includes the case of eight labels for that family. [Mark Hovey, *A-cordial graphs* (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)
- Driscoll, Krop and Nguyen proved the six-label case by choosing smaller families of rooted pieces and fitting their label and weight counts to the core. Their paper states Hovey’s finite test in Theorem 2.2. [*All trees are six-cordial* (2017)](https://www.ejgta.org/index.php/ejgta/article/view/231)
- Driscoll proved the seven-label case by splitting trees, listing local labelings and matching them to deficient weights or surplus vertex labels. [*All Trees are Seven-Cordial* (2019 preprint, version 2)](https://arxiv.org/abs/1909.12351)
- Müyesser and Pokrovskiy discuss how their bounded-degree methods could approach Hovey’s conjecture when the modulus is sufficiently large relative to the degree bound. Section 6 describes the extra strengthening that such a proof would require. [*On the Graham–Sloane harmonious labelling conjecture* (2025 preprint, version 2)](https://arxiv.org/html/2509.05280v2#S6)

A primary-literature search on 26 November 2026 found these results and no earlier all-orders proof for eight labels. The eight-label argument here uses a finite attachment lemma and induction on tree order. The certificate verifies that lemma.

## General moduli

For every fixed maximum degree $\Delta$, there is a threshold $k_0(\Delta)$ above which every tree of that maximum degree is $k$-cordial, with no restriction on its order. A bounded-degree auxiliary tree realizes the prescribed forest boundary weights, so the embedding lemma of Müyesser and Pokrovskiy applies directly. [Proof and checks](research/bounded-degree/README.md)

For fixed $k\ge 5$, a smallest counterexample, if one exists, has at most $k-2$ leaves and $3k^2-13k+3$ vertices. The proof combines Hall’s permutation theorem with explicit labelings of pendant paths and subdivided edges. [Counterexample size bound](research/counterexample-bound.md)

A second sufficient test uses rainbow labelings of forests on $k-1$ free vertices. Choosing a connected core that contains several original leaves reduces the number of forest shapes needed. For composite moduli, a prescribed star can fail the unrestricted version of this test by an explicit divisibility condition. [Rainbow forest reduction](research/rainbow/README.md) · [Pinned star obstruction](research/rainbow/pinned-star.md)

For every prime $p$, a star together with any number of singleton leaves admits the required rainbow extension with arbitrary prescribed parent labels, up to $p-1$ new vertices. The proof computes a signed count modulo $p$. It sharpens the minimum-counterexample bounds to $p-3$ leaves and, for $p\ge7$, $2p^2-10p+4$ vertices. [Prime-modulus extension and proof](research/rainbow/prime-star.md)

For every positive modulus $k$, attaching $k$ identical copies of an arbitrary rooted branch at one vertex preserves any cordial labeling of the core. If the branch has $n$ vertices, the construction adds exactly $n$ of each vertex label and each edge weight. [Repeated-branch theorem and construction](research/repeated-branches.md)

For every prime $p$, a forest on at most $p-1$ free vertices admits a rainbow extension if at most four edges join free vertices, with arbitrary prescribed external parent labels and any forbidden vertex label. A signed count and its first moments reduce all primes to a finite computation on 30 shapes. [Proof and reproducible checks](research/prime/README.md)

Starting with any tree of order at most thirteen, add arbitrarily many leaves at any one specified vertex. Every resulting tree is $k$-cordial for every positive $k$. Integer witnesses on 12,486 rooted cores and a periodic sequence of leaf labels give the large-modulus construction. [Proof for one attachment vertex](research/hub/README.md)

An arbitrary cordial labeling modulo $k$ can fail to lift modulo $sk$ for every even factor $s$. A matching in a labeled caterpillar gives a short obstruction. [Why lifting a fixed labeling can fail](research/cyclic-lifts.md)

For any fixed rooted core $H$, testing cordiality after adding arbitrarily many leaves at its root, for every modulus, reduces to a finite problem. In particular, failure of an explicit rational linear-algebra test produces ordinary counterexamples on exactly $p$ vertices for every sufficiently large prime $p$. [Equivalence, finite bound and exact search](research/hub/rational.md)
