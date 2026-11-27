// Certificates for opening a cycle with one pendant path at a prescribed edge.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

using Mask = std::uint64_t;
constexpr int harmonious = -3, transfer = -2, uniform_edges = -1;

struct Search {
    int k,cycle,kind,vertices,budget;
    int pin=-1, prescribed=0;
    std::uint32_t seed;
    Mask all;
    std::vector<int> label,order,ports;
    std::vector<std::vector<int>> edges,before;

    Search(int n,int c,int mode):
        k(n),cycle(c),kind(mode),vertices(mode==transfer ? k : k-1),
        seed(1991+65537*k+1997*c+mode),all((Mask(1)<<k)-1),label(k),
        ports(vertices),edges(vertices),before(vertices) {}

    unsigned random() {
        seed ^= seed<<13;
        seed ^= seed>>17;
        return seed ^= seed<<5;
    }

    bool place(int i,Mask free,Mask weights,bool spare_zero) {
        if (--budget<0) return false;
        if (i==vertices) return true;
        int v=order[i];
        Mask choices=ports[v] ? free&weights : free;
        if (v==pin) choices&=Mask(1)<<prescribed;
        if (kind==harmonious && v==0) choices&=Mask(1)<<(k/2);
        Mask available=weights|Mask(spare_zero);
        for (int u:before[v]) {
            int a=label[u];
            choices&=(available>>a)|(available<<(k-a));
        }
        Mask low=(Mask(1)<<(random()%k))-1;
        for (Mask part : {choices&~low,choices&low}) for (;part;part&=part-1) {
            int z=__builtin_ctzll(part);
            Mask rest=weights;
            bool extra=spare_zero,ok=true;
            if (ports[v]) rest^=Mask(1)<<z;
            for (int u:before[v]) {
                int w=(z+label[u])%k;
                if (w==0 && extra) extra=false;
                else if (rest&(Mask(1)<<w)) rest^=Mask(1)<<w;
                else { ok=false; break; }
            }
            label[v]=z;
            if (ok && place(i+1,free^(Mask(1)<<z),rest,extra)) return true;
            if (budget<0) return false;
        }
        return false;
    }

    bool next() {
        int cut=kind==transfer ? int(random()%cycle) : kind;
        for (auto& row:edges) row.clear();
        std::fill(ports.begin(),ports.end(),0);
        for (int i=0;i<vertices;++i) {
            int j=i<cycle ? (i+1)%cycle : i==cycle ? 0 : i-1;
            if (i!=cut) {
                edges[i].push_back(j);
                edges[j].push_back(i);
            } else if (kind>=0) {
                ports[i]=ports[j]=1;
            }
        }
        int start=pin>=0 ? pin : int(random()%vertices);
        order={start};
        std::vector<int> rank(vertices,-1);
        rank[start]=0;
        for (int i=0;i<vertices;++i) {
            int a=order[i];
            before[a].clear();
            for (int b:edges[a]) {
                if (rank[b]<0) {
                    rank[b]=order.size();
                    order.push_back(b);
                }
                if (rank[b]<i) before[a].push_back(b);
            }
        }
        budget=3000;
        if (!place(0,kind==transfer ? all : all-1,all,kind>=0)) return false;
        if (kind==harmonious) label.back()=0;
        else if (kind!=transfer) label.back()=k-label[0];
        return true;
    }

    std::vector<int> counts() const {
        std::vector<int> result(k);
        for (int i=0;i<k;++i) {
            int j=i<cycle ? (i+1)%cycle : i==cycle ? 0 : i-1;
            ++result[(label[i]+label[j])%k];
        }
        return result;
    }

    void emit() const {
        std::cout<<k<<' '<<cycle<<' '<<kind;
        for (int x:label) std::cout<<' '<<x;
        std::cout<<'\n';
    }
};

bool reaches_all(const std::vector<Mask>& out,int root) {
    Mask seen=Mask(1)<<root,old=0;
    while (old!=seen) {
        old=seen;
        for (Mask bits=seen;bits;bits&=bits-1) seen|=out[__builtin_ctzll(bits)];
    }
    return seen==(Mask(1)<<out.size())-1;
}

