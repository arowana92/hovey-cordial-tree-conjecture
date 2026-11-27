// Cover all two-parent attachments of two unbranched matched arms and their exposed tips.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using Mask = std::uint32_t;
constexpr int n = 26;
constexpr Mask all=(1U<<n)-1;
int orbit_bit(int x) {
    x = (x%n+n)%n;
    if (x==0) return 8;
    if (x==13) return 4;
    return x%2==0 ? 2 : 1;
}
struct Solver {
    std::vector<int> parent,order,degree;
    std::array<int,n> label{};
    int second_root, budget, difference_orbits=0, deficit_orbits=0;
    Mask seed;
    Mask random() {
        seed ^= seed<<13;
        seed ^= seed>>17;
        return seed ^= seed<<5;
    }
    Solver(int split, int pattern):seed(1+2*(split*4096+pattern)) {
        for (int arm=0; arm<2; ++arm) {
            int prev=-1;
            if (arm) second_root=parent.size();
            int first = arm ? split : 0;
            int last = arm ? 12 : split;
            for (int i=first; i<last; ++i) {
                int a=parent.size();
                parent.push_back(prev);
                parent.push_back(a);
                prev=a+((pattern>>i)&1);
            }
            parent.push_back(prev);
        }
        degree.resize(n,0);
        for (int v=0; v<n; ++v) if (parent[v]>=0) {
            ++degree[v]; ++degree[parent[v]];
        }
        order.push_back(0);
        for (int v=1; v<n; ++v) if (degree[v]>1 || v==second_root) order.push_back(v);
        for (int v=1; v<n; ++v) if (degree[v]<=1 && v!=second_root) order.push_back(v);
    }
    bool place(int i,Mask unused,Mask weights) {
        if (--budget<0) return false;
        if (i==n) {
            int u=__builtin_ctz(weights),v=__builtin_ctz(weights&(weights-1));
            int a=label[0], b=label[second_root];
            int moves=orbit_bit(u-v-a+b)|orbit_bit(v-u-a+b);
            int fills=orbit_bit(u-a-b)|orbit_bit(v-a-b);
            if ((moves&~difference_orbits) || (fills&~deficit_orbits)) {
                difference_orbits|=moves; deficit_orbits|=fills;
                return true;
            }
            return false;
        }
        int v=order[i], p=parent[v];
        int a=p>=0 ? label[p] : 0;
        Mask possible=p<0 ? unused : unused & ((weights>>a)|(weights<<(n-a)));
        Mask cut=(1U<<(random()%n))-1;
        for (Mask set : {possible&~cut,possible&cut}) for(;set;set&=set-1) {
            int x=__builtin_ctz(set);
            label[v]=x;
            Mask remaining = weights;
            if (p>=0) remaining ^= 1U<<((a+x)%n);
            if (place(i+1,unused^(1U<<x),remaining)) return true;
            if (budget<0) return false;
        }
        return false;
    }
    bool run(int split,int pattern) {
        std::cout << split << ' ' << pattern;
        for (int t=0; t<600 && difference_orbits!=15 && deficit_orbits!=15; ++t) {
            budget=2000;
            if (place(1,all-1,all)) {
                std::cout << ' ';
                for (int x:label) std::cout << char('A'+x);
            }
        }
        std::cout << '\n';
        return difference_orbits==15 || deficit_orbits==15;
    }
};
int main() {
    for (int split=0; split<=6; ++split) {
        for (int pattern=0; pattern<4096; ++pattern) {
            Solver search(split,pattern);
            if (!search.run(split,pattern)) {
                std::cerr << "uncovered arms " << split << ' ' << pattern << '\n';
                return 1;
            }
        }
    }
}
