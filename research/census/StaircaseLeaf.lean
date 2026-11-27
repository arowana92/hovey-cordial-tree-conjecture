import Std

namespace Cordial.StaircaseLeaf

/-- Inserting a free slot at r shifts exactly the old ranks from r upwards. -/
def insertRank (r i : Nat) : Nat := if i < r then i else i+1

theorem insertion_image {limit r z : Nat} (hr : r ≤ limit) :
    (∃ i, i < limit ∧ insertRank r i = z) ↔ z ≤ limit ∧ z ≠ r := by
  constructor
  · rintro ⟨i, hi, rfl⟩
    unfold insertRank
    split <;> omega
  · rintro ⟨hz, hne⟩
    by_cases small : z < r
    · exact ⟨z, by omega, by simp [insertRank, small]⟩
    · exact ⟨z-1, by omega, by unfold insertRank; split <;> omega⟩

def otherSlot (b y : Nat) : Nat := if 2*y < b then b-y else b-1-y

/-- The new same-class edge goes one position beyond the enlarged cross-edge interval. -/
theorem mirror {b y : Nat} (hy : y < b) :
    otherSlot b y ≤ b ∧ otherSlot b y + insertRank (otherSlot b y) y = b := by
  unfold otherSlot insertRank
  split <;> split <;> omega

/-- After subtracting twice the shared root label, the allowed weight intervals
    cover every integer of [a,k+a-1]. No two new vertex ranks coincide modulo k. -/
theorem root_interval {a b k D : Nat} (ha : 0 < a) (hb : 0 < b)
    (ht : a+b-1 ≤ k) (hlo : a ≤ D) (hhi : D < k+a) :
    ∃ z, a ≤ z ∧ z+b-1 ≤ k ∧ z ≤ D ∧ D-z < a+b-1 := by
  refine ⟨min D (k-b+1), ?_⟩
  omega

/-- If neither ordinary arm can supply the order remainder, equality of the
    two arm capacities and absence of central leaves are forced. -/
theorem twin_case {left right direct k n t : Nat}
    (hsize : n = left+right+direct+3) (ht : t < k) (hk : t+k ≤ n)
    (hl : left+direct < t) (hr : right+direct < t) :
    n = 2*k-1 ∧ left=k-2 ∧ right=k-2 ∧ direct=0 := by omega

/-- A prefix moves down, a suffix moves up, and their middle stays fixed. -/
def outward (left endStart i : Int) : Int :=
  if i < left then i-1 else if endStart ≤ i then i+1 else i

theorem outward_strict {left endStart i j : Int} (h : i < j) :
    outward left endStart i < outward left endStart j := by
  unfold outward
  (repeat' split) <;> omega

/-- The moved positions for a k-1-edge staircase lie in a length-k+1
    interval. Only its two endpoints can be congruent at distinct positions. -/
theorem outward_collision {left endStart k i j : Int} (hi : 0 ≤ i)
    (hij : i < j) (hj : j < k-1)
    (hmod : k ∣ outward left endStart j - outward left endStart i) :
    outward left endStart i = -1 ∧ outward left endStart j = k-1 := by
  have hinc := outward_strict (left := left) (endStart := endStart) hij
  have lower : -1 ≤ outward left endStart i := by
    unfold outward
    (repeat' split) <;> omega
  have upper : outward left endStart j ≤ k-1 := by
    unfold outward
    (repeat' split) <;> omega
  have pos : 0 < outward left endStart j - outward left endStart i := by omega
  have le := Int.le_of_dvd pos hmod
  omega

end Cordial.StaircaseLeaf
