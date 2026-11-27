import Std

namespace Cordial.ThreeBranch

private theorem few {B C I J V : Nat} (bc : B ≤ C)
    (low : I*B+J*C+V < 2*B) : I+J ≤ 1 := by
  have hi := Nat.mul_le_mul_left J bc
  by_cases ok : I+J ≤ 1
  · exact ok
  exfalso
  have hj := Nat.mul_le_mul_right B (show 2 ≤ I+J by omega)
  rw [Nat.add_mul] at hj
  omega

/-- Remaining counts (2u,b,b+u). No path of cost 2b-2u uses costs b,b+u,3u. -/
theorem first {u b I J V : Nat} (hu : 3 ≤ u) (cop : u.Coprime b) :
    I*b + J*(b+u) + V*(3*u) + 2*u ≠ 2*b := by
  intro eq
  have one := few (B := b) (C := b+u) (I := I) (J := J) (V := V*(3*u))
      (by omega) (by omega)
  have rest : u ∣ V*(3*u) := Nat.dvd_trans (Nat.dvd_mul_left u 3) (Nat.dvd_mul_left _ V)
  by_cases zeros : I+J = 0
  · have hI : I=0 := by omega
    have hJ : J=0 := by omega
    simp [hI,hJ] at eq
    have dv : u ∣ 2*b := eq ▸ Nat.dvd_add rest (Nat.dvd_mul_left u 2)
    have d := Nat.le_of_dvd (by decide : 0 < 2) (cop.dvd_of_dvd_mul_right dv)
    omega
  · have dv : u ∣ b := by
      by_cases zi : I=0
      · have hJ : J=1 := by omega
        simp [zi,hJ] at eq
        have key : b = V*(3*u)+3*u := by omega
        rw [key]
        exact Nat.dvd_add rest (Nat.dvd_mul_left u 3)
      · have hI : I=1 := by omega
        have hJ : J=0 := by omega
        simp [hI,hJ] at eq
        have key : b = V*(3*u)+2*u := by omega
        rw [key]
        exact Nat.dvd_add rest (Nat.dvd_mul_left u 2)
    have := cop.eq_one_of_dvd dv
    omega

/-- Remaining counts (a,2a-3u,3a-4u). The required short cost is 4a-8u. -/
theorem second {a b c u I J V : Nat} (hu : 3 ≤ u) (ha : 3*u < a)
    (hb : b+3*u=2*a) (hc : c+4*u=3*a) (cop : (a+u).Coprime u) :
    I*b + J*c + V*(a+u) + 8*u ≠ 4*a := by
  intro eq
  have one := few (B := b) (C := c) (I := I) (J := J) (V := V*(a+u))
      (by omega) (by omega)
  have exclude : ∀ f n : Nat, 0 < f → f ≤ 12 → V*(a+u)+f*u=n*(a+u) → False := by
    intro f n pos bounded h
    have dv : (a+u) ∣ f*u := (Nat.dvd_add_iff_right (Nat.dvd_mul_left _ V)).mpr
        (h ▸ Nat.dvd_mul_left _ n)
    have := Nat.le_of_dvd pos (cop.dvd_of_dvd_mul_right dv)
    omega
  by_cases zi : I=0
  · by_cases zj : J=0
    · simp [zi,zj] at eq
      exact exclude 12 4 (by decide) (by decide) (by omega)
    · have hJ : J=1 := by omega
      simp [zi,hJ] at eq
      exact exclude 5 1 (by decide) (by decide) (by omega)
  · have hI : I=1 := by omega
    have hJ : J=0 := by omega
    simp [hI,hJ] at eq
    exact exclude 7 2 (by decide) (by decide) (by omega)

end Cordial.ThreeBranch
