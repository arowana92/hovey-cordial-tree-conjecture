// Exhaust the labelings of one tree with one marked edge at orders k and k+1.
#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>

struct Search {
    int k,n,mark,bias;
    std::array<int,12> parent{},label{},vertices{},edges{};
    bool visit(int v,bool repeated) {
        if (v==n) {
            std::array<int,10> vc{},ec{};
            for (int i=0;i<n;++i) {
                ++vc[label[i]];
                if (i) ++ec[(label[i]+label[parent[i]]+(i==mark ? bias : 0))%k];
            }
            auto a=std::minmax_element(vc.begin(),vc.begin()+k);
            auto b=std::minmax_element(ec.begin(),ec.begin()+k);
            if (*a.second-*a.first>1 || *b.second-*b.first>1)
                throw std::logic_error("unbalanced literal witness");
            return true;
        }
        for (int x=0;x<k;++x) {
            if (vertices[x] && (n==k || repeated)) continue;
            int w=(x+label[parent[v]]+(v==mark ? bias : 0))%k;
            if (edges[w]) continue;
            label[v]=x;
            ++vertices[x]; ++edges[w];
            if (visit(v+1,repeated || vertices[x]==2)) return true;
            --vertices[x]; --edges[w];
        }
        return false;
    }
};

int main() {
    Search s{};
    while (std::cin>>s.k>>s.n>>s.mark) {
        if (s.k<2 || s.k>10 || s.n<s.k || s.n>s.k+1 || s.mark<1 || s.mark>=s.n) return 2;
        for (int i=1;i<s.n;++i)
            if (!(std::cin>>s.parent[i]) || s.parent[i]<0 || s.parent[i]>=i) return 2;
        unsigned failed=0;
        for (s.bias=0;s.bias<s.k;++s.bias) {
            s.vertices.fill(0); s.edges.fill(0);
            s.vertices[0]=1; s.label[0]=0;
            if (!s.visit(1,false)) failed|=1U<<s.bias;
        }
        std::cout<<failed<<'\n';
    }
    return std::cin.eof() ? 0 : 2;
}
