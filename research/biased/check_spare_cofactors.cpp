// Two coefficient calculations for lists of r+1 at modulus 27.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using Key = std::uint64_t;
using Mask = std::uint32_t;
constexpr int k=27, max_rows=25, max_types=7;
using Weights=std::array<int,max_types-1>;

struct Term {
    Key key;
    int degree;
    bool positive;
    Weights predecessor;
};

// x_0=1. A point stores exponents of x_1,...,x_{m-1} in base 64.
struct Terms {
    int dim;
    Key guards=0;
    std::array<int,max_rows+1> end{};
    std::vector<Term> terms;
    std::unordered_map<Key,int> index;

    explicit Terms(int dimension) : dim(dimension) {
        for (int i=0; i<dim; ++i) guards |= Key{32} << (6*i);
        for (int n=0; n<=max_rows; ++n) {
            layer(n,n,0,0,true);
            end[n]=static_cast<int>(terms.size());
        }
    }
    void layer(int degree,int remaining,int i,Key key,bool positive) {
        if (i<dim) {
            for (int a=0; a<=remaining; ++a)
                layer(degree,remaining-a,i+1,key|(Key(a)<<(6*i)),positive && a>0);
        } else if (remaining==0) {
            Term t{key,degree,positive,{}};
            for (int j=0; j<dim; ++j) {
                Key unit=Key{1}<<(6*j);
                t.predecessor[j]=(key/unit)%64 ? index.at(key-unit) : -1;
            }
            index.emplace(key,static_cast<int>(terms.size()));
            terms.push_back(t);
        }
    }
};

std::vector<Mask> orbit(Mask support) {
    std::vector<Mask> images;
    for (int u=1; u<k; ++u) if (u%3) {
        Mask m=0;
        for (int i=0; i<k; ++i) if (support&(1u<<i)) m |= 1u<<(u*i%k);
        for (int j=0; j<k; ++j) {
            images.push_back(m);
            m=(m>>1)|((m&1)<<26);
        }
    }
    std::sort(images.begin(),images.end());
    images.erase(std::unique(images.begin(),images.end()),images.end());
    return images;
}
long long binomial(int n,int m) {
    long long value=1;
    for (int j=1; j<=m; ++j) value=value*(n-j+1)/j;
    return value;
}

struct Calculation {
    const Terms& grid;
    int field, root;
    std::array<int,k> power{};
    std::array<Weights,k> weight{};
    std::vector<int> phase;
    std::vector<std::vector<int>> prefix;

    Calculation(const Terms& g,Mask mask,int prime,int z,int last) :
        grid(g),field(prime),root(z),phase(g.terms.size()) {
        power[0]=1;
        for (int j=1; j<k; ++j) power[j]=power[j-1]*root%field;
        if (power[9]==1 || power.back()*root%field!=1)
            throw std::logic_error("root lacks order 27");
        std::vector<int> shifts;
        for (int s=1; s<k; ++s) if (mask&(1u<<s)) shifts.push_back(s);
        for (int j=0; j<k; ++j) for (int s=0; s<g.dim; ++s)
            weight[j][s]=power[j*shifts.at(s)%k];
        for (std::size_t i=0; i<g.terms.size(); ++i) {
            Key v=g.terms[i].key;
            for (int s : shifts) { phase[i]+=s*(v%64); v/=64; }
            phase[i]%=k;
        }
        prefix.push_back({1});
        for (int n=1; n<=last+1; ++n) {
            const auto& old=prefix.back();
            std::vector<int> next(g.end[std::min(n,max_rows)]);
            for (int i=0; i<static_cast<int>(next.size()); ++i) {
                int value=i<static_cast<int>(old.size()) ? old[i] : 0;
                for (int s=0; s<g.dim; ++s) {
                    int before=g.terms[i].predecessor[s];
                    if (before>=0) value+=weight[n-1][s]*old[before];
                }
                next[i]=value%field;
            }
            prefix.push_back(std::move(next));
        }
    }

