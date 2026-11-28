// Find ancestor-closed eight-vertex cuts in the sixteen-vertex forest census.
#include "../rainbow/tip_forests.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

using Mask = std::uint32_t;
using Flags = std::array<int,65536>;

struct Forest {
    std::array<int,16> parent{};
    explicit Forest(Mask word) {
        int stack[16], height = 0, next = 0;
        for (int bit=31; bit>=0; --bit) {
            if ((word >> bit) & 1) {
                // Different old parents give the strongest test.
                parent[next] = height ? stack[height-1] : -next-1;
                stack[height++] = next++;
            } else {
                --height;
            }
        }
    }

    static Mask concatenate(Mask* words, int count, Mask start) {
        std::sort(words,words+count);
        for (int j=0; j<count; ++j)
            start = (start << (32-__builtin_clz(words[j]))) | words[j];
        return start;
    }

    bool uniform(Mask part, const Flags& bad) const {
        Mask children[16][8]{}, roots[8]{};
        int degree[16]{}, sites[8]{}, count = 0;
        for (int i=15; i>=0; --i) if ((part >> i) & 1) {
            Mask tree = concatenate(children[i],degree[i],1) << 1;
            int p = parent[i];
            if (p >= 0 && ((part >> p) & 1)) {
                children[p][degree[p]++] = tree;
            } else {
                roots[count] = tree;
                sites[count++] = p;
            }
        }
        int failure = bad[concatenate(roots,count,0)];
        if (!failure) return true;
        return !(failure & 2) &&
               std::all_of(sites+1,sites+count,[&](int v){ return v==sites[0]; });
    }

    Mask cut(int i, int left, Mask selected, const Flags& bad) const {
        if (!left) return uniform(selected,bad) && uniform(65535 ^ selected,bad) ? selected : 0;
        if (16-i < left) return 0;
        if (parent[i] < 0 || ((selected >> parent[i]) & 1)) {
            Mask found = cut(i+1,left-1,selected|(1u << i),bad);
            if (found) return found;
        }
        return cut(i+1,left,selected,bad);
    }
};

int main(int argc, char** argv) {
    const bool nine = argc == 3 && std::string(argv[2]) == "--nine-tips";
    if (argc != 2 && !nine) return 2;
    std::ifstream input(argv[1]);
    Flags bad{};
    int word, flag;
    while (input >> word >> flag) {
        if (word < 0 || word >= 65536 || (flag != 1 && flag != 3) || bad[word])
            throw std::runtime_error("invalid eight-vertex forest flag");
        bad[word] = flag;
    }
    if (!input.eof()) return 2;
    TipForests shapes(16,nine ? 9 : 8);
    shapes.each(16,[&](std::uint64_t code) {
        Forest forest(code);
        if (nine) {
            Mask nonleaves = 0;
            for (int p : forest.parent)
                if (p >= 0) nonleaves |= 1u << p;
            if (__builtin_popcount(nonleaves) != 7) return;
        }
        std::cout << code << ' ' << forest.cut(0,8,0,bad) << '\n';
    });
    return !std::cout;
}
