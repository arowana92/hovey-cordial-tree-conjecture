// Rank unordered rooted forests by component sizes and colexicographic multisets.
// This ordering uses only rooted-tree counts, with no catalog of tree words.
#pragma once
#include <algorithm>
#include <array>
#include <cstdint>
#include <stdexcept>
#include <iterator>
#include <utility>
#include <vector>

class ShapeRank {
    using Count = std::uint64_t;
    static constexpr int limit = 27;
    int n;
    Count ways[limit+1][limit+2]{};
    Count skip[limit+1][limit+1][limit+1]{};

    static Count choose(Count top,int bottom) {
        if (top<static_cast<Count>(bottom)) return 0;
        Count answer=1;
        for (int i=1;i<=bottom;++i) answer=answer*(top-bottom+i)/i;
        return answer;
    }

    using Component = std::pair<int,Count>;
    Count group_rank(std::array<Component,limit>& pieces,int length,int mass) const {
        std::sort(pieces.begin(),pieces.begin()+length);
        Count rank=0;
        for (int i=0;i<length;) {
            int size=pieces[i].first, copies=0;
            Count subset=0;
            do {
                subset+=choose(pieces[i].second+copies,copies+1);
                ++i;
                ++copies;
            } while (i<length && pieces[i].first==size);
            rank+=skip[mass][size][copies];
            mass-=copies*size;
            rank+=subset*ways[mass][size+1];
        }
        return rank;
    }

public:
    explicit ShapeRank(int mass): n(mass) {
        if (mass<1 || mass>=limit) throw std::invalid_argument("unsupported forest mass");
        std::fill(std::begin(ways[0]),std::end(ways[0]),1);
        for (int s=1;s<=n;++s) for (int t=s;t>=1;--t) {
            Count count=ways[s][t+1], types=ways[t-1][1];
            for (int q=1;q*t<=s;++q) {
                skip[s][t][q]=count;
                count+=choose(types+q-1,q)*ways[s-q*t][t+1];
            }
            ways[s][t]=count;
        }
    }

    Count total() const { return ways[n][1]; }

    Count operator()(const std::vector<int>& parent) const {
        if (parent.size()!=static_cast<unsigned>(n)) throw std::invalid_argument("wrong forest mass");
        // Position n is a dummy whose children are the component roots.
        std::array<int,limit> head{},next{},size{};
        std::array<Count,limit> ranks{};
        std::array<Component,limit> pieces{};
        head.fill(-1);
        auto finish = [&](int v) {
            int degree=0,mass=0;
            for (int u=head[v];u!=-1;u=next[u]) {
                pieces[degree++]={size[u],ranks[u]};
                mass+=size[u];
            }
            size[v]=mass+1;
            ranks[v]=group_rank(pieces,degree,mass);
        };
        for (int i=n-1;i>=0;--i) {
            finish(i);
            if (parent[i]<-1 || parent[i]>=i) throw std::invalid_argument("parents must precede children");
            int v=parent[i]<0 ? n : parent[i];
            next[i]=head[v];
            head[v]=i;
        }
        finish(n);
        return ranks[n];
    }
};
