// Enumerate numerical branch data at a leaf centroid, independently of the
// label search. A profile lists each rooted component's order and tip count.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {
using Part = std::pair<int,int>; // order, tips
using Parts = std::vector<Part>;
using Key = std::pair<Part,Parts>;
using Capacity = std::array<int,8>;
constexpr int k = 27;

struct Test {
    int n, leaves, t, budget;
    bool inventory;
    std::set<Parts> accepted;
    std::map<Key,bool> resolved;
    unsigned long long cases = 0, extensions = 0;

    bool suffixes(int mass,int tips,Part least,Parts& added,const Parts& whole,int whole_tips) {
        if (!mass) {
            if (whole_tips <= budget) return true;
            Parts key = whole;
            key.insert(key.end(),added.begin(),added.end());
            std::sort(key.begin(),key.end());
            return accepted.count(key);
        }
        for (int s = least.first; s <= mass; ++s) {
            int first = s == least.first ? least.second : 1;
            for (int j = first; j <= std::min(tips,std::max(1,s-1)); ++j) {
                added.emplace_back(s,j);
                bool good = suffixes(mass-s,tips-j,{s,j},added,whole,whole_tips+j);
                added.pop_back();
                if (!good) return false;
            }
        }
        return true;
    }

    bool certified(int z,int cap,Parts whole,int h) {
        if (h+cap <= budget) return true;
        std::sort(whole.begin(),whole.end());
        Key key{{z,cap},whole};
        auto it = resolved.find(key);
        if (it != resolved.end()) return it->second;
        Parts added;
        return resolved[key] = suffixes(z,cap,{1,1},added,whole,h);
    }

    bool has_cut(const Parts& p) {
        // The complete untouched branches form a subset at the centroid.
        for (unsigned mask = 0; mask < (1u<<p.size()); ++mask) {
            int mass = 0, tips = 0, smallest = n;
            Parts whole;
            for (unsigned i = 0; i < p.size(); ++i) if ((mask>>i)&1) {
                auto [s,j] = p[i];
                mass += s;
                tips += j;
                smallest = std::min(smallest,s);
                whole.push_back(p[i]);
            }
            int z = t-mass;
            if (z == 0 && certified(0,0,whole,tips)) return true;
            if (z <= 0) continue;
            for (unsigned i = 0; i < p.size(); ++i) if (!(mask & (1u<<i))) {
                auto [s,j] = p[i];
                if (z >= s) continue;
                if (smallest < s && smallest < z+std::min(j,z)) continue;
                if (certified(z,j,whole,tips)) return true;
            }
        }
        return false;
    }

    void grow(int mass,int left,int min_tips,int min_size,const Capacity& used,Parts& p) {
        if (!mass || !left) {
            if (mass || left) return;
            ++cases;
            if (inventory) {
                for (auto [s,j] : p) std::cout << s << ',' << j << ' ';
                std::cout << '\n';
            } else {
                if (!has_cut(p)) throw std::runtime_error("uncovered numerical centroid");
                ++extensions;
            }
            return;
        }
        for (int h = min_tips; h <= std::min(left,leaves/2); ++h) {
            int lower = std::max(h == 1 ? 1 : h+1,h == min_tips ? min_size : 1);
            for (int s = lower; s < t && s <= mass; ++s) {
                if (mass-s < left-h) break;
                // Maximum order selectable from the branches so far with a tip budget.
                Capacity next = used;
                bool easy = false;
                if (h <= budget) for (int j = h; j <= budget; ++j) {
                    next[j] = std::max(used[j],s+used[j-h]);
                    if (next[j] >= t) easy = true;
                }
                if (easy) break;
                p.emplace_back(s,h);
                grow(mass-s,left-h,h,s,next,p);
                p.pop_back();
            }
        }
    }
};
}

int main(int argc,char** argv) {
    if (argc != 4) return 2;
    int n = std::stoi(argv[1]), l = std::stoi(argv[2]);
    if (n < 50 || n > 54 || l < 11 || l > 15) return 2;
    Test test{n,l,n-28,l >= 14 ? 7 : 6,std::string(argv[3]) == "--candidates"};
    if (!test.inventory) {
        std::ifstream file(argv[3]);
        if (!file) throw std::runtime_error("cannot open certified profiles");
        for (std::string line; std::getline(file,line);) {
            Parts p;
            std::istringstream input(line);
            int s,h;
            char comma;
            while (input >> std::ws && !input.eof()) {
                if (!(input>>s>>comma>>h) || s < 1 || h < 1 || h > std::max(1,s-1) || comma != ',') throw std::runtime_error("invalid profile");
                p.emplace_back(s,h);
            }
            int mass = 0;
            for (Part a : p) mass += a.first;
            if (mass != test.t || !std::is_sorted(p.begin(),p.end()) || !test.accepted.insert(p).second)
                throw std::runtime_error("duplicate, unsorted or wrong-order profile");
        }
    }
    Parts p;
    test.grow(n-1,l,1,1,Capacity{},p);
    if (!test.inventory) std::cout << "order " << n << " leaves " << l << " numerical cases "
                                   << test.cases << " covered " << test.extensions << '\n';
}
