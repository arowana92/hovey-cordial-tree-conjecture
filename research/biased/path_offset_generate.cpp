// Enumerate necklaces of cyclic first differences and produce a concrete vertex permutation.
#include <array>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>

struct Generator {
    int k, full;
    std::array<int,16> d{}, b{}, x{};
    std::uint64_t count = 0;
    std::FILE* file;
    int part=0, parts=1;
    bool affine=false;
    int products[16][16]{}, unit_list[16]{}, units=0, minimum[16]{};
    bool least() const {
        for (int i=1;i<=k;++i) for (int idx=0;idx<units;++idx) {
            int u=unit_list[idx];
            if (products[u][d[i]]<d[1]) return false;
            if (products[u][d[i]]!=d[1]) continue;
            for (int step : {-1,1}) {
                int j=i;
                for (int t=2;t<=k;++t) {
                    j+=step;
                    if (j==0) j=k;
                    if (j>k) j=1;
                    int other=products[u][d[j]];
                    if (other<d[t]) return false;
                    if (other>d[t]) break;
                }
            }
        }
        return true;
    }

    bool path(int i, int vertices, int weights) {
        if (i==k) return true;
        int shift=(x[i-1]+b[i])%k, unused=full^weights;
        int choices=(full^vertices)&((unused>>shift)|(unused<<(k-shift)));
        for (; choices; choices&=choices-1) {
            int v=__builtin_ctz(static_cast<unsigned>(choices)), w=(v+shift)%k;
            x[i]=v;
            if (path(i+1,vertices|(1<<v),weights|(1<<w))) return true;
        }
        return false;
    }

    void write(std::uint64_t word) {
        unsigned char bytes[8];
        for (int i=0;i<8;++i) bytes[i]=static_cast<unsigned char>(word>>(8*i));
        if (std::fwrite(bytes,1,8,file)!=8) throw std::runtime_error("write failure");
    }

    void emit() {
        if (affine && !least()) return;
        if (!path(1,1,0)) {
            std::cerr<<"no witness for offsets";
            for (int i=0;i<k;++i) std::cerr<<" "<<b[i];
            throw std::runtime_error(" — no complete catalog");
        }
        std::uint64_t word=0, labels=0;
        for (int i=0;i<k;++i) {
            word=k*word+d[i+1];
            labels=16*labels+x[i];
        }
        write(word); write(labels);
        ++count;
    }

    void extend(int pos, int period, int sum) {
        if (pos==k+1) {
            if (k%period==0) emit();
            return;
        }
        // A lexicographically least cyclic word is a prenecklace. The next digit
        // repeats its period or starts a new, longer Lyndon prefix.
        int floor=d[pos-period], lo=floor, hi=k-1;
        if (pos==k-1) {
            b[k-1]=(k*(k-1)/2-sum%k+k)%k;
            lo=hi=(b[k-1]-b[k-2]+k)%k;
        }
        if (pos==k) lo=hi=(k-b[k-1])%k;
        for (int digit=lo;digit<=hi;++digit) {
            if (digit<floor) continue;
            if (affine && pos>1) {
                if (minimum[digit]<d[1]) continue;
            }
            d[pos]=digit;
            if (affine && pos==5) {
                int code=0;
                for (int i=1;i<=5;++i) code=code*k+d[i];
                if (code%parts!=part) continue;
            }
            int new_sum=sum;
            if (pos<k-1) {
                b[pos]=(b[pos-1]+digit)%k;
                new_sum+=b[pos];
            }
            extend(pos+1,digit==floor?period:pos,new_sum);
        }
    }
};

int main(int argc,char** argv) {
    if (argc!=3 && argc!=5) return 2;
    int k=std::stoi(argv[1]);
    if (k<3 || k>12) return 2;
    std::FILE* out=std::fopen(argv[2],"wb");
    if (!out) return 1;
    Generator gen{k,(1<<k)-1,{}, {}, {},0,out};
    if (argc==5) {
        gen.part=std::stoi(argv[3]);
        gen.parts=std::stoi(argv[4]);
        if (k<5 || gen.parts<1 || gen.part<0 || gen.part>=gen.parts) return 2;
        gen.affine=true;
        for (int u=1;u<k;++u) if (std::gcd(u,k)==1) {
            gen.unit_list[gen.units++]=u;
            for (int d=0;d<k;++d) gen.products[u][d]=u*d%k;
        }
        for (int d=1;d<k;++d) gen.minimum[d]=std::gcd(d,k);
    }
    gen.extend(1,1,0);
    std::cout<<"k="<<k<<" records="<<gen.count<<"\n";
    return std::fclose(out)!=0;
}
