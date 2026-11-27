// Bijections with distinct endpoint sums on even cycles with at most one leaf per site.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;

class LabelSearch {
    int n, c, budget = 0;
    Mask state, all;
    std::vector<int> population, leaf_parent;
    Mask next_random() {
        state ^= state << 13;
        state ^= state >> 17;
        return state ^= state << 5;
    }
    bool assign(int v, Mask unused, Mask weights, int moment) {
        if (--budget < 0) return false;
        if (v == n) return true;
        int u = v < c ? v-1 : leaf_parent[v-c];
        int a = labels[u];
        Mask possible = unused & ((weights>>a)|(weights<<(n-a)));
        Mask below = (1U << (next_random()%n))-1;
        for (Mask choices : {possible & ~below, possible & below}) {
            for (; choices; choices &= choices-1) {
                int x = __builtin_ctz(choices);
                int w = (a+x)%n;
                Mask remain = weights ^ (1U<<w);
                int next_moment = moment;
                if (v < c) next_moment += (1+population[v])*x;
                if (v == c-1) {
                    // Vertex zero is fixed at zero. Close the cycle here.
                    if (next_moment%n || !(remain & (1U<<x))) continue;
                    remain ^= 1U<<x;
                }
                labels[v] = x;
                if (assign(v+1,unused^(1U<<x),remain,next_moment)) return true;
                if (budget < 0) return false;
            }
        }
        return false;
    }

public:
    std::vector<int> labels;
    LabelSearch(int order, int girth, Mask key):
        n(order), c(girth), state((key+1991)|1U), all((1U<<n)-1), labels(n) {
        for (int i = 0; i < c; ++i) {
            population.push_back((key>>(c-1-i))&1);
            if (population.back()) leaf_parent.push_back(i);
        }
    }
    bool solve() {
        for (int trial = 0; trial < 10000; ++trial) {
            budget = trial < 200 ? 1000 : 15000;
            if (assign(1,all-1,all,0)) return true;
            if (budget >= 0) break; // The search finished without a restart.
        }
        return false;
    }
};

bool canonical(Mask mask, int width) {
    Mask reverse = 0, all = (1U<<width)-1;
    for (int i = 0; i < width; ++i) reverse = 2*reverse+((mask>>i)&1U);
    for (Mask v : {mask,reverse}) {
        for (int i = 0; i < width; ++i) {
            if (v < mask) return false;
            v = ((v<<1)&all) | (v>>(width-1));
        }
    }
    return true;
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    int n = std::stoi(argv[1]);
    if (n < 6 || n > 30 || n%2) return 2;
    for (int c = 4; c < n; c += 2) {
        auto enumerate = [&](auto& self, int remaining, int ones, Mask mask) -> void {
            if (ones < 0 || remaining < ones) return;
            if (remaining) {
                self(self,remaining-1,ones,mask<<1);
                self(self,remaining-1,ones-1,(mask<<1)|1);
                return;
            }
            if (!canonical(mask,c)) return;
            Mask key = (1U<<c) | mask;
            LabelSearch search(n,c,key);
            bool found = search.solve();
            if (!found && n > 8)
                throw std::runtime_error("missing witness at key "+std::to_string(key));
            std::cout << key;
            if (found) for (int x : search.labels) std::cout << ' ' << x;
            std::cout << '\n';
        };
        enumerate(enumerate,c,n-c,0);
    }
}
