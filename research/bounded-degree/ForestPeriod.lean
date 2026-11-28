import Std

namespace Cordial.ForestPeriod

/-- A root carrying an integer label, or a new child tree grafted at the root. -/
inductive Tree where
  | vertex : Int → Tree
  | graft : Tree → Tree → Tree

def root : Tree → Int
  | .vertex x => x
  | .graft l _ => root l

def children : Tree → Nat
  | .vertex _ => 0
  | .graft l _ => children l + 1

def labels : Tree → List Int
  | .vertex x => [x]
  | .graft l r => labels l ++ labels r

def edges : Tree → List Int
  | .vertex _ => []
  | .graft l r => edges l ++ [root l + root r] ++ edges r

/-- All nonroot vertices paired with their actual numbers of children. -/
def below : Tree → List (Int × Nat)
  | .vertex _ => []
  | .graft l r => below l ++ (root r, children r) :: below r

def degreeList (t : Tree) := (root t,children t) :: below t

def moment (rows : List (Int × Nat)) : Int :=
  (rows.map (fun p => (p.2 : Int) * p.1)).sum

theorem treeIdentity (t : Tree) :
    (edges t).sum + root t = (labels t).sum + moment (degreeList t) := by
  induction t with
  | vertex x => simp [edges,root,labels,moment,degreeList,children,below]
  | graft l r hl hr =>
    simp [degreeList,moment] at hl hr
    simp [edges,root,labels,degreeList,moment,children,below,List.sum_append,Int.add_mul]
    omega

abbrev Forest := List (Tree × Int)

def vertexList (f : Forest) := f.flatMap (fun p => labels p.1)
def weightList (f : Forest) :=
  f.flatMap (fun p => (root p.1 + p.2) :: edges p.1)
def parents (f : Forest) := f.map Prod.snd
def counts (f : Forest) := f.flatMap (fun p => degreeList p.1)

theorem forestIdentity (f : Forest) :
    (weightList f).sum = (vertexList f).sum + moment (counts f) + (parents f).sum := by
  induction f with
  | nil => simp [weightList,vertexList,moment,counts,parents]
  | cons p tail ih =>
    have ht := treeIdentity p.1
    simp [weightList,vertexList,moment,counts,parents,List.sum_append] at ih ⊢
    simp [moment] at ht
    omega

private theorem momentDvd (rows : List (Int × Nat)) (d : Int)
    (h : ∀ p ∈ rows, d ∣ (p.2 : Int)) : d ∣ moment rows := by
  induction rows with
  | nil => simp [moment]
  | cons p rest ih =>
    have hp := h p (by simp)
    have hr := ih (fun a ha => h a (by simp [ha]))
    change d ∣ (p.2 : Int) * p.1 + moment rest
    exact Int.dvd_add (Int.dvd_mul_of_dvd_left hp) hr

private theorem modSum (xs : List Int) (k : Int) :
    (xs.map (fun a => a % k)).sum % k = xs.sum % k := by
  induction xs with
  | nil => simp
  | cons x t ih =>
    simp only [List.map_cons,List.sum_cons]
    rw [Int.add_emod, Int.emod_emod, ih, ← Int.add_emod]

private theorem permSum {xs ys : List Int} (h : xs.Perm ys) : xs.sum = ys.sum := by
  induction h with
  | nil => rfl
  | cons a _ ih => simp [ih]
  | swap a b t => simp only [List.sum_cons]; omega
  | trans _ _ h1 h2 => exact h1.trans h2

/-- Whenever the two residue histograms agree, every common divisor of the
    modulus and the child counts divides the sum of the actual external labels. -/
theorem parentSumDvd (f : Forest) (k d : Int) (hk : d ∣ k)
    (hc : ∀ p ∈ counts f, d ∣ (p.2 : Int))
    (same : ((weightList f).map (fun a => a % k)).Perm
            ((vertexList f).map (fun a => a % k))) : d ∣ (parents f).sum := by
  have hs : (weightList f).sum % k = (vertexList f).sum % k := by
    rw [← modSum, ← modSum (vertexList f)]
    exact congrArg (fun a : Int => a % k) (permSum same)
  have hd : k ∣ (weightList f).sum - (vertexList f).sum := by
    apply Int.dvd_of_emod_eq_zero
    rw [Int.sub_emod, hs]
    simp
  have all := Int.dvd_trans hk hd
  rw [forestIdentity] at all
  have eq : (vertexList f).sum + moment (counts f) + (parents f).sum -
      (vertexList f).sum = moment (counts f) + (parents f).sum := by omega
  rw [eq] at all
  have diff := Int.dvd_sub all (momentDvd _ _ hc)
  have he : moment (counts f) + (parents f).sum - moment (counts f) = (parents f).sum := by omega
  rwa [he] at diff

end Cordial.ForestPeriod
