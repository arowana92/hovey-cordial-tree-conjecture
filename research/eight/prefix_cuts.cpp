// Certify the two consecutive blocks used in the eight- and nine-label prefix theorem.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;
using Sequence = std::array<int,20>;
Mask bit(int i) { return Mask(1)<<i; }

// Coefficients of R = x product_{j>=1} (1-x^j)^(-R_j), via logarithmic derivative.
long long rooted_count(int order) {
    std::vector<long long> count(order+1);
    count[1]=1;
    for (int n=2; n<=order; ++n) {
        long long total=0;
        for (int j=1; j<n; ++j) for (int d=1; d<=j; ++d)
            if (j%d==0) total+=d*count[d]*count[n-j];
        if (total%(n-1)) throw std::logic_error("rooted tree recurrence");
        count[n]=total/(n-1);
    }
    return count[order];
}

struct Cuts {
    int k,n,first;
    Sequence parent{};
    std::array<Mask,20> children{};
    Mask all;

    void read(const Sequence& level) {
        children.fill(0);
        Sequence previous{},end{};
        for (int i=1; i<=n; ++i) {
            if (level[i]<1 || level[i]>level[i-1]+1) throw std::logic_error("invalid depth");
            parent[i]=previous[level[i]-1];
            previous[level[i]]=i;
            children[parent[i]]|=bit(i);
            end[i]=i+1;
            while (end[i]<=n && level[end[i]]>level[i]) ++end[i];
        }
        // Siblings occur in descending lexicographic order of their level
        // subsequences. This makes the encoding injective on unlabelled trees.
        for (int i=1; i<=n; ++i) {
            int sibling=end[i];
            if (sibling<=n && level[sibling]==level[i] &&
                std::lexicographical_compare(level.begin()+i,level.begin()+end[i],
                                             level.begin()+sibling,level.begin()+end[sibling]))
                throw std::logic_error("noncanonical sibling order");
        }
    }
    bool ordinary_shape(Mask group,int size) const {
        if (size!=k && size!=k-1) return true;
        int roots=0, count=0;
        Mask centers=0;
        for (Mask m=group; m; m&=m-1) {
            int v=__builtin_ctz(m);
            if (!(group & bit(parent[v]))) ++roots;
            Mask descendants=children[v]&group;
            if (descendants) {
                centers|=bit(v);
                count=__builtin_popcount(descendants);
            }
        }
        if (size==k-1)
            return __builtin_popcount(centers)!=1 || (k==8 ? count%2==0 : count!=2 && count!=5);
        if (roots!=2 || __builtin_popcount(centers)!=2) return true;
        for (Mask m=centers; m; m&=m-1)
            if (group & bit(parent[__builtin_ctz(m)])) return true;
        return k==8 ? count%2==0 : count!=2 && count!=5;
    }
    bool admissible(Mask ideal) const {
        return ordinary_shape(ideal,first) && ordinary_shape(all^ideal,n-first);
    }
    bool search(int i,int needed,Mask ideal) const {
        if (needed==0) return admissible(ideal);
        if (n+1-i<needed) return false;
        if ((parent[i]==0 || (ideal&bit(parent[i]))) &&
            search(i+1,needed-1,ideal|bit(i))) return true;
        return search(i+1,needed,ideal);
    }
    bool exceptional_stem() const {
        if (n-first!=k) return false;
        for (int i=1; i<=first; ++i) {
            if (parent[i]!=i-1) return false;
            if (__builtin_popcount(children[i])!=(i==first ? 2 : 1)) return false;
        }
        if (__builtin_popcount(children[0])!=1) return false;
        Mask rest=all^(bit(first+1)-2);
        return !ordinary_shape(rest,k);
    }
    void verify() {
        Sequence level{};
        for (int i=0; i<=n; ++i) level[i]=i;
        all=bit(n+1)-2;
        long long total=0, alternatives=0, stems=0;
        while (true) {
            read(level);
            ++total;
            if (!admissible(bit(first+1)-2)) {
                ++alternatives;
                if (!search(1,first,0)) {
                    if (!exceptional_stem()) throw std::logic_error("uncovered forest");
                    ++stems;
                }
            }
            int p=n;
            while (p && level[p]==1) --p;
            if (!p) break;
            int q=p-1;
            while (level[q]!=level[p]-1) --q;
            auto before=level;
            for (int i=p; i<=n; ++i) level[i]=level[i-p+q];
            if (!(level<before)) throw std::logic_error("duplicate or unordered shape");
        }
        if (total!=rooted_count(n+1)) throw std::logic_error("incomplete forest catalog");
        std::cout<<k<<' '<<n<<' '<<first<<" forests "<<total<<" alternate cuts "
                 <<alternatives<<" stem exceptions "<<stems<<std::endl;
    }
};
int main() {
    for (int k : {8,9}) for (int n : {k+1,2*k-1,2*k})
        Cuts{k,n,n==2*k-1 ? k-1 : k}.verify();
}
