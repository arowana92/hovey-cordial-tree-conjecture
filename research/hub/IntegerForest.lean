import Std

namespace Cordial.IntegerForest

/-- Translating a whole level changes the sum of next-level jumps according
    to the number of children at each translated position. -/
def moment (xs : List (Int × Int)) (x : Int) : Int :=
  (xs.map (fun (d, a) => d * (x + a))).sum

def mass (xs : List (Int × Int)) : Int := (xs.map Prod.fst).sum

theorem translateMoment (xs : List (Int × Int)) (x : Int) :
    moment xs x = mass xs * x + moment xs 0 := by
  induction xs with
  | nil => simp [moment, mass]
  | cons u xs ih =>
    rcases u with ⟨d, a⟩
    simp only [moment, mass, List.map_cons, List.sum_cons, Int.zero_add] at *
    rw [ih, Int.add_mul, Int.mul_add]
    omega

theorem centered (m a r : Int) (hm : 0 < m) :
    m*r-m < m*((-a)/m+r)+a ∧ m*((-a)/m+r)+a ≤ m*r := by
  have h := Int.emod_add_mul_ediv (-a) m
  have lo := Int.emod_nonneg (-a) (by omega : m ≠ 0)
  have hi := Int.emod_lt_of_pos (-a) hm
  rw [Int.mul_add]
  omega

/-- Residual drift from two opposite translations is one remainder plus the
    intentionally bounded transverse displacement. -/
theorem pairedDrift (m n z δ : Int) (hn : 0 < n) :
    n*δ ≤ m*z + n*(-((m*z)/n)+δ) ∧
    m*z + n*(-((m*z)/n)+δ) < n*δ+n := by
  have h := Int.emod_add_mul_ediv (m*z) n
  have lo := Int.emod_nonneg (m*z) (by omega : n ≠ 0)
  have hi := Int.emod_lt_of_pos (m*z) hn
  rw [Int.mul_add, Int.mul_neg]
  omega

theorem finalBelow (a g m x : Int) (hm : 0 < m)
    (hx : (g-a)/m < x) : g-m*x < a := by
  have h := Int.emod_add_mul_ediv (g-a) m
  have hi := Int.emod_lt_of_pos (g-a) hm
  have hl : (g-a)/m+1 ≤ x := by omega
  have hle := Int.mul_le_mul_of_nonneg_left hl (Int.le_of_lt hm)
  rw [Int.mul_add, Int.mul_one] at hle
  omega

/-- After each leaf is put at the previous missing weight minus its parent,
    its own label is the next missing weight. -/
def tips (x g : Int) : Nat → List Int
  | 0 => []
  | n+1 => (g-x) :: tips x (g-x) n

theorem broomWalk (x g : Int) (n : Nat) :
    ((tips x g n).map (x + ·)) ++ [g-(n:Int)*x] = g :: tips x g n := by
  induction n generalizing g with
  | zero => simp [tips]
  | succ n ih =>
    simp only [tips, List.map_cons, List.cons_append, Int.natCast_succ, Int.add_mul, Int.one_mul]
    rw [show x+(g-x)=g by omega, show g-(↑n*x+x)=g-x-↑n*x by omega]
    rw [ih]

theorem broomBelow (x g a : Int) (h : g-x < a) (hx : 0 < x) (n : Nat) :
    g-((n+1 : Nat):Int)*x < a := by
  have hn : 0 ≤ (n:Int)*x := Int.mul_nonneg (by omega) (by omega)
  simp only [Int.natCast_succ, Int.add_mul, Int.one_mul]
  omega

end Cordial.IntegerForest
