// Independent small-template signed sums by propagation of endpoint equations.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

namespace {
constexpr int capacity = 10;
struct Equation {
    std::array<int,capacity> coefficient{};
    int target = 0;
};
struct Template {
    int p, n, mode;
    std::vector<int> parent, bias, moving, labels, inverse, witness;
    std::vector<Equation> equations;
    std::vector<std::int64_t> moments;

    int mod(int a) const { return (a%p+p)%p; }

    // Propagate when only one variable in an equation is unassigned.
    // Otherwise branch on a variable in a shortest unfinished equation.
    void assign(std::uint64_t used, int remaining, int sign) {
        if (mode && !witness.empty()) return;
        int best = n+1, next = -1, forced = -1;
        for (const auto& eq : equations) {
            int rhs = eq.target, unknown = 0, last = -1;
            for (int i = 0; i < n; ++i) if (eq.coefficient[i]) {
                if (labels[i] < 0) { ++unknown; last = i; }
                else rhs -= eq.coefficient[i]*labels[i];
            }
            if (!unknown) {
                if (mod(rhs)) return;
            } else if (unknown < best) {
                best = unknown;
                next = last;
                if (unknown == 1) forced = mod(rhs*inverse[mod(eq.coefficient[last])]);
            }
        }
        if (!remaining) {
            moments[0] += sign;
            for (int i = 0; i < n; ++i) moments[i+1] += sign*labels[i];
            if (witness.empty()) witness = labels;
            return;
        }
        if (next < 0) next = std::find(labels.begin(),labels.end(),-1)-labels.begin();
        std::uint64_t choices = (std::uint64_t(1)<<p)-1;
        if (forced >= 0) choices = std::uint64_t(1)<<forced;
        for (choices &= ~used; choices; choices &= choices-1) {
            int x = __builtin_ctzll(choices);
            labels[next] = x;
            assign(used|(std::uint64_t(1)<<x),remaining-1,sign);
            if (mode && !witness.empty()) break;
        }
        labels[next] = -1;
    }

    void run() {
        inverse.resize(p);
        for (int a = 1; a < p; ++a)
            for (int x = 1; x < p; ++x) if (a*x%p == 1) inverse[a] = x;
        moving = {-1};
        for (int i = 0; i < n; ++i) if (parent[i] >= 0 || bias[i]) moving.push_back(i);
        labels.assign(n,-1);
        moments.assign(n+1,0);
        std::vector<int> perm(moving.size());
        std::iota(perm.begin(),perm.end(),0);
        do {
            equations.clear();
            unsigned seen = 0;
            int cycles = 0;
            for (unsigned i = 0; i < perm.size(); ++i) {
                if (!(seen&(1U<<i))) {
                    ++cycles;
                    for (int j = i; !(seen&(1U<<j)); j = perm[j]) seen |= 1U<<j;
                }
                if (!i) continue;
                int v = moving[i], dest = moving[perm[i]];
                Equation eq;
                ++eq.coefficient[v];
                if (parent[v] >= 0) ++eq.coefficient[parent[v]];
                if (dest >= 0) --eq.coefficient[dest];
                eq.target = -bias[v];
                equations.push_back(eq);
            }
            assign(1,n,(perm.size()-cycles)%2 ? -1 : 1);
            if (mode && !witness.empty()) return;
        } while (std::next_permutation(perm.begin(),perm.end()));
    }
};
}

int main() {
    int p,n,mode;
    while (std::cin >> p >> n >> mode) {
        if (p < 3 || p >= 64 || n <= 0 || n > capacity || n >= p || (mode != 0 && mode != 1))
            throw std::runtime_error("invalid input size or mode");
        for (int d = 2; d*d <= p; ++d) if (!(p%d)) throw std::runtime_error("expected a prime");
        Template t{p,n,mode};
        t.parent.resize(n);
        t.bias.resize(n);
        for (int i = 0; i < n; ++i)
            if (!(std::cin >> t.parent[i]) || t.parent[i] < -1 || t.parent[i] >= i)
                throw std::runtime_error("invalid parent");
        for (int& b : t.bias)
            if (!(std::cin >> b) || b < 0 || b >= p) throw std::runtime_error("invalid bias");
        t.run();
        for (auto a : t.moments) std::cout << (a%p+p)%p << ' ';
        std::cout << '|';
        for (int x : t.witness) std::cout << ' ' << x;
        std::cout << std::endl;
    }
}
