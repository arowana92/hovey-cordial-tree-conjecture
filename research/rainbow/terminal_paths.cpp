// Certify a terminal path forest with one shared parent and a possible
// exceptional parent at its unique shortest arm. Free labels avoid zero.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <utility>
#include <vector>

extern "C" int rainbow_witness(int,const int*,int*);
using Mask = std::uint64_t;

struct Catalog {
    int k;
    long long rows=0, shapes=0, assignments=0;
    std::vector<int> units;

    bool representative(int x,int y) const {
        for (int u : units)
            if (std::pair<int,int>{x*u%k,y*u%k} < std::pair<int,int>{x,y})
                return false;
        return true;
    }
    void certify(const std::vector<int>& lengths) {
        bool mixed=lengths.size()>=2 && lengths[0]<lengths[1];
        std::vector<std::pair<int,int>> todo;
        for (int x=0; x<k; ++x) for (int y=0; y<k; ++y)
            if ((mixed || x==y) && representative(x,y)) todo.emplace_back(x,y);
        std::vector<int> parents,roots,labels(k-1);
        for (int length : lengths) {
            roots.push_back(parents.size());
            for (int i=0; i<length; ++i)
                parents.push_back(i ? int(parents.size())-1 : -1);
        }
        ++shapes;
        assignments+=todo.size();
        std::cout << k << ' ' << lengths.size();
        for (int length : lengths) std::cout << ' ' << length;
        while (!todo.empty()) {
            auto [x,y]=todo.back();
            for (int root : roots) parents[root]=-1-y;
            parents[0]=-1-x;
            if (rainbow_witness(k,parents.data(),labels.data())!=1)
                throw std::runtime_error("unresolved path forest");
            std::cout << ' ';
            for (int value : labels) std::cout << char('!'+value);
            ++rows;
            Mask internal=0;
            for (int i=0; i<k-1; ++i) if (parents[i]>=0)
                internal |= Mask(1)<<((labels[i]+labels[parents[i]])%k);
            auto works = [&](std::pair<int,int> input) {
                Mask used=internal;
                for (int root : roots) {
                    int w=(labels[root]+(root ? input.second : input.first))%k;
                    Mask bit=Mask(1)<<w;
                    if (used & bit) return false;
                    used |= bit;
                }
                return true;
            };
            todo.erase(std::remove_if(todo.begin(),todo.end(),works),todo.end());
        }
        std::cout << '\n';
    }

    void generate(std::vector<int>& lengths,int free,int minimum) {
        if (!free) { certify(lengths); return; }
        for (int length=minimum; length<=free; ++length) {
            lengths.push_back(length);
            generate(lengths,free-length,length);
            lengths.pop_back();
        }
    }
};

int main(int argc,char** argv) {
    if (argc!=2) return 2;
    int k=std::stoi(argv[1]);
    if (k<2 || k>63) return 2;
    Catalog search{k};
    for (int u=1; u<k; ++u) if (std::gcd(u,k)==1) search.units.push_back(u);
    std::vector<int> lengths;
    search.generate(lengths,k-1,1);
    std::cerr << k << ' ' << search.shapes << ' ' << search.rows
              << ' ' << search.assignments << '\n';
}
