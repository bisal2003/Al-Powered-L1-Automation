// #include <bits/stdc++.h>
// using namespace std;

// void solve(int n,int k) {
//     vector<int> ans;
//     stack<int> st;
//     ans.push_back(1);
//     n--;
//     k--;
//     while (n > 0 && k > 0) {
//         if(n==k){
//             for (int i = 0; i < n; i++) {
//                 ans.push_back(1);
//             }
//             for (int i = 0; i < n; i++) {
//                 cout << ans[i] << " ";
//             }
//             return;
//         }
//         else if (n >3 k) {
//             st.push(0);
//             st.push(1);
//             st.push(0);
//             ans.push_back(st.top());
//             k--;
//             n--;



    
// }

// int main() {

//     int s,n,k;
//     cin >> s;
//     cin >> n >> k;

//     for (int i = 0; i < s; i++) {
//         int x;
//         cin >> x;
//         s += x;
//     }

//     cout << "Hello, World!" << endl;
    
//     //
    
//     return 0;
// }

// #include <bits/stdc++.h>
// using namespace std;

// int countSetBits(long long n) {
//     int count = 0;
//     unsigned long long val = n;
//     while (val > 0) {
//         val &= (val - 1);
//         count++;
//     }
//     return count;
// }

// const long long INF_COST = 4e18;

// vector<long long> get_min_ops_for_all_beauties(long long original_val, int max_b) {
//     vector<long long> costs(max_b + 1, INF_COST);

//     int original_beauty = countSetBits(original_val);
//     if (original_beauty <= max_b) {
//         costs[original_beauty] = 0;
//     }
//     for (int ops = 1; ops <= 256 && original_val + ops >= 0; ++ops) {
//         if (original_val > INF_COST - ops) continue;
//         long long next_val = original_val + ops;
//         int beauty = countSetBits(next_val);
//         if (beauty <= max_b) {
//             costs[beauty] = min(costs[beauty], (long long)ops);
//         }
//     }
//     return costs;
// }

// int main() {
//     ios_base::sync_with_stdio(false);
//     cin.tie(NULL);
//     int t;
//     cin >> t;
//     while (t--) {
//         int n;
//         long long k_budget;
//         cin >> n >> k_budget;
//         vector<long long> a(n);
//         for (int i = 0; i < n; ++i) {
//             cin >> a[i];
//         }

//         int max_single_b = 0;
//         if (n > 0) {
//             long long max_val_possible = 0;
//             for(long long val_a : a) max_val_possible = max(max_val_possible, val_a);
//             if (k_budget > 0) max_val_possible += k_budget;
//             if (max_val_possible < 0) max_val_possible = (1LL << 62);
//             max_single_b = 60;
//         }

//         vector<vector<long long>> costs_for_item_beauty(n, vector<long long>(max_single_b + 1));

//         for (int i = 0; i < n; ++i) {
//             costs_for_item_beauty[i] = get_min_ops_for_all_beauties(a[i], max_single_b);
//         }

//         int max_total_b = n * max_single_b;
//         vector<long long> dp(max_total_b + 1, INF_COST);
//         dp[0] = 0;

//         for (int i = 0; i < n; ++i) {
//             vector<long long> dp_next(max_total_b + 1, INF_COST);
//             const auto& current_item_all_ops_costs = costs_for_item_beauty[i];
//             int max_prev_beauty_sum = i * max_single_b;

//             for (int prev_beauty = 0; prev_beauty <= max_prev_beauty_sum; ++prev_beauty) {
//                 if (dp[prev_beauty] == INF_COST) {
//                     continue;
//                 }

//                 for (int p = 0; p <= max_single_b; ++p) {
//                     long long ops_for_p = current_item_all_ops_costs[p];
//                     if (ops_for_p == INF_COST) {
//                         continue;
//                     }

//                     int new_total_beauty = prev_beauty + p;
//                     if (new_total_beauty <= max_total_b) {
//                         long long current_total_ops = dp[prev_beauty] + ops_for_p;
//                         if (dp[prev_beauty] > INF_COST - ops_for_p) {
//                              current_total_ops = INF_COST;
//                         }

//                         if (current_total_ops < dp_next[new_total_beauty]) {
//                             dp_next[new_total_beauty] = current_total_ops;
//                         }
//                     }
//                 }
//             }
//             dp = dp_next;
//         }

//         long long ans_beauty = 0;
//         for (int b = max_total_b; b >= 0; --b) {
//             if (dp[b] <= k_budget) {
//                 ans_beauty = b;
//                 break;
//             }
//         }
//         cout << ans_beauty << endl;
//     }
//     return 0;
// }


#include <iostream>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<vector<int>> operations;
        
        if (n >= 2) {
            if (n == 3) {
                operations.push_back({2, 1, 3});
                operations.push_back({2, 2, 3});
            } else {
                operations.push_back({2, 1, n});
            }
        }
        
        for (int i = 3; i < n; ++i) {
            operations.push_back({i, 1, i});
            operations.push_back({i, 2, n});
        }
        
        if (n >= 3) {
            if (n == 3) {
                operations.push_back({3, 1, 2});
                operations.push_back({3, 2, 3});
            } else {
                operations.push_back({n, 3, n});
                operations.push_back({n, 1, 2});
            }
        }
        
        cout << operations.size() << endl;
        for (const auto& op : operations) {
            cout << op[0] << " " << op[1] << " " << op[2] << endl;
        }
    }
    return 0;
}