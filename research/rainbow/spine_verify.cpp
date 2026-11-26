// Independent verifier for the binary SPN1 forest certificates.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {
using Count = std::uint64_t;
using Mask = std::uint32_t;

void check(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}

class Reader {
    FILE* f;
    std::array<unsigned char, 65536> buf{};
    std::size_t at = 0, size = 0;
public:
    explicit Reader(const char* path): f(std::fopen(path,"rb")) { check(f, "cannot read file"); }
    ~Reader() { std::fclose(f); }
    int next() {
        if (at == size) {
            at = 0;
            size = std::fread(buf.data(), 1, buf.size(), f);
            if (!size) { check(!std::ferror(f), "read error"); return -1; }
        }
        return buf[at++];
    }
    int byte() { int b = next(); check(b >= 0, "truncated record"); return b; }
    Count rest(int first, int bytes) {
        Count result = first;
        for (int j = 1; j < bytes; ++j) result |= Count(byte()) << (8*j);
        return result;
    }
};

// Euler's product R(x)/x = product (1-x^j)^(-R_j) for rooted unordered trees.
// Add one size class of children at a time, with multisets counted by binomials.
Count rooted_count(int k) {
    std::vector<Count> ways(k), next;
    ways[0] = 1;
    for (int j = 1; j < k; ++j) {
        Count types = ways[j-1], choose = 1;
        next = ways;
        for (int copies = 1; copies*j < k; ++copies) {
            choose = choose*(types+copies-1)/copies;
            for (int i = copies*j; i < k; ++i) next[i] += choose*ways[i-copies*j];
        }
        ways.swap(next);
    }
    return ways[k-1];
}

struct Shape {
    int k, pos = 0, leaves = 0;
    Count code;
    std::vector<int> parents, sizes, roots, groups;

    bool opening() const { return (code >> (2*(k-1)-1-pos)) & 1; }

    std::pair<int,Count> subtree(int parent) {
        check(pos < 2*(k-1) && opening(), "expected open");
        int start = pos++, v = static_cast<int>(parents.size());
        parents.push_back(parent);
        std::pair<int,Count> previous{};
        if (pos < 2*(k-1) && !opening()) ++leaves;
        while (pos < 2*(k-1) && opening()) {
            auto child = subtree(v);
            check(previous <= child, "noncanonical siblings");
            previous = child;
        }
        check(pos < 2*(k-1), "missing close");
        ++pos;
        int length = pos-start;
        Count bits = (code >> (2*(k-1)-pos)) & ((Count(1) << length)-1);
        return {length/2, bits};
    }

    Shape(int modulus, Count word): k(modulus), code(word) {
        check((code >> (2*(k-1))) == 0, "invalid high bits");
        int mass = 0, group = -1;
        std::pair<int,Count> previous{};
        while (pos < 2*(k-1)) {
            roots.push_back(static_cast<int>(parents.size()));
            auto s = subtree(-1);
            check(previous <= s, "noncanonical components");
            previous = s;
            if (s.first > mass) ++group;
            sizes.push_back(s.first);
            groups.push_back(group);
            mass += s.first;
        }
        check(mass == k-1, "wrong forest order");
    }
};

struct Profile {
    std::vector<int> canonical; // dense indices for permitted unit orbits
    int groups, representatives = 0;
    Count assignments = 0;
    Profile(int k, const Shape& s): groups(s.groups.back()+1) {
        int total = 1;
        for (int i = 0; i < groups; ++i) total *= k;
        canonical.assign(total,-1);
        std::vector<int> digits(groups);
        for (int raw = 0; raw < total; ++raw) {
            int x = raw;
            for (int j = 0; j < groups; ++j) { digits[j] = x%k; x /= k; }
            // Check the sharp cut using actual runs of *component* colors.
            int runs = 0, last = -1, mass = 0;
            bool valid = true;
            for (std::size_t j = 0; j < s.sizes.size(); ++j) {
                int color = digits[s.groups[j]];
                if (color != last) {
                    if (s.sizes[j] < mass+runs) { valid = false; break; }
                    ++runs;
                }
                last = color;
                mass += s.sizes[j];
            }
            if (!valid) continue;
            ++assignments;
            if (canonical[raw] >= 0) continue;
            for (int unit = 1; unit < k; ++unit) {
                if (std::gcd(k,unit) != 1) continue;
                int image = 0;
                for (int j = groups-1; j >= 0; --j) image = k*image+(unit*digits[j])%k;
                canonical[image] = representatives;
            }
            ++representatives;
        }
    }
};

struct Audit {
    int k;
    std::unordered_set<Count> seen;
    std::map<std::vector<int>,Profile> profiles;
    Count rows = 0, eligible = 0, colorings = 0, base_only = 0;
    explicit Audit(int k): k(k) {}

