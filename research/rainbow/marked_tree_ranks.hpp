// Rank ordinary trees at a vertex centroid, or at their unordered centroid edge.
#pragma once
#include "ranked_forest.hpp"
#include <algorithm>
#include <cstdint>
#include <stdexcept>
#include <vector>

class MarkedTreeRanks {
    using Word = std::uint64_t;
    int n;
    RankedForests centered;
    std::vector<Word> half, first_pair;
public:
    explicit MarkedTreeRanks(int order): n(order), centered(n-1,true) {
        if (n%2) return;
        RankedForests children(n/2-1);
        for (Word j=0; j<children.count(); ++j)
            half.push_back((Word(1)<<(n-1))|(children[j]<<1));
        std::sort(half.begin(),half.end());
        Word start = centered.count();
        for (std::size_t i=0; i<half.size(); ++i) {
            first_pair.push_back(start);
            start += half.size()-i;
        }
        first_pair.push_back(start);
    }

    Word count() const { return n%2 ? centered.count() : first_pair.back(); }

    Word word(Word rank) const {
        if (rank<centered.count()) return (Word(1)<<(2*n-1))|(centered[rank]<<1);
        auto i = std::upper_bound(first_pair.begin(),first_pair.end(),rank)-first_pair.begin()-1;
        Word j = i+(rank-first_pair[i]);
        return ((half[i]>>1)<<(n+1))|(half[j]<<1);
    }

    Word index(Word word,bool central_edge) const {
        if (!central_edge) return centered.index((word>>1)&((Word(1)<<(2*n-2))-1));
        Word right = (word>>1)&((Word(1)<<n)-1);
        Word left = (word>>(n+1))<<1;
        auto a = std::lower_bound(half.begin(),half.end(),left);
        auto b = std::lower_bound(half.begin(),half.end(),right);
        if (a==half.end() || b==half.end() || *a!=left || *b!=right || a>b)
            throw std::runtime_error("noncanonical central edge");
        return first_pair[a-half.begin()]+(b-a);
    }
};
