// Search for uniform replacements of an edge by three paths meeting at a joint.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

constexpr int k=26;
using Mask=std::uint32_t;
struct Search {
    int h, tip=0, remaining_steps=0;
    std::array<std::vector<int>,k+2> neighbors;
    std::array<int,k+2> label;
    std::array<int,k> count{};
    std::mt19937 random;

    Search(int left,int right,int arm,int difference)
        : h(difference), random(k+h*72+right*111+left*142) {
        label.fill(-1);
        label[k]=0;
        label[k+1]=h;
        int next=1;
        auto edge=[&](int a,int b) { neighbors[a].push_back(b); neighbors[b].push_back(a); };
        for (auto [length,endpoint] : {std::pair{left,k},{right,k+1},{arm,-1}}) {
            int previous=0;
            for (int j=0; j<length; ++j) {
                edge(previous,next);
                previous=next++;
            }
            if (endpoint>=0) edge(previous,endpoint);
            else tip=previous;
        }
    }
    bool place(int v,int x) {
        label[v]=x;
        bool allowed=true;
        for (int p : neighbors[v]) if (label[p]>=0) {
            int w=(x+label[p])%k;
            if (++count[w]>1+(w==h)) allowed=false;
        }
        return allowed;
    }
    void undo(int v) {
        for (int p : neighbors[v]) if (label[p]>=0) --count[(label[v]+label[p])%k];
        label[v]=-1;
    }
    bool solve(Mask unused) {
        if (--remaining_steps<0) return false;
        if (!unused) return true;
        int selected=-1, best=k+1;
        Mask options=0;
        for (int v=0; v<k; ++v) {
            if (label[v]>=0 || std::none_of(neighbors[v].begin(),neighbors[v].end(),
                                            [&](int p){return label[p]>=0;})) continue;
            Mask valid=0;
            for (Mask m=unused; m; m&=m-1) {
                int x=__builtin_ctz(m);
                if (place(v,x)) valid|=Mask(1)<<x;
                undo(v);
            }
            int size=__builtin_popcount(valid);
            if (!size) return false;
            if (size<best) { best=size; selected=v; options=valid; }
        }
        std::vector<int> choices;
        for (Mask m=options; m; m&=m-1) choices.push_back(__builtin_ctz(m));
        for (int i=int(choices.size())-1; i>0; --i)
            std::swap(choices[i],choices[random()%(i+1)]);
        for (int x : choices) {
            if (remaining_steps<=0) break;
            place(selected,x);
            if (solve(unused^(Mask(1)<<x))) return true;
            undo(selected);
        }
        return false;
    }
    bool run() {
        for (int attempt=0; attempt<100; ++attempt) for (int joint=0; joint<k; ++joint) {
            int end=(joint+k/2)%k;
            bool joint_ok=place(0,joint);
            bool tip_ok=place(tip,end);
            remaining_steps=1500+30*attempt;
            Mask free=((Mask(1)<<k)-1)^(Mask(1)<<joint)^(Mask(1)<<end);
            if (joint_ok && tip_ok && solve(free)) return true;
            undo(tip);
            undo(0);
        }
        return false;
    }
};
int main() {
    for (int arm=1; arm<k; ++arm) for (int left=0; 2*left<=k-arm-1; ++left) {
        int right=k-arm-left-1;
        for (int h : {0,1,2,13}) {
            Search search(left,right,arm,h);
            if (!search.run()) return 1;
            std::cout<<left<<' '<<right<<' '<<arm<<' '<<h;
            for (int i=0; i<k; ++i) std::cout<<' '<<search.label[i];
            std::cout<<'\n';
        }
    }
}
