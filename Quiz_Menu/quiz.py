import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QComboBox, QSpinBox, QDialog, QFormLayout)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QComboBox, QSpinBox,
                             QDialog, QFormLayout)

from PyQt5.QtCore import Qt

class QuizGame(QMainWindow):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Quiz Game")
        self.setGeometry(100, 100, 600, 400)

        # Data for questions
        self.all_questions = {
            "Data Structures": [
                {
                    "question": "What is the amortized time complexity for the split operation in a splay tree?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(log n) amortized"],
                    "answer": 4
                },
                {
                    "question": "In a Red-Black tree, which of the following properties ensures logarithmic height?",
                    "options": ["Every red node has a black parent", 
                                "The tree is balanced after each insertion or deletion", 
                                "Every path from root to a null node has the same number of black nodes", 
                                "The height of the tree is always log n"],
                    "answer": 3
                },
                {
                    "question": "Which of the following best explains the difference between B-Trees and B+ Trees?",
                    "options": ["B-Trees allow duplicates, but B+ Trees do not", 
                                "B+ Trees store only keys in internal nodes, data is stored only in leaf nodes", 
                                "B+ Trees are not self-balancing", 
                                "B-Trees store data only in leaf nodes"],
                    "answer": 2
                },
                {
                    "question": "How does the use of lazy propagation in segment trees affect time complexity?",
                    "options": ["Improves query time from O(n) to O(log n)", 
                                "Improves update time from O(n log n) to O(log n)", 
                                "Reduces memory usage", 
                                "Has no effect on complexity but simplifies implementation"],
                    "answer": 2
                },
                {
                    "question": "In a van Emde Boas tree, what is the significance of the cluster and summary arrays?",
                    "options": ["They allow for O(1) access time", 
                                "They enable O(log log n) operations for successor/predecessor", 
                                "They maintain the balance of the tree", 
                                "They ensure memory usage is proportional to n"],
                    "answer": 2
                },
                {
                    "question": "Which condition must always be met during rotation in an AVL tree?",
                    "options": ["The height difference between subtrees must be 1", 
                                "The height difference between subtrees must not exceed 1", 
                                "Nodes must remain sorted after rotation", 
                                "All the above"],
                    "answer": 4
                },
                {
                    "question": "In the context of a Bloom filter, what is the relationship between the false positive rate and the number of hash functions?",
                    "options": ["Increasing hash functions decreases false positives indefinitely", 
                                "False positive rate is minimal when the number of hash functions is proportional to the table size", 
                                "False positive rate increases linearly with the number of hash functions", 
                                "Hash functions have no impact on the false positive rate"],
                    "answer": 2
                },
                {
                    "question": "What is the primary drawback of using a Trie for string storage?",
                    "options": ["Poor memory efficiency for sparse datasets", 
                                "Slow search times compared to binary search trees", 
                                "Difficulty in handling prefix searches", 
                                "Inability to support dynamic key insertion"],
                    "answer": 1
                },
                {
                    "question": "How does a Fenwick tree optimize prefix sum queries compared to a segment tree?",
                    "options": ["Fenwick tree uses logarithmic memory space", 
                                "Fenwick tree has faster query times", 
                                "Fenwick tree uses less memory but has comparable query times", 
                                "Fenwick tree supports range queries natively"],
                    "answer": 3
                },
                {
                    "question": "Which of the following operations is not natively supported in a skip list?",
                    "options": ["Insertion", "Deletion", "Search", "Range queries"],
                    "answer": 4
                },
                {
                    "question": "In a k-d tree, how is the median chosen during the partitioning step?",
                    "options": ["Randomly from the dataset", 
                                "Using a quicksort-like partitioning", 
                                "By sorting all nodes along the chosen dimension", 
                                "Using a balanced binary search tree for each dimension"],
                    "answer": 3
                },
                {
                    "question": "What is the key benefit of using a treap over an AVL or Red-Black tree?",
                    "options": ["Faster rotations", 
                                "Better balance guarantees", 
                                "Randomized balancing using heap properties", 
                                "Support for persistent versions"],
                    "answer": 3
                },
                {
                    "question": "What is the computational complexity of finding the longest palindromic subsequence using a suffix tree?",
                    "options": ["O(n)", "O(n^2)", "O(log n)", "O(n log n)"],
                    "answer": 1
                },
                {
                    "question": "Why is cuckoo hashing considered an efficient alternative to traditional hash tables?",
                    "options": ["It requires fewer hash functions", 
                                "It guarantees O(1) worst-case operations", 
                                "It resolves collisions without clustering", 
                                "It reduces memory usage"],
                    "answer": 3
                },
                {
                    "question": "Which data structure is most suitable for implementing a sparse matrix?",
                    "options": ["2D array", "Linked list", "Hash table", "Compressed sparse row format"],
                    "answer": 4
                },
                {
                    "question": "Which condition is violated if a B-tree node is overfull during insertion?",
                    "options": ["Maximum degree", "Height balance", "Leaf-node equality", "Root node must always be balanced"],
                    "answer": 1
                },
                {
                    "question": "In a Fibonacci heap, how is the amortized time complexity of decrease-key achieved?",
                    "options": ["Using lazy updates to child nodes", 
                                "Using cascading cuts to maintain tree balance", 
                                "By restricting the number of nodes in the heap", 
                                "By maintaining a fixed height for trees"],
                    "answer": 2
                },
                {
                    "question": "Which operation in a doubly linked list requires the most computational effort?",
                    "options": ["Traversal", "Insertion at the beginning", "Deletion of a specific node", "Reversing the list"],
                    "answer": 4
                },
                {
                    "question": "What is the primary benefit of using an order-statistic tree?",
                    "options": ["O(1) insertion times", 
                                "Efficient range queries", 
                                "Efficient kth element retrieval", 
                                "Supports constant-time updates"],
                    "answer": 3
                },
                {
                    "question": "What is the trade-off involved in using open addressing in hash tables?",
                    "options": ["Higher memory usage but faster search times", 
                                "Lower memory usage but slower search in clusters", 
                                "Higher collision rate but faster deletions", 
                                "Complexity of rebalancing but faster insertions"],
                    "answer": 2
                },
                {
                    "question": "What is the worst-case time complexity of union-by-rank in a disjoint-set data structure with path compression?",
                    "options": ["O(n log n)", "O(log n)", "O(α(n))", "O(n)"],
                    "answer": 3
                },
                {
                    "question": "Which of the following best describes the runtime of finding the k-th smallest element using a modified QuickSort algorithm?",
                    "options": ["O(n log k)", "O(n + k log n)", "O(n)", "O(n log n)"],
                    "answer": 3
                },
                {
                    "question": "What is the primary advantage of a Trie over a Ternary Search Tree (TST) for storing strings?",
                    "options": ["Lower memory usage", 
                                "Faster prefix-based searches", 
                                "Easier to delete keys", 
                                "Supports efficient lexicographical ordering"],
                    "answer": 2
                },
                {
                    "question": "In a Fenwick Tree, what is the maximum number of bits required for a single prefix query?",
                    "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                    "answer": 2
                },
                {
                    "question": "Which of the following operations is most efficient in a Bloom Filter?",
                    "options": ["Insertion", "Search", "Deletion", "Handling collisions"],
                    "answer": 1
                },
                {
                    "question": "What is the advantage of using a Segment Tree with lazy propagation over a Fenwick Tree?",
                    "options": ["Faster updates", 
                                "Supports range updates efficiently", 
                                "Lower memory usage", 
                                "Easier to implement"],
                    "answer": 2
                },
                {
                    "question": "Which data structure is used to efficiently solve the range minimum query problem in logarithmic time?",
                    "options": ["Fenwick Tree", "Sparse Table", "Segment Tree", "Heap"],
                    "answer": 2
                },
                {
                    "question": "What is the height of a B+ Tree with n elements and a branching factor of m?",
                    "options": ["O(log m n)", "O(m log n)", "O(log n m)", "O(n log m)"],
                    "answer": 1
                },
                {
                    "question": "In an Suffix Array, what is the runtime of constructing it using the DC3 (Difference Cover) algorithm?",
                    "options": ["O(n log n)", "O(n)", "O(n^2)", "O(n log^2 n)"],
                    "answer": 2
                },
                {
                    "question": "Which condition must always be satisfied in a Fibonacci Heap?",
                    "options": ["Degree of any node must not exceed log n", 
                                "Root nodes must always be balanced", 
                                "The heap must maintain a leftist bias", 
                                "No condition on degree, only order property"],
                    "answer": 1
                },
                {
                    "question": "What is the expected runtime of an operation in a skip list with n elements?",
                    "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                    "answer": 2
                },
                {
                    "question": "Which data structure would you use to compute dynamic connectivity in an undirected graph?",
                    "options": ["Fenwick Tree", "Union-Find with path compression", 
                                "Dynamic Segment Tree", "Adjacency Matrix"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of performing a delete-min operation in a Binary Heap?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                    "answer": 2
                },
                {
                    "question": "What is the primary challenge when implementing a persistent Red-Black Tree?",
                    "options": ["Balancing the tree after updates", 
                                "Avoiding excessive memory overhead", 
                                "Maintaining logarithmic time for operations", 
                                "Implementing lazy propagation"],
                    "answer": 2
                },
                {
                    "question": "Which of the following problems can be solved efficiently using a Persistent Segment Tree?",
                    "options": ["Dynamic range updates", "Dynamic range queries", 
                                "Finding historical range sums", "Handling sparse datasets"],
                    "answer": 3
                },
                {
                    "question": "What is the main difference between an Euler Tour Tree and a Segment Tree in graph processing?",
                    "options": ["Euler Tour Tree supports dynamic edge addition, Segment Tree does not", 
                                "Segment Tree is more memory efficient", 
                                "Euler Tour Tree captures graph structure, Segment Tree does not", 
                                "Segment Tree allows better range queries"],
                    "answer": 3
                },
                {
                    "question": "What is the worst-case time complexity of building a Cartesian Tree?",
                    "options": ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"],
                    "answer": 2
                },
                {
                    "question": "What is the primary advantage of a k-d tree over a Quad-Tree for multidimensional range searches?",
                    "options": ["Better space complexity", 
                                "More balanced structure for non-uniform distributions", 
                                "Handles higher dimensions better", 
                                "Easier to update dynamically"],
                    "answer": 2
                },
                {
                    "question": "Which of the following is a key application of a Heavy-Light Decomposition?",
                    "options": ["Finding shortest paths in weighted graphs", 
                                "Solving LCA and path queries efficiently", 
                                "Maintaining dynamic connectivity", 
                                "Optimizing flow in a network"],
                    "answer": 2
                },
                {
                    "question": "What is the expected height of a randomly generated treap with n nodes?",
                    "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
                    "answer": 2
                },
                {
                    "question": "Which is the best approach for finding the diameter of a tree in linear time?",
                    "options": ["Depth-first search (DFS)", "Breadth-first search (BFS)", 
                                "Kruskal's algorithm", "Dynamic programming"],
                    "answer": 1
                },
                {
                    "question": "What is the amortized time complexity of a split operation in a splay tree?",
                    "options": ["O(log n)", "O(n log n)", "O(n)", "O(1)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following operations cannot be performed efficiently in an Interval Tree?",
                    "options": ["Range queries", "Insertion", 
                                "Merging intervals", "Finding overlapping intervals"],
                    "answer": 3
                },
                {
                    "question": "What is the purpose of van Emde Boas trees in advanced data structures?",
                    "options": ["Efficient dynamic hashing", 
                                "Fast operations in integer ranges", 
                                "Optimizing string manipulations", 
                                "Handling graph adjacency lists"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of constructing a Persistent Segment Tree with n elements?",
                    "options": ["O(n log n)", "O(n)", "O(log n)", "O(n^2)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms is most suitable for maximum bipartite matching?",
                    "options": ["Bellman-Ford", "Ford-Fulkerson", 
                                "Floyd-Warshall", "Hungarian algorithm"],
                    "answer": 4
                },
                {
                    "question": "In a Cartesian Tree, what relationship is maintained between the heap property and in-order traversal?",
                    "options": ["Heap property is preserved, but not in-order traversal", 
                                "In-order traversal is preserved, but not heap property", 
                                "Both heap property and in-order traversal are preserved", 
                                "Neither property is preserved"],
                    "answer": 3
                },
                {
                    "question": "Which data structure is commonly used to implement a Least Recently Used (LRU) cache?",
                    "options": ["Hash map and doubly linked list", "AVL Tree", 
                                "Skip List", "Fibonacci Heap"],
                    "answer": 1
                },
                {
                    "question": "What is the best way to dynamically maintain the median of a stream of numbers?",
                    "options": ["Fenwick Tree", "Heap with two priority queues", 
                                "Segment Tree", "AVL Tree"],
                    "answer": 2
                },
                {
                    "question": "In a Bloom Filter, what determines the false positive rate?",
                    "options": ["Number of hash functions and bit array size", 
                                "Number of elements inserted", 
                                "Both A and B", 
                                "False positives do not occur in Bloom Filters"],
                    "answer": 3
                },
                {
                    "question": "Which of the following best describes the use of KMP algorithm in advanced DSA?",
                    "options": ["It is used for finding shortest paths in graphs", 
                                "Efficiently searching substrings within a text", 
                                "Dynamic programming optimization", 
                                "Constructing tries for string sets"],
                    "answer": 2
                },
                {
                    "question": "What is the primary advantage of using a Treap over an AVL Tree?",
                    "options": ["Simpler rotation mechanism", 
                                "Guaranteed logarithmic height", 
                                "Supports randomized balancing", 
                                "Smaller memory overhead"],
                    "answer": 3
                },
                {
                    "question": "What is the complexity of finding articulation points in an undirected graph?",
                    "options": ["O(V + E)", "O(V^2)", "O(E log V)", "O(V log V + E)"],
                    "answer": 1
                },
                {
                    "question": "Which advanced data structure can solve the dynamic connectivity problem efficiently?",
                    "options": ["Union-Find with link-by-size and path compression", 
                                "Fibonacci Heap", "Binary Indexed Tree", "Trie"],
                    "answer": 1
                },
                {
                    "question": "What is the advantage of a centroid decomposition of a tree?",
                    "options": ["Efficient path queries", 
                                "Allows divide-and-conquer strategies on trees", 
                                "Both A and B", 
                                "None of the above"],
                    "answer": 3
                },
                {
                    "question": "What is the space complexity of a Sparse Table used for Range Minimum Queries (RMQ)?",
                    "options": ["O(n)", "O(n log n)", "O(log n)", "O(n^2)"],
                    "answer": 2
                },
                {
                    "question": "What is the worst-case complexity of Kruskal’s MST algorithm when using Union-Find with path compression?",
                    "options": ["O(E log V)", "O(E + V)", "O(V^2)", "O(E log E + α(V))"],
                    "answer": 4
                },
                {
                    "question": "Which algorithm is best suited for finding bridges in a graph?",
                    "options": ["Kosaraju’s algorithm", "Tarjan's algorithm", 
                                "Prim’s algorithm", "Dijkstra’s algorithm"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of inserting an element in an Order Statistic Tree?",
                    "options": ["O(log n)", "O(n)", "O(n log n)", "O(1)"],
                    "answer": 1
                },
                {
                    "question": "Which advanced algorithm efficiently finds the shortest path in graphs with negative edge weights?",
                    "options": ["Dijkstra's algorithm", "Bellman-Ford algorithm", 
                                "Floyd-Warshall algorithm", "Johnson's algorithm"],
                    "answer": 2
                },
                {
                    "question": "Which technique can optimize the solution of the All-Pairs Shortest Path problem in a graph?",
                    "options": ["Dynamic programming with Floyd-Warshall", 
                                "Dijkstra's algorithm repeated for each vertex", 
                                "Bellman-Ford for every edge", 
                                "Union-Find based MST"],
                    "answer": 1
                },
                {
                    "question": "What is the amortized time complexity for split and merge operations in a Treap?",
                    "options": ["O(log n)", "O(n)", "O(n log n)", "O(1)"],
                    "answer": 1
                },
                {
                    "question": "In dynamic programming, what is the complexity of solving the Longest Increasing Subsequence using a Fenwick Tree?",
                    "options": ["O(n)", "O(n log n)", "O(n^2)", "O(n^2 log n)"],
                    "answer": 2
                },
                {
                    "question": "Which of the following problems can be solved using Tarjan's strongly connected components algorithm?",
                    "options": ["Cycle detection in directed graphs", 
                                "Shortest path in weighted graphs", 
                                "Maximum flow in a network", 
                                "Finding articulation points"],
                    "answer": 1
                },
                {
                    "question": "What is the purpose of Heavy-Light Decomposition in advanced DSA?",
                    "options": ["Efficiently handling path queries in trees", 
                                "Optimizing range queries in arrays", 
                                "Improving shortest-path algorithms", 
                                "Partitioning graphs into connected components"],
                    "answer": 1
                },
                {
                    "question": "Which of the following is the primary use of a Link/Cut Tree?",
                    "options": ["Dynamic tree queries", 
                                "Efficient string searching", 
                                "Graph cycle detection", 
                                "Range minimum queries"],
                    "answer": 1
                },
                {
                    "question": "What is the time complexity of a Boyer-Moore majority vote algorithm for finding a majority element?",
                    "options": ["O(n)", "O(n log n)", "O(log n)", "O(n^2)"],
                    "answer": 1
                },
                {
                    "question": "Which algorithm is best for finding the centroid of a tree in linear time?",
                    "options": ["DFS-based centroid decomposition", 
                                "Dynamic programming", 
                                "Prim's algorithm", 
                                "Segment tree with path queries"],
                    "answer": 1
                },
                {
                    "question": "What is the complexity of preprocessing a Suffix Array for longest repeated substrings?",
                    "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"],
                    "answer": 2
                },
                {
                    "question": "Which problem does the Edmonds-Karp algorithm solve efficiently?",
                    "options": ["Maximum bipartite matching", 
                                "Minimum spanning tree", 
                                "Maximum flow in a network", 
                                "Shortest path with negative weights"],
                    "answer": 3
                },
                {
                    "question": "What is the main advantage of using Mo’s algorithm in competitive programming?",
                    "options": ["Solving range queries on static arrays efficiently", 
                                "Handling graph traversal problems", 
                                "Optimizing MST construction", 
                                "Efficient hash table operations"],
                    "answer": 1
                },
                {
                    "question": "What is the time complexity of building a Persistent Fenwick Tree?",
                    "options": ["O(n log n)", "O(log n)", "O(n^2)", "O(n)"],
                    "answer": 1
                },
                {
                    "question": "Which advanced technique is used in solving problems like path queries over dynamic graphs?",
                    "options": ["Dynamic segment trees", 
                                "Heavy-light decomposition", 
                                "Link/Cut Trees", 
                                "All of the above"],
                    "answer": 4
                },
                {
                    "question": "In advanced DSA, which algorithm can find the number of distinct substrings in a string?",
                    "options": ["KMP algorithm", "Suffix Array with LCP", 
                                "Rabin-Karp algorithm", "Dynamic Programming"],
                    "answer": 2
                },
                {
                    "question": "What is the worst-case complexity of the Hopcroft-Karp algorithm for finding maximum bipartite matching?",
                    "options": ["O(V + E)", "O(V^3)", "O(E√V)", "O(V log E)"],
                    "answer": 3
                },
                {
                    "question": "Which data structure is best for efficiently performing point update and range maximum queries?",
                    "options": ["Segment Tree", "Fenwick Tree", 
                                "AVL Tree", "Order Statistic Tree"],
                    "answer": 1
                },
                {
                    "question": "What is the purpose of the Rabin-Karp algorithm in advanced DSA?",
                    "options": ["Finding minimum spanning tree", 
                                "Efficiently searching substrings with hashing", 
                                "Dynamic connectivity in graphs", 
                                "Shortest path in negative edge-weighted graphs"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of performing k-nearest neighbor queries using a KD-Tree?",
                    "options": ["O(log n)", "O(n)", "O(k log n)", "O(k)"],
                    "answer": 3
                },
                {
                    "question": "Which advanced graph traversal algorithm handles Eulerian paths efficiently?",
                    "options": ["Hierholzer's algorithm", 
                                "Tarjan's algorithm", 
                                "Dijkstra's algorithm", 
                                "Kruskal's algorithm"],
                    "answer": 1
                },
                {
                    "question": "What is the key advantage of using a Fibonacci Heap over a Binary Heap in Prim's algorithm?",
                    "options": ["Faster decrease-key operation", 
                                "Smaller memory overhead", 
                                "Faster insertions", 
                                "Both A and C"],
                    "answer": 4
                }
            ], 
            "Algorithms": [
                {
                    "question": "What is the time complexity of finding the longest common subsequence (LCS) using dynamic programming?",
                    "options": ["O(n^2)", "O(n log n)", "O(n^3)", "O(n)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms can solve the problem of finding the shortest path in a graph with negative weights but no negative cycles?",
                    "options": ["Dijkstra’s algorithm", "Bellman-Ford algorithm", 
                                "Floyd-Warshall algorithm", "A* search algorithm"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of the Ford-Fulkerson algorithm in a graph with V vertices and E edges?",
                    "options": ["O(V * E)", "O(E^2)", "O(V^2)", "O(V * E^2)"],
                    "answer": 1
                },
                {
                    "question": "What is the purpose of the Knuth-Morris-Pratt (KMP) algorithm?",
                    "options": ["Substring search", "Minimum spanning tree", 
                                "Graph traversal", "Topological sorting"],
                    "answer": 1
                },
                {
                    "question": "What is the expected time complexity of quicksort in the average case?",
                    "options": ["O(n^2)", "O(n log n)", "O(n log n) with high probability", "O(n)"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm is used to solve the problem of finding the maximum bipartite matching?",
                    "options": ["Hungarian algorithm", "Edmonds-Karp algorithm", 
                                "Hopcroft-Karp algorithm", "Kruskal’s algorithm"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of the A* search algorithm when using a priority queue?",
                    "options": ["O(E + V log V)", "O(V^2)", "O(V log V + E)", "O(V + E)"],
                    "answer": 1
                },
                {
                    "question": "Which algorithm can be used for finding strongly connected components in a directed graph?",
                    "options": ["Tarjan’s algorithm", "Kruskal’s algorithm", 
                                "Prim’s algorithm", "Dijkstra’s algorithm"],
                    "answer": 1
                },
                {
                    "question": "What is the primary use case of the Sieve of Eratosthenes algorithm?",
                    "options": ["Finding prime numbers", "Finding the shortest path in a graph", 
                                "Solving dynamic programming problems", "Sorting an array"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms guarantees an optimal solution for the Fractional Knapsack problem?",
                    "options": ["Dynamic programming", "Greedy algorithm", 
                                "Divide and conquer", "Backtracking"],
                    "answer": 2
                },
                {
                    "question": "What is the best algorithm for solving the Traveling Salesman Problem (TSP) for large instances?",
                    "options": ["Dynamic programming", "Greedy algorithm", 
                                "Brute force", "Approximation algorithm (Christofides)"],
                    "answer": 4
                },
                {
                    "question": "What is the primary advantage of using a Fibonacci heap over a binary heap?",
                    "options": ["Faster insertions", "Faster decrease-key operation", 
                                "Smaller memory overhead", "Both A and B"],
                    "answer": 4
                },
                {
                    "question": "What is the worst-case time complexity of the Bellman-Ford algorithm?",
                    "options": ["O(V + E)", "O(V^2)", "O(V * E)", "O(V^3)"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of matrix multiplication using Strassen’s algorithm?",
                    "options": ["O(n^3)", "O(n^2 log n)", "O(n^2)", "O(n^log 7)"],
                    "answer": 4
                },
                {
                    "question": "In a binary search tree, what is the time complexity of the delete operation in the worst case?",
                    "options": ["O(log n)", "O(n)", "O(n^2)", "O(log n + n)"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm is used to find the kth smallest element in an unsorted array?",
                    "options": ["Quickselect", "Quicksort", 
                                "Merge Sort", "Insertion Sort"],
                    "answer": 1
                },
                {
                    "question": "What is the time complexity of the Floyd-Warshall algorithm for finding shortest paths between all pairs of vertices?",
                    "options": ["O(V^2)", "O(V^3)", "O(V^4)", "O(E log V)"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of the binary search algorithm on a sorted array of size n?",
                    "options": ["O(n)", "O(log n)", "O(n log n)", "O(n^2)"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm is used to find the maximum spanning tree in a weighted graph?",
                    "options": ["Kruskal’s algorithm", "Prim’s algorithm", 
                                "Boruvka’s algorithm", "Floyd-Warshall algorithm"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of the merge sort algorithm in the worst case?",
                    "options": ["O(n log n)", "O(n^2)", "O(n)", "O(log n)"],
                    "answer": 1
                },
                {
                    "question": "In the context of graph algorithms, what is the primary function of the depth-first search (DFS) algorithm?",
                    "options": ["Find shortest paths", "Detect cycles", 
                                "Find the minimum spanning tree", "All of the above"],
                    "answer": 2
                },
                {
                    "question": "What is the expected time complexity of a good hash function with open addressing for search, insert, and delete operations?",
                    "options": ["O(n)", "O(log n)", "O(1) on average", "O(n^2)"],
                    "answer": 3
                },
                {
                    "question": "Which of the following algorithms is used to solve the Maximum Flow problem?",
                    "options": ["Dijkstra’s algorithm", "Bellman-Ford algorithm", 
                                "Ford-Fulkerson algorithm", "A* algorithm"],
                    "answer": 3
                },
                {
                    "question": "Which sorting algorithm has the best time complexity in the best case?",
                    "options": ["Bubble Sort", "Selection Sort", 
                                "Merge Sort", "Quick Sort"],
                    "answer": 3
                },
                {
                    "question": "In graph theory, what is the complexity of checking whether a directed graph is strongly connected?",
                    "options": ["O(V + E)", "O(E log V)", "O(V^2)", "O(E^2)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms is used to detect negative weight cycles in a graph?",
                    "options": ["Dijkstra’s algorithm", "Bellman-Ford algorithm", 
                                "Floyd-Warshall algorithm", "Topological sorting"],
                    "answer": 2
                },
                {
                    "question": "What is the primary use case for the Rabin-Karp algorithm?",
                    "options": ["Substring matching", "Graph traversal", 
                                "Cycle detection", "Finding the shortest path"],
                    "answer": 1
                },
                {
                    "question": "What is the time complexity of performing a union operation in a disjoint set using path compression and union by rank?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(α(n))"],
                    "answer": 4
                },
                {
                    "question": "Which technique is used in Prim’s algorithm to efficiently choose the next vertex to add to the MST?",
                    "options": ["Breadth-first search", "Dijkstra’s algorithm", 
                                "Greedy approach using a priority queue", "Depth-first search"],
                    "answer": 3
                },
                {
                    "question": "Which is the most efficient algorithm for finding the longest path in an acyclic directed graph?",
                    "options": ["Depth-first search", "Topological sort", 
                                "Bellman-Ford algorithm", "Dijkstra’s algorithm"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm can efficiently find the diameter of a tree?",
                    "options": ["Breadth-first search", "Depth-first search", 
                                "Dijkstra’s algorithm", "Floyd-Warshall algorithm"],
                    "answer": 1
                },
                {
                    "question": "Which of the following is an optimal solution for the Subset Sum problem?",
                    "options": ["Greedy approach", "Backtracking", 
                                "Dynamic programming", "Brute force"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of the depth-first search (DFS) algorithm on a graph with V vertices and E edges?",
                    "options": ["O(V + E)", "O(V^2)", "O(E log V)", "O(V log V)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following is an efficient algorithm to solve the problem of finding the maximum independent set in a graph?",
                    "options": ["Greedy algorithm", "Dynamic programming", 
                                "Branch and bound", "Backtracking with pruning"],
                    "answer": 3
                },
                {
                    "question": "Which of the following sorting algorithms can guarantee O(n log n) time complexity even in the worst case?",
                    "options": ["QuickSort", "MergeSort", 
                                "HeapSort", "InsertionSort"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of the Bellman-Ford algorithm in the worst case, for a graph with V vertices and E edges?",
                    "options": ["O(V + E)", "O(V^2)", "O(V * E)", "O(E^2)"],
                    "answer": 3
                },
                {
                    "question": "Which of the following algorithms is used to find the shortest path in a graph with positive and negative edge weights, but no negative cycles?",
                    "options": ["Dijkstra’s algorithm", "Bellman-Ford algorithm", 
                                "A* search algorithm", "Floyd-Warshall algorithm"],
                    "answer": 2
                },
                {
                    "question": "What is the worst-case time complexity of Dijkstra's algorithm with a Fibonacci heap?",
                    "options": ["O(V^2)", "O(E log V)", "O(V log V + E)", "O(V log V)"],
                    "answer": 3
                },
                {
                    "question": "Which data structure can be used to implement the priority queue in Dijkstra's algorithm for efficiency?",
                    "options": ["Stack", "Queue", 
                                "Min-heap", "Linked list"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of the Floyd-Warshall algorithm for all pairs shortest path in a graph with V vertices?",
                    "options": ["O(V^2)", "O(V^3)", "O(V^4)", "O(E log V)"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm can be used to find the maximum flow in a flow network with multiple sources and sinks?",
                    "options": ["Ford-Fulkerson", "Edmonds-Karp", 
                                "Push-Relabel algorithm", "Dinic’s algorithm"],
                    "answer": 3
                },
                {
                    "question": "Which of the following techniques is used to solve the Knapsack problem optimally in polynomial time?",
                    "options": ["Brute force", "Greedy algorithm", 
                                "Dynamic programming", "Divide and conquer"],
                    "answer": 3
                },
                {
                    "question": "Which of the following sorting algorithms uses the divide-and-conquer technique and guarantees O(n log n) time in the worst case?",
                    "options": ["QuickSort", "MergeSort", 
                                "HeapSort", "InsertionSort"],
                    "answer": 2
                },
                {
                    "question": "What is the best algorithm for finding the longest common subsequence (LCS) between two strings of length n and m?",
                    "options": ["Dynamic programming", "Greedy approach", 
                                "Divide and conquer", "Backtracking"],
                    "answer": 1
                },
                {
                    "question": "Which algorithm is used for finding the least common ancestor (LCA) in a binary tree efficiently?",
                    "options": ["Binary search", "Depth-first search", 
                                "Dynamic programming", "Euler tour technique"],
                    "answer": 4
                },
                {
                    "question": "What is the time complexity of performing a range query on a segment tree?",
                    "options": ["O(1)", "O(log n)", 
                                "O(n)", "O(n log n)"],
                    "answer": 2
                },
                {
                    "question": "What is the primary disadvantage of using a brute-force approach for the Traveling Salesman Problem (TSP)?",
                    "options": ["It is NP-complete", "It has exponential time complexity", 
                                "It cannot guarantee an optimal solution", "It requires too much memory"],
                    "answer": 2
                },
                {
                    "question": "Which algorithm is used to find the minimum spanning tree of a graph?",
                    "options": ["Kruskal’s algorithm", "Prim’s algorithm", 
                                "Floyd-Warshall algorithm", "Bellman-Ford algorithm"],
                    "answer": 1
                },
                {
                    "question": "What is the worst-case time complexity of the Prim’s algorithm for finding the minimum spanning tree using a binary heap?",
                    "options": ["O(V^2)", "O(E log V)", 
                                "O(V log V + E)", "O(E log E)"],
                    "answer": 3
                },
                {
                    "question": "Which technique can be used to reduce the time complexity of finding a subset sum in a set of integers?",
                    "options": ["Brute force", "Greedy approach", 
                                "Dynamic programming", "Backtracking"],
                    "answer": 3
                },
                {
                    "question": "Which of the following algorithms is used to solve the maximum bipartite matching problem efficiently?",
                    "options": ["Hopcroft-Karp algorithm", "Ford-Fulkerson algorithm", 
                                "Kruskal’s algorithm", "Edmonds-Karp algorithm"],
                    "answer": 1
                },
                {
                    "question": "Which algorithm solves the All-Pairs Shortest Path (APSP) problem in O(V^3) time complexity?",
                    "options": ["Dijkstra’s algorithm", "Floyd-Warshall algorithm", 
                                "Bellman-Ford algorithm", "A* search algorithm"],
                    "answer": 2
                },
                {
                    "question": "In which case does the QuickSort algorithm achieve its worst-case time complexity of O(n^2)?",
                    "options": ["When the array is sorted", "When the array is reverse sorted", 
                                "When the pivot is the median", "When all elements are equal"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of performing a union operation in a disjoint set using union by rank and path compression?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(α(n))"],
                    "answer": 4
                },
                {
                    "question": "Which of the following algorithms is not suitable for solving the NP-complete problem?",
                    "options": ["Dynamic programming", "Greedy approach", 
                                "Backtracking", "Brute force"],
                    "answer": 2
                },
                {
                    "question": "Which of the following is a key characteristic of a strongly connected component in a directed graph?",
                    "options": ["There is a directed edge from every vertex to every other vertex", 
                                "Every vertex is reachable from the other vertices", 
                                "The graph is undirected", "There is no path between any pair of vertices"],
                    "answer": 1
                },
                {
                    "question": "What is the time complexity of searching for an element in a Red-Black Tree?",
                    "options": ["O(log n)", "O(n)", "O(n log n)", "O(log n log n)"],
                    "answer": 1
                },
                {
                    "question": "Which algorithm is used to solve the problem of finding the longest path in a directed acyclic graph (DAG)?",
                    "options": ["Depth-first search", "Topological sort", 
                                "Dynamic programming", "Breadth-first search"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of the Edmonds-Karp algorithm for solving the maximum flow problem?",
                    "options": ["O(V^3)", "O(VE)", "O(E log V)", "O(V^2E)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms can efficiently find the minimum spanning tree in a dense graph?",
                    "options": ["Kruskal’s algorithm", "Prim’s algorithm", 
                                "Dijkstra’s algorithm", "Bellman-Ford algorithm"],
                    "answer": 2
                },
                {
                    "question": "What is the time complexity of solving the Longest Increasing Subsequence (LIS) problem using dynamic programming?",
                    "options": ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms is used to find the number of strongly connected components in a directed graph?",
                    "options": ["Kahn’s algorithm", "Kosaraju’s algorithm", 
                                "Tarjan’s algorithm", "BFS"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of the HeapSort algorithm in the worst case?",
                    "options": ["O(n^2)", "O(n log n)", 
                                "O(log n)", "O(n)"],
                    "answer": 2
                },
                {
                    "question": "Which of the following algorithms guarantees an optimal solution for the 0/1 Knapsack problem?",
                    "options": ["Dynamic programming", "Greedy algorithm", 
                                "Branch and Bound", "Backtracking"],
                    "answer": 1
                },
                {
                    "question": "Which of the following algorithms solves the maximum subarray sum problem optimally?",
                    "options": ["Greedy algorithm", "Divide and conquer", 
                                "Dynamic programming", "Brute force"],
                    "answer": 2
                },
                {
                    "question": "Which of the following algorithms uses the min-heap data structure to efficiently solve the problem of finding the k-th smallest element in an array?",
                    "options": ["HeapSort", "QuickSelect", 
                                "MergeSort", "Selection Sort"],
                    "answer": 2
                },
                {
                    "question": "Which graph algorithm can be used to detect a cycle in a directed graph?",
                    "options": ["Kruskal’s algorithm", "Prim’s algorithm", 
                                "Depth-First Search", "Breadth-First Search"],
                    "answer": 3
                },
                {
                    "question": "What is the time complexity of finding the shortest path from a source node to all other nodes in a graph using the Dijkstra’s algorithm with a priority queue?",
                    "options": ["O(E log V)", "O(V^2)", 
                                "O(V log V + E)", "O(E + V)"],
                    "answer": 3
                }
            ]
        }
        

        self.questions = []
        self.current_question = 0
        self.score = 0

        self.init_menu()

    def init_menu(self):
    # Create a dialog to select topic and number of questions
        dialog = TopicSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            topic = dialog.selected_topic()
            num_questions = dialog.selected_num_questions()
    
            # Ensure the number of questions doesn't exceed the available questions in the topic
            max_questions = len(self.all_questions[topic])
            if num_questions > max_questions:
                num_questions = max_questions
    
            # Debugging statement to check the topic and number of questions
            print(f"Topic selected: {topic}, Number of questions: {num_questions}")
    
            self.questions = random.sample(self.all_questions[topic], num_questions)
    
            # Debugging statement to check the loaded questions
            print(f"Loaded questions: {self.questions}")
    
            self.current_question = 0  # Reset to the first question
            self.score = 0  # Reset the score
    
            self.init_ui()



    def init_ui(self):
        """Initializes the user interface for the quiz."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Question label
        self.question_label = QLabel(self)
        self.layout.addWidget(self.question_label)

        # Option buttons
        self.option_buttons = []
        for i in range(4):
            button = QPushButton(self)
            self.option_buttons.append(button)
            self.layout.addWidget(button)
            button.clicked.connect(lambda _, index=i: self.check_answer(index + 1))

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)
        self.next_button.setEnabled(False)

        self.central_widget.setLayout(self.layout)

        self.load_question()

    def load_question(self):
        """Loads the current question and its options."""
        if not self.questions:
            print("Error: No questions loaded.")
            return

        question = self.questions[self.current_question]
        self.question_label.setText(f"Q: {question['question']}")
        for i, option in enumerate(question['options']):
            self.option_buttons[i].setText(option)
            self.option_buttons[i].setEnabled(True)
            self.option_buttons[i].setStyleSheet("background-color: none;")
        self.next_button.setEnabled(False)

    def check_answer(self, selected_index):
        """Checks the user's selected answer."""
        question = self.questions[self.current_question]
        correct_answer = question['answer']

        if selected_index == correct_answer:
            self.score += 1

        for i, button in enumerate(self.option_buttons):
            if i + 1 == correct_answer:
                button.setStyleSheet("background-color: green; color: white;")
            elif i + 1 == selected_index:
                button.setStyleSheet("background-color: red; color: white;")
            button.setEnabled(False)

        self.next_button.setEnabled(True)

    def next_question(self):
        """Loads the next question or ends the quiz."""
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        """Displays the final score and asks for next steps."""
        self.question_label.setText(f"Quiz Completed! Your final score is: {self.score}/{len(self.questions)}")

        # Hide option buttons and the next button
        for button in self.option_buttons:
            button.hide()

        self.next_button.hide()

        # Create new buttons for retry and return to menu
        self.retry_button = QPushButton("Retry", self)
        self.retry_button.clicked.connect(self.retry_quiz)
        self.layout.addWidget(self.retry_button)

        self.menu_button = QPushButton("Return to Menu", self)
        self.menu_button.clicked.connect(self.init_menu)
        self.layout.addWidget(self.menu_button)

    def retry_quiz(self):
        """Restarts the quiz with the same questions."""
        # Reset score and current question index
        self.current_question = 0
        self.score = 0

        # Hide retry and menu buttons
        self.retry_button.hide()
        self.menu_button.hide()

        # Show the option buttons and re-enable them
        for button in self.option_buttons:
            button.show()
            button.setEnabled(True)  # Re-enable the option buttons
            button.setStyleSheet("background-color: none;")  # Clear any previous styles

        # Show the "Next" button again and load the first question
        self.next_button.show()
        self.load_question()




class TopicSelectionDialog(QDialog):
    def _init_(self, parent=None):
        super()._init_(parent)
        self.setWindowTitle("Select Topic and Number of Questions")
        self.setGeometry(820, 400, 700, 100)

        # Create a form layout
        self.layout = QFormLayout(self)

        # ComboBox for selecting the topic
        self.topic_combo = QComboBox(self)
        self.topic_combo.addItems(list(parent.all_questions.keys()))
        self.layout.addRow("Topic:", self.topic_combo)

        # SpinBox for selecting the number of questions
        self.num_questions_spin = QSpinBox(self)
        self.num_questions_spin.setRange(1, 80)  # You can change this range
        self.num_questions_spin.setValue(10)  # Default value
        self.layout.addRow("Number of Questions:", self.num_questions_spin)

        # Accept button
        self.accept_button = QPushButton("Start Quiz", self)
        self.accept_button.clicked.connect(self.accept)
        self.layout.addRow(self.accept_button)

    def selected_topic(self):
        """Returns the selected topic."""
        return self.topic_combo.currentText()

    def selected_num_questions(self):
        """Returns the selected number of questions."""
        return self.num_questions_spin.value()

if __name__ == "_main_":
    app = QApplication(sys.argv)
    quiz = QuizGame()
    quiz.show()
    sys.exit(app.exec_())