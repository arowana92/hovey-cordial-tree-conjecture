// Generate a binary witness stream for the size-ordered cut test.
#include "ranked_forest.hpp"
#include "tip_forests.hpp"
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
    int k, mass, shard, shards;
    bool cover;
    std::ofstream file;
    std::ostream& out;
    std::map<int,std::vector<int>> orbit_codes;
    std::vector<std::uint64_t> stamp;
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

    int encode(const Colors& colors) const {
        int value = 0;
        for (int c : colors) value = k*value+c;
        return value;
    }

    const std::vector<int>& orbits(int groups) {
        auto& table = orbit_codes[groups];
        if (!table.empty()) return table;
        int total = 1;
        for (int i = 0; i < groups; ++i) total *= k;
        table.resize(total);
        for (int x = 0; x < total; ++x) {
            int smallest = x;
            for (int unit = 2; unit < k; ++unit) {
                if (std::gcd(unit,k) != 1) continue;
                int y = x, image = 0, power = 1;
                while (y) {
                    image += power*((y%k)*unit%k);
                    y /= k;
                    power *= k;
                }
                smallest = std::min(smallest,image);
            }
            table[x] = smallest;
        }
        if (stamp.size() < table.size()) stamp.resize(table.size());
        return table;
    }

    void mark_coverage(const std::array<int,32>& parents, const std::array<int,32>& labels,
                       const std::vector<int>& roots, const std::array<int,32>& group,
                       const std::vector<int>& orbit) {
        using Bits = std::uint64_t;
        const Bits all = (Bits(1)<<k)-1;
        Bits internal = 0;
        for (int i = 0; i < mass; ++i)
            if (parents[i] >= 0) internal |= Bits(1)<<((labels[i]+labels[parents[i]])%k);
        int groups = group[roots.back()]+1;
        std::array<Bits,8> root_labels{};
        for (int v : roots) root_labels[group[v]] |= Bits(1)<<labels[v];
        std::array<std::array<Bits,40>,8> options{};
        std::array<int,8> sizes{};
        std::array<std::array<int,40>,8> colors{};
        for (int j = 0; j < groups; ++j) {
            Bits shifted = root_labels[j];
            for (int c = 0; c < k; ++c) {
                if (!(shifted & internal)) {
                    colors[j][sizes[j]] = c;
                    options[j][sizes[j]++] = shifted;
                }
                shifted = ((shifted<<1)&all) | (shifted>>(k-1));
            }
        }
        auto mark = [&](auto& self, int j, Bits occupied, int code) -> void {
            if (j == groups) { stamp[orbit[code]] = selected; return; }
            for (int i = 0; i < sizes[j]; ++i)
                if (!(options[j][i] & occupied))
                    self(self, j+1, occupied | options[j][i], code*k+colors[j][i]);
        };
        mark(mark, 0, internal, 0);
    }

    bool short_witness(const std::array<int,32>& parents, std::array<int,32>& labels) const {
        using Mask = std::uint64_t;
        const Mask all = (Mask(1)<<k)-1;
        auto visit = [&](auto& self, int i, Mask vertices, Mask weights) -> bool {
            if (i == mass) return true;
            int a = parents[i] < 0 ? -1-parents[i] : labels[parents[i]];
            Mask choices = vertices & ((weights >> a) | (weights << (k-a)));
            while (choices) {
                int x = __builtin_ctzll(choices);
                choices &= choices-1;
                labels[i] = x;
                if (self(self,i+1,vertices^(Mask(1)<<x),weights^(Mask(1)<<((x+a)%k))))
                    return true;
            }
            return false;
        };
        return visit(visit,0,all^1,all);
    }

    void number(Code value, int bytes) {
        for (int i = 0; i < bytes; ++i) {
            out.put(static_cast<char>(value & 255));
            value >>= 8;
        }
    }

    void forest(Code code) {
        ++selected;
        std::array<int, 32> p{}, stack{}, labels{}, group{};
        std::vector<int> roots, gaps;
        int n = 0, depth = 0, leaves = 0;
        bool opening = false;
        for (int bit = 2*mass-1; bit >= 0; --bit) {
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
        if (!cover) number(count, 4);
        const auto* orbit = cover ? &orbits(static_cast<int>(gaps.size())) : nullptr;
        std::vector<unsigned char> batch;
        for (int j = 0; j < count; ++j) {
            const Colors& pattern = colors[j];
            if (cover && stamp[encode(pattern)] == selected) continue;
            for (int root : roots) p[root] = -1-pattern[group[root]];
            bool found = mass == k-1 ? rainbow_witness(k, p.data(), labels.data()) == 1
                                     : short_witness(p, labels);
            if (!found) {
                std::cerr << "Failed forest " << code << " parents";
                for (int i = 0; i < n; ++i) std::cerr << ' ' << p[i];
                throw std::runtime_error("no witness");
            }
            if (cover) {
                for (int i = 0; i < n; ++i) batch.push_back(static_cast<unsigned char>(labels[i]));
                if (count > 1) mark_coverage(p, labels, roots, group, *orbit);
            } else {
                for (auto c : pattern) out.put(static_cast<char>(c));
                for (int i = 0; i < n; ++i) out.put(static_cast<char>(labels[i]));
            }
            ++cases;
        }
        if (cover) {
            number(batch.size()/n, 4);
            out.write(reinterpret_cast<const char*>(batch.data()), batch.size());
        }
        if (selected % 100000 == 0) std::cerr << "shard " << shard << ": " << selected
                                               << " shapes, " << cases << " witnesses\n";
    }

public:
    Generator(int mod, int free_vertices, int part, int total, const char* path, bool packed):
        k(mod), mass(free_vertices), shard(part), shards(total), cover(packed),
        out(std::string(path)=="-" ? std::cout : static_cast<std::ostream&>(file)) {
        if (&out==&file) file.open(path,std::ios::binary);
        if (!out) throw std::runtime_error("cannot open output");
    }

    void run(bool ranked, int tip_limit) {
        out.write(mass < k-1 ? "SPN3" : cover ? "SPN2" : "SPN1", 4);
        out.put(static_cast<char>(k));
        if (mass < k-1) out.put(static_cast<char>(mass));
        if (tip_limit) {
            TipForests limited(mass, tip_limit);
            limited.each(mass, [&](Code word) {
                if (shapes++ % shards == static_cast<unsigned>(shard)) forest(word);
            });
        } else if (ranked) {
            RankedForests catalog(k-1);
            shapes = catalog.count();
            for (Code i = shard; i < shapes; i += shards) forest(catalog[i]);
        } else {
            for (int size = 1; size < k; ++size) {
                std::vector<Tree> layer;
                auto add = [&](Code f) { layer.push_back({size, (Code(1) << (2*size-1)) | (f<<1)}); };
                enumerate(size-1, 0, 0, add);
                std::sort(layer.begin(), layer.end(), [](Tree a, Tree b) { return a.code < b.code; });
                catalog.insert(catalog.end(), layer.begin(), layer.end());
            }
            auto check = [&](Code f) {
                if (shapes++ % shards == static_cast<unsigned>(shard)) forest(f);
            };
            enumerate(k-1, 0, 0, check);
        }
        if (file.is_open()) file.close();
        else out.flush();
        if (!out) throw std::runtime_error("write failed");
        auto& report = &out==&file ? std::cout : std::cerr;
        report << "shard " << shard << ": " << selected << " shapes, " << cases
                  << " witnesses, " << (tip_limit ? "tip-limited catalog " : "full catalog ") << shapes << '\n';
    }
};
}

int main(int argc, char** argv) {
    std::ios::sync_with_stdio(false);
    if (argc < 5 || argc > 8) return 2;
    std::string mode = argc >= 6 ? argv[5] : "";
    bool partial = mode == "--short", limited = partial || mode == "--tips";
    if (partial ? argc != 8 : limited ? argc != 7 : argc > 6) return 2;
    if (!limited && !mode.empty() && mode != "--cover" && mode != "--ranked-cover") return 2;
    int k = std::stoi(argv[1]), shard = std::stoi(argv[2]), total = std::stoi(argv[3]);
    int max_modulus = partial ? 40 : limited ? 30 : 27;
    if (k < 5 || k > max_modulus || shard < 0 || shard >= total) return 2;
    int mass = partial ? std::stoi(argv[6]) : k-1;
    int tips = limited ? std::stoi(argv[argc-1]) : 0;
    if (partial && (mass < 1 || mass > 30 || mass >= k-1)) return 2;
    if (limited && (tips < 1 || tips > mass || tips > 2*(k-2)/3)) return 2;
    Generator(k, mass, shard, total, argv[4], argc >= 6).run(mode == "--ranked-cover", tips);
}
