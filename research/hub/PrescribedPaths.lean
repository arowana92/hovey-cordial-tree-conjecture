import Std

namespace Cordial.PrescribedPaths

abbrev Form := Int × Int

def plus (f g : Form) : Form := (f.1+g.1, f.2+g.2)
def eval (p t : Int) (f : Form) : Int := f.1*p + f.2*t

def eight : List Form :=
  [(1,-2),(-1,1),(2,-2),(-2,3),(0,-1),(1,-1),(-2,2),(0,1)]

def nine : List Form :=
  [(1,2),(2,2),(-4,-5),(3,4),(-1,-1),(2,3),(-2,-2),(-2,-3),(0,1)]

def extreme : List Form :=
  [(0,-2),(-1,1),(0,2),(-1,-1),(1,-1),(-1,3),(1,-2),(0,1)]

def extremeNine : List Form :=
  [(-1,2),(0,2),(1,-5),(-1,3),(0,-1),(-1,4),(1,-3),(0,-2),(0,1)]

def weights (parent : Form) : List Form → List Form
  | [] => []
  | x :: xs => plus parent x :: weights x xs

def sums (parent : Int) : List Int → List Int
  | [] => []
  | x :: xs => (parent+x) :: sums x xs

theorem eval_plus (p t : Int) (a b : Form) :
    eval p t (plus a b) = eval p t a + eval p t b := by
  simp only [eval, plus, Int.add_mul]
  omega

theorem eval_path (p t : Int) (parent : Form) (xs : List Form) :
    (weights parent xs).map (eval p t) = sums (eval p t parent) (xs.map (eval p t)) := by
  induction xs generalizing parent with
  | nil => rfl
  | cons x xs ih => simp [weights, sums, eval_plus, ih]

theorem tables : (weights (1,0) eight).Perm eight ∧
    (weights (1,0) nine).Perm nine ∧ (weights (1,0) extreme).Perm extreme ∧
    (weights (1,0) extremeNine).Perm extremeNine := by decide

theorem neutral (p t : Int) (xs : List Form) (h : (weights (1,0) xs).Perm xs) :
    (sums p (xs.map (eval p t))).Perm (xs.map (eval p t)) := by
  have hm := h.map (eval p t)
  rw [eval_path] at hm
  simpa [eval] using hm

end Cordial.PrescribedPaths

namespace Cordial.PrescribedPaths

theorem highPreparation (m p u : Int) (hm : 0 < m) (hp : -m ≤ p ∧ p ≤ m)
    (hu : -60*m ≤ u ∧ u ≤ -59*m) (row : Form) (h : row ∈ eight) :
    -182*m ≤ eval p u row ∧ eval p u row < 160*m := by
  simp [eight] at h
  rcases h with h|h|h|h|h|h|h|h <;> subst row <;> simp only [eval] <;> omega

theorem highFinish (m u t : Int) (hm : 0 < m) (hu : -60*m ≤ u ∧ u ≤ -59*m)
    (ht : 79*m ≤ t ∧ t ≤ 81*m) (row : Form) (h : row ∈ nine) :
    -182*m ≤ eval u t row ∧ eval u t row < 160*m := by
  simp [nine] at h
  rcases h with h|h|h|h|h|h|h|h|h <;> subst row <;> simp only [eval] <;> omega

end Cordial.PrescribedPaths
