# Hovey’s cordial tree conjecture

**Work in progress.** This repository gives reproducible computer-assisted proofs that every finite tree is 8-, 9- and 10-cordial. Hovey’s conjecture for every positive integer $k$ remains open. [Eight-label proof](research/eight/README.md) · [Nine- and ten-label proofs and certificates](research/rainbow/README.md)

A vertex labeling takes values in the residues modulo $k$. Each edge receives the sum of its endpoint labels modulo $k$. Among vertices, every two residue counts must differ by at most one. The same condition holds independently among edges, including residues with count zero.

## Primary literature

- Hovey introduced the conjecture, proved the tree results for three through five labels, and gave a sufficient finite test using rooted forests. His caterpillar theorem includes the case of eight labels for that family. [Mark Hovey, *A-cordial graphs* (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)
- Driscoll, Krop and Nguyen proved the six-label case by choosing smaller families of rooted pieces and fitting their label and weight counts to the core. Their paper states Hovey’s finite test in Theorem 2.2. [*All trees are six-cordial* (2017)](https://www.ejgta.org/index.php/ejgta/article/view/231)
- Driscoll proved the seven-label case by splitting trees, listing local labelings and matching them to deficient weights or surplus vertex labels. [*All Trees are Seven-Cordial* (2019 preprint, version 2)](https://arxiv.org/abs/1909.12351)
- Müyesser and Pokrovskiy discuss how their bounded-degree methods could approach Hovey’s conjecture when the modulus is sufficiently large relative to the degree bound. Section 6 describes the extra strengthening that such a proof would require. [*On the Graham–Sloane harmonious labelling conjecture* (2025 preprint, version 2)](https://arxiv.org/html/2509.05280v2#S6)

A primary-literature search on 26 November 2026 found these results and no earlier all-orders proof for eight labels. The eight-label argument here uses a finite attachment lemma and induction on tree order. The certificate verifies that lemma.

## General moduli

For fixed $k\ge 5$, a smallest counterexample, if one exists, has at most $k-2$ leaves and $3k^2-13k+3$ vertices. The proof combines Hall’s permutation theorem with explicit labelings of pendant paths and subdivided edges. [Counterexample size bound](research/counterexample-bound.md)

A second sufficient test uses rainbow labelings of forests on $k-1$ free vertices. Choosing a connected core that contains several original leaves reduces the number of forest shapes needed. For composite moduli, a prescribed star can fail the unrestricted version of this test by an explicit divisibility condition. [Rainbow forest reduction](research/rainbow/README.md) · [Pinned star obstruction](research/rainbow/pinned-star.md)
