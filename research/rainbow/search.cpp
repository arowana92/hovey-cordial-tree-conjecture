// Optional native search for rainbow witnesses. Input and output vertex indices
// have the parent-vector order used in the JSON certificates.
#include <algorithm>
#include <array>
#include <cstdint>

namespace {
constexpr int capacity = 63;
using Mask = std::uint64_t;

struct Search {
    int k;
    int n;
    const int* parents;
    int* labels;
    Mask all;
    std::array<int, capacity> order{};
    std::array<int, capacity> size{};

    Mask candidates(Mask vertices, Mask weights, int shift) const {
        const Mask rotated = (weights >> shift) | ((weights << (k - shift)) & all);
        return vertices & rotated;
    }

    bool assign(int step, Mask vertices, Mask weights) {
        if (step == n) return true;
        const int i = order[step];
        const int p = parents[i];
        const int boundary = p < 0 ? -p - 1 : labels[p];
        Mask options = candidates(vertices, weights, boundary);
        if (size[i] == 1) {
            // Leaves with equal parent labels can exchange their vertex labels.
            // Require increasing labels within each such class.
            int needed = 1;
            for (int j = step + 1; j < n; ++j) {
                const int q = parents[order[j]];
                if ((q < 0 ? -q - 1 : labels[q]) == boundary) ++needed;
            }
            for (int j = step - 1; j >= 0 && size[order[j]] == 1; --j) {
                const int earlier = order[j];
                const int q = parents[earlier];
                if ((q < 0 ? -q - 1 : labels[q]) == boundary) {
                    options &= ~((Mask(1) << (labels[earlier] + 1)) - 1);
                    break;
                }
            }
            if (__builtin_popcountll(options) < needed) return false;
        }
        while (options) {
            const Mask bit = options & -options;
            options ^= bit;
            const int value = __builtin_ctzll(bit);
            labels[i] = value;
            const int weight = (boundary + value) % k;
            if (assign(step + 1, vertices ^ bit, weights ^ (Mask(1) << weight)))
                return true;
        }
        return false;
    }
};
}

// parents and output have k-1 entries. Negative parents encode -1-boundary.
// Return 1 with a witness, 0 after exhaustive search, or -1 on invalid input.
extern "C" int rainbow_witness(int k, const int* parents, int* output) {
    if (k < 2 || k > capacity) return -1;
    const Mask all = (Mask(1) << k) - 1;
    Search search{k, k - 1, parents, output, all};
    search.size.fill(1);
    for (int i = k - 2; i >= 0; --i) {
        const int p = parents[i];
        if (p >= i || p < -k) return -1;
        search.order[i] = i;
        if (p >= 0) search.size[p] += search.size[i];
    }
    std::stable_sort(search.order.begin(), search.order.begin() + k - 1,
                     [&](int a, int b) { return search.size[a] > search.size[b]; });
    return search.assign(0, all ^ 1, all) ? 1 : 0;
}
