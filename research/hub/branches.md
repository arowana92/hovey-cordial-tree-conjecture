# Which branches can be attached at a hub?

Fix a tree $H$ rooted at $o$. We seek distinct integer labels with $x_o=0$ such that all edge sums are distinct members of the vertex label set. Such a labeling has a unique unused vertex label $s$ among its edge weights. For every modulus greater than the span of the labels, the tree and every extension by leaves at $o$ are cordial. The cyclic list of leaf labels in the [periodic extension proof](README.md) gives the labeling for each extension.

## One short branch allows arbitrary other branches

**Theorem.** Suppose a neighbor $a$ of $o$ has at least one child and at most one of its children has children of its own. The required integer labels exist, and their minimum is the unused weight. In particular, adjoining a two-edge path at the root of *any* fixed tree makes the result cordial for all sufficiently large moduli, uniformly over the number of further leaves at that root.

Let $c$ be the degree of $o$. Give the other neighbors of $o$ the labels $1,\ldots,c-1$. Choose the nonterminal child $v$ of $a$ if there is one, and otherwise any child of $a$. Set $x_v=-c$. Reserve $a$, its edge to $v$, and all its other children for later. Those other children are leaves.

Start with $P=0$ and $N=c$. Process all remaining unlabeled vertices with parents before children. When the parent has positive label $x$, give the child label $-(N+x)$, so its edge weighs $-N$, and increase $N$ by $x$. When the parent has negative label $-y$, give the child label $P+y$, so its edge weighs $P$, and increase $P$ by $y$. These steps only use parents already labeled. Give $a$ the label $P+c$, making its edge to $v$ weigh $P$. Finally process each reserved leaf of $a$ by the negative-child rule.

Each new positive nonroot-neighbor label is at least $c$, and these labels strictly increase. The label $P+c$ of $a$ exceeds them all. Negative magnitudes strictly increase from $c$. The edges at $o$ use the labels of its neighbors. The ordinary positive-child steps and the edge $av$ together use zero and every positive label assigned by those steps exactly once. The negative-child steps use every negative label except the last exactly once. This accounts for all edges and proves the theorem.

## An integer certificate for attaching a whole branch

Let $B$ be a rooted branch on $m\ge2$ vertices. Its root will become a new neighbor of $o$. Choose any order of the other vertices with parents before children. Give the branch root the vector $(1,0)$ and start a running vector at $(0,1)$. At each vertex assign the current vector to it, then add its parent's vector to the running vector. Write $L=(A,B')$ for the terminal vector. Both coordinates of $L$ are positive. Call an order coprime if $\gcd(A,B')=1$.

**Branch lemma.** Given a core with unused weight $s$, a branch with a coprime order can always be attached at $o$ while preserving distinct integer vertex labels and edge sums in the vertex set.

Evaluate a vector $(u,v)$ as $ux+vy$. Choose integers $x_0,y_0$ with $Ax_0+B'y_0=s$. All evaluations with
$$
x=x_0+B't,\qquad y=y_0-At
$$
give $L$ the value $s$. The slope of a vertex with vector $(u,v)$ as $t$ varies is $uB'-vA$.

These slopes are nonzero and pairwise distinct. Indeed, an integer vector parallel to $L$ is an integer multiple of $L$ by coprimality. The nonroot vectors, starting at $(0,1)$, strictly increase in the coordinatewise order and all precede $L$. None can be a multiple of $L$. The difference of two of them, taken later minus earlier, has nonnegative coordinates, is nonzero, and has second coordinate strictly smaller than $B'$. It cannot be a multiple either. Subtracting the root vector from a nonroot vector gives positive second coordinate and first coordinate at most $A-1$, so it cannot be a multiple of $L$. The root itself has slope $B'>0$.

Each collision with an old vertex or between two new vertices thus excludes at most one integer $t$. Choose any remaining $t$. The hub edge uses the branch root label. Every internal edge weighs the next running value, so these edges use every nonroot branch label except the first, together with the old unused weight $s$. The label of the first nonroot branch vertex becomes the new unused weight. A singleton branch can instead receive any fresh label and leaves $s$ unchanged.

**A linear bound in the core order.** For a mixture of branches with chosen coprime orders, let $b$ bound the size of each branch and $D\ge1$ bound the largest span of the slopes together with zero in any branch. Let $h$ be the order of the resulting core, including its hub. Every $k>Dbh$ works, uniformly over further leaves at the hub. In fact use the same integer particular solution, then choose $t$ modulo $k$. A collision has a nonzero integer slope difference $d$ with $|d|\le D$, and excludes at most $\gcd(d,k)\le D$ parameters. Fewer than $bh$ pairs involving a new vertex need to be compared at a step. Singleton branches require only a fresh residue. For a prime $p>D$, each comparison excludes at most one parameter, so $p>bh$ suffices.

## Branches of unbounded height and branching

The branch lemma applies when, at each distance from the branch root, every vertex has the same number of children. Both the height and each level's branching number are unrestricted. Different branches at the hub can use different branching numbers and heights.

To see this, process each child subtree in full before proceeding to the next. For a subtree entered with running vector $z$ and parent vector $w$, write the outgoing vector as $\alpha z+\beta w$. A leaf has $(\alpha,\beta)=(1,1)$. If the child subtrees in order have coefficients $(\alpha_i,\beta_i)$, put
$$
P=\prod_{i=1}^d\alpha_i,\qquad
Q=\sum_{i=1}^d\beta_i\prod_{j>i}\alpha_j .
$$
The subtree root receives $z$, and the first addition gives $z+w$. Composing the child operations therefore gives $(\alpha,\beta)=(P+Q,P)$. At the free branch root, which has its own variable, the terminal vector is $(Q,P)$, since the initial running vector is $(0,1)$ and the parent vector of each child is $(1,0)$.

When all children have the same coprime pair $(a,d')$, we have $P=a^d$ and $Q=d'(1+a+\cdots+a^{d-1})$. Every prime dividing $P$ is coprime to $Q$. Thus $(P+Q,P)$ and $(Q,P)$ are coprime. Induction from the leaves proves the assertion. The same argument works for different child types if every prime dividing some $\alpha_i$ divides the last $\alpha_d$ and $\gcd(\alpha_d,\beta_d)=1$.

## Arbitrary mixtures of branches of order at most sixteen

Every rooted branch of order two through sixteen admits a coprime order. This is a finite computation. The largest slope span among the orders used, including slope zero, is 1,597. Consequently a core of order $h$ assembled from any number of such branches and singletons works for every $k>25{,}552h$ and every prime $p>\max(1597,16h)$. The number of additional hub leaves is unrestricted. The bound certifies a sufficient range and can be replaced by the actual branch sizes and slope differences.

The program grows all rooted tree shapes by leaf insertion. For each it finds a parent-before-child order, checks coprimality, evaluates the actual integer labels and checks their distinctness, their edge sums and the predicted missing weight. It also checks the short-branch construction whenever its hypothesis holds, and glues mixed branches over the integers and modulo 1009, 1024 and 1155. At order sixteen alone there are 235,381 rooted shapes, of which 179,626 satisfy the short-branch hypothesis as rooted cores.

~~~sh
python3 -B -m research.hub.branches 16
~~~

Whether every rooted branch has a coprime order is open in this work. Even a proof would give a threshold for each fixed core; the full conjecture includes smaller moduli and cores that vary with the modulus. [Construction and direct checks](branches.py) · [Equivalence with large-prime obstructions](rational.md)
