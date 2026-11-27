// Enumerate canonical forest words, retaining only a bounded number of tips.
#pragma once
#include <algorithm>
#include <cstdint>
#include <vector>

class TipForests {
    using Word = std::uint64_t;
    using Layer = std::vector<std::vector<Word>>; // indexed by exact tip count
    std::vector<Layer> trees;
    int limit;

    template<class Emit>
    void forest(int left, int budget, int least_size, Word least_word,
                Word prefix, int tips, const Emit& emit) const {
        if (left == 0) {
            emit(prefix, tips);
            return;
        }
        if (budget == 0) return;
        auto add_size = [&](int size) {
            for (int count = 1; count <= std::min(budget, size); ++count) {
                const auto& words = trees[size][count];
                auto start = size == least_size
                    ? std::lower_bound(words.begin(), words.end(), least_word) : words.begin();
                for (auto it = start; it != words.end(); ++it)
                    forest(left-size, budget-count, size, *it, (prefix << (2*size)) | *it,
                           tips+count, emit);
            }
        };
        // A following component must have at least the size of this one.
        if (budget > 1)
            for (int size = least_size; size <= left/2; ++size) add_size(size);
        if (left >= least_size) add_size(left);
    }

public:
    TipForests(int order, int max_tips): trees(order+1, Layer(max_tips+1)), limit(max_tips) {
        trees[1][1].push_back(2);
        for (int size = 2; size <= order; ++size) {
            forest(size-1, limit, 1, 0, 0, 0, [&](Word children, int tips) {
                trees[size][tips].push_back((Word(1) << (2*size-1)) | (children << 1));
            });
            for (auto& words : trees[size]) std::sort(words.begin(), words.end());
        }
    }
    template<class Emit>
    void each(int order, const Emit& emit) const {
        forest(order, limit, 1, 0, 0, 0, [&](Word code, int) { emit(code); });
    }
};
