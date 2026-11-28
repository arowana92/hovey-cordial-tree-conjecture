// Enumerate the centroid branch data for a possible 50-vertex counterexample.
#include <algorithm>
#include <array>
#include <cstdint>
#include <string>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

using Part = std::pair<int,int>;
using Parts = std::vector<Part>;
using Mask = std::uint32_t;
using Budget = std::array<Mask,8>;

constexpr Mask bit(int n) { return Mask{1} << n; }

// Forest[s] minimizes the total tips after choosing a first rooted component.
// A rooted s-tree has a forest of s-1 children below its root.
const std::array<int,22>& lower_bounds(Mask excluded) {
    static std::map<Mask,std::array<int,22>> cache;
    auto entry = cache.try_emplace(excluded);
    auto& tree = entry.first->second;
    if (entry.second) {
        std::array<int,22> forest{};
        for (int s=1; s<=21; ++s) {
            tree[s] = excluded & bit(s) ? 50 : std::max(1,forest[s-1]);
            forest[s] = tree[s];
            for (int a=1; a<s; ++a)
                forest[s] = std::min(forest[s],tree[a]+forest[s-a]);
        }
    }
    return tree;
}

void report(const Parts& parts) {
    for (size_t i=0; i<parts.size(); ++i) {
        Mask excluded = 0;
        for (size_t j=0; j<parts.size(); ++j)
            if (j!=i) excluded |= bit(23-parts[j].first);
        auto [s,h] = parts[i];
        if (h < lower_bounds(excluded)[s]) return;
    }
    auto sorted=parts;
    std::sort(sorted.begin(),sorted.end());
    for (auto [s,h] : sorted) std::cout << s << ',' << h << ' ';
    std::cout << '\n';
}

void grow(int mass,int tips,int min_tips,int tie,Mask singles,Mask sums,
          const Budget& attained,Parts& chosen) {
    if (!mass || !tips) {
        if (!mass && !tips) report(chosen);
        return;
    }
    for (int h=min_tips; h<=tips; ++h) {
        int first = std::max(h==1 ? 1 : h+1,h==min_tips ? tie : 1);
        for (int s=first; s<=std::min(21,mass-tips+h); ++s) {
            if (singles & bit(23-s)) continue;
            Mask next_sums = (sums | (sums<<s)) & (bit(23)-1);
            if (next_sums & bit(22)) continue;
            Budget next = attained;
            bool small_cut = false;
            for (int j=h; j<=7; ++j) {
                // Only masses at most 21 survive. Use 64 bits when shifting.
                std::uint64_t more = std::uint64_t(attained[j-h]) << s;
                if (more >= bit(22)) { small_cut=true; break; }
                next[j] |= static_cast<Mask>(more);
            }
            if (small_cut) break;
            chosen.emplace_back(s,h);
            grow(mass-s,tips-h,h,s,singles|bit(s),next_sums,next,chosen);
            chosen.pop_back();
        }
    }
}
int main(int argc,char** argv) {
    if (argc!=2) return 2;
    int leaves=std::stoi(argv[1]);
    if (leaves<17 || leaves>21) return 2;
    Parts parts;
    Budget initial{};
    initial[0]=1;
    grow(49,leaves,1,1,0,1,initial,parts);
}