    // Divide the product over 0..r by its linear factor at the absent exponent j.
    void divide(int r,int j,std::vector<int>& pending) const {
        std::vector<int> q(pending.back()+1);
        for (int i=0; i<static_cast<int>(q.size()); ++i) {
            int a=prefix[r+1][i];
            for (int s=0; s<grid.dim; ++s) {
                int before=grid.terms[i].predecessor[s];
                if (before>=0) a-=weight[j][s]*q[before];
            }
            q[i]=(a%field+field)%field;
        }
        pending.erase(std::remove_if(pending.begin(),pending.end(),
                      [&](int i){return q[i]!=0;}),pending.end());
    }

    // Multiply the independent products on [0,j) and (j,r], shifting the second.
    bool split(int r,int j,int target) const {
        const int short_len=std::min(j,r-j), long_len=r-short_len;
        const Key key=grid.terms[target].key;
        long long result=0;
        for (int i=0; i<grid.end[short_len]; ++i) {
            Key part=grid.terms[i].key;
            if (((key+grid.guards-part)&grid.guards)!=grid.guards) continue;
            if (grid.terms[target].degree-grid.terms[i].degree>long_len) continue;
            int other=grid.index.at(key-part);
            int phase_right= j<=r-j ? phase[other] : phase[i];
            result+=static_cast<long long>(prefix[short_len][i])*prefix[long_len][other]*
                    power[(j+1)*phase_right%k];
        }
        return result%field!=0;
    }
    void cover(int r,bool convolution,std::vector<int>& pending) const {
        for (int j=0; j<=r && !pending.empty(); ++j) {
            if (convolution)
                pending.erase(std::remove_if(pending.begin(),pending.end(),
                              [&](int i){return split(r,j,i);}),pending.end());
            else divide(r,j,pending);
        }
    }
};

int main(int argc,char** argv) {
    if (argc!=5) return 2;
    std::string mode=argv[1];
    int m=std::atoi(argv[2]), low=std::atoi(argv[3]), high=std::atoi(argv[4]);
    if ((mode!="split" && mode!="divide") || m<2 || m>max_types || low<1 ||
        low>high || high>max_rows) return 2;
    Terms grid(m-1);
    long long supports=0, cases=0, weighted=0, second_field=0;
    int representatives=0;
    auto visit=[&](auto&& self, int left, int start, Mask mask)->void {
        if (left) {
            for (int s=start; s<=k-left; ++s) self(self,left-1,s+1,mask|(1u<<s));
            return;
        }
        auto images=orbit(mask);
        // The least numeric mask may omit zero. Select the least anchored image.
        auto first=std::find_if(images.begin(),images.end(),[](Mask x){return x&1;});
        if (first==images.end() || *first!=mask) return;
        ++representatives;
        supports+=images.size();
        Calculation main(grid,mask,487,19,high);
        for (int r=std::max(low,m); r<=high; ++r) {
            std::vector<int> pending;
            for (int i=0; i<grid.end[r-1]; ++i)
                if (grid.terms[i].positive) pending.push_back(i);
            if (static_cast<long long>(pending.size())!=binomial(r-1,m-1))
                throw std::logic_error("missing multiplicities");
            cases+=pending.size();
            weighted+=static_cast<long long>(images.size())*pending.size();
            main.cover(r,mode=="split",pending);
            if (!pending.empty()) {
                second_field+=pending.size();
                Calculation backup(grid,mask,109,3,r);
                backup.cover(r,mode=="split",pending);
                if (!pending.empty()) throw std::runtime_error("unresolved cofactor");
            }
        }
    };
    visit(visit,m-1,1,1);
    if (supports!=binomial(k,m)) throw std::logic_error("missing support");
    std::cout<<"types "<<m<<" orbits "<<representatives<<" cases "<<cases
             <<" literal multisets "<<weighted<<" backup "<<second_field<<"\n";
}
