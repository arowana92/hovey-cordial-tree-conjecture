import research.Reduction

namespace Cordial

/-- A singleton or two disjoint rooted trees joined by an edge between their roots.
    The root of the first tree stays the root of the result. -/
inductive GraftTree where
  | vertex : GraftTree
  | graft : GraftTree → GraftTree → GraftTree

namespace GraftTree

def order : GraftTree → Nat
  | vertex => 1
  | graft left right => order left + order right

theorem positive (t : GraftTree) : 0 < t.order := by
  induction t with
  | vertex => decide
  | graft l r hl hr => simp only [order]; omega

/-- Vertices of the right copy have their indices shifted by the left order.
    The first endpoint is the child, the second its actual neighbor. -/
def edges : GraftTree → List (Nat × Nat)
  | vertex => []
  | graft l r => l.edges ++ [(l.order,0)] ++
      r.edges.map (fun e => (l.order+e.1,l.order+e.2))

private theorem children (t : GraftTree) :
    t.edges.map Prod.fst = List.range' 1 (t.order-1) := by
  induction t with
  | vertex => rfl
  | graft l r hl hr =>
    have h₁ := positive l
    have h₂ := positive r
    have shift : r.edges.map (fun e => l.order+e.1) = List.range' (l.order+1) (r.order-1) := by
      rw [← List.map_add_range', ← hr, List.map_map]
      rfl
    simp only [edges, List.map_append, List.map_cons, List.map_nil, List.map_map, order]
    change l.edges.map Prod.fst ++ [l.order] ++ r.edges.map (fun e => l.order+e.1) = _
    rw [hl, shift]
    have head : List.range' 1 (l.order-1) ++ [l.order] = List.range' 1 l.order := by
      have h := @List.range'_append_1 1 (l.order-1) 1
      simpa [show 1+(l.order-1)=l.order by omega,
        show l.order-1+1=l.order by omega] using h
    rw [head, Nat.add_comm l.order 1, List.range'_append_1]
    congr 1
    omega

private theorem parentLess (t : GraftTree) (e : Nat × Nat) (he : e ∈ t.edges) : e.2 < e.1 := by
  induction t generalizing e with
  | vertex => simp [edges] at he
  | graft l r hl hr =>
    simp only [edges, List.mem_append, List.mem_singleton, List.mem_map] at he
    rcases he with (old|rfl)|⟨x,hx,rfl⟩
    · exact hl e old
    · exact positive l
    · exact Nat.add_lt_add_left (hr x hx) _

private theorem countTally {k : Nat} (g : Nat → Fin k) (n : Nat) (a : Fin k) :
    ((List.range n).map g).count a = tally g 0 n a := by
  induction n with
  | zero => simp [tally]
  | succ n ih =>
    by_cases h : g n = a <;> simp [tally,List.range_succ,List.count_append,h,ih]

/-- Transfer a theorem about parent arrays to the actual edge list of every
    recursively built tree. Vertex and edge frequency functions count all residues. -/
theorem ofParentArrays {k : Nat}
    (all : ∀ (p : Nat → Nat), (∀ i, p i ≤ i) → ∀ n, ∃ f : Nat → Fin k, IsCordial p n f)
    (t : GraftTree) : ∃ f : Nat → Fin k,
      Balanced (fun a => ((List.range t.order).map f).count a) ∧
      Balanced (fun a => (t.edges.map (fun e => f e.1+f e.2)).count a) := by
  let p := fun (i : Nat) => (t.edges[i]?.getD (0,0)).2
  have length : t.edges.length = t.order-1 := by
    simpa using congrArg List.length (children t)
  have child (i : Nat) (hi : i<t.edges.length) : t.edges[i].1=i+1 := by
    have h := congrArg (fun xs : List Nat => xs[i]?) (children t)
    have hr : i < (List.range' 1 (t.order-1)).length := by simpa [length] using hi
    simpa [List.getElem?_eq_getElem (by simpa using hi : i<(t.edges.map Prod.fst).length),
      List.getElem?_eq_getElem hr, Nat.add_comm] using h
  have bounded (i : Nat) : p i ≤ i := by
    by_cases hi : i<t.edges.length
    · have h := parentLess t t.edges[i] (List.getElem_mem hi)
      rw [child i hi] at h
      simpa [p,List.getElem?_eq_getElem hi] using Nat.le_of_lt_succ h
    · simp [p,List.getElem?_eq_none (by omega : t.edges.length ≤ i)]
  obtain ⟨f,hv,he⟩ := all p bounded t.order
  have ew : t.edges.map (fun e => f e.1+f e.2) = (List.range (t.order-1)).map (weight p f) := by
    apply List.ext_getElem
    · simp [length]
    · intro i hi hj
      have h : i<t.edges.length := by simpa using hi
      simp [weight,p,child i h,List.getElem?_eq_getElem h]
  exact ⟨f,by simpa only [countTally] using hv,by simpa only [ew,countTally] using he⟩

end GraftTree
end Cordial
