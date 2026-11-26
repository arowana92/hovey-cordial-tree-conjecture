# Hovey’s cordial tree conjecture

**Work in progress.** This repository gives reproducible computer-assisted proofs that every finite tree is $k$-cordial for each modulus from 8 through 21. Hovey’s conjecture for every positive integer $k$ remains open. [Eight labels](research/eight/README.md) · [Nine through thirteen](research/rainbow/README.md) · [Fourteen through seventeen](research/rainbow/ordered-cut.md) · [Eighteen through twenty-one](research/rainbow/native-spine.md)

At eight labels, Lean proves the theorem for finite trees built by joining rooted subtrees. It checks the finite certificate, the induction and the counts on each tree’s actual edges. [Formal proof and replay](research/eight/README.md#the-complete-eight-label-theorem-in-lean)

For **any finite tree and any chosen vertex**, adding sufficiently many leaves at that vertex gives a super edge-magic tree. One integer labeling then works at every positive modulus. For each fixed bound on the matching number or on the number of nonleaf vertices, only finitely many trees can fail to be super edge-magic. [Construction, proof and independent checks](research/hub/endpoint-hub.md)

Every tree of diameter at most four is cordial for **every** positive modulus. A computer-assisted construction gives one integer labeling with consecutive vertex labels and consecutive edge sums. [Proof, certificates and independent checks](research/hub/all-radius-two.md)

For diameter five, every tree is $k$-cordial for $1\le k\le36$. At any modulus, testing only trees of order exactly $k$ suffices. Every diameter-five tree of order at least $2k-5$ is $k$-cordial regardless of that test. [Reduction, finite proofs and reproducible checks](research/hub/diameter-five.md)

A vertex labeling takes values in the residues modulo $k$. Each edge receives the sum of its endpoint labels modulo $k$. Among vertices, every two residue counts must differ by at most one. The same condition holds independently among edges, including residues with count zero.

## Primary literature

- At one label every tree is immediate. Cahit proved that every tree is cordial at two labels in 1987. [Cahit, *Cordial graphs*, Ars Combinatoria 23, pp. 201–207](https://combinatorialpress.com/ars/vol23/)
- Hovey introduced the conjecture, proved the tree results for three through five labels, and gave a sufficient finite test using rooted forests. His caterpillar theorem includes the case of eight labels for that family. [Mark Hovey, *A-cordial graphs* (1991)](https://doi.org/10.1016/0012-365X(91)90254-Y)
- Hegde and Srinivasa Murthy report a result for trees of order below a prime modulus. Lemma 2.6 in their author-posted manuscript fails on four distinct residues modulo five, leaving a gap in that derivation. [2014 paper](https://doi.org/10.1080/09720529.2013.867698) · [Four-variable example, manuscript and Lean verification](research/prime/restricted-value.md)
- Driscoll, Krop and Nguyen proved the six-label case by choosing smaller families of rooted pieces and fitting their label and weight counts to the core. Their paper states Hovey’s finite test in Theorem 2.2. [*All trees are six-cordial* (2017)](https://www.ejgta.org/index.php/ejgta/article/view/231)
- Driscoll proved the seven-label case by splitting trees, listing local labelings and matching them to deficient weights or surplus vertex labels. [*All Trees are Seven-Cordial* (2019 preprint, version 2)](https://arxiv.org/abs/1909.12351)
- Youssef’s Theorem 4 shows that consecutive vertex labels and consecutive edge sums imply cordiality at every modulus. This relates the tree question to super edge-magic labelings. [*On k-cordial labelling* (2009)](https://ajc.maths.uq.edu.au/pdf/43/ajc_v43_p031.pdf)
- Müyesser and Pokrovskiy discuss how their bounded-degree methods could approach Hovey’s conjecture when the modulus is sufficiently large relative to the degree bound. Section 6 describes the extra strengthening that such a proof would require. [*On the Graham–Sloane harmonious labelling conjecture* (2025 preprint, version 2)](https://arxiv.org/html/2509.05280v2#S6)

At modulus $k=n-1$, a cordial labeling of an $n$-vertex tree uses every edge residue once and repeats exactly one vertex residue. Thus the full conjecture includes the Graham–Sloane harmonious tree conjecture. [Müyesser and Pokrovskiy, introduction](https://arxiv.org/html/2509.05280v2#S1)

A related polynomial argument by Gnang and Williams concerns the order-equals-modulus base case. A check of its symmetrized term on the roots of unity gives zero when $n$ does not divide 4. A degree-dependent normalization gives an exact count of valid labelings. [Calculation and corrected polynomial stabilizer](research/orbit-polynomial.md) · [Gnang and Williams, version 1](https://arxiv.org/abs/2201.02240v1)

Primary-literature searches on 26–27 November 2026 found these results and no earlier all-orders proof for eight labels. The eight-label argument here uses a finite attachment lemma and induction on tree order. The certificate verifies that lemma.

## General moduli

At any modulus $k$, testing all trees below order $2^{26}k$ suffices to decide the conjecture at that modulus. A smallest counterexample has fewer than $k$ leaves, and three collections of degree-two vertices give a labeling of every larger tree with that few leaves. Every counterexample has fewer than $2^{28}k$ nonleaf vertices. [Linear order test, permutation construction and checks](research/large-order/hall-pools.md)

For each fixed $0<\varepsilon<1$, all but $O_\varepsilon(k\sqrt{\log(2k)})$ leaves of a counterexample are adjacent to its $\lceil k^\varepsilon\rceil$ largest leaf parents, ranked by their numbers of leaf neighbors. If every parent has at most $k^{1-\varepsilon}$ leaf neighbors, the same bound holds for the entire tree order. If at most $k^{1-\delta}$ parents have leaves as well, the order is $O_{\varepsilon,\delta}(k)$ for fixed $0<\delta<1$. A separate linear bound allows arbitrarily many such parents when the nonleaf tree has bounded degree apart from a bounded number of vertices. [Leaf routing, proof and independent checks](research/large-order/leaf-routing.md)

Every tree of maximum degree at least $13001k$ is $k$-cordial. In fact, adding $13000k$ leaves at any one prescribed vertex suffices. Seven successive vertices can transfer a missing edge weight between arbitrary residues. Enough disjoint paths make the vertex and edge histograms agree except for one unit, with absolute constant discrepancy in each bin. [Proof, Lean identity and whole-tree checks](research/large-order/gap-path.md)

Every possible counterexample at modulus $k$ has order $O(k\log(2k))$. An earlier construction first makes the vertex and edge histograms differ by exactly one unit, with logarithmic error in every bin, then fills the bins with leaves. [Order bound by interval rounding](research/large-order/primitive.md) · [Squared differences](research/large-order/diagonal.md) · [Twelve-vertex path, rounding and degree bound](research/large-order/flexible-path.md)

For every fixed $k$, **every sufficiently large tree is $k$-cordial**, with unrestricted degrees. In fact order $(2^{34}+4)k^2$ suffices, and independently a single vertex of degree at least $4k^2$ suffices at any order. For every fixed $\gamma>0$ and sufficiently large $k$, a vertex of degree at least $k^{3/2+\gamma}$ also suffices. [Asymptotic degree bound](research/large-order/pruning-depth.md) [Quadratic bound for every counterexample](research/large-order/quadratic.md) · [High-degree construction](research/large-order/high-degree.md) · [Basic correction and Lean verification](research/large-order/README.md)

For every $\gamma>0$ and all sufficiently large $k$, if a counterexample exists then a smallest one has fewer than $k^{1+\gamma}$ vertices. In addition, its order must lie within $o(k)$ of a multiple of $k$ from below, including that multiple. These restrictions hold at unrestricted maximum degree. The first proof uses a larger cyclic group, and the second adapts the almost-spanning rainbow embedding theorem to prescribed parent labels. [Near-linear counterexample bound](research/bounded-degree/projection.md) · [Order residue and prescribed embeddings](research/rainbow/pinned-prefix.md)

A path on at least $k^{1+\gamma}$ vertices, for any fixed $\gamma>0$ and sufficiently large $k$, also suffices for the entire tree to be $k$-cordial, regardless of the branches attached to it. At each modulus a separate criterion uses the sizes of successive neighborhoods of a cordial subtree. [Protected subtrees and the neighborhood criterion](research/large-order/balls.md)

For every fixed maximum degree $\Delta$, there is a threshold $k_0(\Delta)$ above which every tree of that maximum degree is $k$-cordial, with no restriction on its order. A bounded-degree auxiliary tree realizes the prescribed forest boundary weights, so the embedding lemma of Müyesser and Pokrovskiy applies directly. [Proof and checks](research/bounded-degree/README.md)

For fixed $k\ge 5$, a smallest counterexample, if one exists, has at most $k-2$ leaves and $3k^2-13k+3$ vertices. The proof combines Hall’s permutation theorem with explicit labelings of pendant paths and subdivided edges. [Counterexample size bound](research/counterexample-bound.md)

A second sufficient test uses rainbow labelings of forests on $k-1$ free vertices. Choosing a connected core that contains several original leaves reduces the number of forest shapes needed. For composite moduli, a prescribed star can fail the unrestricted version of this test by an explicit divisibility condition. [Rainbow forest reduction](research/rainbow/README.md) · [Pinned star obstruction](research/rainbow/pinned-star.md)

For every prime $p$, a star together with any number of singleton leaves admits the required rainbow extension with arbitrary prescribed parent labels, up to $p-1$ new vertices. The proof computes a signed count modulo $p$. It sharpens the minimum-counterexample bounds to $p-3$ leaves and, for $p\ge7$, $2p^2-10p+4$ vertices. [Prime-modulus extension and proof](research/rainbow/prime-star.md)

For every positive modulus $k$, attaching $k$ identical copies of an arbitrary rooted branch at one vertex preserves any cordial labeling of the core. If the branch has $n$ vertices, the construction adds exactly $n$ of each vertex label and each edge weight. [Repeated-branch theorem and construction](research/repeated-branches.md)

For every prime $p$, a forest on at most $p-1$ free vertices admits a rainbow extension if at most four edges join free vertices, with arbitrary prescribed external parent labels and any forbidden vertex label. A signed count and its first moments reduce all primes to a finite computation on 30 shapes. [Proof and reproducible checks](research/prime/README.md)

Starting with any tree of order at most twenty, add arbitrarily many leaves at any one specified vertex. Every resulting tree is super edge-magic and $k$-cordial for every positive $k$. This includes every tree with some vertex incident to all but at most ten edges. The verifier checks 20,247,374 rooted shapes across all orders through twenty. [Interval proof, generators and digests](research/hub/one-hub-interval.md) · [Earlier one-site modular construction](research/hub/README.md)

For every $k,s\ge2$, a prescribed cordial labeling modulo $k$ of a caterpillar on $sk$ vertices can fail to lift modulo $sk$. Summing one fiber of leaf weights forces its two parents to have the same lifted label. [Why lifting a fixed labeling can fail](research/cyclic-lifts.md)

For **every finite tree with a specified root**, every sufficiently large modulus works for every number of leaves added there. Also, adding sufficiently many leaves at that one root gives a tree cordial at **all** positive moduli. The proof constructs distinct integer vertex labels with root zero whose endpoint sums use all but one vertex label. It follows that for any fixed bound on the number of nonleaf vertices, only finitely many tree–modulus pairs can be counterexamples, and they are effectively testable. [Proof, explicit bounds and independent checks](research/hub/universal-hub.md) · [Earlier rational criterion](research/hub/rational.md)

The large-modulus result also allows unbounded degrees. For any fixed $D\ge3$ and $\epsilon>0$ with $\epsilon<1$, every tree with total degree excess $\sum_v(\deg(v)-D)_+\le k^{1-\epsilon}$ is $k$-cordial for sufficiently large $k$. The proof cuts excess child edges and uses a matching to restore all original weights. [Unbounded-degree extension](research/bounded-degree/excess.md)

Attaching a two-edge path at the root of any fixed tree makes the resulting tree cordial for all sufficiently large moduli, even after adding arbitrarily many further leaves there. Another construction allows arbitrary mixtures of rooted branches of order at most sixteen and branches with level-wise uniform branching of any height. [Hub constructions and explicit modulus bounds](research/hub/branches.md)

Every star with any subset of its edges subdivided once is cordial for every positive modulus. The construction also covers certain paired branches of arbitrary sizes. For the entire radius-two family, it suffices at each modulus $k$ to check the trees of order exactly $k$. [Proof, high-degree lemma and label checks](research/hub/subdivided-stars.md)

For each fixed $0<\delta<1/9$ and all sufficiently large $k$, every radius-two tree of order at least $k+4k^{1-\delta}$ is $k$-cordial. Rotations of integer intervals allow exact leaf counts at several large branches. [Near-modulus radius-two bound and direct checks](research/hub/radius-threshold.md)

At every even modulus $k=2s$, a radius-two tree is $k$-cordial if a center has degree at least $s-1$, for every tree order. A subgroup construction reduces the order-$2s$ proof to a permutation sum. Two explicit labelings handle the remaining fork-shaped exceptions. [Even-modulus theorem and subgroup criterion](research/hub/even-radius.md)

Signed Langford sequences extend six sets of finite labelings to unbounded numbers of branching neighbors. Combined with the layer constructions, this proves that every radius-two tree is super edge-magic and hence cordial for all moduli. [Full diameter-four theorem](research/hub/all-radius-two.md) · [Six-branch example](research/hub/even-layers.md) · [Earlier layer constructions](research/hub/branch-levels.md)

For any fixed tree with at least three nonsingleton branches at a specified hub, every sufficiently large modulus works uniformly over all numbers of extra leaves at the hub. The edge sums around a cycle of branches use every nonzero vertex label once. Branch shapes and branching depths are unrestricted. [Proof, explicit bounds and checks](research/hub/cyclic-transfer.md)

For a fixed rooted tree, a bare path of seventeen edges anywhere suffices for every sufficiently large modulus, uniformly over extra leaves at the root. The same conclusion holds when each branch has at most four terminal vertices, even with unbounded path lengths. For any fixed bound on tips per branch, the rational obstruction question reduces to a finite test. [Path construction, Lean identity and branch coverage](research/hub/bare-path.md)

For any fixed tree in which every vertex except a specified hub has degree at most three, every sufficiently large modulus works for arbitrarily many extra leaves at the hub. A finite induction on binary branches uses 29 rational pendant-tree certificates and permits unrestricted branch height. [Proof and exact boundary-ratio checks](research/hub/binary-absorbers.md)

At all sufficiently large $k$, a tree with all but at most $(\log_2 k)/100$ of its leaves adjacent to one vertex is $k$-cordial, regardless of its order. Long paths in the other branches may have arbitrary lengths. A separate positive-density result allows up to $k^{1-\epsilon}$ terminal vertices in the core, using two coupled random collections of paths. [Proof, source theorems and arithmetic checks](research/hub/long-branches.md)

For a rooted tree with $a$ nonroot terminal vertices, some prime $p=O((a+1)^4)$ works at **every multiple of $p$** for all extra leaf populations at the root. This bound permits arbitrary path lengths. A separate bound controls the number of exceptional composite moduli. [Divisibility proof and exact prefix checks](research/hub/exceptional-moduli.md)

Every rooted tree of order $n$ has integer labels of magnitude at most $81n$ whose endpoint sums match its nonroot vertex labels up to sign, with all vertex magnitudes distinct. Using opposite labels on two copies gives ordinary cordiality for every $k>162n$ in two one-hub families with arbitrary additional leaves. In the edge-joined family, $166n$ extra leaves suffice for a super edge-magic labeling at every larger population. [Signed theorem, ordinary corollaries and symbolic verification](research/hub/signed-tree.md)

For every $h$ there is a computable $C_h$ such that attaching at least $C_h$ leaves to each vertex of **any** $h$-vertex tree gives a super edge-magic tree, hence a cordial tree at every modulus. Each population may grow independently. For five core vertices, 5,940 leaves per site suffice. An earlier criterion can apply when only five sites receive many leaves. [Uniform threshold, proof and certificates](research/hub/uniform-leaf-threshold.md) · [Five-site and diameter-five criteria](research/hub/many-leaf-parents.md)

On any fixed tree, select any two or more vertices and attach leaves only there. A computable minimum at each selected site suffices for a super edge-magic labeling, with independently varying counts. Consequently, for every fixed bound on the number of nonleaf vertices, there is a finite decision for the entire class at all moduli and all orders. [Proof, finite decision and independent verifier](research/hub/marked-leaf-threshold.md)

Every tree with at most five nonleaf vertices is super edge-magic and cordial at every modulus. This includes all trees of matching number at most three. The fork-shaped nonleaf core uses 2,619 finite labelings whose repeatable leaf layers cover every population vector. [Proof, certificate and coverage check](research/hub/five-nonleaf.md)

For a fixed core the exact successful combinations of modulus and leaf counts form an effectively semilinear set. A bound on just the second-largest leaf count from below, depending only on core order, suffices at every modulus. The one-site projection also gives exact spectra with prescribed labels at specified vertices. [Spectrum theorem, one-site projections and checks](research/hub/bounded-core-spectra.md)

Choose any two distinct vertices of an arbitrary finite tree. After adding sufficiently many leaves at each, the resulting tree is cordial at every modulus. The proof uses consecutive integer intervals and Hovey’s caterpillar theorem. The two leaf counts may grow independently. This also gives a finite decision for all leaf counts at the chosen hubs. [Two-hub construction and exact checks](research/hub/two-hubs.md)

For every core of order at most thirteen, arbitrary leaf counts at **two** specified vertices work at every modulus, including small counts at either hub. The independent coverage check verifies 31,820 marked-core witnesses and six residual one-hub cases. [Proof and reproducible certificate](research/hub/two-hubs-small.md)

Joining an odd number $q$ of equally large $m$-cordial trees in a path gives a $qm$-cordial tree whenever $q$ and $m$ are coprime. For other quotient trees with distinct quotient edge sums, the determinant governing the construction is always odd, so every power-of-two factor $m$ works. There are also sufficient conditions and exact obstructions at singular factors. [Odd quotients](research/odd-quotient.md) · [Path theorem and checks](research/path-quotient.md)

For any prime $p$, join equally large $p$-cordial trees along an odd quotient tree with a bijective labeling and distinct edge sums. If $p$ does not divide the common piece order, the joined tree is $qp$-cordial, where $q$ is the number of pieces. A leaf of the quotient has at most two simultaneous equations, which can be satisfied by scaling and translating its labels. [Leaf elimination and tests at shared factors](research/quotient-peeling.md)

For every odd-order $q$-vertex tree with a bijective cordial labeling, adding the same number of leaves at every vertex gives a tree cordial at every multiple of $q$. A construction with repeated copies of an arbitrary labeled tree also permits iterated rooted products at shared prime factors. [Product theorem and explicit labelings](research/repeated-product.md)
