// Native search for rainbow witnesses. Vertex indices follow the input parent order.
#include <algorithm>
#include <array>
#include <cstdint>

namespace {
constexpr int capacity = 63;
using Mask = std::uint64_t;

struct Traversal {
    int n = 0;
    int first_leaf = 0;
    std::array<int, capacity> shape{}, order{};

    bool prepare(int k, const int* parents) {
        bool unchanged = n == k - 1;
        for (int i = 0; i < k - 1; ++i) {
            if (parents[i] >= i || parents[i] < -k) return false;
            if (std::max(-1, parents[i]) != shape[i]) unchanged = false;
        }
        if (unchanged) return true;

        n = k - 1;
        std::array<int, capacity> sizes;
        sizes.fill(1);
        for (int i = n - 1; i >= 0; --i) {
            shape[i] = std::max(-1, parents[i]);
            if (shape[i] >= 0) sizes[shape[i]] += sizes[i];
        }

        // Stable descending sort by subtree size. Every parent precedes its children.
        std::array<int, capacity + 1> starts{};
        for (int i = 0; i < n; ++i) ++starts[sizes[i]];
        int position = 0;
        for (int size = n; size >= 1; --size) {
            int count = starts[size];
            starts[size] = position;
            position += count;
        }
        first_leaf = starts[1];
        for (int i = 0; i < n; ++i) order[starts[sizes[i]]++] = i;
        return true;
    }
};

struct Search {
    int k;
    const Traversal& traversal;
    const int* parents;
    int* labels;
    Mask all;
    std::array<int, capacity> leaf_boundary, needed;
    std::array<Mask, capacity> allowed;

    int boundary(int i) const {
        return parents[i] < 0 ? -parents[i] - 1 : labels[parents[i]];
    }

    int weight(int a, int b) const {
        const int sum = a + b;
        return sum < k ? sum : sum - k;
    }

    Mask candidates(Mask vertices, Mask weights, int shift) const {
        return vertices & ((weights >> shift) | (weights << (k - shift)));
    }

    bool leaves(int step, Mask vertices, Mask weights) {
        if (!vertices) return true;
        const int i = traversal.order[step];
        const int parent_label = leaf_boundary[step];
        const Mask previous = allowed[parent_label];
        Mask options = candidates(vertices, weights, parent_label) & previous;
        if (__builtin_popcountll(options) < needed[step]) return false;
        while (options) {
            const Mask bit = options & -options;
            options ^= bit;
            const int value = __builtin_ctzll(bit);
            labels[i] = value;
            // Leaves at the same parent residue can exchange labels. Keep increasing order.
            allowed[parent_label] = ~((bit << 1) - 1);
            if (leaves(step + 1, vertices ^ bit, weights ^ (Mask(1) << weight(parent_label, value))))
                return true;
        }
        allowed[parent_label] = previous;
        return false;
    }

    bool assign(int step, Mask vertices, Mask weights) {
        if (step == traversal.first_leaf) {
            // Parent residues stay fixed throughout this leaf suffix.
            std::array<int, capacity> counts{};
            for (int j = traversal.n - 1; j >= step; --j) {
                const int parent_label = boundary(traversal.order[j]);
                leaf_boundary[j] = parent_label;
                needed[j] = ++counts[parent_label];
                allowed[parent_label] = all;
            }
            return leaves(step, vertices, weights);
        }
        const int i = traversal.order[step];
        const int parent_label = boundary(i);
        Mask options = candidates(vertices, weights, parent_label);
        while (options) {
            const Mask bit = options & -options;
            options ^= bit;
            const int value = __builtin_ctzll(bit);
            labels[i] = value;
            if (assign(step + 1, vertices ^ bit, weights ^ (Mask(1) << weight(parent_label, value))))
                return true;
        }
        return false;
    }
};
}

// Negative parents encode -1-boundary. Return 1 with a witness, 0 after
// exhaustive search, or -1 on invalid input. Both arrays have k-1 entries.
extern "C" int rainbow_witness(int k, const int* parents, int* output) {
    if (k < 2 || k > capacity) return -1;
    // Consecutive boundary colorings usually have the same forest.
    thread_local Traversal traversal;
    if (!traversal.prepare(k, parents)) return -1;
    const Mask all = (Mask(1) << k) - 1;
    Search search{k, traversal, parents, output, all};
    return search.assign(0, all ^ 1, all) ? 1 : 0;
}
