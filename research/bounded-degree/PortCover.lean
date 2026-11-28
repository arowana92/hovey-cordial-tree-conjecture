import Std

namespace Cordial.PortCover

/-- Every m successive positions on a circle of length k contain a residue
    divisible by m, even when m does not divide k. -/
theorem hit (x k m : Nat) (hk : 0 < k) (hm : 0 < m) :
    ∃ i < m, ((x+i)%k)%m = 0 := by
  let a := x%k
  have ha : a < k := Nat.mod_lt x hk
  have hr : a%m < m := Nat.mod_lt a hm
  by_cases zero : a%m = 0
  · exact ⟨0, hm, by simpa [a] using zero⟩
  let i := m-a%m
  have hi : i < m := by dsimp [i]; omega
  by_cases inside : a+i < k
  · refine ⟨i, hi, ?_⟩
    rw [← Nat.mod_add_mod x k i]
    change ((a+i)%k)%m=0
    rw [Nat.mod_eq_of_lt inside, Nat.add_mod, Nat.mod_eq_of_lt hi]
    have eq : a%m+i=m := by dsimp [i]; omega
    rw [eq, Nat.mod_self]
  · refine ⟨k-a, by omega, ?_⟩
    rw [← Nat.mod_add_mod x k (k-a)]
    change ((a+(k-a))%k)%m=0
    have eq : a+(k-a)=k := by omega
    simp [eq]

private theorem different (x i j k : Nat) (order : i < j) (span : j-i < k) :
    (x+i)%k ≠ (x+j)%k := by
  have hk : 0 < k := by omega
  let a := (x+i)%k
  have ha : a < k := Nat.mod_lt _ hk
  have eq : x+j = x+i+(j-i) := by omega
  rw [eq, ← Nat.mod_add_mod (x+i) k (j-i)]
  change a ≠ (a+(j-i))%k
  by_cases inside : a+(j-i)<k
  · rw [Nat.mod_eq_of_lt inside]; omega
  · rw [Nat.mod_eq_sub_mod (by omega : k ≤ a+(j-i)),
        Nat.mod_eq_of_lt (by omega : a+(j-i)-k<k)]
    omega

/-- Two distinct elements of every length-2m cyclic interval lie in the grid.
    At most one of their labels can equal a prescribed deleted weight. -/
theorem twoHits (x k m : Nat) (hm : 0 < m) (room : m+m ≤ k) :
    ∃ i j, i < m ∧ m ≤ j ∧ j < m+m ∧
      ((x+i)%k)%m=0 ∧ ((x+j)%k)%m=0 ∧ (x+i)%k ≠ (x+j)%k := by
  have hk : 0<k := by omega
  obtain ⟨i,hi,first⟩ := hit x k m hk hm
  obtain ⟨d,hd,second⟩ := hit (x+m) k m hk hm
  exact ⟨i,m+d,hi,by omega,by omega,first,by simpa [Nat.add_assoc] using second,
    different x i (m+d) k (by omega) (by omega)⟩

end Cordial.PortCover
