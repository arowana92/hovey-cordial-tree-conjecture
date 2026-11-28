// Test every projected low-edge support and look for an obstructing low-vertex set.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

using Mask = std::uint64_t;
struct Motion {
    Mask vertices, edges, bridge;
};

class Quotient {
    int m;
    Mask all;
    std::vector<int> units;

    Mask bit(int x) const { return Mask(1) << (x % m); }
    Mask shift(Mask x, int d) const {
        d %= m;
        return ((x << d) & all) | (x >> (m-d));
    }
    Mask scale(Mask x, int u) const {
        Mask result = 0;
        while (x) {
            int i = __builtin_ctzll(x);
            result |= bit(i*u);
            x &= x-1;
        }
        return result;
    }

    void supports(int next, int left, Mask chosen, std::vector<Mask>& out) const {
        if (!left) {
            for (int u : units) if (scale(chosen,u) < chosen) return;
            out.push_back(chosen);
            return;
        }
        for (int i=next; i<=m-left; ++i) supports(i+1,left-1,chosen|bit(i),out);
    }

    std::vector<Motion> motions(int h, int b, int first_edge) const {
        std::vector<Motion> result;
        for (int u : units) {
            Mask v = 0, e = 0;
            for (int i=0; i<h; ++i) v |= bit(u*i);
            for (int j=0; j<=h; ++j) e |= bit(u*(first_edge+j));
            for (int d=0; d<m; ++d)
                result.push_back({shift(v,d),shift(e,2*d),bit(d+u*b)});
        }
        return result;
    }

    static bool hitting_set(const std::vector<Mask>& sets, Mask chosen, int left, size_t first) {
        for (size_t i=first; i<sets.size(); ++i) if (!(chosen & sets[i])) {
            if (!left) return false;
            for (Mask choices=sets[i]; choices; choices &= choices-1)
                if (hitting_set(sets,chosen|(choices & -choices),left-1,i+1)) return true;
            return false;
        }
        return true;
    }

public:
    explicit Quotient(int order) : m(order), all((Mask(1) << m)-1) {
        for (int u=1; u<m; ++u) if (std::gcd(u,m)==1) units.push_back(u);
    }

    std::uint64_t check(int a, int h) const {
        std::vector<Mask> core;
        for (int size=1; size<=a+1; ++size) supports(0,size,0,core);
        for (int b=0; b<m; ++b) for (int f=0; f<m; ++f) {
            auto moves = motions(h,b,f);
            for (Mask old : core) {
                std::vector<Mask> sets;
                Mask used = 0;
                int disjoint = 0;
                for (auto move : moves) {
                    if (old & move.edges & ~move.bridge) continue;
                    if (!((old | move.edges) & move.bridge)) continue;
                    sets.push_back(move.vertices);
                    if (!(used & move.vertices)) {
                        used |= move.vertices;
                        if (++disjoint > a) break;
                    }
                }
                if (disjoint <= a && hitting_set(sets,0,a,0))
                    throw std::runtime_error("a projected input admits no affine join");
            }
        }
        return std::uint64_t(m)*m*core.size();
    }
};

int main() {
    const std::vector<std::vector<int>> quotients = {
        {8,9,12}, {7,10,15,16,18,24,25,27}, {11,14,20,21,25,27,30,32,35,36,45,48,49}
    };
    for (int H=2; H<=4; ++H) {
        std::uint64_t total = 0;
        for (int m : quotients[H-2]) {
            Quotient check(m);
            for (int h=1; h<H; ++h) total += check.check(H-h,h);
        }
        std::cout << "total deficit=" << H << " projected profiles=" << total << std::endl;
    }
}
