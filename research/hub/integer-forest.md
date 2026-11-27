# A polynomial integer labeling with prescribed boundary values

**Forest lemma.** Let a forest have at most $h$ free vertices, each component root with an entering edge from a fixed parent. Its parent has a prescribed integer label. The fixed occupied set $F$ includes all boundary labels and is contained in $[-w,w]$. Distinct component roots can have the same external parent. There is an injection of all free vertices into the integers outside $F$, with magnitudes
$$
O\big((h+1)(h+w+1)\big).
$$
Writing $V$ for its free vertex histogram and $E$ for the histogram of **all entering edges**, including the external ones, it satisfies
$$
 E-V=\sum_{i=1}^e([t_i]-[b_i]),\qquad e\le864 .
$$
Each $b_i$ is occupied by a free vertex. The $2e$ integers $\pm t_i$ are distinct and unoccupied, $b_i+2t_i\ne0$, and for every occupied label $p$ we have $t_i\ne2p$ and $b_i\notin\{-p,-2p,-3p\}$. The same magnitude bound holds for all the $t_i$. The implicit constant is absolute.

## The integer construction

Use the [neutral partial forest](polynomial-two-hubs.md#a-partially-labeled-forest-with-its-incoming-edges), with a virtual root and the actual prescribed label on each entering boundary edge. It labels an ancestor-closed portion, avoiding $[-w,w]$, with magnitude less than $2^{19}(h+w+1)$. Its entering-edge and free vertex histograms agree. Every remaining vertex is within 432 downward edges of this portion or an external parent. This step can label no vertices.

For any group of vertices within one remaining level, let $p_v$ be its parent jumps, $K$ the greatest absolute magnitude assigned so far including the fixed set, and $P=\sum p_v$. Walk from zero. While both signs remain, take a positive jump at a nonpositive position and a negative jump at a positive position. During this part the walk stays in $[-K,K]$. The last one-sign part goes monotonically to $P$; zero jumps may go first. Thus every position has magnitude at most $\max(K,|P|)$. Erase simple cycles at repetitions, associating each vertex with the tail of its own step. On the remaining simple path all tails differ from $P$. Translate the cycles successively away from $P$, the residual tails and all earlier translated tails. At each translation at most $h(h+1)$ nonnegative shifts are forbidden by a tail-value equality. All resulting offsets $a_v$ are distinct, avoid $P$, and satisfy
$$
 |a_v|\le \max(K,|P|)+h(h+1).
$$
The offset heads minus tails give $[P]-[0]$, also when the residual path is empty.

Label the vertices by $X+a_v$. At $P\ne0$ this adds the pair $(b,t)=(X,X+P)$ and $b$ is occupied by the initial residual tail. Forbid the following collisions when choosing $X$.

- All arrivals avoid earlier labels, both signs of old targets, and every integer solution of $2p=t_i$ or $jp=-b_i$ for $j=1,2,3$ from an earlier pair.
- At $P\ne0$, require $\pm t$ distinct and free of all earlier labels and target signs. The positive $t$ is already distinct from every current arrival by the offset construction. Avoid $-t$ at every arrival and require $b+2t\ne0$.
- For the new pair impose $2p\ne t$ and $jp\ne-b$ for all earlier and current labels. For current $p=X+a_v$ each comparison has nonzero coefficient in $X$.

Every test that requires sampling excludes at most one integer per equality, including comparisons with nonunit coefficient. Only four future parent positions per old pair need guarding. There are $O((h+1)(h+w+1))$ excluded integers in total, since $|F|\le2w+1$ and there are at most 432 levels. For $P=0$ just perform the first set of tests.

## Two groups keep the next total small

Let $P$ now denote the total jump of the **whole** present level, and let $d_v$ count the still unassigned children of each vertex. Write $M=\sum d_v$. A group with offsets $a_v$, total child count $m$ and weighted sum $A=\sum d_va_v$ contributes $mX+A$ to the next level's total. If $M=0$, a single placement suffices.

If one vertex carries at least $M/3$ children, put it alone in the second group. The current jump totals of both groups have magnitude at most $|P|+K$. Place the first group with the usual exclusions starting at zero. Its label magnitudes are $O(K+|P|+(h+1)(h+w+1))$. If its actual weighted sum is $T$, choose the singleton's label starting at $\lfloor-T/d_v\rfloor$. Its sole offset is zero for a nonzero singleton jump (for a zero jump the translated singleton cycle can have offset one; subtract this offset from the starting translation). A singleton placement has only $O(h+w+1)$ exclusions. Since $(M-d_v)/d_v\le2$, the singleton magnitude has the same bound as the first group's. The next total has magnitude $O((h+1)(h+w+1))$.

Otherwise order the whole level by the signed-walk rule above. Stop its first group when its accumulated child count first reaches $M/3$. Both group masses $m,n$ lie between $M/3$ and $2M/3$. The prefix sum of jumps has magnitude at most $\max(K,|P|)$, so both group jump totals have magnitude at most $K+2|P|$. Recompute offsets separately within each group. For respective weighted offset sums $A,B$, use
$$
 X_1=\lfloor-A/m\rfloor+z,\qquad
 X_2=\lfloor-B/n\rfloor-\lfloor mz/n\rfloor+\delta .
$$
Choose $z$ uniformly from $0,\ldots,L-1$ and $\delta$ independently from $0,\ldots,D-1$. If the level has $u$ vertices and $f$ values were blocked before it, one may use $L=200(u+8)(u+f+8)$ and $D=100(u+8)$. All offsets have magnitude $O(K+|P|+(h+1)^2)$. The absolute sizes of the new labels are $O(K+|P|+(h+1)(h+w+1))$ since the centers are negative weighted averages up to rounding and $1/2\le m/n\le2$.

Here are the exclusions for this box. Within either group or against the previously fixed values, every test from the preceding section excludes at most one value of its translation. For group one this costs probability at most $1/L$ per test. For group two, fix $\delta$. Each value of $\lfloor mz/n\rfloor$ occurs at most twice, so each test costs at most $2/L$. Across groups, an equality of two ordinary arrivals prescribes $X_1-X_2$. This difference strictly increases with $z$ for fixed $\delta$, costing at most $1/L$. The remaining cross-group comparisons all involve a target or guard of at least one of the two new pairs. There are only $O(u+1)$ such tests. For fixed $z$, each prescribes at most one $\delta$, because the second-group arrival, target, or multiple compared has a nonzero coefficient in $X_2$. Divisibility in a guard such as $2p=t$ can be tested as the original integer equality. For explicit counts, the first two within-group lists together have at most $(u+12)f+8u+8$ tests, at most $u^2$ more compare ordinary arrivals, and at most $20(u+8)$ cross comparisons involve a target or guard. These bounds give total excluded probability less than one with the displayed box. Enumeration therefore also suffices.

After both placements the next total is the sum of the two baseline remainders (each of magnitude at most its mass), the remainder $mz-n\lfloor mz/n\rfloor$, and $n\delta$. Its magnitude is $O((h+1)^2)$. Thus in both cases the next total is $O((h+1)(h+w+1))$. The initial total is bounded by $2^{19}h(h+w+1)$. The magnitude recurrence has a constant multiplier on $K+|P|$ and is iterated only 432 times. This proves the asserted bound with at most two errors per level. In particular a seed of linear width permits **quadratic ordinary integer magnitudes** regardless of the degrees or height.

## Independent checks

The verifier recomputes every entering weight on the original forest, adds back the claimed deficits and compares the two complete integer histograms. It also tests all exclusions against the finished labels and original fixed values. The data include all 7,813 rooted shapes through order twelve and 12 further forests with 14,928 entering edges, exercising the deep neutral seed and up to 470 discrepancy pairs. A further 245 signed level tests independently evaluate the next total in the heavy-child, balanced and terminal cases. Lean verifies the weighted-translation identity for arbitrary lists and both integer-division estimates. [Constructor](integer_layers.py) · [Actual-edge checks](check_integer_layers.py) · [Lean identities](IntegerForest.lean)

~~~sh
python3 -B -m research.hub.check_integer_layers
lean research/hub/IntegerForest.lean
~~~
