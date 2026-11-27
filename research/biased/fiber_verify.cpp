// Independently verify half-turn covers from the actual integer endpoint sums.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>

using Word = std::uint64_t;
using Digits = std::array<int,16>;
void require(bool ok,const char* msg) { if (!ok) throw std::runtime_error(msg); }
Word get(FILE* input,int bytes) {
    unsigned char data[8];
    require(std::fread(data,1,bytes,input)==static_cast<unsigned>(bytes),"truncated record");
    Word value=0;
    for (int j=bytes-1;j>=0;--j) value=256*value+data[j];
    return value;
}

struct Forest {
    int n, next=0, bit, leaves=0;
    Word word;
    Digits parent{};
    std::vector<int> roots,sizes;
    int take() { require(bit>=0,"missing closing bit"); return (word>>bit--)&1; }
    std::pair<int,Word> tree(int p) {
        int start=bit, v=next++;
        require(v<n && take()==1,"invalid opening bit");
        parent[v]=p;
        std::pair<int,Word> last{};
        while (bit>=0 && ((word>>bit)&1)) {
            auto child=tree(v);
            require(last<=child,"noncanonical children");
            last=child;
        }
        if (!last.first) ++leaves;
        require(take()==0,"invalid close");
        int length=start-bit;
        return {length/2,(word>>(bit+1))&((Word(1)<<length)-1)};
    }
    Forest(int count,Word code): n(count),bit(2*n-1),word(code) {
        require(!(word>>(2*n)),"extra shape bits");
        std::pair<int,Word> last{};
        while (bit>=0) {
            roots.push_back(next);
            auto component=tree(-1);
            require(last<=component,"noncanonical components");
            sizes.push_back(component.first);last=component;
        }
        require(next==n,"wrong forest order");
    }
    int profile(int raw,int m,bool active) {
        int prefix=0,runs=0,color=-1,previous=-1;
        for (unsigned j=0;j<roots.size();++j) {
            if (sizes[j]>prefix) {color=raw%m;raw/=m;}
            if (color!=previous) {
                require(sizes[j]>=prefix+runs,"inadmissible color run");
                ++runs;
            }
            require(active || color==0,"nonzero base-only boundary");
            parent[roots[j]]=-1-color;
            previous=color;prefix+=sizes[j];
        }
        require(!raw,"extra boundary digits");
        // The low units lift to units at k. Products may introduce a high
        // digit at a boundary; that digit is among the independent offsets.
        int original=0,place=1;
        for (unsigned j=0;j<roots.size();++j) if (sizes[j]>roots[j]) {
            original+=place*(-1-parent[roots[j]]);place*=m;
        }
        std::set<int> orbit;
        for (int u=1;u<m;u+=2) {
            int image=0;
            for (int p=1;p<place;p*=m) image+=p*(u*(original/p%m)%m);
            orbit.insert(image);
        }
        require(original==*orbit.begin(),"noncanonical boundary orbit");
        return orbit.size();
    }
    int expected(int m) const {
        // Count exact sets of changes by their positions, independently of unit orbits.
        int total=0;
        for (unsigned subset=0;subset<(1u<<(sizes.size()-1));++subset) {
            int ways=m, runs=1, prefix=sizes[0];
            for (unsigned j=1;j<sizes.size();++j) {
                if (subset>>(j-1)&1) {
                    if (sizes[j]<prefix+runs) {ways=0;break;}
                    ++runs;ways*=m-1;
                }
                prefix+=sizes[j];
            }
            total+=ways;
        }
        return total;
    }
};

struct Audit {
    int k,m,n,words,assignments;
    std::vector<Word> signs;
    std::array<std::array<Word,2>,128> orth{};
    std::vector<Word> shapes;
    Word low=0,orbits=0,rows=0;
    explicit Audit(int modulus): k(modulus),m(k/2),n(k-1),
        words(std::max(1,(1<<(n-1))/64)),assignments(1<<(n-1)),
        signs(assignments*words) {
        for (int a=0;a<assignments;++a) {
            Word pattern=0;
            for (int b=0;b<64;++b)
                if (__builtin_parity(a&b)) pattern|=Word(1)<<b;
            for (int b=0;b<words;++b)
                signs[a*words+b]=__builtin_parity(a&(b*64)) ? ~pattern : pattern;
        }
        for (int d=0;d<(1<<(m-1));++d)
            for (int h=1;h<(1<<(m-1));++h)
                if (!__builtin_parity(d&h)) orth[d][h/64]|=Word(1)<<(h%64);
    }

