/*
You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where
edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a
probability of success of traversing that edge succProb[i].

Given two nodes start and end, find the path with the maximum probability of success
to go from start to end and return its success probability.

If there is no path from start to end, return 0.

Example 1:
Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end,
one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.

Example 2:
Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
Explanation: There is no path between 0 and 2.

Thoughts:
(1) This is like Dijkstra's, trying to find the min path, but in stead of adding, you have to multiply
(2) You can basically do a BFS, tracking the min cost to get to the node of interest. It starts at zero
(3) You want a priority queue for edges, pick max edge each time
*/

#include<iostream>
#include<vector>
#include<unordered_map>
#include<utility>
#include<queue>

using namespace std;


class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start, int end) {

        int from, to;
        double edgeProb, newProb;
        double bestProb = 0;
        double endProb = 0;
        vector<pair<int, double>> *vertEdges;
        vector<bool> visited(n, false);

        priority_queue<pair<double, int>> Q;
        unordered_map<int, vector<pair<int, double>>> edgeMap;


        // Put all of the edges in a map that goes from: (to, prob)
        for (int i=0; i < succProb.size(); i++) {
            from = edges[i][0];
            to = edges[i][1];
            edgeProb = succProb[i];

            edgeMap[from].push_back(pair<int, double>(to, edgeProb));
            edgeMap[to].push_back(pair<int, double>(from, edgeProb));
        }

        // Initialize sorted map of unvisited vertices based on their probability to reach
        Q.push(pair<double, int>(1., start));

        while ( !Q.empty() ) {

            // Get the highest probability element
            auto p = Q.top();
            bestProb = p.first;
            from = p.second;
            Q.pop();

            if ( visited[from] )
                continue;

            visited[from] = true;

            if ( bestProb == 0 || bestProb < endProb || from == end)
                break;

            // Use edge map to update queue
            vertEdges = &edgeMap[from];
            for (int j = 0; j < vertEdges->size(); j++) {
                to = (*vertEdges)[j].first;
                if ( !visited[to] ) {
                    edgeProb = (*vertEdges)[j].second;
                    newProb = bestProb*edgeProb;

                    Q.push(pair<double, int>(newProb, to));

                    if ( to == end && newProb > endProb)
                        endProb = newProb;
                }
            }
        }
        return endProb;
    }
};


int main() {

    Solution s = Solution();

    double out;
    vector<vector<int>> edges;
    edges.push_back({0,1});
    edges.push_back({1,2});
    edges.push_back({0,2});
    vector<double> prob = {0.5,0.5,0.2};
    out = s.maxProbability(3, edges, prob, 0, 2);

    cout << "Expected 0.25, got: " << out << endl<< endl;

    edges.push_back({3,2});
    prob.push_back(1.);
    edges.push_back({0,3});
    prob.push_back(0.75);
    out = s.maxProbability(4, edges, prob, 0, 2);
    cout << "Expected 0.75, got: " << out << endl<< endl;


    vector<vector<int>> edges2;
    edges2.push_back({0,1});
    vector<double> prob2 = {0.5};
    out = s.maxProbability(3, edges2, prob2, 0, 2);

    cout << "Expected 0, got: " << out << endl << endl;


    vector<vector<int>> edges3;
    edges3.push_back({2,3});
    edges3.push_back({1,2});
    edges3.push_back({3,4});
    edges3.push_back({1,3});
    edges3.push_back({1,4});
    edges3.push_back({0,1});
    edges3.push_back({2,4});
    edges3.push_back({0,4});
    edges3.push_back({0,2});
    vector<double> prob3 = {0.06,0.26,0.49,0.25,0.2,0.64,0.23,0.21,0.77};

    out = s.maxProbability(5, edges3, prob3, 0, 3);

    cout << "Expected 0.16, got: " << out << endl;



    vector<vector<int>> edges4;
    edges4.push_back({1,4});
    edges4.push_back({2,4});
    edges4.push_back({0,4});
    edges4.push_back({0,3});
    edges4.push_back({0,2});
    edges4.push_back({2,3});
    vector<double> prob4 = {0.37,0.17,0.93,0.23,0.39,0.04};
    out = s.maxProbability(5, edges4, prob4, 3, 4);

    cout << "Expected 0.21390, got: " << out << endl;

    return 0;
}
