import Std

namespace RestrictedValue

def factor (a b c d : Fin 5) : Int :=
  (1 + ((a : Int) - (b : Int)) * ((c : Int) - (d : Int)) ^ 3) % 5

def test (a b c d : Fin 5) : Bool :=
  a == b || a == c || a == d || b == c || b == d || c == d ||
    (factor a c b d * factor a b c d * factor a b d c) % 5 == 0

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
private theorem table :
    (List.finRange 5).all (fun a => (List.finRange 5).all (fun b =>
      (List.finRange 5).all (fun c => (List.finRange 5).all (test a b c)))) = true := by
  decide

theorem emptyNonzeroImage (a b c d : Fin 5)
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    (factor a c b d * factor a b c d * factor a b d c) % 5 = 0 := by
  have ha := List.all_eq_true.mp table a (List.mem_finRange a)
  have hb := List.all_eq_true.mp ha b (List.mem_finRange b)
  have hc := List.all_eq_true.mp hb c (List.mem_finRange c)
  have hd := List.all_eq_true.mp hc d (List.mem_finRange d)
  simpa [test, hab, hac, had, hbc, hbd, hcd] using hd

end RestrictedValue
