// Unrank canonical unordered rooted forests using only components of half order.
#pragma once
#include <algorithm>
#include <cstdint>
#include <stdexcept>
#include <vector>

class RankedForests {
    using Word = std::uint64_t;
    struct Tree { int size; Word word; };
    int half;
    std::vector<Tree> small;
    // ways[s][i] permits small types i,i+1,... and at most one larger tree.
    std::vector<std::vector<Word>> ways;

    template<class Emit>
    void small_forests(int s, std::size_t i, Word prefix, Emit& emit) {
        if (!s) { emit(prefix); return; }
        for (; i < small.size() && small[i].size <= s; ++i) {
            const auto t = small[i];
            small_forests(s-t.size,i,(prefix<<(2*t.size))|t.word,emit);
        }
    }

    Word decode(int s, std::size_t i, Word rank) const {
        if (!s) return 0;
        const auto& row = ways[s];
        Word total = row[i];
        if (rank >= total-row.back()) {
            // Only one component of size > half fits. Its children have no
            // inherited sibling restrictions, and are a forest of size s-1.
            auto children = decode(s-1,0,rank-(total-row.back()));
            return (Word(1)<<(2*s-1))|(children<<1);
        }
        // Block j has row[j]-row[j+1] completions. Skip entire blocks.
        auto end = std::upper_bound(row.begin()+i,row.end(),total-rank,
                                    [](Word target,Word count){ return target > count; });
        std::size_t j = (end-row.begin())-1;
        const auto t = small[j];
        return (t.word<<(2*(s-t.size)))|decode(s-t.size,j,rank-(total-row[j]));
    }
public:
    explicit RankedForests(int order, bool small_only = false): half(order/2), ways(order+1) {
        if (order < 1 || order > 30) throw std::invalid_argument("forest order");
        for (int size = 1; size <= half; ++size) {
            std::vector<Word> layer;
            auto add = [&](Word f){ layer.push_back((Word(1)<<(2*size-1))|(f<<1)); };
            small_forests(size-1,0,0,add);
            std::sort(layer.begin(),layer.end());
            for (auto code : layer) small.push_back({size,code});
        }
        ways[0].assign(small.size()+1,1);
        for (int s = 1; s <= order; ++s) {
            auto& row = ways[s];
            row.resize(small.size()+1);
            row.back() = !small_only && s > half ? ways[s-1][0] : 0;
            for (std::size_t i = small.size(); i-- > 0;) {
                row[i] = row[i+1];
                if (s >= small[i].size) row[i] += ways[s-small[i].size][i];
            }
        }
    }
    Word count() const { return ways.back()[0]; }
    Word operator[](Word rank) const {
        if (rank >= count()) throw std::out_of_range("forest rank");
        return decode(static_cast<int>(ways.size())-1,0,rank);
    }
};
