# A linear-range signed construction for every rooted tree

**Theorem.** Every $n$-vertex tree with a specified root $r$ has integer vertex labels $x_v$ in $[-81n,81n]$ with pairwise distinct absolute values, such that
$$
\big\{|x_u+x_v|:uv\in E\big\}=\big\{|x_v|:v\ne r\big\}
$$
as multisets. We can require $x_r=0$ with all other labels nonzero, or require every label to be nonzero. The bound is independent of height, degree and the chosen root.

The absolute values permit each edge sum to have either sign. Hovey's conjecture uses the actual endpoint sum. The reflected trees below turn the signed identities into ordinary cordial labelings.

## Ordinary one-hub families with a linear modulus bound

Let $A$ be **any** tree of order $n$. Each of the following constructions gives an ordinary $k$-cordial tree at every $k>162n$, uniformly over all further leaves at the indicated new hub.

1. Join two copies of $A$ to a new hub $o$ by edges to the two copies of a chosen vertex $v$.
2. Choose vertices $u,v$ of $A$ independently. Join the two copies of $u$ by an edge. Add a new vertex $o$ adjacent to one copy of $v$.

Use the nonzero theorem rooted at $v$, with labels $x$ on one copy and $-x$ on the other. Their internal edge sums together use both signs of each nonroot label. In (1), label $o$ zero and the two hub edges supply $x_v,-x_v$. Only zero is missing. In (2), the joining edge weighs zero, and the edge from $o$ supplies $x_v$. Only $-x_v$ is missing. Distinctness survives reduction at $k>162n$. The [periodic leaf extension](README.md) now fills arbitrary populations at $o$.

**At every modulus, $166n$ extra leaves suffice in construction (2).** In the nonzero-root proof below use the bound $M=84n$, and multiply the initial piece by $7n$. This puts $x_v=M$ and all other magnitudes strictly below $M$. The same parameter count applies. The reflected core uses $2n+1$ distinct integers of $[-M,M]$, and its edge sums omit only the minimum $-M$ from those vertex labels. Give one leaf at $o$ each of the $2(M-n)=166n$ still unused integers. Each such label is its own edge sum. Vertices now fill $[-M,M]$ and edge sums fill $[1-M,M]$. Further leaves use consecutive integers above $M$. This produces a super edge-magic tree for every larger population, as well as ordinary cordiality for every positive modulus. The construction and the $k>162n$ theorem together leave only a rectangle of at most $162n$ moduli and $166n$ populations for this family.

For comparison, if $A$ has a graceful labeling, Makadia, Kaneria, Andharia and Jadeja prove that joining the copies of any corresponding vertex gives an $\alpha$-graceful tree. Their theorem takes a graceful labeling as input. The two one-hub results above accept an arbitrary tree and add a movable star at the specified site. [Makadia et al., Theorem 2.1 (2022)](https://jaem.isikun.edu.tr/web/images/articles/vol.12.no.3/14.pdf)

## Five small pieces

Use the following pieces below an already labeled nonzero parent $p$. Within a piece give its vertices the displayed labels, where $t$ is a free integer. A parent index of 0 denotes the external parent $p$, the other indices are one-based. A negative weight index means the negative of the specified new label. In the last column setting $t=cp$ over the rationals gives every label magnitude at most $|p|/2$.

| Piece | Parent indices | New labels in order | Weight indices | $c$ |
|---|---|---|---|---:|
| Two siblings | 0,0 | $-t-p,t$ | $-2,-1$ | $-1/2$ |
| One arm of length one and one of length two | 0,0,2 | $2t-p,-2t,t$ | $-2,-1,-3$ | $1/4$ |
| Three arms of length two | 0,1,0,3,0,5 | $2t,2t+p,6t+p,-4t-p,-6t-2p,3t+p$ | $2,-4,-5,1,-3,-6$ | $-1/4$ |
| Path of length three | 0,1,2 | $t,t+p,-2t-p$ | $2,-3,-1$ | $-1/2$ |
| One vertex with two arms of length two | 0,1,2,1,4 | $4t,4t+p,-8t-p,-2t,t$ | $2,-3,-1,-4,-5$ | $-1/8$ |

Each weight index follows by adding its incident labels. Within each row the coefficient pairs of the labels are distinct even up to simultaneous negation. All coefficients of $t$ are nonzero.

## Decomposing an arbitrary rooted tree

Work from the leaves up. Each processed child returns an empty set or a path of one or two pending vertices starting at that child. Other vertices of its subtree have already been allocated to pieces. The following rules allocate pending vertices, so every piece attaches by its specified parent edges.

At a vertex take pairs of one-vertex arms, then triples of two-vertex arms. If both lengths remain, take one arm of each. The remaining arms are either empty, a single one-vertex arm, or one or two two-vertex arms. In the last two-vertex-arm cases, include the current vertex and use the path or fork row of the table, returning nothing. Otherwise return the current vertex followed by the remaining one-vertex arm, if present. Induction shows these are all possible returns. Reverse the order of piece allocation for labeling, so each exterior parent already has a label.

At the root, perform the groups of sibling arms but keep the root together with the remaining arms as an initial piece. The following labels cover its four possibilities. Their internal edge-sum magnitudes are exactly the magnitudes other than the root.

| Remaining arms | Initial labels, root first |
|---|---|
| None | $12$ |
| One of length one | $12,-6$ |
| One of length two | $12,-4,8$ |
| Two of length two | $12,-2,1,-10,5$ |

This gives the nonzero-root construction. To put zero at the root, apply the same decomposition separately in each of its branches. A hub edge uses its branch-root label. Multiply each branch's initial piece by a positive integer to avoid all earlier magnitudes. At most $5n$ positive choices are excluded, since there are at most five initial entries. Scale at most $5n+1$ thus suffices and the initial labels are bounded by $12(5n+1)\le81n$.

## Keeping the labels in a linear interval

Set $M=81n$. In a table row on $b$ vertices let $A$ be the largest absolute coefficient of $t$. Given $|p|\le M$, every choice $|t-cp|\le M/(2A)$ keeps the whole row within $[-M,M]$. The interval contains at least $\lfloor M/A\rfloor\ge 2bn$ integers by the five explicit values of $A$.

If $m$ vertices are already labeled, forbidding both signs of every old label and zero removes at most $b(2m+1)$ choices. Forbidding equality up to sign among the new vertices removes at most $b(b-1)$ further choices. Each comparison either excludes at most one $t$ or has nonzero constant difference, since the coefficient pairs are distinct up to sign and $p\ne0$. As $m+b\le n$, the total is at most $2bn-b^2$. Some parameter therefore remains at every step.

## Reproduction

The symbolic checker adds the coefficient pairs on the actual parent edges of each piece, compares the unsigned forms as multisets, and verifies the bounds. The full-tree checker verifies the signed endpoint sums under both root conventions and both ordinary reflected constructions. It includes every rooted shape through nine vertices, and trees up to order 400 including a path, a star, a binary tree and irregular trees. The universal statements follow from the decomposition and the parameter count.

~~~sh
python3 -B -m research.hub.check_signed_blocks
python3 -B -m research.hub.signed_tree
~~~

[Integer constructor](signed_tree.py) · [Symbolic checks](check_signed_blocks.py)
