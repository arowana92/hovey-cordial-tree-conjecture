// Independent replay using multisets of child IDs and bottom-up subtree data.
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
using Profile = std::array<int,3>;
using Groups = std::map<Profile,std::vector<int>>;
struct Tree {
    int size, leaves, corridor = 0, first = 100, second = 100;
    std::vector<int> children, arms;
    std::array<std::array<Mask,3>,5> prunable{};
    std::array<int,26> suffix{};
    Mask terminals = 0;
    Word code = 0;
};
std::vector<Tree> trees;
std::vector<int> by_size[26][5];
Groups grouped[26][5];

bool precedes(int a, int b) {
    return std::make_pair(trees[a].size,trees[a].code) < std::make_pair(trees[b].size,trees[b].code);
}

void assemble(int n, int leaves, std::vector<int> children) {
    std::sort(children.begin(),children.end(),precedes);
    Tree t{n,leaves};
    t.children = children;
    t.prunable[leaves][0] = Mask(1)<<n;
    t.code = 1;
    int pos = 1;
    for (int u : children) {
        const Tree& child = trees[u];
        t.code = (t.code << (2*child.size)) | child.code;
        t.terminals |= child.terminals << pos;
        pos += child.size;
        t.arms.insert(t.arms.end(),child.arms.begin(),child.arms.end());
        for (int j = 1; j <= child.leaves; ++j) {
            t.prunable[j][1] |= child.prunable[j][0];
            t.prunable[j][2] |= child.prunable[j][1] | child.prunable[j][2];
        }
    }
    t.code <<= 1;
    if (leaves == 1) t.arms = {n};
    if (children.empty()) {
        t.first = 1;
        t.terminals = 1;
    } else {
        if (children.size() == 1) t.corridor = 1+trees[children[0]].corridor;
        // A branch has at most four children, so try every legal tie order.
        std::sort(children.begin(),children.end());
        do {
            if (!std::is_sorted(children.begin(),children.end(),[](int a,int b) {
                    return trees[a].size < trees[b].size;
                })) continue;
            const Tree& child = trees[children[0]];
            t.first = std::min(t.first,1+child.first);
            if (child.leaves >= 2) t.second = std::min(t.second,1+child.second);
            else if (children.size() > 1)
                t.second = std::min(t.second,1+child.size+trees[children[1]].first);
        } while (std::next_permutation(children.begin(),children.end()));
    }
    for (int z = 1; z <= n; ++z) {
        t.suffix[z] = __builtin_popcount(t.terminals >> (n-z));
        for (int u : children) if (trees[u].size >= z)
            t.suffix[z] = std::min(t.suffix[z],trees[u].suffix[z]);
    }
    int id = trees.size();
    by_size[n][leaves].push_back(id);
    grouped[n][leaves][{t.corridor,t.first,t.second}].push_back(id);
    trees.push_back(std::move(t));
}

void multisets(int n, int l, int mass, int leaves, int min_size, int min_id, std::vector<int>& children) {
    if (mass == 0 || leaves == 0) {
        if (mass == 0 && leaves == 0) assemble(n,l,children);
        return;
    }
    for (int s = min_size; s <= mass; ++s) for (int j = 1; j <= leaves; ++j) {
        if (s < j || mass-s < leaves-j) continue;
        for (int id : by_size[s][j]) {
            if (s == min_size && id < min_id) continue;
            children.push_back(id);
            multisets(n,l,mass-s,leaves-j,s,id,children);
            children.pop_back();
        }
    }
}

