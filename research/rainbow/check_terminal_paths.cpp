// Independently check the two-center bases and every boundary-color orbit
// on terminal paths. In the latter test a row is evaluated at all common colors.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Mask = std::uint64_t;
void require(bool ok,const char* reason) {
    if (!ok) throw std::runtime_error(reason);
}
std::vector<long long> partition_counts(int k) {
    std::vector<long long> counts(k+1,0);
    counts[0]=1;
    for (int part=1; part<=k; ++part)
        for (int n=part; n<=k; ++n) counts[n]+=counts[n-part];
    return counts;
}
std::vector<int> permutation(const std::string& word,int k) {
    require(int(word.size())==k-1,"wrong label count");
    std::vector<int> f{0};
    Mask used=1;
    for (char c : word) {
        int x=c-'!';
        require(0<x && x<k && !(used&(Mask(1)<<x)),"bad vertex label");
        used |= Mask(1)<<x;
        f.push_back(x);
    }
    return f;
}

void paths(int k) {
    int classes=0;
    std::vector<int> orbit(k*k,-1);
    for (int x=0; x<k; ++x) for (int y=0; y<k; ++y) {
        if (orbit[k*x+y]>=0) continue;
        for (int u=1; u<k; ++u) if (std::gcd(k,u)==1)
            orbit[k*(u*x%k)+u*y%k]=classes;
        ++classes;
    }
    Mask all=(Mask(1)<<k)-1;
    std::vector<int> previous;
    long long shapes=0, rows=0, raw=0, quotient=0;
    std::string line;
    while (std::getline(std::cin,line)) {
        std::istringstream input(line);
        int modulus,parts;
        require(bool(input>>modulus>>parts) && modulus==k && parts>0 && parts<k,"bad shape");
        std::vector<int> legs(parts);
        for (int& length : legs) require(bool(input>>length) && length>0,"invalid length");
        require(legs>previous && std::is_sorted(legs.begin(),legs.end()) &&
                std::accumulate(legs.begin(),legs.end(),0)==k-1,"repeated or invalid partition");
        previous=legs;
        bool mixed=parts>=2 && legs[0]<legs[1];
        std::vector<bool> covered(classes,false);
        std::string word;
        while (input>>word) {
            auto f=permutation(word,k);
            int v=1;
            Mask weights=0,other_roots=0;
            for (int length : legs) {
                if (v!=1) other_roots |= Mask(1)<<f[v];
                for (int j=v+1; j<v+length; ++j) {
                    Mask bit=Mask(1)<<((f[j]+f[j-1])%k);
                    require(!(weights&bit),"repeated internal weight");
                    weights |= bit;
                }
                v+=length;
            }
            for (int y=0; y<k; ++y) {
                Mask entering=((other_roots<<y)|(other_roots>>(k-y)))&all;
                if (entering&weights) continue;
                for (Mask free=all^(entering|weights); free; free &= free-1) {
                    int x=(__builtin_ctzll(free)-f[1]+k)%k;
                    covered[orbit[k*x+y]]=true;
                }
            }
            ++rows;
        }
        std::vector<bool> requested(classes,mixed);
        if (!mixed) for (int y=0; y<k; ++y) requested[orbit[k*y+y]]=true;
        for (int j=0; j<classes; ++j) if (requested[j]) {
            require(covered[j],"missing boundary assignment");
            ++quotient;
        }
        raw += mixed ? k*k : k;
        ++shapes;
    }
    require(shapes==partition_counts(k)[k-1],"missing partition");
    std::cout << k << ' ' << shapes << ' ' << rows << ' ' << quotient << ' ' << raw << '\n';
}

std::vector<int> lengths(Mask key,int k) {
    std::vector<int> result;
    int last=0;
    for (int end=1; key; ++end,key>>=1) if (key&1) {
        require(end<k,"side too long");
        result.push_back(end-last);
        last=end;
    }
    require(result.size()>=2 && std::is_sorted(result.begin(),result.end()),"invalid arm list");
    return result;
}

void bases(int k) {
    long long count=0;
    std::pair<Mask,Mask> previous{0,0};
    std::string line;
    while (std::getline(std::cin,line)) {
        std::istringstream record(line);
        Mask a,b;
        std::string word,extra;
        require(bool(record>>a>>b>>word) && !(record>>extra),"invalid base");
        require(a<=b && previous<std::make_pair(a,b),"repeated or unordered base");
        previous={a,b};
        auto left=lengths(a,k),right=lengths(b,k),f=permutation(word,k);
        int gap=k-1-std::accumulate(left.begin(),left.end(),0)
                   -std::accumulate(right.begin(),right.end(),0);
        require(gap>=1,"invalid connector");
        Mask weights=0;
        auto edge=[&](int u,int v) {
            Mask bit=Mask(1)<<((f[u]+f[v])%k);
            require(!(weights&bit),"repeated tree weight");
            weights |= bit;
        };
        for (int j=1; j<=gap; ++j) edge(j-1,j);
        int next=gap+1;
        for (const auto* side : {&left,&right}) {
            for (int length : *side) {
                edge(side==&left ? 0 : gap,next);
                for (int v=next+1; v<next+length; ++v) edge(v-1,v);
                next+=length;
            }
        }
        require(next==k,"wrong base order");
        ++count;
    }
    auto part=partition_counts(k);
    long long expected=0;
    for (int a=2; 2*a<=k-2; ++a) for (int b=a; a+b<=k-2; ++b) {
        long long na=part[a]-1,nb=part[b]-1;
        expected += a==b ? na*(na+1)/2 : na*nb;
    }
    require(count==expected,"missing two-center base");
    std::cout << k << ' ' << count << '\n';
}
int main(int argc,char** argv) {
    if (argc!=3) return 2;
    int k=std::stoi(argv[2]);
    if (k<2 || k>63) return 2;
    if (std::string(argv[1])=="paths") paths(k);
    else if (std::string(argv[1])=="bases") bases(k);
    else return 2;
}