void transfers(int k,int c) {
    Search search(k,c,transfer);
    std::vector<int> orbit(k);
    std::vector<int> types;
    for (int i=0;i<k;++i) {
        int d=std::gcd(k,i);
        auto pos=std::find(types.begin(),types.end(),d);
        orbit[i]=pos-types.begin();
        if (pos==types.end()) types.push_back(d);
    }
    std::vector<std::vector<Mask>> graph(c,std::vector<Mask>(types.size())),reverse=graph;
    std::vector<bool> ready(c);
    for (int i=0;i<200000;++i) if (search.next()) {
        auto bins=search.counts();
        int dup=std::find(bins.begin(),bins.end(),2)-bins.begin();
        int gap=std::find(bins.begin(),bins.end(),0)-bins.begin();
        if (dup==k || gap==k) throw std::runtime_error("expected a single transfer");
        bool used=false;
        for (int v=0;v<c;++v) if (!ready[v]) {
            int offset=2*(k-search.label[v]);
            int a=orbit[(dup+offset)%k],b=orbit[(gap+offset)%k];
            if (!(graph[v][a]&(Mask(1)<<b))) used=true;
            graph[v][a]|=Mask(1)<<b;
            reverse[v][b]|=Mask(1)<<a;
            ready[v]=reaches_all(graph[v],orbit[0]) && reaches_all(reverse[v],orbit[0]);
        }
        if (used) search.emit();
        bool covered=true;
        for (int v=0;v<c;++v) if (!ready[v] && !ready[(v+1)%c]) covered=false;
        if (covered) return;
    }
    throw std::runtime_error("transfer search incomplete");
}

void vertex_witnesses(int k,int c,int cut) {
    Search search(k,c,cut);
    if (k==5 && cut>=0) {
        // Try all sets of locations for the duplicated label at this small order.
        for (int extra=1;extra<k;++extra) {
            search.label={1,2,3,4,extra};
            std::sort(search.label.begin(),search.label.end());
            do {
                auto bins=search.counts();
                int a=search.label[cut],b=search.label[(cut+1)%c];
                --bins[(a+b)%k];
                ++bins[a];
                ++bins[b];
                --bins[0];
                if (std::count(bins.begin(),bins.end(),1)==k) {
                    search.emit();
                    return;
                }
            } while (std::next_permutation(search.label.begin(),search.label.end()));
        }
        throw std::runtime_error("small cut unresolved");
    }
    Mask target=0;
    for (int i=1;i<k;++i) target|=Mask(1)<<std::gcd(k,i);
    std::vector<Mask> hit(c);
    for (int i=0;i<200000;++i) {
        if (cut==uniform_edges) {
            // A unit can move any member of this class to its gcd with k.
            search.pin=std::find_if(hit.begin(),hit.end(),[&](Mask row){return row!=target;})-hit.begin();
            search.prescribed=__builtin_ctzll(target&~hit[search.pin]);
        }
        if (!search.next()) continue;
        if (cut==harmonious || cut>=0) { search.emit(); return; }
        bool used=false;
        for (int v=0;v<c;++v) {
            Mask bit=Mask(1)<<std::gcd(k,search.label[v]);
            if (!(hit[v]&bit)) used=true;
            hit[v]|=bit;
        }
        if (used) search.emit();
        if (std::all_of(hit.begin(),hit.end(),[&](Mask row){return row==target;})) return;
    }
    throw std::runtime_error("vertex search incomplete");
}

// The order-six triangle with a three-edge tail has no harmonious
// labeling. Check the actual opening with prescribed old labels 0 and d.
void six_triangle() {
    Search search(6,3,harmonious);
    for (int cut=0;cut<3;++cut) for (int d=0;d<6;++d) {
        std::iota(search.label.begin(),search.label.end(),0);
        do {
            auto counts=search.counts();
            int x=search.label[cut],y=search.label[(cut+1)%3];
            --counts[(x+y)%6];
            ++counts[x];
            ++counts[(y+d)%6];
            --counts[d];
            if (std::count(counts.begin(),counts.end(),1)==6) {
                std::cout<<"6 3 -4 "<<cut<<' '<<d;
                for (int z:search.label) std::cout<<' '<<z;
                std::cout<<'\n';
                break;
            }
        } while (std::next_permutation(search.label.begin(),search.label.end()));
    }
}

int main(int argc,char** argv) {
    if (argc!=2) return 2;
    int k=std::stoi(argv[1]);
    if (k<4 || k>63) return 2;
    for (int c=3;c<k;++c) {
        if (k==6 && c==3) {
            six_triangle();
        } else if (k%2==0) {
            vertex_witnesses(k,c,harmonious);
        } else {
            transfers(k,c);
            for (int cut=uniform_edges;cut<c;++cut) vertex_witnesses(k,c,cut);
        }
    }
}
