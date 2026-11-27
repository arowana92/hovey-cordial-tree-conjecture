// Word order agrees with the unrestricted one- and two-centroid census.
#pragma once
#include "../rainbow/tip_forests.hpp"
#include <iterator>

class LeafCentroids {
    using Word = std::uint64_t;
    using Layer = std::vector<std::vector<Word>>;
    int n, limit;
    std::vector<Layer> allowed;

    static int leaves(Word code) { return __builtin_popcountll(code & ~(code << 1)); }

    template<class Emit>
    void centered(int left, int budget, int least, Word bound, Word prefix, const Emit& emit) const {
        if (left == 0) {
            emit((Word(1) << (2*n-1)) | (prefix << 1));
            return;
        }
        if (budget == 0) return;
        int cap = (n-1)/2;
        auto attach = [&](int size) {
            const auto& words = allowed[size][budget];
            auto start = size == least ? std::lower_bound(words.begin(),words.end(),bound) : words.begin();
            for (auto it = start; it != words.end(); ++it)
                centered(left-size, budget-leaves(*it), size, *it, (prefix << (2*size)) | *it, emit);
        };
        if (budget > 1)
            for (int size=least; size <= std::min(cap,left/2); ++size) attach(size);
        if (least <= left && left <= cap) attach(left);
    }
public:
    LeafCentroids(int order, int max_leaves):
        n(order), limit(max_leaves), allowed(n/2+1,Layer(limit+1)) {
        TipForests catalog(n/2,limit);
        for (int s=1; s<=n/2; ++s) {
            for (int t=1; t<=limit; ++t) {
                const auto& prev = allowed[s][t-1];
                const auto& more = catalog.branches(s,t);
                auto& layer = allowed[s][t];
                layer.reserve(prev.size()+more.size());
                std::merge(prev.begin(),prev.end(),more.begin(),more.end(),std::back_inserter(layer));
            }
        }
    }
    template<class Emit>
    void each(const Emit& emit) const {
        centered(n-1,limit,1,0,0,emit);
        if (n%2) return;
        for (Word first : allowed[n/2][limit]) {
            const auto& seconds = allowed[n/2][limit-leaves(first)];
            for (auto it=std::lower_bound(seconds.begin(),seconds.end(),first); it!=seconds.end(); ++it)
                emit(((first >> 1) << (n+1)) | (*it << 1));
        }
    }
};
