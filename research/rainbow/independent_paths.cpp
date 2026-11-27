// Cover every tuple of boundary labels for a fixed number of disjoint paths.
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
extern "C" int rainbow_witness(int, const int*, int*);

struct Catalog {
    int k, count;
    std::vector<int> powers{1}, orbit, representatives;

    Catalog(int modulus, int paths): k(modulus), count(paths) {
        for (int i=0; i<count; ++i) powers.push_back(k*powers.back());
        orbit.assign(powers.back(),-1);
        for (int code=0; code<powers.back(); ++code) {
            if (orbit[code]!=-1) continue;
            int id=representatives.size();
            representatives.push_back(code);
            for (int u=1; u<k; ++u) if (std::gcd(u,k)==1) {
                int target=0;
                for (int place=0; place<count; ++place)
                    target+=powers[place]*(u*(code/powers[place]%k)%k);
                orbit[target]=id;
            }
        }
    }
    void cover(const std::vector<int>& lengths) const {
        std::vector<int> roots, parents, labels(k-1);
        for (int n : lengths) {
            roots.push_back(parents.size());
            parents.push_back(-1);
            for (int i=1; i<n; ++i) parents.push_back(int(parents.size())-1);
        }
        std::vector<char> covered(representatives.size());
        std::cout << k << ' ' << count;
        for (int n : lengths) std::cout << ' ' << n;
        for (int code : representatives) {
            if (covered[orbit[code]]) continue;
            for (int i=0; i<count; ++i) parents[roots[i]]=-1-code/powers[i]%k;
            if (rainbow_witness(k,parents.data(),labels.data())!=1)
                throw std::runtime_error("missing path witness at boundary "+std::to_string(code));
            std::cout << ' ';
            for (int x : labels) std::cout << char('!'+x);
            std::vector<bool> used(k);
            for (int j=0; j<k-1; ++j)
                if (parents[j]>=0) used[(labels[j]+labels[parents[j]])%k]=true;
            std::vector<int> available;
            for (int w=0; w<k; ++w) if (!used[w]) available.push_back(w);
            if (int(available.size())!=count+1) throw std::logic_error("internal weights");
            std::vector<std::vector<int>> digit(count,std::vector<int>(k));
            for (int i=0; i<count; ++i) for (int w : available)
                digit[i][w]=powers[i]*((k+w-labels[roots[i]])%k);
            do {
                int boundary=0;
                for (int i=0; i<count; ++i) boundary+=digit[i][available[i]];
                covered[orbit[boundary]]=true;
            } while (std::next_permutation(available.begin(),available.end()));
            if (!covered[orbit[code]]) throw std::logic_error("witness missed its input");
        }
        std::cout << std::endl;
    }
    void generate(std::vector<int>& lengths,int remaining,int least) const {
        int slots=count-int(lengths.size());
        if (slots==1) {
            if (remaining>=least) {
                lengths.push_back(remaining);
                cover(lengths);
                lengths.pop_back();
            }
            return;
        }
        for (int n=least; n*slots<=remaining; ++n) {
            lengths.push_back(n);
            generate(lengths,remaining-n,n);
            lengths.pop_back();
        }
    }
};
int main(int argc,char** argv) {
    if (argc!=3) return 2;
    int k=std::stoi(argv[1]), count=std::stoi(argv[2]);
    if (k<2 || k>30 || count<1 || count>6) return 2;
    Catalog catalog{k,count};
    std::vector<int> lengths;
    catalog.generate(lengths,catalog.k-1,1);
}
