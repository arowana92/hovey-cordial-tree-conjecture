import Std

namespace Cordial.BatchTransfer

/-- Slopes of the seven arrivals from a parent of slope c, transferring X to
    a terminal of slope L. Earlier moving labels have slopes in [1,L). -/
def slopes (c L : Int) : List Int :=
  [L, -c-2*L, c+L, 1+L, -L, -c-L, c+1+2*L]

theorem separate (c L : Int) (hc : 1 < c) (hL : c < L) :
    (slopes c L).Nodup ∧ (∀ a ∈ slopes c L, a < 0 ∨ L ≤ a) := by
  constructor
  · simp [slopes, List.nodup_cons]
    omega
  · intro a h
    simp [slopes] at h
    omega

end Cordial.BatchTransfer