bool compatible_sides(const Tree& a, const Tree& b, int t) {
    // A middle piece of size 27 leaves n-27 = t+1 vertices outside.
    for (int i = 1; i <= a.leaves; ++i) for (int depth = 0; depth <= 2; ++depth) {
        for (Mask bits = a.prunable[i][depth]; bits; bits &= bits-1) {
            int size = __builtin_ctz(bits), other = t+1-size;
            if (other > 0 && other <= b.size) {
                for (int j = std::max(1,5-i); j <= b.leaves; ++j)
                    for (int d = 2-depth; d <= 2; ++d)
                        if (b.prunable[j][d] & (Mask(1)<<other)) return true;
            }
            int tail = t-size;
            if (tail >= 1 && tail <= b.size && i+b.suffix[tail] <= 6 &&
                size+26-t >= tail+b.suffix[tail]) return true;
        }
    }
    return false;
}

void suffix_components(int id,int& used,std::vector<int>& roots) {
    if (!used) { roots.push_back(id); return; }
    if (used >= trees[id].size) { used -= trees[id].size; return; }
    --used;
    for (int child : trees[id].children) suffix_components(child,used,roots);
}

Word forest_code(int a,int b,int used) {
    if (precedes(b,a)) std::swap(a,b);
    std::vector<int> roots;
    suffix_components(a,used,roots);
    suffix_components(b,used,roots);
    assert(!used);
    std::sort(roots.begin(),roots.end(),precedes);
    Word code = 0;
    for (int v : roots) code = (code << (2*trees[v].size)) | trees[v].code;
    return code;
}

void check_order(int n,const std::string& directory) {
    const int t = n-28;
    Word remainder = 0;
    std::set<Word> required;
    for (int a = 4; a < t; ++a) for (int b = 5; b < t; ++b) {
        int c = n-1-a-b;
        if (c < b || c >= t) continue;
        std::array<int,3> size{a,b,c};
        for (const auto& [A,aa] : grouped[a][3]) for (const auto& [B,bb] : grouped[b][4]) {
            for (const auto& [C,cc] : grouped[c][4]) {
                std::array<Profile,3> p{A,B,C};
                std::array<int,3> perm{0,1,2};
                bool settled = false;
                do {
                    auto [i,j,h] = perm;
                    if (size[j] <= size[h] && size[i]+p[j][i == 0 ? 2 : 1] <= 27) settled = true;
                    int through = 26-size[i];
                    if (through >= 2 && through <= p[j][0]+p[h][0]) settled = true;
                } while (!settled && std::next_permutation(perm.begin(),perm.end()));
                if (settled) continue;
                for (int x : aa) for (int y : bb) {
                    if (compatible_sides(trees[x],trees[y],t) || compatible_sides(trees[y],trees[x],t)) continue;
                    for (int z : cc) {
                        if (compatible_sides(trees[x],trees[z],t) || compatible_sides(trees[z],trees[x],t) ||
                            compatible_sides(trees[y],trees[z],t) || compatible_sides(trees[z],trees[y],t)) continue;
                        std::vector<int> lengths;
                        for (int id : {x,y,z})
                            lengths.insert(lengths.end(),trees[id].arms.begin(),trees[id].arms.end());
                        std::sort(lengths.rbegin(),lengths.rend());
                        int sum = 0;
                        for (int i = 0; i < 6; ++i) sum += lengths[i];
                        if (sum >= t) continue;
                        ++remainder;
                        required.insert(forest_code(x,y,27-c));
                    }
                }
            }
        }
    }
    std::ifstream input(directory+"/words-"+std::to_string(n));
    if (!input) throw std::runtime_error("required list missing");
    std::vector<Word> actual;
    for (Word w; input >> w;) actual.push_back(w);
    if (!input.eof() || !std::equal(required.begin(),required.end(),actual.begin(),actual.end()))
        throw std::runtime_error("independent exterior list mismatch");
    std::cout << n << " confirmed " << remainder << " triples and " << required.size() << " exteriors\n";
}
}

int main(int argc,char** argv) {
    if (argc != 2) return 2;
    assemble(1,1,{});
    for (int n = 2; n <= 25; ++n) for (int l = 1; l <= 4; ++l) {
        std::vector<int> children;
        multisets(n,l,n-1,l,1,0,children);
    }
    for (int n = 50; n <= 54; ++n) check_order(n,argv[1]);
}
