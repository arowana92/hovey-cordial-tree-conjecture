# Attaching a path to a prescribed core of order one modulo the modulus

**Theorem.** Fix a cordial labeling on a tree of order $1\pmod k$. Join a new path by an edge from any old vertex to any vertex of the path. For **every odd $k$**, the labeling extends with every old label preserved. At **every modulus**, the same conclusion holds when the joining edge enters an endpoint. The path length and the core order are arbitrary. An offset on the joining edge can be included in the old parent's label.

For example, at modulus 45 an already labeled tree of order 91 can acquire a path on 76 vertices by a single edge entering its 23rd vertex. Both the old attachment vertex and its label are unrestricted. Repeated extensions are possible whenever a stage returns the order to one modulo the modulus. In particular a path on $k-1$ vertices attached at any position, followed by a new leaf at any old or new site, is such a stage at odd $k$.

## A path with one vertex label forbidden

The core has uniform edge counts and exactly one surplus vertex residue. Translate its labels so that this surplus is zero. Let $c$ be the boundary label in these coordinates. First take a path on $n=k-1$ free vertices. It must use every nonzero residue exactly once and all $k-1$ added weights must be distinct. Later we undo the translation on the whole tree.

Use [path ranks and the endpoint lemma](four-leaves.md#paths-with-a-specified-rank). Each path class uses the consecutive ranks from zero to its size minus one, and the edge rank sums run from zero to $n-2$. Choose one class as the lower class, of size $A$. Make the labels $1+x$ in that class and $1+A+x$ in the other, for local rank $x$. The internal weights start at $A+2$ and omit precisely $A,A+1$ modulo $k$. The joining edge only has to hit one of these two holes.

**Endpoint attachment at every modulus.** The marked endpoint belongs to a class of size $B=\lceil n/2\rceil$. It can have each rank $0\le x<B$ except possibly $n=4x+1$ with $x>0$. Putting its class below permits $c=B-1-x$ or $B-x$; putting it above permits $c=-1-x$ or $-x$. The lower choices cover $[0,B]$ and the upper choices cover $[-B,0]$. Omitting one internal rank leaves both intervals covered, since each interior integer belongs to two successive pairs. As $2B+1\ge k$, this deals with every $c$. Modulus one is immediate.

**An arbitrary marked position at an odd modulus.** Now $n$ is even and each class has size $A=(k-1)/2$. For $c=0$ give the mark rank zero in the upper class. This rank is possible at every position of an even path. For $c\ne0$, set $d=\gcd(k,c)$, $q=k/d$ and $h=(d-1)/2$. The element
$$
c_0=(k-d)/2=d(q-1)/2
$$
also has gcd $d$ with $k$, since $q$ is odd. Thus some unit modulo $k$ takes $c_0$ to $c$. Indeed one can first solve for that unit modulo $q$ and then choose its lift to avoid each prime dividing $k$ but not $q$. It suffices to solve the problem for $c_0$ and scale every free label by the unit.

Put the marked class below. When $h=0$, rank zero works. Otherwise $q\ge3$, so $n=k-1\ge6h+2$. The next lemma attains rank $h$ or $h-1$ at the mark. Since $c_0=A-h$, the joining edge then weighs $A+1$ or $A$. This proves the full block.

## Two consecutive target ranks

**Lemma.** At any marked vertex of an even path on at least $6h+2$ vertices, one of the class ranks $h-1,h$ is attainable, for each $h\ge1$.

Let $a\le b$ be the distances to the endpoints. For a path of order $m$, call $y$ usable if $0\le2y<m$ and either $y=0$ or $m\ne4y+1$. The endpoint lemma gives a path starting at rank $y$ and ending at deficiency $y$. When two disjoint path blocks are joined by an edge, the first block's terminal deficiency must equal the second block's starting rank. Each class rank in the second block increases by the size of its class in the first. Use any of the following joins at target $x$.

1. End a block of order $a+1$ at the mark with rank $x$. Append a block of order $b$ starting at $\lfloor a/2\rfloor-x$. Both endpoint ranks must be usable. The same rule works with the sides exchanged.
2. Start with a block of order $a$ and use $z=x-\lfloor a/2\rfloor$ as its starting rank. Its terminal deficiency is $z$. Append the block of order $b+1$ starting at the mark with rank $z$. The earlier class offset gives the mark rank $x$.
3. Start with the reverse staircase path on $m>a$ vertices, with ranks $\lfloor(m-1-i)/2\rfloor$ in path order. Choose $m$ to give $x$ at $i=a$. Append a block of order $a+b+1-m$ starting at $\lfloor(m-1)/2\rfloor$, the first block's terminal deficiency.

Here are the covering inequalities. If $a\le h+1$, rule 3 works at $h-1$ with $m=2\lfloor a/2\rfloor+2h$. Otherwise, if $h\le\lfloor a/2\rfloor$ and rule 1 fails on the short side at both targets, its two endpoint exceptions force $a=4h$ and $b=4h+5$. Rule 1 from the other side then works at $h$ for $h\ge3$. For $h=1,2$ use rule 3 at $h-1$ with $m=6,11$, respectively. In the remaining range $a>h+1$, $h>\lfloor a/2\rfloor$, rule 2 works at one of the targets. These disjunctions, including all parity and endpoint exceptions, are proved in Lean using integer arithmetic. [Lean 4.36 proof](PathRankWindow.lean) · [Rank constructor](surplus_path.py)

## Arbitrary path length

For a shorter path, pad one end to $k-1$, apply the construction and restrict. If the mark is an endpoint, pad at the opposite end. For a longer path, set aside multiples of $k$ on each side of the mark until the remaining distances $a,b$ are at most $k-1$. If the remaining path still has at least $k$ vertices, start with $k-1$ consecutive vertices including the mark. Start at the leftmost vertex if $a\le k-2$, or the second vertex if $a=k-1$. For an endpoint attachment orient the path with the mark first.

The core with this block has order zero modulo $k$ and one deficient edge weight. Fill that weight using the omitted leftmost vertex if present, or the next vertex at the right otherwise. Vertex counts were uniform, so this single addition returns to order one modulo $k$. Everything still missing in the reduced path is a single endpoint-attached path of length at most $k-1$, handled above. Finally restore the set-aside multiples of $k$ as [uniform pendant path blocks](../counterexample-bound.md#shortening-paths), each of which adds one to every vertex and edge count.

In a minimum counterexample of order $mk+s$ with $1\le s\le k$, every terminal arm consequently has length at most $s-2$. A longer terminal arm would allow deleting exactly $s-1$ vertices down to order one modulo $k$. The leaf-deletion lemma already excludes $s=1$. At odd moduli the same deletion also rules out any path on $s-1$ free vertices attached to the rest by one edge at an interior position. [Minimum-counterexample argument](../counterexample-bound.md#removing-leaves)

The suppressed tree with $L$ leaves has at most $L-3$ internal segments. Each has length at most $2k$, or $k$ at an odd modulus. Thus the order is at most $1+L(s-2)+2k(L-3)$, with $2k$ replaced by $k$ in the odd case. Using $L\le k-2$ gives $3k^2-14k+5$ at all $k\ge5$ and $2k^2-9k+5$ at odd $k\ge5$.

## Reproduction

~~~sh
python3 -B -m research.census.check_surplus_path
lean research/census/PathRankWindow.lean
~~~

The checker recomputes both class permutations and all edge rank sums. It checks all marked vertices and boundary labels through odd modulus 73 and every endpoint case in that range, then constructs whole trees, keeping the original labels fixed and recomputing the two histograms. [Independent checks](check_surplus_path.py)
