// Classify eleven-leaf trees at orders 50 through 54 for the 27-label proof.
#include "../rainbow/tip_forests.hpp"
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <vector>

namespace {
using Word = std::uint64_t;
using Mask = std::uint32_t;
using Key = std::pair<int, Word>;
constexpr int largest = 25;
constexpr int infinity = 100;

struct Node {
    std::vector<int> children;
    int parent, depth, size = 0, tips = 0;
    int first = infinity, second = infinity;
    Word word = 0;
};

std::vector<Node> decode(Key tree) {
    std::vector<Node> nodes;
    std::vector<int> stack;
    for (int bit = 2*tree.first-1; bit >= 0; --bit) {
        if ((tree.second >> bit) & 1) {
            int p = stack.empty() ? -1 : stack.back();
            int v = nodes.size();
            if (p >= 0) nodes[p].children.push_back(v);
            nodes.push_back({{}, p, static_cast<int>(stack.size())});
            stack.push_back(v);
        } else {
            int v = stack.back();
            stack.pop_back();
            Node& x = nodes[v];
            x.size = nodes.size()-v;
            x.word = (tree.second >> bit) & ((Word(1) << (2*x.size))-1);
            if (x.children.empty()) {
                x.tips = x.first = 1;
                continue;
            }
            for (int u : x.children) x.tips += nodes[u].tips;
            // Earliest first or second leaf over preorder traversals in size order.
            for (int u : x.children) {
                const Node& child = nodes[u];
                if (child.size != nodes[x.children.front()].size) break;
                x.first = std::min(x.first, 1+child.first);
                if (child.tips >= 2) {
                    x.second = std::min(x.second, 1+child.second);
                } else {
                    int smallest = infinity;
                    for (int w : x.children) if (w != u) {
                        if (nodes[w].size > smallest) break;
                        smallest = nodes[w].size;
                        x.second = std::min(x.second, 1+child.size+nodes[w].first);
                    }
                }
            }
        }
    }
    assert(stack.empty() && nodes[0].size == tree.first);
    return nodes;
}

struct Branch {
    Key key;
    int tips, stem = 0;
    std::array<Mask, 5> all{};
    std::array<std::array<Mask, 3>, 5> cuts{};
    std::array<int, 4> arms{};
    std::array<unsigned char, largest+1> suffix_tips{};
};

using Profile = std::array<int, 3>; // initial corridor, first leaf, second leaf
using Group = std::map<Profile, std::vector<Branch>>;

void add_branch(Group& groups, Key key, int tips) {
    Branch b{key, tips};
    auto nodes = decode(key);
    assert(nodes[0].tips == tips);
    while (nodes[b.stem].children.size() == 1) ++b.stem;
    int leaf = 0;
    std::array<int, largest+1> prefix{};
    for (int u = 0; u < key.first; ++u) {
        const Node& v = nodes[u];
        b.cuts[v.tips][std::min(2,v.depth)] |= Mask(1) << v.size;
        b.all[v.tips] |= Mask(1) << v.size;
        prefix[u+1] = prefix[u] + v.children.empty();
        if (v.children.empty()) {
            int length = 1;
            for (int p = v.parent; p >= 0 && nodes[p].children.size() == 1; p = nodes[p].parent)
                ++length;
            b.arms[leaf++] = length;
        }
    }
    b.suffix_tips.fill(infinity);
    for (int u = 0; u < key.first; ++u) {
        int end = u+nodes[u].size;
        for (int z = 1; z <= nodes[u].size; ++z)
            b.suffix_tips[z] = std::min<int>(b.suffix_tips[z], prefix[end]-prefix[end-z]);
    }
    groups[{b.stem, nodes[0].first, nodes[0].second}].push_back(b);
}

bool seed_or_central_ring(const std::array<int,3>& size, const std::array<Profile,3>& p) {
    for (int i = 0; i < 3; ++i) {
        int j = (i+1)%3, h = (i+2)%3;
        int wanted = i == 0 ? 2 : 1;
        if (size[j] <= size[h] && size[i]+p[j][wanted] <= 27) return true;
        if (size[h] <= size[j] && size[i]+p[h][wanted] <= 27) return true;
        if (size[i] <= 24 && 1+size[i]+p[j][0]+p[h][0] >= 27) return true;
    }
    return false;
}

bool ring(const Branch& a, const Branch& b, int discard) {
    for (int i = 1; i <= a.tips; ++i) for (int j = std::max(1,5-i); j <= b.tips; ++j) {
        for (int depth = 0; depth <= 2; ++depth) {
            Mask partners = 0;
            for (int other = 2-depth; other <= 2; ++other) partners |= b.cuts[j][other];
            for (Mask m = a.cuts[i][depth]; m; m &= m-1) {
                int z = discard-__builtin_ctz(m);
                if (z > 0 && z <= largest && (partners & (Mask(1)<<z))) return true;
            }
        }
    }
    return false;
}

bool six_paths(const Branch& a, const Branch& b, const Branch& c, int t) {
    std::array<int,12> lengths{};
    auto next = lengths.begin();
    for (auto side : {&a,&b,&c}) next = std::copy(side->arms.begin(),side->arms.end(),next);
    std::sort(lengths.rbegin(), lengths.rend());
    int total = 0;
    for (int i = 0; i < 6; ++i) total += lengths[i];
    return total >= t;
}

bool two_sides(const Branch& a, const Branch& b, int t) {
    for (int leaves = 1; leaves <= a.tips; ++leaves) {
        for (Mask m = a.all[leaves]; m; m &= m-1) {
            int size = __builtin_ctz(m), z = t-size;
            if (z < 1 || z > b.key.first) continue;
            int tips = b.suffix_tips[z];
            if (leaves+tips <= 6 && size+26-t >= z+tips) return true;
        }
    }
    return false;
}

Word exterior(const Branch& a, const Branch& b, int keep, int t) {
    std::array<Key,2> sides{a.key,b.key};
    std::sort(sides.begin(), sides.end());
    std::vector<Key> forest;
    for (Key key : sides) {
        auto nodes = decode(key);
        int pos = std::min(keep,key.first);
        keep -= pos;
        while (pos < key.first) {
            const Node& v = nodes[pos];
            forest.emplace_back(v.size,v.word);
            pos += v.size;
        }
    }
    std::sort(forest.begin(),forest.end());
    Word word = 0;
    int mass = 0;
    for (auto [size,code] : forest) {
        word = (word << (2*size)) | code;
        mass += size;
    }
    assert(keep == 0 && mass == t);
    return word;
}

void inspect(int n, const Group groups[][5], const std::string& output) {
    int t = n-28;
    std::set<Word> needed;
    Word triples = 0;
    for (int a = 4; a < t; ++a) for (int b = 5; b < t; ++b) {
        int c = n-1-a-b;
        if (c < b || c >= t) continue;
        for (const auto& [pa,as] : groups[a][3]) for (const auto& [pb,bs] : groups[b][4]) {
            if ((a <= c && b+pa[1] <= 27) || (b <= c && a+pb[2] <= 27)) continue;
            for (const auto& [pc,cs] : groups[c][4]) {
                if (seed_or_central_ring({a,b,c},{pa,pb,pc})) continue;
                for (const Branch& x : as) for (const Branch& y : bs) {
                    if (ring(x,y,n-27) || two_sides(x,y,t) || two_sides(y,x,t)) continue;
                    for (const Branch& z : cs) {
                        if (ring(x,z,n-27) || ring(y,z,n-27) || six_paths(x,y,z,t)) continue;
                        if (two_sides(x,z,t) || two_sides(z,x,t) ||
                            two_sides(y,z,t) || two_sides(z,y,t)) continue;
                        ++triples;
                        needed.insert(exterior(x,y,27-c,t));
                    }
                }
            }
        }
    }
    std::ofstream file(output+"/words-"+std::to_string(n));
    for (Word word : needed) file << word << '\n';
    if (!file) throw std::runtime_error("cannot write exterior list");
    std::cout << "order " << n << " remaining triples " << triples
              << " distinct exteriors " << needed.size() << std::endl;
}
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    TipForests trees(largest,4);
    Group groups[largest+1][5];
    int used = 0;
    for (int size = 1; size <= largest; ++size) for (int tips : {3,4}) {
        const auto& words = trees.branches(size,tips);
        for (Word w : words) add_branch(groups[size][tips], {size,w}, tips);
        used += words.size();
    }
    std::cout << "three- and four-leaf branches " << used << std::endl;
    for (int n = 50; n <= 54; ++n) inspect(n,groups,argv[1]);
}
