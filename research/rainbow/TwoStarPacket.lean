import Std

namespace Cordial.TwoStarPacket

def residues (k : Int) (xs : List Int) := xs.map (fun z => z % k)

def weights (a b x y : Int) (l r : List Int) :=
  (a+x) :: (b+y) :: (l.map (fun z => x+z) ++ r.map (fun z => y+z))

private theorem cancel (k a b z : Int) (h : (a+z)%k = (b+z)%k) : a%k=b%k := by
  rw [Int.emod_eq_emod_iff_emod_sub_eq_zero] at h ⊢
  rwa [show a+z-(b+z)=a-b by omega] at h

private theorem permSum {u v : List Int} (h : u.Perm v) : u.sum=v.sum := by
  induction h with
  | nil => rfl
  | cons _ _ ih => simp [ih]
  | swap => simp [Int.add_left_comm]
  | trans _ _ l r => exact l.trans r

private theorem sumResidues (k : Int) (l : List Int) : (residues k l).sum%k=l.sum%k := by
  induction l with
  | nil => rfl
  | cons a as ih =>
    simp only [residues,List.map_cons,List.sum_cons] at *
    rw [Int.emod_add_emod,Int.add_emod a,ih,← Int.add_emod]

private theorem shifted (x : Int) (l : List Int) :
    (l.map (fun z => x+z)).sum=l.sum+(l.length:Int)*x := by
  induction l with
  | nil => simp
  | cons a as ih => simp [ih,Int.add_mul]; omega

private theorem forcedAux {k a b d gap x y e : Int} {l r : List Int}
    (size : k = (l.length:Int)+(r.length:Int)+2+e)
    (complete : (x+y)%k ∈ residues k (d::x::y::(l++r)))
    (left : ∀ z ∈ l, z%k ≠ y%k) (right : ∀ z ∈ r, z%k ≠ x%k)
    (profile : (residues k (gap::weights a b x y l r)).Perm
      (residues k (d::x::y::(l++r))))
    (ha : a%k ≠ y%k) (hb : b%k ≠ x%k) :
    gap%k = (x+y)%k ∧ ((l.length+1:Int)*(x-y)-e*y)%k = (d-a-b)%k := by
  have seen : (x+y)%k ∈ residues k (gap::weights a b x y l r) := by
    apply profile.mem_iff.mpr
    exact complete
  have gapEq : gap%k = (x+y)%k := by
    simp only [residues,weights,List.map_cons,List.map_append,List.mem_cons,
      List.mem_append,List.mem_map,List.map_map,Function.comp_apply] at seen
    rcases seen with g|p|q|h|h
    · exact g.symm
    · exact False.elim (ha (cancel k a y x (by simpa [Int.add_comm] using p.symm)))
    · exact False.elim (hb (cancel k b x y q.symm))
    · obtain ⟨z,hz,e⟩ := h
      exact False.elim (left z hz (cancel k z y x (by simpa [Int.add_comm] using e)))
    · obtain ⟨z,hz,e⟩ := h
      exact False.elim (right z hz (cancel k z x y (by simpa [Int.add_comm] using e)))
  refine ⟨gapEq,?_⟩
  have moment := congrArg (fun n : Int => n%k) (permSum profile)
  change (residues k (gap::weights a b x y l r)).sum%k =
    (residues k (d::x::y::(l++r))).sum%k at moment
  rw [sumResidues,sumResidues] at moment
  simp only [weights,List.sum_cons,List.sum_append,shifted] at moment
  rw [Int.add_emod gap,gapEq,← Int.add_emod,Int.emod_eq_emod_iff_emod_sub_eq_zero] at moment
  rw [Int.emod_eq_emod_iff_emod_sub_eq_zero]
  have algebra :
    x+y+(a+x+(b+y+(l.sum+(l.length:Int)*x+(r.sum+(r.length:Int)*y))))-
      (d+(x+(y+(l.sum+r.sum)))) =
    ((l.length+1:Int)*(x-y)-e*y-(d-a-b))+k*y := by rw [size]; grind
  rw [algebra,Int.add_mul_emod_self_left] at moment
  exact moment

/-- If neither center receives the opposite boundary label, the star orders and
    the center difference must realize the discrepancy between the old deficit
    and the sum of the two parent labels. All weights are actual endpoint sums. -/
theorem forced {k a b d gap x y : Int} {l r : List Int}
    (size : k = (l.length:Int)+(r.length:Int)+2)
    (complete : (x+y)%k ∈ residues k (x::y::(l++r)))
    (left : ∀ z ∈ l, z%k ≠ y%k) (right : ∀ z ∈ r, z%k ≠ x%k)
    (profile : (residues k (gap::weights a b x y l r)).Perm
      (residues k (d::x::y::(l++r))))
    (ha : a%k ≠ y%k) (hb : b%k ≠ x%k) :
    gap%k = (x+y)%k ∧ ((l.length+1:Int)*(x-y))%k = (d-a-b)%k := by
  simpa using forcedAux (e:=0) (by simpa using size)
    (List.mem_cons_of_mem _ complete) left right profile ha hb

/-- In a one-surplus packet the missing vertex is zero and the missing weight
    is x+y unless the opposite center produces it. The second congruence fixes
    the second center once its difference from the first has been chosen. -/
theorem forcedSurplus {k a b gap x y : Int} {l r : List Int}
    (size : k = (l.length:Int)+(r.length:Int)+3)
    (complete : (x+y)%k ∈ residues k (0::x::y::(l++r)))
    (left : ∀ z ∈ l, z%k ≠ y%k) (right : ∀ z ∈ r, z%k ≠ x%k)
    (profile : (residues k (gap::weights a b x y l r)).Perm
      (residues k (0::x::y::(l++r))))
    (ha : a%k ≠ y%k) (hb : b%k ≠ x%k) :
    gap%k = (x+y)%k ∧ ((l.length+1:Int)*(x-y)-y)%k = (0-a-b)%k := by
  simpa using forcedAux (e:=1) (by omega) complete left right profile ha hb

end Cordial.TwoStarPacket
