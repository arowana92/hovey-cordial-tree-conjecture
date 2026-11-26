import Std

/-!
A finite tree can be numbered with its root first and each parent before its
children. The parent of vertex i+1 is p i, where p i ≤ i. Only the finite
prefix in question matters. Both hypotheses of the reduction below are local.
-/
namespace Cordial

variable {k : Nat}

def tally (f : Nat → Fin k) (start : Nat) : Nat → Fin k → Nat
  | 0, _ => 0
  | len + 1, a => tally f start len a + (if f (start + len) = a then 1 else 0)

private theorem tally_add (f : Nat → Fin k) (s n r : Nat) (a : Fin k) :
    tally f s (n + r) a = tally f s n a + tally f (s + n) r a := by
  induction r with
  | zero => simp [tally]
  | succ r ih => simp [tally, ih, Nat.add_assoc]

private theorem tally_congr (f g : Nat → Fin k) (s t len : Nat) (a : Fin k)
    (h : ∀ i < len, f (s + i) = g (t + i)) :
    tally f s len a = tally g t len a := by
  induction len with
  | zero => rfl
  | succ len ih =>
    simp only [tally, h len (by omega), ih (fun i hi => h i (by omega))]

private theorem tally_mono (f : Nat → Fin k) (s n m : Nat) (a : Fin k) (h : n ≤ m) :
    tally f s n a ≤ tally f s m a := by
  obtain ⟨r, rfl⟩ := Nat.le.dest h
  rw [tally_add]
  omega

def weight (p : Nat → Nat) (f : Nat → Fin k) (i : Nat) := f (i + 1) + f (p i)

def Balanced (c : Fin k → Nat) := ∀ a b, c a ≤ c b + 1

def IsCordial (p : Nat → Nat) (n : Nat) (f : Nat → Fin k) :=
  Balanced (tally f 0 n) ∧ Balanced (tally (weight p f) 0 (n - 1))

-- At order (q+1)k, the edge histogram is q + bump d.
def bump (d a : Fin k) : Nat := if a = d then 0 else 1

def Core (p : Nat → Nat) (f : Nat → Fin k) (n q : Nat) (d : Fin k) :=
  (∀ a, tally f 0 n a = q + 1) ∧
  (∀ a, tally (weight p f) 0 (n - 1) a = q + bump d a)

def localWeight (parent : Nat → Fin k ⊕ Nat) (g : Nat → Fin k) (j : Nat) :=
  g j + (parent j).elim id g

def Fits (parent : Nat → Fin k ⊕ Nat) (g : Nat → Fin k) (r : Nat) (d : Fin k) :=
  (∀ a, tally g 0 r a ≤ 1) ∧
  (∀ a, 1 ≤ bump d a + tally (localWeight parent g) 0 r a ∧
        bump d a + tally (localWeight parent g) 0 r a ≤ 2) ∧
  (r = k → ∃ next : Fin k,
    (∀ a, tally g 0 r a = 1) ∧
    (∀ a, bump d a + tally (localWeight parent g) 0 r a = 1 + bump next a))

def BaseTest (k : Nat) := ∀ (p : Nat → Nat), (∀ i, p i ≤ i) →
  ∃ (f : Nat → Fin k) (d : Fin k), Core p f k 0 d

def ForestTest (k : Nat) := ∀ r, 0 < r → r ≤ k →
  ∀ (parent : Nat → Fin k ⊕ Nat), (∀ j < r, ∀ i, parent j = .inr i → i < j) →
  ∀ d, ∃ g, Fits parent g r d

private def join (n : Nat) (f g : Nat → Fin k) (i : Nat) :=
  if i < n then f i else g (i - n)

private def boundary (n : Nat) (p : Nat → Nat) (f : Nat → Fin k) (j : Nat) :
    Fin k ⊕ Nat :=
  let i := p (n - 1 + j)
  if i < n then .inl (f i) else .inr (i - n)

