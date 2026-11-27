// A bounded search with the missing weight determined before completing leaves.
// Link the earlier exhaustive solver under the name reference_witness for fallback.
#include <algorithm>
#include <cstdint>
#include <numeric>
#ifdef RAINBOW_WIDE_MASK
#include "swap_search.hpp"
#endif

namespace {
#ifdef RAINBOW_WIDE_MASK
using Mask = std::uint64_t;
constexpr int capacity = 63;
int first_bit(Mask x) { return __builtin_ctzll(x); }
int population(Mask x) { return __builtin_popcountll(x); }
#else
using Mask = std::uint32_t;
constexpr int capacity = 30;
int first_bit(Mask x) { return __builtin_ctz(x); }
int population(Mask x) { return __builtin_popcount(x); }
#endif

struct Shape {
    int n = 0, internal = 0;
    int parents[capacity], order[capacity], children[capacity];

    void prepare(int count, const int* input) {
        bool same = n == count;
        for (int i = 0; same && i < count; ++i) same = parents[i] == std::max(-1,input[i]);
        if (same) return;
        n = count;
        std::fill_n(children,n,0);
        std::iota(order,order+n,0);
        int size[capacity];
        std::fill_n(size,n,1);
        for (int i = n-1; i >= 0; --i) {
            parents[i] = std::max(-1,input[i]);
            if (input[i] >= 0) {
                ++children[input[i]];
                size[input[i]] += size[i];
            }
        }
        std::stable_sort(order,order+n,[&](int a,int b){ return size[a] > size[b]; });
        internal = 0;
        while (internal < n && children[order[internal]]) ++internal;
    }
};

template<bool shifted, bool uniform> struct Solver {
    int k;
    const Shape& shape;
    const int* parents;
    int* labels;
    Mask all;
    int budget;
    std::uint32_t state;
    const int* offsets;
    int leaf_at[capacity][capacity], leaf_count[capacity];

    Mask right(Mask v, int a) const { return ((v>>a)|(v<<(k-a)))&all; }
    Mask left(Mask v, int a) const { return ((v<<a)|(v>>(k-a)))&all; }
    int add(int x, int y) const { int s = x+y; return s < k ? s : s-k; }
    int neg(int x) const { return x ? k-x : 0; }
    int parent_label(int i) const {
        int value = parents[i] < 0 ? -1-parents[i] : labels[parents[i]];
        if constexpr (shifted) return add(value,offsets[i]);
        return value;
    }
    std::uint32_t random() {
        state ^= state << 13;
        state ^= state >> 17;
        state ^= state << 5;
        return state;
    }

    bool fill(Mask vertices, Mask negatives, Mask weights, Mask parent_digits) {
        if (!vertices) return true;
        if (--budget < 0) return false;
        Mask options = 0;
        int min_count = capacity+1, slot = 0;
        bool weight_first = false;
        for (int pass = 0; pass < 2; ++pass) {
            for (Mask open = pass ? weights : vertices; open; open &= open-1) {
                int i = first_bit(open);
                Mask choices = (pass ? left(negatives,i) : right(weights,i)) & parent_digits;
                int count = population(choices);
                if (!count) return false;
                if (count < min_count) {
                    min_count = count;
                    slot = i;
                    weight_first = pass;
                    options = choices;
                }
            }
        }
        for (; options; options &= options-1) {
            int a = first_bit(options);
            int x = weight_first ? add(slot,neg(a)) : slot;
            int y = add(x,a);
            int leaf = leaf_at[a][--leaf_count[a]];
            Mask active = leaf_count[a] ? parent_digits : parent_digits^(Mask(1)<<a);
            if (fill(vertices^(Mask(1)<<x),negatives^(Mask(1)<<neg(x)),weights^(Mask(1)<<y),active)) {
                labels[leaf] = x;
                return true;
            }
            ++leaf_count[a];
            if (budget < 0) return false;
        }
        return false;
    }

    bool visit(int step, Mask vertices, Mask negatives, Mask weights, int parent_sum) {
        if (--budget < 0) return false;
        if (step == shape.internal) {
            // The parent terms sum to zero when both histograms are permutations.
            if constexpr (uniform) {
                if (parent_sum%k != 0) return false;
            } else {
                int absent = neg(parent_sum%k);
                if (!(weights & (Mask(1)<<absent))) return false;
                weights ^= Mask(1)<<absent;
            }
            Mask digits = 0;
            std::fill_n(leaf_count,k,0);
            for (int j = shape.internal; j < shape.n; ++j) {
                int i = shape.order[j], a = parent_label(i);
                digits |= Mask(1)<<a;
                leaf_at[a][leaf_count[a]++] = i;
            }
            return fill(vertices,negatives,weights,digits);
        }
        int i = shape.order[step], a = parent_label(i);
        Mask options = vertices & right(weights,a);
        if (!options) return false;
        Mask below = (Mask(1)<<(random()%k))-1;
        for (Mask choices : {options & ~below, options & below}) {
            for (; choices; choices &= choices-1) {
                int x = first_bit(choices);
                labels[i] = x;
                if (visit(step+1,vertices^(Mask(1)<<x),negatives^(Mask(1)<<neg(x)),weights^(Mask(1)<<add(x,a)),
                          parent_sum+shape.children[i]*x)) return true;
                if (budget < 0) return false;
            }
        }
        return false;
    }
};
}

