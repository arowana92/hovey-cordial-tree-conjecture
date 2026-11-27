# Attaching a path at any vertex of a prescribed cordial core

**Theorem.** Fix a cordial labeling on a tree of order $0$ or $1\pmod k$. Join a new path by an edge from any old vertex to **any vertex of the path**. At every positive modulus the labeling extends with every old label preserved. The path length and the core order are arbitrary. An offset on the joining edge can be included in the old parent's label.

For example, at modulus 45 an already labeled tree of order 91 can acquire a path on 76 vertices by a single edge entering its 23rd vertex. Both the old attachment vertex and its label are unrestricted. Repeated extensions are possible whenever the next core has order zero or one modulo the modulus. In particular, from order one a path on $k-1$ vertices followed by a new leaf at any old or new site returns to order one.

## A path with one vertex label forbidden

Start with the order-one residue. The core has uniform edge counts and exactly one surplus vertex residue. Translate its labels so that this surplus is zero. Let $c$ be the boundary label in these coordinates. First take a path on $n=k-1$ free vertices. It must use every nonzero residue exactly once and all $k-1$ added weights must be distinct. Later we undo the translation on the whole tree.

Use [path ranks and the endpoint lemma](four-leaves.md#paths-with-a-specified-rank). Each path class uses the consecutive ranks from zero to its size minus one, and the edge rank sums run from zero to $n-2$. Choose one class as the lower class, of size $A$. Make the labels $1+x$ in that class and $1+A+x$ in the other, for local rank $x$. The internal weights start at $A+2$ and omit precisely $A,A+1$ modulo $k$. The joining edge only has to hit one of these two holes.

**Endpoint attachment at every modulus.** The marked endpoint belongs to a class of size $B=\lceil n/2\rceil$. It can have each rank $0\le x<B$ except possibly $n=4x+1$ with $x>0$. Putting its class below permits $c=B-1-x$ or $B-x$; putting it above permits $c=-1-x$ or $-x$. The lower choices cover $[0,B]$ and the upper choices cover $[-B,0]$. Omitting one internal rank leaves both intervals covered, since each interior integer belongs to two successive pairs. As $2B+1\ge k$, this deals with every $c$. Modulus one is immediate.

**An arbitrary marked position at an odd modulus.** Now $n$ is even and each class has size $A=(k-1)/2$. For $c=0$ give the mark rank zero in the upper class. This rank is possible at every position of an even path. For $c\ne0$, set $d=\gcd(k,c)$, $q=k/d$ and $h=(d-1)/2$. The element
$$
c_0=(k-d)/2=d(q-1)/2
$$
also has gcd $d$ with $k$, since $q$ is odd. Thus some unit modulo $k$ takes $c_0$ to $c$. Indeed one can first solve for that unit modulo $q$ and then choose its lift to avoid each prime dividing $k$ but not $q$. It suffices to solve the problem for $c_0$ and scale every free label by the unit.

Put the marked class below. When $h=0$, rank zero works. Otherwise $q\ge3$, so $n=k-1\ge6h+2$. The next lemma attains rank $h$ or $h-1$ at the mark. Since $c_0=A-h$, the joining edge then weighs $A+1$ or $A$. This proves the full block.

## Two consecutive target ranks

**Lemma.** At any marked vertex of an even path on at least $6h+2$ vertices, one of the class ranks $h-1,h$ is attainable, for each $h\ge1$. On an odd path the sufficient order is $6h-1$.

Let $a\le b$ be the distances to the endpoints. For a path of order $m$, call $y$ usable if $0\le2y<m$ and either $y=0$ or $m\ne4y+1$. The endpoint lemma gives a path starting at rank $y$ and ending at deficiency $y$. When two disjoint path blocks are joined by an edge, the first block's terminal deficiency must equal the second block's starting rank. Each class rank in the second block increases by the size of its class in the first. Use any of the following joins at target $x$.

1. End a block of order $a+1$ at the mark with rank $x$. Append a block of order $b$ starting at $\lfloor a/2\rfloor-x$. Both endpoint ranks must be usable. The same rule works with the sides exchanged.
2. Start with a block of order $a$ and use $z=x-\lfloor a/2\rfloor$ as its starting rank. Its terminal deficiency is $z$. Append the block of order $b+1$ starting at the mark with rank $z$. The earlier class offset gives the mark rank $x$.
3. Start with the reverse staircase path on $m>a$ vertices, with ranks $\lfloor(m-1-i)/2\rfloor$ in path order. Choose $m$ to give $x$ at $i=a$. Append a block of order $a+b+1-m$ starting at $\lfloor(m-1)/2\rfloor$, the first block's terminal deficiency.

For even path order, if $a\le h+1$, rule 3 works at $h-1$ with $m=2\lfloor a/2\rfloor+2h$. Otherwise, if $h\le\lfloor a/2\rfloor$ and rule 1 fails on the short side at both targets, its two endpoint exceptions force $a=4h$ and $b=4h+5$. Rule 1 from the other side then works at $h$ for $h\ge3$. For $h=1,2$ use rule 3 at $h-1$ with $m=6,11$, respectively. In the remaining range $a>h+1$, $h>\lfloor a/2\rfloor$, rule 2 works at one of the targets. These disjunctions, including all parity and endpoint exceptions, are proved in Lean using integer arithmetic. [Lean 4.36 proof](PathRankWindow.lean) · [Rank constructor](surplus_path.py)

For odd path order use rule 3 when $a<h$, with $m=2\lfloor(a+1)/2\rfloor+2h-1$ and $x=h-1$. When $a\ge h$ use rule 1 for $h\le\lfloor a/2\rfloor$ and rule 2 otherwise. The two blocks now have opposite parities. The only surviving exception to these choices is $a=b=4,h=1$, where the [rank-zero path lemma](four-leaves.md#paths-with-a-specified-rank) gives rank zero. The theorem `oddWindow` checks the disjunction for all lengths.

## Even moduli

Let $k$ be even and $n=k-1$. The class containing the mark has size $B=k/2-(a\bmod2)$, where $a$ is its distance from an endpoint. At $c=0$ rank zero in the upper class works. The only rank-zero exception is the midpoint at $k=6$, treated below. For $c\ne0$ set $q=k/d$, $d=\gcd(c,k)$ as before.

- If $q$ is odd, take $c_0=(k-d)/2$ and $h=B-c_0\ge0$. Since $k\ge3d$, $n\ge6h-1$. In the lower class rank $h$ or $h-1$ gives a missing weight. At $h=0$ use rank zero.
- If $q$ is even and $q\ge6$, take $c_0=-d$ and $h=d$. Again $n\ge6h-1$. Put the mark in the upper class. Its label is $1+A+x$, so $c_0$ plus that label is $A$ or $A+1$. In both cases multiplication by a unit takes $c_0$ to the required $c$.

For orders two and four split the free path into disjoint blocks on $m$ and $s=n-m$ vertices. Each block may choose its two classes independently. Give labels $1$ through $A$ to the combined lower class and $A+1$ through $k-1$ to the combined upper class, where $A$ is the total lower size. Within each class the second block's ranks follow the first block's ranks. Before the bridge is added the three free weights are $A,A+1,A+1+m$ modulo $k$, by counting the two internal intervals.

**Order two.** Here $c=k/2$. At an even distance from a tip the mark belongs to a class of size $k/2$, and rank zero in that lower class works. At odd distances $a,b$ from the tips, use the first $a+1$ vertices as the first block, ending with the mark at rank zero in the lower class. Make the beginning of the second block lower as well. Then $A=k/2$ and the mark has label 1. The joining edge from the core hits $A+1$. Give the second block's first vertex rank $(b-3)/2$, hence label $A-1$. The bridge hits $A$. This rank is usable whenever $b\ge3$ and $b\ne5$. Either arm can play this role. If both lengths lie in $\{1,5\}$ there are three explicit rows below.

**Order four.** Normalize to $c=d=k/4$ by negating labels if necessary. Let $a\le b$ be the distances from the tips. For $a=2d-1$ the mark is the midpoint. Put it in the upper class of the staircase so that its rank is $d-1$. This handles $c=-d$, and negation handles $d$. Otherwise take $m=d+\lfloor a/2\rfloor$. Then $a<m<s$. Use the staircase on the first block with the mark in the upper class. Its edge from the core hits $A+1+m$. Start the second block in the same class as the *final* vertex of the first block. These two vertices' classes have local sizes $u=\lceil m/2\rceil$ and $v=\lceil s/2\rceil$ respectively. The final vertex already has the maximum local rank $u-1$. If both bridge endpoints are lower, starting ranks $v-u$ and $v-u-1$ on the second block yield bridge weights $A+1$ and $A$. If both are upper, ranks $v-u$ and $v-u+1$ yield $A$ and $A+1$ modulo $k$. At least one of the two indicated ranks is usable in each case, including $v=u$. These inequalities are the Lean theorem `quarterCut`.

For the three exceptional half-turns, path rows in order from the first tip are $(1,2,3)$ at $(a,b)=(1,1)$, $(1,2,6,7,3,4,5)$ at $(1,5)$ and $(1,2,3,4,8,10,11,9,5,6,7)$ at $(5,5)$. At $k=6$ with the midpoint marked, the rows for $c=0,1,2,3,4,5$ are respectively $12435,12435,13542,25314,13254,13245$, one label per digit. Each uses exactly the nonzero residues and gives distinct sums including the boundary edge. This exhausts the even-modulus cases.

## Arbitrary path length

For a shorter path, pad one end to $k-1$, apply the construction and restrict. If the mark is an endpoint, pad at the opposite end. For a longer path, set aside multiples of $k$ on each side of the mark until the remaining distances $a,b$ are at most $k-1$. If the remaining path still has at least $k$ vertices, start with $k-1$ consecutive vertices including the mark. Start at the leftmost vertex if $a\le k-2$, or the second vertex if $a=k-1$. For an endpoint attachment orient the path with the mark first.

The core with this block has order zero modulo $k$ and one deficient edge weight. Fill that weight using the omitted leftmost vertex if present, or the next vertex at the right otherwise. Vertex counts were uniform, so this single addition returns to order one modulo $k$. Everything still missing in the reduced path is a single endpoint-attached path of length at most $k-1$, handled above. Finally restore the set-aside multiples of $k$ as [uniform pendant path blocks](../counterexample-bound.md#shortening-paths), each of which adds one to every vertex and edge count.

For a core of order zero modulo $k$, again set aside the multiples of $k$ at both tips. On the remaining path take up to $k$ consecutive vertices starting at the left tip, including the mark, which is at distance less than $k$ from it. Restrict the ordinary staircase labeling of an order-$k$ path to this block. Translate all its labels together so that the boundary edge hits the deficient old weight. The new vertex labels are distinct and the internal weights are distinct, as required after filling the deficit. If the block had order $k$, the enlarged core again has order zero modulo $k$. The remaining endpoint-attached block has fewer than $k$ vertices, so the same step finishes it. Restore the set-aside periods.

In a minimum counterexample of order $mk+s$ with $1\le s\le k$, every terminal arm consequently has length at most $s-2$. A longer terminal arm would allow deleting exactly $s-1$ vertices down to order one modulo $k$. The leaf-deletion lemma already excludes $s=1$. At every modulus the same deletion also rules out any path on $s-1$ free vertices attached to the rest by one edge at an interior position. [Minimum-counterexample argument](../counterexample-bound.md#removing-leaves)

The suppressed tree with $L$ leaves has at most $L-3$ internal segments. Each has length at most $2k$, or $k$ at an odd modulus. Thus the order is at most $1+L(s-2)+2k(L-3)$, with $2k$ replaced by $k$ in the odd case. Using $L\le k-2$ gives $3k^2-14k+5$ at all $k\ge5$ and $2k^2-9k+5$ at odd $k\ge5$.

## Reproduction

~~~sh
python3 -B -m research.census.check_surplus_path
lean research/census/PathRankWindow.lean
~~~

The checker recomputes both class permutations and all edge rank sums. It checks every marked vertex and boundary label at every modulus from 2 through 73, then constructs whole trees at both core residues, keeping the original labels fixed and recomputing the two histograms. [Independent checks](check_surplus_path.py)