    void row(Word packed,const Digits& parent,std::vector<Word>& open) {
        Digits x{}, multiplicity{}, prior{}, a{}, b{};
        prior.fill(-1);
        int pairs=0;
        for (int i=0;i<n;++i) {
            int c=packed&7;packed>>=3;
            require(c<m && multiplicity[c]<(c ? 2 : 1),"invalid low vertex permutation");
            x[i]=c+(c==0 || multiplicity[c] ? m : 0);
            ++multiplicity[c];
            int weight=(x[i]+(parent[i]<0 ? -1-parent[i] : x[parent[i]]))%m;
            int& previous=prior[weight];
            require(previous!=-2,"three equal low weights");
            if (previous>=0) {a[pairs]=previous;b[pairs++]=i;previous=-2;}
            else previous=i;
        }
        require(!packed && pairs==m-1,"wrong fiber shape");
        // Lift the canonical permutation, then swap one pair of equal low
        // digits at a time. Read the required offset-pair parities directly
        // from the integer edge sums in each such permutation.
        auto syndrome=[&](int swap) {
            int highs=0;
            for (int i=0;i<n;++i) {
                auto label=[&](int j) {return (x[j]%m==swap) ? x[j]^m : x[j];};
                int sum=label(i)+(parent[i]<0 ? -1-parent[i] : label(parent[i]));
                highs|=((sum/m)&1)<<i;
            }
            int s=0;
            for (int i=0;i<pairs;++i) s|=(1^((highs>>a[i])&1)^((highs>>b[i])&1))<<i;
            return s;
        };
        int origin=syndrome(-1);
        auto dual=orth[0];
        for (int swap=1;swap<m;++swap) {
            auto allowed=orth[origin^syndrome(swap)];
            dual[0]&=allowed[0];dual[1]&=allowed[1];
        }
        // Every half-turn offset word determines a syndrome. Its difference
        // from origin must annihilate all characters in the dual space.
        // Fix the LAST edge offset to zero using simultaneous translation.
        std::array<int,128> masks{},values{};
        int checks=0;
        for (int j=0;j<2;++j) for (Word left=dual[j];left;left&=left-1) {
            int h=64*j+__builtin_ctzll(left), mask=0;
            for (int v=h;v;v&=v-1) {
                int i=__builtin_ctz(v);
                mask|=(1<<a[i])|(1<<b[i]);
            }
            masks[checks]=mask&(assignments-1);
            values[checks++]=__builtin_parity(h&origin);
        }
        for (int j=0;j<words;++j) if (open[j]) {
            Word hit=open[j];
            for (int t=0;t<checks && hit;++t) {
                Word sign=signs[masks[t]*words+j];
                hit &= values[t] ? sign : ~sign;
            }
            open[j]&=~hit;
        }
    }
    void file(const char* name) {
        FILE* in=std::fopen(name,"rb");
        require(in,"cannot open shard");
        require(get(in,4)==0x314c4246 && get(in,1)==static_cast<unsigned>(k),"invalid header");
        int peek;
        while ((peek=std::getc(in))!=EOF) {
            std::ungetc(peek,in);
            Word code=get(in,8);shapes.push_back(code);
            Forest forest(n,code);
            bool eligible=3*forest.leaves<=2*(k-2);
            Word count=get(in,4);
            std::set<int> profiles;
            int covered=0;
            for (Word j=0;j<count;++j) {
                int raw=get(in,2);
                require(profiles.insert(raw).second,"duplicate profile");
                covered+=forest.profile(raw,m,eligible);
                Word length=get(in,4);
                std::vector<Word> open(words,~Word(0));
                if (assignments<64) open[0]=(Word(1)<<assignments)-1;
                for (Word v=0;v<length;++v) row(get(in,8),forest.parent,open);
                require(std::none_of(open.begin(),open.end(),[](Word x){return x;}),"uncovered offset");
                rows+=length;
            }
            require(covered==(eligible ? forest.expected(m) : 1),"missing low boundary");
            low+=covered;orbits+=count;
        }
        require(!std::ferror(in),"read error");std::fclose(in);
    }
    void finish(bool partial) {
        std::sort(shapes.begin(),shapes.end());
        require(std::adjacent_find(shapes.begin(),shapes.end())==shapes.end(),"repeated shape");
        // Coefficient of the multiset product for rooted forests of order s-1.
        std::vector<Word> r(k+1),ways(k+1);r[1]=1;ways[0]=1;
        for (int s=1;s<k;++s) {
            std::vector<Word> after(k+1);
            for (int j=0;j<k;++j) if (ways[j]) {
                Word multiset=1;
                for (int t=0;j+s*t<k;++t) {
                    after[j+s*t]+=ways[j]*multiset;
                    multiset=multiset*(r[s]+t)/(t+1);
                }
            }
            ways=after;r[s+1]=ways[s];
        }
        require(partial || shapes.size()==r[k],"incomplete forest catalog");
        std::cout<<"k="<<k<<" shapes="<<shapes.size()<<" low inputs="<<low
                 <<" unit orbits="<<orbits<<" offset vectors="<<(low<<n)<<" fiber witnesses="<<rows<<"\n";
    }
};
int main(int argc,char** argv) {
    try {
        if (argc<3) return 2;
        int k=std::stoi(argv[1]);bool partial=std::strcmp(argv[2],"--partial")==0;
        if ((k!=4 && k!=8 && k!=16) || (partial && argc<4)) return 2;
        Audit audit(k);
        for (int i=2+partial;i<argc;++i) audit.file(argv[i]);
        audit.finish(partial);
    } catch (const std::exception& e) { std::cerr<<e.what()<<"\n"; return 1; }
}
