// Verify boundary assignments by trying the actual two possible missing weights.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

constexpr int n = 26;
using Mask = std::uint32_t;
constexpr Mask all = (1U<<n)-1;
void check(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}

struct Ring {
    int c;
    std::vector<std::pair<int,int>> edges;
    std::array<Mask,n> neighbors{};

    void add(int a, int b) {
        check(a>=0 && a<n && b>=0 && b<n && a!=b,"invalid edge");
        edges.emplace_back(a,b);
        neighbors[a] |= 1U<<b;
        neighbors[b] |= 1U<<a;
    }
    explicit Ring(const std::string& key) {
        c = 1+std::count(key.begin(),key.end(),'.');
        check(c>=3 && c<=n,"invalid girth");
        for (int i=0; i<c; ++i) add(i,(i+1)%c);
        int next=c, site=0;
        std::vector<int> stack;
        for (char token : key) {
            if (token=='(') {
                if (stack.empty()) stack.push_back(site);
                else {
                    add(stack.back(),next);
                    stack.push_back(next++);
                }
            } else if (token==')') {
                check(!stack.empty(),"unbalanced tree");
                stack.pop_back();
            } else {
                check(token=='.' && stack.empty(),"invalid tree separator");
                ++site;
            }
        }
        check(stack.empty() && next==n && edges.size()==n,"incorrect order");
    }

    // Removing the candidate edge's two endpoints leaves a forest. Every leaf
    // must use its only neighbor, so greedy deletion decides perfect matching.
    bool possible_mate(int i) const {
        Mask active = all ^ (1U<<i) ^ (1U<<((i+1)%c));
        while (active) {
            Mask old = active;
            for (Mask todo=active; todo; todo &= todo-1) {
                int v = __builtin_ctz(todo);
                Mask adj = neighbors[v] & active;
                if (!adj) return false;
                if (!(adj & (adj-1))) {
                    active ^= adj | (1U<<v);
                    break;
                }
            }
            check(active!=old,"residual cycle");
        }
        return true;
    }
};

struct Assignments {
    int i,j;
    // Four bits per difference orbit, one for each old-deficit orbit.
    unsigned covered=0;
};

int main(int argc, char** argv) {
    bool divisible = argc==4 && std::string(argv[3])=="--divisible";
    bool neutral = argc==4 && std::string(argv[3])=="--neutral";
    if (argc!=3 && !divisible && !neutral) return 2;
    std::ifstream catalog(argv[1]), proof(argv[2]);
    check(bool(catalog) && bool(proof),"missing input");
    // For any candidate difference, record the two normalized parent
    // differences obtainable by multiplying the new labels by a unit.
    std::array<int,n> orbit{};
    for (int d=0; d<n; ++d) for (int u=1; u<n; ++u) if (std::gcd(u,n)==1) {
        if ((d*u)%n==1) orbit[d] |= 1;
        if ((d*u)%n==2) orbit[d] |= 2;
        if ((d*u)%n==13) orbit[d] |= 4;
        if ((d*u)%n==0) orbit[d] |= 8;
    }
    std::string key,prev,line;
    long graphs=0,eligible=0,rows=0;
    long long ports=0;
    while (std::getline(catalog,key)) {
        check(prev<key,"repeated or unordered shape");
        prev=key;
        Ring g(key);
        std::vector<int> candidates;
        for (int i=0; i<g.c; ++i) if (g.possible_mate(i)) candidates.push_back(i);
        ++graphs;
        if (candidates.empty() && !divisible && !neutral) continue;
        if (!candidates.empty()) ++eligible;
        check(bool(std::getline(proof,line)),"missing record");
        std::istringstream fields(line);
        std::string word;
        check(bool(fields>>word) && word==key,"mismatched record");
        std::vector<std::array<Mask,2>> covered(g.c);
        std::vector<Assignments> pending;
        if (divisible || neutral) {
            for (int i : candidates) for (int j=0; j<g.c; ++j) if (i!=j) {
                pending.push_back({i,j});
                ports+=neutral ? 4 : 16;
            }
        }
        while (fields>>word) {
            check(word.size()==n,"wrong label count");
            std::array<int,n> f;
            Mask vz=0,ez=0;
            for (int v=0; v<n; ++v) {
                f[v]=word[v]-'A';
                check(f[v]>=0 && f[v]<n,"invalid residue");
                vz |= 1U<<f[v];
            }
            for (auto [a,b] : g.edges) ez |= 1U<<((f[a]+f[b])%n);
            check(vz==all && ez==all,"invalid bijection");
            ++rows;
            if (divisible || neutral) {
                size_t left=0;
                for (auto request : pending) {
                    int j=request.j, i=request.i;
                    int a=f[j], b=f[(j+1)%g.c];
                    int u=(a+b)%n, v=(f[i]+f[(i+1)%g.c])%n;
                    int diff=orbit[(u-v-a+b+2*n)%n] | orbit[(v-u-a+b+2*n)%n];
                    int deficit=orbit[(u-a-b+2*n)%n] | orbit[(v-a-b+2*n)%n];
                    for (int d=0; d<4; ++d) {
                        unsigned supported=(diff & (1<<d)) ? 15 : (neutral ? 0 : deficit);
                        request.covered |= supported<<(4*d);
                    }
                    if (request.covered!=65535) pending[left++]=request;
                }
                pending.resize(left);
                continue;
            }
            for (int i : candidates) {
                int lost=(f[i]+f[(i+1)%g.c])%n;
                int parity=lost%2;
                if (__builtin_popcount(covered[i][parity])>=g.c-1) continue;
                for (int j=0; j<g.c; ++j) if (i!=j) {
                    int a=f[j], b=f[(j+1)%g.c], closing=(a+b)%n;
                    int direct=(lost-closing-a+b+2*n)%n;
                    int swapped=(closing-lost-a+b+2*n)%n;
                    int works=orbit[direct]|orbit[swapped];
                    int target = parity ? 1 : 2;
                    if (works & target) covered[i][parity] |= 1U<<j;
                }
            }
        }
        if (divisible || neutral) {
            check(pending.empty(),"uncovered difference and deficit");
            continue;
        }
        for (int i : candidates) {
            Mask required=((1U<<g.c)-1) ^ (1U<<i);
            check(covered[i][0]==required && covered[i][1]==required,"uncovered ports");
            ports+=2*(g.c-1);
        }
    }
    check(!std::getline(proof,line),"unexpected record");
    std::cout << graphs << ' ' << eligible << ' ' << rows << ' ' << ports << '\n';
}
