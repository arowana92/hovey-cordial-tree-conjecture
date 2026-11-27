// Exhaustive independent affine gluing test. A bit represents a residue in Z/(2p).
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;
using Count = std::uint64_t;
using Profile = std::array<int, 3>;

Count choose(int n, int r) {
    Count result = 1;
    for (int i = 1; i <= r; ++i) result = result * (n - i + 1) / i;
    return result;
}

struct EdgeChange {
    Mask holes;
    Mask bridge;

    bool balanced(Mask low) const {
        if (holes & bridge) return !(low & (holes ^ bridge));
        return (low & bridge) && !(low & holes);
    }
};

std::map<Profile, int> profiles(int k, const std::vector<int>& units) {
    std::map<Profile, int> multiplicity;
    for (int b = 0; b < k; ++b) {
        for (int d = 0; d < k; ++d) {
            for (int e = d + 1; e < k; ++e) {
                Profile key{b, d, e};
                for (int u : units) {
                    int v = u*d % k, w = u*e % k;
                    key = std::min(key, Profile{u*b % k, std::min(v,w), std::max(v,w)});
                }
                ++multiplicity[key];
            }
        }
    }
    return multiplicity;
}

bool predicts_obstruction(Profile shape, int p, int loss, int doubling_order) {
    auto [b,d,e] = shape;
    if (d % p != e % p) return false;
    if (b % p == 0 && d % p == 0) return true;
    return d % p == 2*b % p && (loss == 1 || loss > doubling_order);
}

void audit(int p) {
    const int k = 2*p;
    const int max_loss = (p-5)/2;
    std::vector<int> units;
    for (int u = 1; u < k; ++u) if (std::gcd(k,u) == 1) units.push_back(u);
    int order = 1;
    for (int v = 2; v != 1; v = 2*v % p) ++order;
    const auto catalogue = profiles(k,units);
    std::vector<Count> cases(max_loss+1), blocked(max_loss+1), exceptional(max_loss+1);
    for (const auto& [shape, copies] : catalogue) {
        auto [b,d,e] = shape;
        std::vector<std::vector<EdgeChange>> choices(k);
        for (int x = 0; x < k; ++x) {
            for (int u : units) {
                Mask left = Mask(1) << ((2*x + u*d) % k);
                Mask right = Mask(1) << ((2*x + u*e) % k);
                Mask bridge = Mask(1) << ((x + u*b) % k);
                choices[x].push_back({left | right, bridge});
            }
        }
        for (int a = 1; a <= max_loss; ++a) {
            Count failures = 0, seen = 0;
            Mask low = (Mask(1) << (a+1)) - 1;
            while (low < (Mask(1) << k)) {
                int viable = 0;
                for (const auto& row : choices) {
                    if (std::any_of(row.begin(), row.end(),
                                    [low](EdgeChange change) { return change.balanced(low); })) {
                        if (++viable > a) break;
                    }
                }
                if (viable <= a) failures += choose(k-viable,a-viable);
                ++seen;
                // Next subset of the same cardinality in numeric order.
                Mask bit = low & -low, next = low + bit;
                low = next | (((next ^ low) >> 2) / bit);
            }
            if (seen != choose(k,a+1)) throw std::logic_error("incomplete edge enumeration");
            if ((failures != 0) != predicts_obstruction(shape,p,a,order))
                throw std::logic_error("classification disagrees with direct edge checks");
            cases[a] += seen * choose(k,a) * copies;
            blocked[a] += failures * copies;
            exceptional[a] += failures != 0;
        }
    }
    for (int a = 1; a <= max_loss; ++a) {
        const Count expected = k * choose(k,2) * choose(k,a) * choose(k,a+1);
        if (cases[a] != expected) throw std::logic_error("incomplete profile enumeration");
        std::cout << "k=" << k << " loss=" << a << " profile orbits=" << catalogue.size()
                  << " exceptional orbits=" << exceptional[a] << " inputs=" << cases[a]
                  << " blocked fixed inputs=" << blocked[a] << '\n';
    }
}

int main() {
    for (int p : {7, 11, 13}) audit(p);
}
