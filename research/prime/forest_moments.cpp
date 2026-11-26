// Count directly on all free vertex labelings. Each input line is one forest
// on p-1 vertices. Negative parent indices encode boundary labels -1-parent.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Row = std::vector<int>;
using Mask = std::uint32_t;

struct Counter {
    int p;
    Mask full;
    Row parents, labels, sums;
    bool zero_boundary;

    void visit(int pos, Mask used, Mask weights, int sign) {
        if (pos == p - 1) {
            // Insert the missing weight before the tuple of observed weights.
            // There are exactly 'missing' smaller weights to its right.
            int missing = __builtin_ctz(full ^ weights);
            if (missing % 2) sign = -sign;
            sums[0] = (sums[0] + sign) % p;
            if (!zero_boundary)
                for (int i = 0; i < pos; ++i)
                    sums[1 + i] = (sums[1 + i] + sign * labels[i]) % p;
            return;
        }
        int parent = parents[pos];
        int boundary = parent < 0 ? -1 - parent : labels[parent];
        Mask candidates = zero_boundary && pos == 0 ? 2u : full ^ used;
        while (candidates) {
            int x = __builtin_ctz(candidates);
            Mask bit = Mask{1} << x;
            candidates ^= bit;
            int y = (x + boundary) % p;
            Mask weight_bit = Mask{1} << y;
            if (weights & weight_bit) continue;
            int inversions = __builtin_popcount(used >> (x + 1))
                           + __builtin_popcount(weights >> (y + 1));
            labels[pos] = x;
            visit(pos + 1, used | bit, weights | weight_bit,
                  inversions % 2 ? -sign : sign);
        }
    }

    void count() {
        zero_boundary = std::none_of(parents.begin(), parents.end(), [](int x) { return x < -1; });
        std::fill(sums.begin(), sums.end(), 0);
        visit(0, 1u, 0u, 1);
        // At zero boundary the first label was fixed to one. Dilations have
        // the same sign, and their first moments sum to zero for an odd prime.
        if (zero_boundary) sums[0] *= p - 1;
        for (int x : sums) std::cout << (x % p + p) % p << ' ';
        std::cout << std::endl;
    }
};

int main(int argc, char** argv) {
    if (argc != 2) throw std::runtime_error("expected an odd prime below 31");
    int p = std::stoi(argv[1]);
    if (p < 3 || p >= 31 || p % 2 == 0) throw std::runtime_error("invalid prime");
    for (int d = 3; d * d <= p; d += 2)
        if (p % d == 0) throw std::runtime_error("invalid prime");
    Counter counter{p, (Mask{1} << p) - 1, Row(p - 1), Row(p - 1), Row(p), false};
    while (std::cin >> counter.parents[0]) {
        for (int i = 0; i < p - 1; ++i) {
            if (i && !(std::cin >> counter.parents[i])) throw std::runtime_error("short input");
            int parent = counter.parents[i];
            if (parent < -p || parent >= i) throw std::runtime_error("invalid parent");
        }
        counter.count();
    }
}
