// Independent verifier for the binary SPN1 and SPN2 forest certificates.
#include <algorithm>
#include <atomic>
#include <future>
#include <mutex>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
#include "shape_rank.hpp"
#include "forest_type.hpp"

namespace {
using Count = std::uint64_t;
using Mask = std::uint64_t;

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

// Bivariate multiset product for all forests of order k-1 with at most limit tips.
Count tip_count(int k, int limit) {
    std::vector<std::vector<Count>> ways(k, std::vector<Count>(limit+1));
    ways[0][0] = 1;
    for (int size = 1; size < k; ++size) {
        auto layer = ways[size-1];
        if (size == 1) layer[1] = 1; // a singleton has one tip
        for (int tips = 1; tips <= limit; ++tips) {
            Count types = layer[tips];
            if (types == 0) continue;
            auto next = ways;
            Count choices = 1;
            for (int n = 1; n*size < k && n*tips <= limit; ++n) {
                choices = choices*(types+n-1)/n;
                for (int s = n*size; s < k; ++s)
                    for (int t = n*tips; t <= limit; ++t)
                        next[s][t] += choices*ways[s-n*size][t-n*tips];
            }
            ways.swap(next);
        }
    }
    return std::accumulate(ways.back().begin(), ways.back().end(), Count(0));
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

class ShapeBits {
    ShapeRank rank;
    std::vector<std::atomic<Count>> bits;
public:
    explicit ShapeBits(int k): rank(k-1),bits((rank.total()+63)/64) {
        check(rank.total()==rooted_count(k),"forest rank total");
        for (auto& word : bits) word.store(0,std::memory_order_relaxed);
    }
    void insert(const Shape& s) {
        Count id=rank(s.parents);
        check(id<rank.total(),"forest rank out of range");
        Count mask=Count(1)<<(id%64);
        check(!(bits[id/64].fetch_or(mask,std::memory_order_relaxed)&mask),"repeated forest rank");
    }
};

struct Audit {
    int k;
    std::unordered_set<Count> seen;
    std::map<std::vector<int>,Profile> profiles;
    Count rows = 0, eligible = 0, colorings = 0, base_only = 0;
    ShapeBits* bits;
    explicit Audit(int k,ShapeBits* compact=nullptr): k(k),bits(compact) {}

    void cover_witness(Reader& in, const Shape& s, const Profile& p,
                       std::vector<bool>& covered, bool active) const {
        std::array<int,32> lab{}, first_root{};
        Mask used_v = 1, internal = 0;
        for (std::size_t v = 0; v < s.parents.size(); ++v) {
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
                int w = __builtin_ctzll(choices);
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

    void verify(const char* path, int tip_limit=0, int short_mass=0, const ForestType* type=nullptr) {
        Reader in(path);
        for (char c : std::string("SPN")) check(in.byte() == c, "bad header");
        int version = in.byte();
        check(short_mass ? version == '3' : version == '1' || version == '2', "unexpected stream version");
        check(in.byte() == k, "wrong modulus");
        if (short_mass) check(in.byte() == short_mass, "wrong short forest order");
        for (int first; (first = in.next()) >= 0;) {
            Count word = in.rest(first,8);
            Shape s(short_mass ? short_mass+1 : k,word);
            check(!tip_limit || s.leaves <= tip_limit, "too many tips in restricted catalog");
            if (type) {
                std::array<bool,32> parent{};
                for (int v : s.parents) if (v >= 0) parent[v] = true;
                std::vector<std::pair<int,int>> actual;
                int mass = static_cast<int>(s.parents.size());
                for (int i = 0; i < type->stem; ++i)
                    check(s.parents[i] == i-1, "broken initial stem");
                int parent_index = type->stem-1;
                int end = mass;
                for (int v = mass-1; v >= type->stem; --v) {
                    check(s.parents[v] >= parent_index, "branch attached above stem end");
                    if (s.parents[v] == parent_index) {
                        int tips = std::count(parent.begin()+v,parent.begin()+end,false);
                        actual.emplace_back(end-v,tips);
                        end = v;
                    }
                }
                std::sort(actual.begin(),actual.end());
                check(actual == type->parts, "wrong component order or tip count");
            }
            if (bits) bits->insert(s);
            else check(seen.insert(word).second, "repeated forest");
            const Profile& p = profiles.try_emplace(s.sizes, k, s).first->second;
            const bool active = s.leaves <= 2*(k-2)/3;
            int count = active ? p.representatives : 1;
            Count stored = in.rest(in.byte(),4);
            if (version == '1') check(stored == static_cast<Count>(count), "wrong record count");
            else check(stored > 0 && stored <= static_cast<Count>(count), "invalid packed count");
            std::vector<bool> covered(p.representatives);
            bool zero = false;
            for (Count j = 0; j < stored; ++j) {
                if (version != '1') {
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
            if (version != '1') {
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
    void finish(Count distinct) const {
        check(distinct == rooted_count(k), "incomplete rooted-tree catalog");
        std::cout << "k=" << k << " rooted bases=" << distinct << " eligible forests=" << eligible
                  << " base-only shapes=" << base_only << " witness rows=" << rows
                  << " eligible boundary assignments=" << colorings << '\n';
    }
};
// Across files, establish uniqueness by sorting words or setting canonical rank bits.
void parallel_audit(int k, int workers, const std::vector<std::string>& paths, bool compact) {
    check(workers > 0 && !paths.empty(), "expected a worker count and shard files");
    Audit totals(k);
    std::atomic<std::size_t> next{0};
    std::mutex output;
    std::vector<Count> keys;
    std::unique_ptr<ShapeBits> bits;
    if (compact) bits=std::make_unique<ShapeBits>(k);
    else keys.reserve(rooted_count(k));
    std::vector<std::future<void>> jobs;
    for (int w = 0; w < workers && static_cast<std::size_t>(w) < paths.size(); ++w) {
        jobs.push_back(std::async(std::launch::async,[&] {
            Audit local(k,bits.get());
            for (auto j = next.fetch_add(1); j < paths.size(); j = next.fetch_add(1)) {
                try {
                    local.verify(paths[j].c_str());
                } catch (const std::exception& error) {
                    // A sibling may be blocked opening a FIFO whose writer is waiting for us.
                    // End this CLI audit immediately so its producer can cancel the whole run.
                    std::fprintf(stderr,"%s\n",error.what());
                    std::fflush(stderr);
                    std::_Exit(1);
                }
                if (!compact) {
                    std::lock_guard<std::mutex> guard(output);
                    keys.insert(keys.end(),local.seen.begin(),local.seen.end());
                }
                local.seen.clear();
            }
            std::lock_guard<std::mutex> guard(output);
            totals.rows += local.rows;
            totals.eligible += local.eligible;
            totals.base_only += local.base_only;
            totals.colorings += local.colorings;
        }));
    }
    for (auto& job : jobs) job.get();
    if (compact) {
        totals.finish(totals.eligible+totals.base_only);
        return;
    }
    std::sort(keys.begin(),keys.end());
    check(std::adjacent_find(keys.begin(),keys.end()) == keys.end(), "repeated forest across shards");
    totals.finish(keys.size());
}

}
int main(int argc, char** argv) {
    if (argc < 3) return 2;
    int k = std::stoi(argv[1]);
    bool partial = std::string(argv[2])=="--short";
    bool limited = partial || std::string(argv[2])=="--tips";
    int max_modulus = partial ? 40 : limited ? 30 : 27;
    if (k < 5 || k > max_modulus) return 2;
    try {
        if (std::string(argv[2]) == "--typed") {
            if (argc < 5) return 2;
            ForestType type(k,argc-4,argv+4);
            Audit audit(k);
            audit.verify(argv[3],0,type.mass < k-1 ? type.mass : 0,&type);
            Count expected = 1;
            for (std::size_t i = 0; i < type.parts.size();) {
                auto [size,tips] = type.parts[i];
                Count trees = size == 1 ? 1 : tip_count(size,tips) - (tips == 1 ? 0 : tip_count(size,tips-1));
                std::size_t j = i+1;
                while (j < type.parts.size() && type.parts[j] == type.parts[i]) ++j;
                Count choices = 1;
                for (Count c = 0; c < j-i; ++c) choices = choices*(trees+c)/(c+1);
                expected *= choices;
                i = j;
            }
            check(audit.seen.size() == expected && audit.eligible == expected, "incomplete component type");
            std::cout << "forests=" << expected << " rows=" << audit.rows << " assignments=" << audit.colorings << '\n';
            return 0;
        }
        if (std::string(argv[2]) == "--listed") {
            if (argc < 5) return 2;
            std::ifstream expected(argv[3]);
            check(expected.is_open(), "cannot open required forest list");
            std::unordered_set<Count> required;
            Count word;
            while (expected >> word)
                check(required.insert(word).second, "duplicate in required forest list");
            check(expected.eof() && !required.empty(), "invalid required forest list");
            Audit audit(k);
            for (int i = 4; i < argc; ++i) audit.verify(argv[i]);
            check(audit.seen == required, "forest list and stream disagree");
            check(audit.eligible == required.size(), "listed forest is base-only");
            std::cout << "k=" << k << " listed forests=" << audit.eligible
                      << " witness rows=" << audit.rows << " boundary assignments=" << audit.colorings << '\n';
            return 0;
        }
        if (limited) {
            if (argc < (partial ? 6 : 5)) return 2;
            int mass = partial ? std::stoi(argv[3]) : k-1;
            int tips = std::stoi(argv[partial ? 4 : 3]);
            if (partial && (mass < 1 || mass > 30 || mass >= k-1)) return 2;
            if (tips < 1 || tips > mass || tips > 2*(k-2)/3) return 2;
            Audit audit(k);
            for (int i=partial ? 5 : 4; i<argc; ++i) audit.verify(argv[i],tips,partial ? mass : 0);
            check(audit.seen.size()==tip_count(mass+1,tips),"incomplete tip-limited catalog");
            check(audit.eligible==audit.seen.size(),"unverified boundary colors");
            std::cout << "k=" << k;
            if (partial) std::cout << " free vertices=" << mass;
            std::cout << " tip limit=" << tips << " forests=" << audit.eligible
                      << " witness rows=" << audit.rows << " boundary assignments=" << audit.colorings << '\n';
            return 0;
        }
        bool compact=std::string(argv[2])=="--rank-bits";
        if (compact || std::string(argv[2]) == "--parallel") {
            if (argc < 5) return 2;
            parallel_audit(k,std::stoi(argv[3]),std::vector<std::string>(argv+4,argv+argc),compact);
            return 0;
        }
        Audit audit(k);
        if (argc == 3 && std::string(argv[2]) == "--files-stdin") {
            std::string path;
            while (std::getline(std::cin, path)) audit.verify(path.c_str());
            check(std::cin.eof(), "could not read shard list");
        } else {
            for (int i = 2; i < argc; ++i) audit.verify(argv[i]);
        }
        audit.finish(audit.seen.size());
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
