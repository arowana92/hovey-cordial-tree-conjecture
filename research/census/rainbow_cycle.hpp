#pragma once
#include <algorithm>
#include <cstdint>
#include <random>
#include <vector>

namespace rainbow_cycle {
using Mask = std::uint64_t;

struct Search {
    int k;
    int budget = 0;
    int first = 0;
    std::mt19937 random;
    std::vector<int> path;

    Mask bit(int x) const { return Mask(1) << x; }

    bool extend(int last, Mask vertices, Mask weights) {
        if (--budget < 0) return false;
        if (!vertices) return weights == bit((first + last) % k);
        int choices[64];
        int count = 0;
        for (Mask remaining = vertices; remaining; remaining &= remaining - 1) {
            int x = __builtin_ctzll(remaining);
            if (weights & bit((last + x) % k)) choices[count++] = x;
        }
        for (int j = count - 1; j > 0; --j)
            std::swap(choices[j], choices[random() % (j + 1)]);
        for (int j = 0; j < count && budget > 0; ++j) {
            int x = choices[j];
            path.push_back(x);
            if (extend(x, vertices ^ bit(x), weights ^ bit((last + x) % k))) return true;
            path.pop_back();
        }
        return false;
    }

    bool cycle(Mask vertices, Mask weights, int steps) {
        first = __builtin_ctzll(vertices);
        budget = steps;
        path.assign(1, first);
        return extend(first, vertices ^ bit(first), weights);
    }
};
} // namespace rainbow_cycle
