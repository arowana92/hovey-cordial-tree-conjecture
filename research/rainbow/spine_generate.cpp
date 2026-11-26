// Generate a binary witness stream for the size-ordered cut test.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

extern "C" int rainbow_witness(int, const int*, int*);

namespace {
using Code = std::uint64_t;
using Colors = std::vector<unsigned char>;
struct Tree { int size; Code code; };

class Generator {
    int k, shard, shards;
    std::ofstream out;
    std::vector<Tree> catalog;
    std::map<std::vector<int>, std::vector<Colors>> cache;
    std::uint64_t shapes = 0, cases = 0, selected = 0;

    template<class Emit>
    void enumerate(int remaining, std::size_t start, Code prefix, Emit& emit) {
        if (remaining == 0) {
            emit(prefix);
            return;
        }
        for (std::size_t i = start; i < catalog.size(); ++i) {
            Tree tree = catalog[i];
            if (tree.size > remaining) break;
            enumerate(remaining-tree.size, i, (prefix << (2*tree.size)) | tree.code, emit);
        }
    }

    const std::vector<Colors>& assignments(const std::vector<int>& gaps) {
        auto inserted = cache.try_emplace(gaps);
        auto& result = inserted.first->second;
        if (!inserted.second) return result;
        Colors colors(gaps.size());
        auto visit = [&](auto& self, std::size_t i, int runs) -> void {
            if (i == colors.size()) {
                for (int unit = 2; unit < k; ++unit) {
                    if (std::gcd(unit,k) != 1) continue;
                    for (auto c : colors) {
                        int image = unit*c % k;
                        if (image < c) return;
                        if (image > c) break;
                    }
                }
                result.push_back(colors);
                return;
            }
            for (int c = 0; c < k; ++c) {
                bool change = i == 0 || c != colors[i-1];
                if (change && gaps[i] < runs) continue;
                colors[i] = static_cast<unsigned char>(c);
                self(self, i+1, runs+change);
            }
        };
        visit(visit, 0, 0);
        return result;
    }

    void number(Code value, int bytes) {
        for (int i = 0; i < bytes; ++i) {
            out.put(static_cast<char>(value & 255));
            value >>= 8;
        }
    }

    void forest(Code code) {
        if (shapes++ % shards != static_cast<unsigned>(shard)) return;
        ++selected;
        std::array<int, 32> p{}, stack{}, labels{}, group{};
        std::vector<int> roots, gaps;
        int n = 0, depth = 0, leaves = 0;
        bool opening = false;
        for (int bit = 2*(k-1)-1; bit >= 0; --bit) {
            if ((code >> bit) & 1) {
                p[n] = depth ? stack[depth-1] : -1;
                if (depth == 0) roots.push_back(n);
                stack[depth++] = n++;
                opening = true;
            } else {
                leaves += opening;
                opening = false;
                --depth;
            }
        }
        for (std::size_t j = 0; j < roots.size(); ++j) {
            int at = roots[j];
            int size = (j+1 < roots.size() ? roots[j+1] : n)-at;
            if (size > at) gaps.push_back(size-at);
            group[at] = static_cast<int>(gaps.size())-1;
        }
        // A zero boundary on every component is the base case at the dummy root.
        const auto& colors = assignments(gaps);
        int count = leaves <= 2*(k-2)/3 ? static_cast<int>(colors.size()) : 1;
        number(code, 8);
        number(count, 4);
        for (int j = 0; j < count; ++j) {
            const Colors& pattern = colors[j];
            for (int root : roots) p[root] = -1-pattern[group[root]];
            if (rainbow_witness(k, p.data(), labels.data()) != 1) {
                std::cerr << "Failed forest " << code << " parents";
                for (int i = 0; i < n; ++i) std::cerr << ' ' << p[i];
                throw std::runtime_error("no witness");
            }
            for (auto c : pattern) out.put(static_cast<char>(c));
            for (int i = 0; i < n; ++i) out.put(static_cast<char>(labels[i]));
            ++cases;
        }
        if (selected % 100000 == 0) std::cerr << "shard " << shard << ": " << selected
                                               << " shapes, " << cases << " witnesses\n";
    }

public:
    Generator(int mod, int part, int total, const char* path):
        k(mod), shard(part), shards(total), out(path, std::ios::binary) {
        if (!out) throw std::runtime_error("cannot open output");
    }

    void run() {
        out.write("SPN1", 4);
        out.put(static_cast<char>(k));
        for (int size = 1; size < k; ++size) {
            std::vector<Tree> layer;
            auto add = [&](Code f) { layer.push_back({size, (Code(1) << (2*size-1)) | (f<<1)}); };
            enumerate(size-1, 0, 0, add);
            std::sort(layer.begin(), layer.end(), [](Tree a, Tree b) { return a.code < b.code; });
            catalog.insert(catalog.end(), layer.begin(), layer.end());
        }
        auto check = [&](Code f) { forest(f); };
        enumerate(k-1, 0, 0, check);
        out.close();
        if (!out) throw std::runtime_error("write failed");
        std::cout << "shard " << shard << ": " << selected << " shapes, " << cases
                  << " witnesses, full catalog " << shapes << '\n';
    }
};
}

int main(int argc, char** argv) {
    if (argc != 5) return 2;
    int k = std::stoi(argv[1]), shard = std::stoi(argv[2]), total = std::stoi(argv[3]);
    if (k < 5 || k > 26 || shard < 0 || shard >= total) return 2;
    Generator(k, shard, total, argv[4]).run();
}
