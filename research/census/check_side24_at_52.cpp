// Replay from actual endpoint sums. Only the repaired abstract inputs can specify
// a leaf incidence that is absent from the representative double star.
#include <algorithm>
#include <array>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <utility>
#include <vector>

using Row = std::array<unsigned char,5>;
using Histogram = std::array<int,27>;
using Edges = std::vector<std::pair<int,int>>;

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
Row read_row(int bytes) {
    Row row{};
    require(std::fread(row.data(),1,bytes,stdin)==static_cast<std::size_t>(bytes),
            "truncated witness");
    if (row[0]==0) require(row==Row{}, "invalid missing-row marker");
    else require(std::gcd(static_cast<int>(row[0]),27)==1 &&
                 *std::max_element(row.begin(),row.end())<27, "invalid affine row");
    return row;
}
Edges double_star(int n, int start) {
    Edges edges;
    for (int x=0; x<start; ++x) edges.emplace_back(x,start);
    for (int x=start+1; x<n; ++x) edges.emplace_back(start-1,x);
    return edges;
}
void balanced(const Histogram& h) {
    for (int count : h) require(count==1 || count==2, "unbalanced histogram");
}

struct Input {
    int a,f,b,g,shape,p;
    const Edges& left;
    const Edges& right;

    void recount(const Row& row, int leaf=-1, int parent=-1, bool abstract=false) const {
        std::array<int,52> label{};
        for (int i=0; i<24; ++i) label[i]=(row[0]*i+row[1])%27;
        for (int i=0; i<26; ++i) label[24+i]=(i==leaf ? row[4] : i);
        label[50]=row[2];
        label[51]=row[3];
        Histogram vertices{},weights{};
        for (int x : label) ++vertices[x];
        auto edge=[&](int x,int y) { ++weights[(label[x]+label[y])%27]; };
        for (auto [x,y] : left) edge(x,y);
        if (abstract) {
            // One occurrence of the old leaf edge z+t is removed from the interval.
            for (int s=g; s<g+25; ++s)
                if (s!=leaf+parent) ++weights[s%27];
            edge(24+leaf,24+parent);
        } else {
            for (auto [x,y] : right) edge(24+x,24+y);
        }
        edge(a,24+b);
        edge(24+p,50);
        edge(shape ? 50 : 24+p,51);
        balanced(vertices);
        balanced(weights);
    }
};

int main() {
    long direct=0, exceptional=0, repaired=0, skipped=0, samples=0, moved_port=0;
    int most_bad=0;
    for (int a=0; a<24; ++a) for (int f=1; f<=23; ++f) {
        Edges left=double_star(24,f);
        for (int b=0; b<26; ++b) for (int g=1; g<=25; ++g) {
            Edges right=double_star(26,g);
            std::array<int,26> degree{}, adjacent{};
            for (auto [i,j] : right) {
                ++degree[i]; ++degree[j];
                adjacent[i]=j; adjacent[j]=i;
            }
            for (int shape=0; shape<2; ++shape) for (int p=0; p<26; ++p) {
                Input input{a,f,b,g,shape,p,left,right};
                Row row=read_row(4);
                if (row[0]) {
                    input.recount(row);
                    ++direct;
                    continue;
                }
                ++exceptional;
                int bad=0, concrete=0;
                for (int z=0; z<26; ++z) {
                    bool every_parent=true;
                    for (int t=0; t<26; ++t) {
                        if (t==z || z+t<g || z+t>=g+25) continue;
                        Row correction=read_row(5);
                        if (!correction[0]) {
                            every_parent=false;
                            ++skipped;
                            continue;
                        }
                        input.recount(correction,z,t,true);
                        ++repaired;
                        if (degree[z]==1 && adjacent[z]==t) {
                            input.recount(correction,z,t);
                            ++concrete;
                            if (correction[4]!=z && (z==b || z==p)) ++moved_port;
                        }
                    }
                    if (!every_parent) ++bad;
                }
                require(bad<=3, "four leaf labels without a universal repair");
                require(concrete>0, "exception lacks a whole-tree example");
                samples+=concrete;
                most_bad=std::max(most_bad,bad);
            }
        }
    }
    require(std::fgetc(stdin)==EOF && !std::ferror(stdin), "extra or unreadable data");
    std::cout<<"direct whole trees "<<direct<<", exceptional inputs "<<exceptional
             <<", repaired incidences "<<repaired<<", omitted incidences "<<skipped
             <<", maximum exceptional leaf labels "<<most_bad
             <<", repaired whole trees "<<samples<<", changed ports "<<moved_port<<"\n";
}