    void cover_witness(Reader& in, const Shape& s, const Profile& p,
                       std::vector<bool>& covered, bool active) const {
        std::array<int,32> lab{}, first_root{};
        Mask used_v = 1, internal = 0;
        for (int v = 0; v < k-1; ++v) {
            int a = in.byte();
            check(a < k && !(used_v & (Mask(1)<<a)), "invalid packed vertex permutation");
            used_v |= Mask(1)<<a;
            lab[v] = a;
            if (s.parents[v] >= 0) {
                int w = (a+lab[s.parents[v]]) % k;
                check(!(internal & (Mask(1)<<w)), "repeated internal weight");
                internal |= Mask(1)<<w;
            }
        }
        std::array<std::vector<int>,8> roots;
        for (std::size_t i = 0; i < s.roots.size(); ++i) {
            int g = s.groups[i];
            roots[g].push_back(lab[s.roots[i]]);
            first_root[g] = roots[g].front();
        }
        const Mask all = (Mask(1)<<k)-1;
        // Give a specific root in each group an unused edge weight. This
        // determines its parent's color. Check the other roots by addition.
        auto visit = [&](auto& self, int g, Mask weights, int raw, int place) -> void {
            if (g == p.groups) {
                int id = p.canonical[raw];
                if (id >= 0) covered[id] = true;
                return;
            }
            Mask choices = active ? all ^ weights : (Mask(1)<<first_root[g]) & ~weights;
            while (choices) {
                int w = __builtin_ctz(choices);
                choices &= choices-1;
                int c = w-first_root[g];
                if (c < 0) c += k;
                Mask next = weights | (Mask(1)<<w);
                bool valid = true;
                for (std::size_t j = 1; j < roots[g].size(); ++j) {
                    int y = c+roots[g][j];
                    if (y >= k) y -= k;
                    Mask b = Mask(1)<<y;
                    if (next & b) { valid = false; break; }
                    next |= b;
                }
                if (valid) self(self, g+1, next, raw+place*c, place*k);
            }
        };
        visit(visit, 0, internal, 0, 1);
    }

    void verify(const char* path) {
        Reader in(path);
        for (char c : std::string("SPN")) check(in.byte() == c, "bad header");
        int version = in.byte();
        check(version == '1' || version == '2', "unsupported version");
        check(in.byte() == k, "wrong modulus");
        for (int first; (first = in.next()) >= 0;) {
            Count word = in.rest(first,8);
            check(seen.insert(word).second, "repeated forest");
            Shape s(k,word);
            const Profile& p = profiles.try_emplace(s.sizes, k, s).first->second;
            const bool active = s.leaves <= 2*(k-2)/3;
            int count = active ? p.representatives : 1;
            Count stored = in.rest(in.byte(),4);
            if (version == '1') check(stored == static_cast<Count>(count), "wrong record count");
            else check(stored > 0 && stored <= static_cast<Count>(count), "invalid packed count");
            std::vector<bool> covered(p.representatives);
            bool zero = false;
            for (Count j = 0; j < stored; ++j) {
                if (version == '2') {
                    cover_witness(in, s, p, covered, active);
                    continue;
                }
                int raw = 0, power = 1;
                std::array<int,32> colors{}, lab{}, parent_label{};
                for (int t = 0; t < p.groups; ++t) {
                    colors[t] = in.byte();
                    check(colors[t] < k, "invalid color");
                    raw += power*colors[t];
                    power *= k;
                }
                int id = p.canonical[raw];
                check(id >= 0 && !covered[id], "unexpected or repeated orbit");
                zero |= raw == 0;
                covered[id] = true;
                for (std::size_t t = 0; t < s.roots.size(); ++t)
                    parent_label[s.roots[t]] = colors[s.groups[t]];
                Mask vertices = 1, weights = 0;
                for (int t = 0; t < k-1; ++t) {
                    int a = in.byte();
                    check(a < k, "vertex residue out of range");
                    lab[t] = a;
                    int b = s.parents[t] < 0 ? parent_label[t] : lab[s.parents[t]];
                    int w = a+b;
                    if (w >= k) w -= k;
                    Mask vbit = Mask(1)<<a, wbit = Mask(1)<<w;
                    check(!(vertices & vbit) && !(weights & wbit), "non-rainbow witness");
                    vertices |= vbit;
                    weights |= wbit;
                }
            }
            if (version == '2') {
                zero = covered[p.canonical[0]];
                check(!active || std::find(covered.begin(), covered.end(), false) == covered.end(),
                      "incomplete packed coverage");
            }
            check(zero, "missing base case");
            rows += stored;
            if (active) { ++eligible; colorings += p.assignments; }
            else ++base_only;
        }
    }
    void finish() const {
        check(seen.size() == rooted_count(k), "incomplete rooted-tree catalog");
        std::cout << "k=" << k << " rooted bases=" << seen.size() << " eligible forests=" << eligible
                  << " base-only shapes=" << base_only << " witness rows=" << rows
                  << " eligible boundary assignments=" << colorings << '\n';
    }
};
}
int main(int argc, char** argv) {
    if (argc < 3) return 2;
    int k = std::stoi(argv[1]);
    if (k < 5 || k > 26) return 2;
    try {
        Audit audit(k);
        for (int i = 2; i < argc; ++i) audit.verify(argv[i]);
        audit.finish();
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