private theorem joined_counts (n r : Nat) (hn : 0 < n)
    (p : Nat → Nat) (hp : ∀ i, p i ≤ i) (f g : Nat → Fin k) (a : Fin k) :
    tally (join n f g) 0 (n + r) a = tally f 0 n a + tally g 0 r a ∧
    tally (weight p (join n f g)) 0 (n + r - 1) a =
      tally (weight p f) 0 (n - 1) a + tally (localWeight (boundary n p f) g) 0 r a := by
  constructor
  · rw [tally_add]
    congr 1
    · apply tally_congr
      intro i hi
      simp [join, hi]
    · apply tally_congr
      intro i _
      simp [join, Nat.add_sub_cancel_left, Nat.not_lt_of_ge (Nat.le_add_right n i)]
  · rw [show n + r - 1 = (n - 1) + r by omega, tally_add]
    congr 1
    · apply tally_congr
      intro i hi
      have hchild : i + 1 < n := by omega
      have hparent : p i < n := by have := hp i; omega
      simp [weight, join, hchild, hparent]
    · apply tally_congr
      intro j _
      have eq : n - 1 + j + 1 = n + j := by omega
      simp only [Nat.zero_add, weight, localWeight, boundary, eq, join]
      split <;> rename_i h
      · omega
      · simp only [Nat.add_sub_cancel_left]
        split <;> simp_all

private theorem extension (forest : ForestTest k) (n r : Nat) (hn : 0 < n)
    (hr : 0 < r) (hrk : r ≤ k) (p : Nat → Nat) (hp : ∀ i, p i ≤ i)
    (f : Nat → Fin k) (d : Fin k) :
    ∃ g, Fits (boundary n p f) g r d := by
  apply forest r hr hrk
  intro j _ i h
  have hparent := hp (n - 1 + j)
  simp only [boundary] at h
  split at h
  · contradiction
  · cases h
    omega

private theorem all_cores (hk : 0 < k) (base : BaseTest k) (forest : ForestTest k)
    (p : Nat → Nat) (hp : ∀ i, p i ≤ i) (q : Nat) :
    ∃ (f : Nat → Fin k) (d : Fin k), Core p f (k + q * k) q d := by
  induction q with
  | zero => simpa using base p hp
  | succ q ih =>
    obtain ⟨f, d, hv, he⟩ := ih
    let n := k + q * k
    have hn : 0 < n := by dsimp [n]; omega
    obtain ⟨g, _, _, hfull⟩ := extension forest n k hn hk (by omega) p hp f d
    obtain ⟨next, gv, ge⟩ := hfull rfl
    refine ⟨join n f g, next, ?_⟩
    change Core p (join n f g) (k + (q + 1) * k) (q + 1) next
    rw [Nat.succ_mul, ← Nat.add_assoc]
    constructor
    · intro a
      rw [(joined_counts n k hn p hp f g a).1, hv, gv]
    · intro a
      rw [(joined_counts n k hn p hp f g a).2, he]
      have h := ge a
      omega

/-- Both finite tests imply cordiality for every order and every parent array. -/
theorem reduction (hk : 0 < k) (base : BaseTest k) (forest : ForestTest k)
    (p : Nat → Nat) (hp : ∀ i, p i ≤ i) (n : Nat) :
    ∃ f : Nat → Fin k, IsCordial p n f := by
  by_cases small : n ≤ k
  · obtain ⟨f, d, hv, he⟩ := base p hp
    refine ⟨f, ?_, ?_⟩
    · intro a b
      have h := tally_mono f 0 n k a small
      rw [hv] at h
      omega
    · intro a b
      have h := tally_mono (weight p f) 0 (n - 1) (k - 1) a (by omega)
      rw [he] at h
      unfold bump at h
      split at h <;> omega
  · let q := (n - k) / k
    let r := (n - k) % k
    let m := k + q * k
    have hm : 0 < m := by dsimp [m]; omega
    have hsum : n = m + r := by
      have h := Nat.div_add_mod (n - k) k
      rw [Nat.mul_comm] at h
      change n = k + ((n - k) / k) * k + (n - k) % k
      omega
    have hr : r < k := Nat.mod_lt _ hk
    obtain ⟨f, d, hv, he⟩ := all_cores hk base forest p hp q
    change ∀ a, tally f 0 m a = q + 1 at hv
    change ∀ a, tally (weight p f) 0 (m - 1) a = q + bump d a at he
    by_cases empty : r = 0
    · have eq : n = m := by omega
      rw [eq]
      refine ⟨f, ?_, ?_⟩
      · intro a b
        rw [hv, hv]
        omega
      · intro a b
        rw [he, he]
        unfold bump
        split <;> split <;> omega
    · obtain ⟨g, gv, ge, _⟩ := extension forest m r hm (by omega) (by omega) p hp f d
      rw [hsum]
      refine ⟨join m f g, ?_, ?_⟩
      · intro a b
        rw [(joined_counts m r hm p hp f g a).1, (joined_counts m r hm p hp f g b).1, hv, hv]
        have := gv a
        omega
      · intro a b
        rw [(joined_counts m r hm p hp f g a).2, (joined_counts m r hm p hp f g b).2, he, he]
        have := ge a
        have := ge b
        omega

end Cordial
