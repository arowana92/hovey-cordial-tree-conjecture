// Enumerate every partition and one representative per boundary difference.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
extern "C" int uniform_witness(int,const int*,int*);
void generate(int k,int left,int least,std::vector<int>& parts) {
    if (left) {
        for (int n=least;n<=left;++n) {
            parts.push_back(n);
            generate(k,left-n,n,parts);
            parts.pop_back();
        }
        return;
    }
    std::vector<int> parents,labels(k);
    for (int n:parts) {
        parents.push_back(-1);
        for (int i=1;i<n;++i) parents.push_back(static_cast<int>(parents.size())-1);
    }
    bool mixed=parts.size()>=2 && parts.front()<parts[1];
    for (int x=0;x<k;++x) {
        if (x && (!mixed || k%x)) continue;
        parents[0]=-1-x;
        if (uniform_witness(k,parents.data(),labels.data())!=1) {
            std::cerr<<"unresolved "<<k<<" "<<x;
            for (int n:parts) std::cerr<<" "<<n;
            std::cerr<<"\n";
            std::exit(1);
        }
        std::cout<<k<<" "<<x;
        for (int n:parts) std::cout<<" "<<n;
        std::cout<<" ";
        for (int z:labels) std::cout<<char('!'+z);
        std::cout<<"\n";
    }
}
int main(int argc,char**argv) {
    if (argc!=2) return 2;
    int k=std::stoi(argv[1]);
    if (k<2 || k>63) return 2;
    std::vector<int> parts;
    generate(k,k,1,parts);
}
