// A bounded search with the missing weight determined before completing leaves.
// Link the earlier exhaustive solver under the name reference_witness for fallback.
#include <algorithm>
#include <cstdint>
#include <numeric>

namespace {
using Mask = std::uint32_t;
constexpr int capacity = 30;

struct Shape {
    int n = 0, internal = 0;
    int parents[capacity], order[capacity], children[capacity];

    void prepare(int k, const int* input) {
        bool same = n == k-1;
        for (int i = 0; same && i < k-1; ++i) same = parents[i] == std::max(-1,input[i]);
        if (same) return;
        n = k-1;
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

struct Solver {
    int k;
    const Shape& shape;
    const int* parents;
    int* labels;
    Mask all;
    int budget;
    std::uint32_t state;
    int leaf_at[capacity][capacity], leaf_count[capacity];

    Mask right(Mask v, int a) const { return ((v>>a)|(v<<(k-a)))&all; }
    Mask left(Mask v, int a) const { return ((v<<a)|(v>>(k-a)))&all; }
    int add(int x, int y) const { int s = x+y; return s < k ? s : s-k; }
    int neg(int x) const { return x ? k-x : 0; }
    int parent_label(int i) const { return parents[i] < 0 ? -1-parents[i] : labels[parents[i]]; }
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
                int i = __builtin_ctz(open);
                Mask choices = (pass ? left(negatives,i) : right(weights,i)) & parent_digits;
                int count = __builtin_popcount(choices);
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
            int a = __builtin_ctz(options);
            int x = weight_first ? add(slot,neg(a)) : slot;
            int y = add(x,a);
            int leaf = leaf_at[a][--leaf_count[a]];
            Mask active = leaf_count[a] ? parent_digits : parent_digits^(1U<<a);
            if (fill(vertices^(1U<<x),negatives^(1U<<neg(x)),weights^(1U<<y),active)) {
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
            int absent = neg(parent_sum%k);
            if (!(weights & (1U<<absent))) return false;
            Mask digits = 0;
            std::fill_n(leaf_count,k,0);
            for (int j = shape.internal; j < shape.n; ++j) {
                int i = shape.order[j], a = parent_label(i);
                digits |= 1U<<a;
                leaf_at[a][leaf_count[a]++] = i;
            }
            return fill(vertices,negatives,weights^(1U<<absent),digits);
        }
        int i = shape.order[step], a = parent_label(i);
        Mask options = vertices & right(weights,a);
        if (!options) return false;
        Mask below = (1U<<(random()%k))-1;
        for (Mask choices : {options & ~below, options & below}) {
            for (; choices; choices &= choices-1) {
                int x = __builtin_ctz(choices);
                labels[i] = x;
                if (visit(step+1,vertices^(1U<<x),negatives^(1U<<neg(x)),weights^(1U<<add(x,a)),
                          parent_sum+shape.children[i]*x)) return true;
                if (budget < 0) return false;
            }
        }
        return false;
    }
};
}

extern "C" int reference_witness(int, const int*, int*);
extern "C" int rainbow_witness(int k, const int* parents, int* output) {
    if (k < 2 || k > capacity) return -1;
    for (int i = 0; i < k-1; ++i) if (parents[i] >= i || parents[i] < -k) return -1;
    thread_local Shape shape;
    shape.prepare(k,parents);
    Mask all = (1U<<k)-1;
    std::uint32_t seed = 1991;
    int boundary = 0;
    for (int i = 0; i < k-1; ++i) {
        seed = seed*16777619U+static_cast<std::uint32_t>(parents[i]);
        if (parents[i] < 0) boundary += -1-parents[i];
    }
    Solver search{k,shape,parents,output,all,0,seed|1U};
    for (int trial = 0; trial < 40; ++trial) {
        search.budget = trial < 8 ? 80 : trial < 20 ? 500 : 5000;
        if (search.visit(0,all^1,all^1,all,boundary)) return 1;
        if (search.budget >= 0) break;
    }
    return reference_witness(k,parents,output);
}
