import Std

namespace Cordial.LeafIntervals

abbrev Choice := Int × Int

def weight (p : Choice) : Int := p.1 + p.2

/-- A monotone scan chooses one integer for each shift and charges each
    skipped integer to one entry of the forbidden weight list. -/
theorem scan (start : Int) (shifts holes : List Int) (sorted : shifts.Pairwise (· ≤ ·)) :
    ∃ out : List Choice, out.map Prod.snd = shifts ∧
      out.Pairwise (fun p q => p.1 < q.1) ∧
      out.Pairwise (fun p q => weight p < weight q) ∧
      ∀ p ∈ out, start ≤ p.1 ∧ p.1 < start + shifts.length + holes.length ∧
        weight p ∉ holes := by
  cases shifts with
  | nil => exact ⟨[], by simp⟩
  | cons s ss =>
    obtain ⟨hmin, hss⟩ := List.pairwise_cons.mp sorted
    by_cases blocked : start + s ∈ holes
    · obtain ⟨out, eq, increasing, rainbow, bounds⟩ :=
        scan (start+1) (s::ss) (holes.erase (start+s)) sorted
      refine ⟨out, eq, increasing, rainbow, ?_⟩
      intro p hp
      obtain ⟨lo,hi,avoids⟩ := bounds p hp
      have member : p.2 ∈ s :: ss := eq ▸ List.mem_map_of_mem hp
      have hs : s ≤ p.2 := by
        rcases List.mem_cons.mp member with heq | hm
        · omega
        · exact hmin _ hm
      have ne : weight p ≠ start+s := by unfold weight; omega
      have len := List.length_erase_of_mem blocked
      have positive := List.length_pos_of_mem blocked
      refine ⟨by omega, by omega, ?_⟩
      exact fun h => avoids ((List.mem_erase_of_ne ne).mpr h)
    · obtain ⟨out, eq, increasing, rainbow, bounds⟩ := scan (start+1) ss holes hss
      have later (p : Choice) (hp : p ∈ out) : start < p.1 ∧ start+s < weight p := by
        have lo := (bounds p hp).1
        have hs := hmin p.2 (eq ▸ List.mem_map_of_mem hp)
        unfold weight
        omega
      refine ⟨(start,s)::out, by simp [eq], List.pairwise_cons.mpr ⟨?_, increasing⟩,
              List.pairwise_cons.mpr ⟨?_, rainbow⟩, ?_⟩
      · exact fun p hp => (later p hp).1
      · exact fun p hp => (later p hp).2
      · intro p hp
        rcases List.mem_cons.mp hp with rfl | hm
        · exact ⟨by simp, by simp; omega, blocked⟩
        · obtain ⟨lo,hi,avoids⟩ := bounds p hm
          exact ⟨by omega, by simp; omega, avoids⟩
termination_by shifts.length + holes.length
decreasing_by
  all_goals subst shifts
  · have len := List.length_erase_of_mem blocked
    have positive := List.length_pos_of_mem blocked
    omega
  · simp

/-- Uniform edge interval for the two scans and the already labeled core. -/
theorem common_window (H A B threshold spare a b l u x s w : Int)
    (left : threshold = A+a) (budget : a+b ≤ spare)
    (anchors : B < A+H+spare) (hl : 0 ≤ l) (hu : 0 ≤ u)
    (origin :
      (A ≤ w ∧ w ≤ B) ∨
      (-l-a ≤ x ∧ threshold ≤ s ∧ x+s ≤ B ∧ w = x+s) ∨
      (x < H+u+b ∧ s < threshold ∧ A ≤ x+s ∧ w = x+s)) :
    A-l ≤ w ∧ w < A+H+u+spare := by
  rcases origin with old | lower | upper <;> omega

end Cordial.LeafIntervals
