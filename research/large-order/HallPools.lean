import Std

namespace HallPools

theorem twoMoments (a b : Int) :
    (b-a)+(2*a-b)=a ∧ 2*(b-a)+(2*a-b)=b := by omega

theorem evenSplit (f g prev : Int) (h : (f-g-prev)%2=0) :
    2*((f-g-prev)/2)+g+prev=f := by omega

theorem repairMoment (m : Int) (h : m%2=0) : -m+2*(m/2)=0 := by omega

theorem toggle (r0 r1 : Int) :
    ((1-r0)+(1-r1))%2=(r0+r1)%2 ∧ (1-r1)%2≠r1%2 := by omega

end HallPools
