// Find ring bijections allowing either parity at a specified matching edge.
#include "branched_search.hpp"
#include <array>

int main() {
    std::string key;
    while (std::getline(std::cin,key)) {
        Graph g(key);
        int c = g.cycle;
        std::vector<int> need(g.parent.size(),1);
        for (int i = int(need.size())-1; i >= c; --i)
            if (need[i]) --need[g.parent[i]];
        for (int b : need) if (b < 0) return 2;
        std::vector<int> mate(c,0);
        if (std::all_of(need.begin(),need.begin()+c,[](int b){return b==1;})) {
            std::fill(mate.begin(),mate.end(),1);
        } else {
            int a = std::find(need.begin(),need.begin()+c,0)-need.begin();
            bool odd = false;
            for (int k = 1; k <= c; ++k) {
                int j = (a+k)%c;
                if (need[j]) {
                    if (!odd) mate[j] = 1;
                    odd = !odd;
                } else if (odd) return 3;
            }
        }
        if (std::none_of(mate.begin(),mate.end(),[](int x){return x!=0;})) continue;
        Search s(g,key);
        std::vector<int> done(c,0);
        std::vector<std::string> proofs;
        bool complete = false;
        for (int attempt = 0; attempt < 300 && !complete; ++attempt) {
            if (!s.solve()) break;
            std::array<int,13> blocked;
            blocked.fill(-1);
            for (int i = 0; i < c; ++i) {
                int a = s.label[i],b = s.label[(i+1)%c];
                if (a%13 == b%13) blocked[(a+b)%13] = i;
            }
            bool used = false;
            for (int i = 0; i < c; ++i) if (mate[i]) {
                int w = s.label[i]+s.label[(i+1)%c];
                int j = blocked[w%13];
                int flag = 1<<(w%2);
                if ((j<0 || j==i) && !(done[i]&flag)) {
                    done[i] |= flag;
                    used = true;
                }
            }
            if (used) {
                std::string row;
                for (int x : s.label) row += char('A'+x);
                proofs.push_back(row);
            }
            complete = true;
            for (int i = 0; i < c; ++i) if (mate[i] && done[i]!=3) complete = false;
        }
        if (!complete) {
            std::cerr << "unresolved " << key << '\n';
            return 1;
        }
        std::cout << key;
        for (auto row : proofs) std::cout << ' ' << row;
        std::cout << '\n';
    }
}
