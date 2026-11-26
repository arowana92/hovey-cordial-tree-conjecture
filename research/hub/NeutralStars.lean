import Std

namespace Cordial.NeutralStars

/-- The two root edges from p and the two child edges from u and -2p-u.
    The two children may lie in different rooted stars. -/
theorem progression (p x u : Int) :
    [p+x, p+(x+p), u+(x+2*p), (-2*p-u)+(x+2*p+u)].Perm
      [x, x+p, x+2*p, x+2*p+u] := by
  have h : [p+x, p+(x+p), u+(x+2*p), (-2*p-u)+(x+2*p+u)] =
      [x+p, x+2*p, x+2*p+u, x] := by
    simp only [List.cons.injEq, and_true]
    omega
  rw [h, List.perm_iff_count]
  intro z
  simp only [List.count_cons, List.count_nil]
  omega

theorem oppositeChildren (z b : Int) :
    [z+b, -z+(b+z)].Perm [b, b+z] := by
  have h : [z+b, -z+(b+z)] = [b+z, b] := by
    simp only [List.cons.injEq, and_true]
    omega
  rw [h]
  exact List.Perm.swap _ _ []

end Cordial.NeutralStars
