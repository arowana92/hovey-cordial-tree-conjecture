// Find ring bijections allowing either parity at a specified matching edge.
#include "branched_search.hpp"
#include <array>

int orbit_bit(int x) {
    x = (x%26+26)%26;
    if (x==0) return 8;
    if (x==13) return 4;
    return x%2 ? 1 : 2;
}

struct SelectedEdges {
    int mate,closing;
    int deficits=8, differences=0;
};

void boundary_rows(const Graph& g,const std::string& key,const std::vector<int>& mate, bool neutral) {
    int c = g.cycle;
    std::vector<SelectedEdges> needed;
    for (int i=0; i<c; ++i) if (mate[i]) {
        for (int j=0; j<c; ++j) if (i!=j) needed.push_back({i,j});
    }
    Search search(g,key);
    std::cout << key;
    for (int attempt=0; attempt<(neutral ? 2000 : 1500) && !needed.empty(); ++attempt) {
        if (!search.solve()) break;
        size_t kept=0;
        bool used=false;
        for (auto pair : needed) {
            int i=pair.mate, j=pair.closing;
            int w=search.label[i]+search.label[(i+1)%c];
            int a=search.label[j], b=search.label[(j+1)%c];
            int deficits=pair.deficits | orbit_bit(w-a-b);
            int differences=pair.differences | orbit_bit(w-2*a) | orbit_bit(2*b-w);
            if (differences!=pair.differences || (!neutral && deficits!=pair.deficits)) used=true;
            if (differences!=15 && (neutral || deficits!=15)) {
                pair.deficits=deficits;
                pair.differences=differences;
                needed[kept++]=pair;
            }
        }
        needed.resize(kept);
        if (used) {
            std::cout << ' ';
            for (int x : search.label) std::cout << char('A'+x);
        }
    }
    if (!needed.empty()) throw std::runtime_error("unresolved graph "+key);
    std::cout << '\n';
}

int main(int argc,char** argv) {
    bool divisible = argc==2 && std::string(argv[1])=="--divisible";
    bool neutral = argc==2 && std::string(argv[1])=="--neutral";
    if (argc!=1 && !divisible && !neutral) return 2;
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
        if (divisible || neutral) {
            boundary_rows(g,key,mate,neutral);
            continue;
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
