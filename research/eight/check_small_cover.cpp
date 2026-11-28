// Exhaust all vertex permutations and exclude smaller covers of each SPN2 record.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint64_t;
using Row = std::array<int,7>;
using Colors = std::vector<int>;

Row orbit(const Row& row) {
    Row key = row;
    for (int u : {3,5,7}) {
        Row other = row;
        for (int& a : other) a = (u*a) % 8;
        key = std::min(key,other);
    }
    return key;
}

unsigned read_number(std::istream& in, int bytes) {
    Mask value = 0;
    for (int i = 0; i < bytes; ++i) {
        int byte = in.get();
        if (byte < 0) throw std::runtime_error("truncated input");
        value |= Mask(byte) << (8*i);
    }
    if (value > UINT32_MAX) throw std::runtime_error("invalid eight-label record");
    return unsigned(value);
}

struct Forest {
    Row parent{};
    std::vector<int> roots, sizes;
    int tips = 0;

    explicit Forest(unsigned word) {
        std::vector<int> stack;
        int next = 0;
        for (int bit = 13; bit >= 0; --bit) {
            if ((word >> bit) & 1) {
                if (next == 7) throw std::runtime_error("extra vertex");
                if (stack.empty()) roots.push_back(next);
                parent[next] = stack.empty() ? -1 : stack.back();
                stack.push_back(next++);
            } else {
                if (stack.empty()) throw std::runtime_error("unmatched close");
                stack.pop_back();
            }
        }
        if (next != 7 || !stack.empty() || word >= (1u<<14))
            throw std::runtime_error("invalid forest");
        for (int i = 0; i < 7; ++i)
            tips += std::find(parent.begin(),parent.end(),i) == parent.end();
        for (unsigned i = 0; i < roots.size(); ++i)
            sizes.push_back((i+1 == roots.size() ? 7 : roots[i+1]) - roots[i]);
    }

    std::vector<Colors> representatives() const {
        std::set<Colors> cases;
        int limit = tips > 4 ? 1 : 1 << (3*roots.size());
        for (int raw = 0; raw < limit; ++raw) {
            Colors c;
            int mass = 0, runs = 0;
            for (unsigned i = 0; i < roots.size(); ++i) {
                int color = (raw >> (3*i)) & 7;
                if (i == 0 || color != c.back()) {
                    if (sizes[i] < mass+runs) break;
                    ++runs;
                }
                c.push_back(color);
                mass += sizes[i];
            }
            if (c.size() != roots.size()) continue;
            Colors key = c;
            for (int u : {3,5,7}) {
                Colors other = c;
                for (int& a : other) a = (u*a) % 8;
                key = std::min(key,other);
            }
            cases.insert(key);
        }
        return {cases.begin(),cases.end()};
    }

    Mask covered(const Row& row, const std::vector<Colors>& cases) const {
        Mask result = 0;
        for (unsigned i = 0; i < cases.size(); ++i) {
            int weights = 0, root = 0;
            for (int j = 0; j < 7; ++j) {
                int a = parent[j] < 0 ? cases[i][root++] : row[parent[j]];
                weights |= 1 << ((a+row[j]) % 8);
            }
            if (__builtin_popcount(unsigned(weights)) == 7) result |= Mask(1) << i;
        }
        return result;
    }
};

// Partition the available rows on an uncovered input. Each branch takes one
// row containing that input and excludes earlier alternatives. Every solution
// occurs in the branch of its first such row.
bool possible(Mask need, int left, const std::vector<Mask>& rows) {
    if (!need) return true;
    if (!left) return false;
    int width = __builtin_popcountll(need);
    Mask united = 0;
    std::array<int,64> counts{};
    std::vector<Mask> available;
    for (Mask m : rows) {
        Mask hit = m & need;
        if (!hit) continue;
        if (hit == need) return true;
        united |= hit;
        available.push_back(hit);
        for (Mask h = hit; h; h &= h-1) ++counts[__builtin_ctzll(h)];
    }
    if (united != need || left == 1) return false;
    std::sort(available.begin(),available.end(),[](Mask a, Mask b) {
        return __builtin_popcountll(a) > __builtin_popcountll(b);
    });
    if (left * __builtin_popcountll(available.front()) < width) return false;
    int pivot = __builtin_ctzll(need);
    for (Mask h = need; h; h &= h-1) {
        int bit = __builtin_ctzll(h);
        if (counts[bit] < counts[pivot]) pivot = bit;
    }
    Mask target = Mask(1) << pivot;
    std::vector<Mask> others;
    for (Mask m : available) if (!(m & target)) others.push_back(m);
    // Iterate backwards. "others" contains every permitted later alternative.
    for (auto it = available.rbegin(); it != available.rend(); ++it) {
        if (!(*it & target)) continue;
        if (possible(need & ~*it,left-1,others)) return true;
        others.push_back(*it);
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream in(argv[1],std::ios::binary);
    char header[5];
    if (!in.read(header,5) || std::string(header,5) != "SPN2\x08") return 2;
    std::set<unsigned> catalog;
    int total = 0;
    while (in.peek() != EOF) {
        unsigned word = read_number(in,8), n = read_number(in,4);
        if (!catalog.insert(word).second || n < 1 || n > 40) return 2;
        Forest forest(word);
        auto cases = forest.representatives();
        if (cases.empty() || cases.size() >= 64) return 2;
        Mask full = (Mask(1) << cases.size())-1;
        std::map<Row,Mask> group;
        Row row{1,2,3,4,5,6,7};
        do {
            group[orbit(row)] |= forest.covered(row,cases);
        } while (std::next_permutation(row.begin(),row.end()));
        Mask covered = 0;
        for (unsigned i = 0; i < n; ++i) {
            for (int& a : row) a = read_number(in,1);
            Row sorted = row;
            std::sort(sorted.begin(),sorted.end());
            if (sorted != Row{1,2,3,4,5,6,7}) throw std::runtime_error("invalid permutation");
            covered |= group.at(orbit(row));
        }
        if (covered != full) throw std::runtime_error("stored rows miss a boundary");
        std::set<Mask> different;
        for (const auto& entry : group) if (entry.second) different.insert(entry.second);
        std::vector<Mask> maximal;
        for (Mask m : different) {
            bool contained = std::any_of(different.upper_bound(m),different.end(),
                                         [m](Mask other) { return (m & other) == m; });
            if (!contained) maximal.push_back(m);
        }
        if (possible(full,int(n)-1,maximal)) throw std::runtime_error("smaller cover exists");
        total += n;
    }
    if (catalog.size() != 115) return 2;
    std::cout << catalog.size() << " shape minima checked, " << total << " rows necessary\n";
}
