// Verify the independent-path streams from the actual edge and vertex sets.
// The least representative of every ordered boundary tuple is computed digitwise.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

void require(bool condition, const char* reason) {
    if (!condition) throw std::runtime_error(reason);
}

void compositions(int remaining, int parts, std::vector<int>& prefix,
                  std::set<std::vector<int>>& catalog) {
    if (!parts) {
        if (!remaining) {
            auto sorted=prefix;
            std::sort(sorted.begin(),sorted.end());
            catalog.insert(sorted);
        }
        return;
    }
    for (int x=1; x<=remaining-parts+1; ++x) {
        prefix.push_back(x);
        compositions(remaining-x,parts-1,prefix,catalog);
        prefix.pop_back();
    }
}

struct Record {
    const std::vector<int>& min_tuple;
    std::vector<unsigned char>& seen;
    int k, paths;
    const std::vector<int>& first;
    void assign(const std::vector<int>& label, int index, std::uint32_t spare, int code) {
        if (index<0) {
            seen[min_tuple[code]]=1;
            return;
        }
        for (auto bits=spare; bits; bits&=bits-1) {
            int w=__builtin_ctz(bits);
            int parent=(w-label[first[index]]+k)%k;
            assign(label,index-1,spare^(1U<<w),k*code+parent);
        }
    }
    void verify(const std::string& word) {
        require(int(word.size())==k-1,"wrong word length");
        std::uint32_t vertices=1, weights=0;
        std::vector<int> label;
        for (int i=0; i<k-1; ++i) {
            int x=word[i]-'!';
            require(x>=1 && x<k && !(vertices & (1U<<x)), "invalid vertex label");
            vertices |= 1U<<x;
            if (!std::binary_search(first.begin(),first.end(),i)) {
                int w=(label.back()+x)%k;
                require(!(weights & (1U<<w)), "duplicate internal weight");
                weights |= 1U<<w;
            }
            label.push_back(x);
        }
        assign(label,paths-1,((1U<<k)-1)^weights,0);
    }
};

int main(int argc,char** argv) {
    if (argc!=4) return 2;
    int k=std::stoi(argv[1]), paths=std::stoi(argv[2]);
    if (k<2 || k>30 || paths<1 || paths>6) return 2;
    int space=1;
    for (int i=0; i<paths; ++i) space*=k;
    std::vector<int> least(space), times(space), representatives;
    std::iota(least.begin(),least.end(),0);
    for (int u=2; u<k; ++u) if (std::gcd(u,k)==1)
        for (int code=1; code<space; ++code) {
            times[code]=k*times[code/k]+(u*(code%k))%k;
            least[code]=std::min(least[code],times[code]);
        }
    for (int i=0; i<space; ++i) if (i==least[i]) representatives.push_back(i);
    std::set<std::vector<int>> expected;
    std::vector<int> prefix;
    compositions(k-1,paths,prefix,expected);
    std::ifstream stream(argv[3]);
    require(bool(stream),"missing certificate");
    int shapes=expected.size();
    std::uint64_t witnesses=0;
    for (std::string line; std::getline(stream,line);) {
        std::istringstream fields(line);
        int a,b;
        require(bool(fields>>a>>b) && a==k && b==paths,"wrong header");
        std::vector<int> lengths(paths), first;
        int sum=0;
        for (int& n : lengths) {
            require(bool(fields>>n) && n>0,"invalid length");
            first.push_back(sum);
            sum+=n;
        }
        require(expected.erase(lengths)==1,"unexpected length list");
        std::vector<unsigned char> seen(space);
        Record record{least,seen,k,paths,first};
        for (std::string word; fields>>word;) {
            record.verify(word);
            ++witnesses;
        }
        for (int r : representatives) require(seen[r],"missing parent tuple");
    }
    require(expected.empty(),"missing length list");
    std::cout<<k<<' '<<paths<<" shapes "<<shapes<<" permutations "<<witnesses
             <<" parent tuples "<<std::uint64_t(shapes)*space<<'\n';
}