extern "C" int reference_witness(int, const int*, int*);
extern "C" int rainbow_offset_witness(int, const int*, const int*, int*);
template<bool shifted, bool uniform = false> static int search_forest(int k, const int* parents, int* output,
                                                const int* offsets) {
    if (k < 2 || k > capacity) return -1;
    int count = uniform ? k : k-1;
    for (int i = 0; i < count; ++i) if (parents[i] >= i || parents[i] < -k) return -1;
    thread_local Shape shape;
    shape.prepare(count,parents);
    Mask all = (Mask(1)<<k)-1;
    std::uint32_t seed = 1991;
    int boundary = 0;
    for (int i = 0; i < count; ++i) {
        seed = seed*16777619U+static_cast<std::uint32_t>(parents[i]);
        if (parents[i] < 0) boundary += -1-parents[i];
        if constexpr (shifted) {
            if (offsets[i] < 0 || offsets[i] >= k) return -1;
            boundary += offsets[i];
            seed = seed*16777619U+static_cast<std::uint32_t>(offsets[i]);
        }
    }
    Solver<shifted,uniform> search{k,shape,parents,output,all,0,seed|1U,offsets};
    Mask available = uniform ? all : all^1;
    for (int trial = 0; trial < 40; ++trial) {
        search.budget = trial < 8 ? 80 : trial < 20 ? 500 : 5000;
        if (search.visit(0,available,available,all,boundary)) return 1;
        if (search.budget >= 0) break;
    }
#ifdef RAINBOW_WIDE_MASK
    if constexpr (!shifted) {
        if ((k>=31 || uniform) && swap_search(k,parents,output,seed|1U,uniform)) return 1;
    }
#endif
    if constexpr (uniform) {
#ifdef RAINBOW_WIDE_MASK
        for (int retry = 0; retry < 32; ++retry) {
            seed = seed*1664525U+1013904223U;
            if (swap_search(k,parents,output,seed|1U,true)) return 1;
        }
#endif
        return 0;
    }
    else if constexpr (shifted) return rainbow_offset_witness(k,parents,offsets,output);
    else return reference_witness(k,parents,output);
}

extern "C" int rainbow_witness(int k, const int* parents, int* output) {
    return search_forest<false>(k,parents,output,nullptr);
}

extern "C" int fast_offset_witness(int k, const int* parents, const int* offsets, int* output) {
    return search_forest<true>(k,parents,output,offsets);
}

extern "C" int uniform_witness(int k, const int* parents, int* output) {
    return search_forest<false,true>(k,parents,output,nullptr);
}
