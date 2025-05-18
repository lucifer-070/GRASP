from pyvis.network import Network
from graph_models import topological_sort, bfs, shortest_path
import streamlit as st
import tempfile
import os
import time
import streamlit.components.v1 as components

RELATED_TOPICS = {
    "Array": ["Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Bucket Sort", "Combinatorics", "Counting", "Counting Sort", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Iterator", "Line Sweep", "Linked List", "Math", "Matrix", "Memoization", "Merge Sort", "Minimum Spanning Tree", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Probability and Statistics", "Queue", "Quickselect", "Radix Sort", "Randomized", "Recursion", "Reservoir Sampling", "Rolling Hash", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Strongly Connected Component", "Suffix Array", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Backtracking": ["Array", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Table", "Interactive", "Iterator", "Math", "Matrix", "Memoization", "Number Theory", "Probability and Statistics", "Simulation", "Sorting", "Stack", "String", "Tree", "Trie", "Union Find"],
    "Biconnected Component": ["Depth-First Search", "Graph"],
    "Binary Indexed Tree": ["Array", "Binary Search", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Geometry", "Greedy", "Hash Table", "Heap (Priority Queue)", "Line Sweep", "Math", "Matrix", "Merge Sort", "Monotonic Queue", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Binary Search": ["Array", "Binary Indexed Tree", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Combinatorics", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Line Sweep", "Math", "Matrix", "Memoization", "Merge Sort", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Randomized", "Reservoir Sampling", "Rolling Hash", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Suffix Array", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Binary Search Tree": ["Array", "Backtracking", "Binary Search", "Binary Tree", "Breadth-First Search", "Combinatorics", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Greedy", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Memoization", "Monotonic Stack", "Ordered Set", "Recursion", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Binary Tree": ["Array", "Backtracking", "Binary Search", "Binary Search Tree", "Bit Manipulation", "Breadth-First Search", "Combinatorics", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Game Theory", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Memoization", "Monotonic Stack", "Ordered Set", "Recursion", "Sorting", "Stack", "String", "String Matching", "Tree", "Two Pointers", "Union Find"],
    "Bit Manipulation": ["Array", "Backtracking", "Binary Search", "Binary Tree", "Bitmask", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Math", "Matrix", "Memoization", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Recursion", "Rolling Hash", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "String", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Bitmask": ["Array", "Backtracking", "Binary Search", "Bit Manipulation", "Breadth-First Search", "Depth-First Search", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Hash Table", "Math", "Matrix", "Memoization", "Number Theory", "Ordered Set", "Sorting", "String", "Tree", "Two Pointers"],
    "Brainteaser": ["Array", "Bit Manipulation", "Dynamic Programming", "Enumeration", "Game Theory", "Greedy", "Math", "Prefix Sum", "Probability and Statistics", "Simulation", "Sorting", "String", "Two Pointers"],
    "Breadth-First Search": ["Array", "Backtracking", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Concurrency", "Counting", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Linked List", "Math", "Matrix", "Memoization", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Shortest Path", "Simulation", "Sorting", "Stack", "String", "Strongly Connected Component", "Topological Sort", "Tree", "Two Pointers", "Union Find"],
    "Bucket Sort": ["Array", "Counting", "Counting Sort", "Divide and Conquer", "Hash Table", "Heap (Priority Queue)", "Merge Sort", "Ordered Set", "Quickselect", "Radix Sort", "Sliding Window", "Sorting", "String", "Trie"],
    "Combinatorics": ["Array", "Backtracking", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Counting", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Graph", "Greedy", "Hash Table", "Math", "Memoization", "Number Theory", "Prefix Sum", "Probability and Statistics", "Simulation", "Sorting", "String", "Topological Sort", "Tree", "Union Find"],
    "Concurrency": ["Breadth-First Search", "Depth-First Search"],
    "Counting": ["Array", "Backtracking", "Binary Search", "Binary Tree", "Bit Manipulation", "Breadth-First Search", "Bucket Sort", "Combinatorics", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Iterator", "Linked List", "Math", "Matrix", "Memoization", "Number Theory", "Prefix Sum", "Queue", "Quickselect", "Rolling Hash", "Simulation", "Sliding Window", "Sorting", "String", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Counting Sort": ["Array", "Bucket Sort", "Divide and Conquer", "Greedy", "Hash Table", "Heap (Priority Queue)", "Merge Sort", "Radix Sort", "Sorting", "String"],
    "Data Stream": ["Array", "Binary Search", "Binary Search Tree", "Binary Tree", "Counting", "Depth-First Search", "Design", "Doubly-Linked List", "Hash Table", "Heap (Priority Queue)", "Linked List", "Math", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Sorting", "Stack", "String", "Tree", "Trie", "Two Pointers"],
    "Depth-First Search": ["Array", "Backtracking", "Biconnected Component", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Concurrency", "Counting", "Data Stream", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Eulerian Circuit", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Iterator", "Linked List", "Math", "Matrix", "Memoization", "Number Theory", "Prefix Sum", "Queue", "Segment Tree", "Shortest Path", "Simulation", "Sorting", "Stack", "String", "String Matching", "Strongly Connected Component", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Design": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Breadth-First Search", "Counting", "Data Stream", "Depth-First Search", "Doubly-Linked List", "Dynamic Programming", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Matrix", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Randomized", "Segment Tree", "Shortest Path", "Simulation", "Sorting", "Stack", "String", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Divide and Conquer": ["Array", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bucket Sort", "Combinatorics", "Counting", "Counting Sort", "Depth-First Search", "Dynamic Programming", "Geometry", "Greedy", "Hash Table", "Heap (Priority Queue)", "Interactive", "Line Sweep", "Linked List", "Math", "Matrix", "Memoization", "Merge Sort", "Monotonic Queue", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Radix Sort", "Segment Tree", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Doubly-Linked List": ["Array", "Binary Search Tree", "Binary Tree", "Data Stream", "Depth-First Search", "Design", "Hash Table", "Heap (Priority Queue)", "Linked List", "Ordered Set", "Simulation", "Stack", "String", "Tree"],
    "Dynamic Programming": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Divide and Conquer", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Memoization", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Probability and Statistics", "Queue", "Recursion", "Rolling Hash", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Suffix Array", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Enumeration": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Dynamic Programming", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Number Theory", "Prefix Sum", "Recursion", "Rolling Hash", "Segment Tree", "Shortest Path", "Sliding Window", "Sorting", "String", "Topological Sort", "Tree", "Trie", "Two Pointers"],
    "Eulerian Circuit": ["Depth-First Search", "Graph"],
    "Game Theory": ["Array", "Backtracking", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Counting", "Dynamic Programming", "Graph", "Greedy", "Heap (Priority Queue)", "Interactive", "Math", "Matrix", "Memoization", "Prefix Sum", "Recursion", "Simulation", "Sorting", "String", "Topological Sort", "Tree", "Two Pointers"],
    "Geometry": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Depth-First Search", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Graph", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Number Theory", "Ordered Set", "Quickselect", "Randomized", "Rejection Sampling", "Segment Tree", "Sliding Window", "Sorting", "Union Find"],
    "Graph": ["Array", "Backtracking", "Biconnected Component", "Binary Search", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Eulerian Circuit", "Game Theory", "Geometry", "Greedy", "Hash Table", "Heap (Priority Queue)", "Interactive", "Math", "Matrix", "Memoization", "Minimum Spanning Tree", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Shortest Path", "Sorting", "Stack", "String", "Strongly Connected Component", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Greedy": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Counting Sort", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Memoization", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Recursion", "Rolling Hash", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Hash Function": ["Array", "Binary Search", "Binary Tree", "Bit Manipulation", "Breadth-First Search", "Counting", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Greedy", "Hash Table", "Linked List", "Rolling Hash", "Segment Tree", "Sliding Window", "String", "String Matching", "Suffix Array", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Hash Table": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Bucket Sort", "Combinatorics", "Counting", "Counting Sort", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Geometry", "Graph", "Greedy", "Hash Function", "Heap (Priority Queue)", "Linked List", "Math", "Matrix", "Memoization", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Randomized", "Recursion", "Reservoir Sampling", "Rolling Hash", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Heap (Priority Queue)": ["Array", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Breadth-First Search", "Bucket Sort", "Counting", "Counting Sort", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Table", "Interactive", "Line Sweep", "Linked List", "Math", "Matrix", "Merge Sort", "Minimum Spanning Tree", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Radix Sort", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Interactive": ["Array", "Backtracking", "Binary Search", "Bit Manipulation", "Breadth-First Search", "Counting", "Depth-First Search", "Divide and Conquer", "Game Theory", "Graph", "Heap (Priority Queue)", "Math", "Matrix", "Shortest Path", "Simulation", "String", "Two Pointers", "Union Find"],
    "Iterator": ["Array", "Backtracking", "Binary Search Tree", "Binary Tree", "Counting", "Depth-First Search", "Design", "Queue", "Stack", "String", "Tree", "Two Pointers"],
    "Line Sweep": ["Array", "Binary Indexed Tree", "Binary Search", "Divide and Conquer", "Heap (Priority Queue)", "Ordered Set", "Segment Tree", "Sorting", "Two Pointers"],
    "Linked List": ["Array", "Binary Search Tree", "Binary Tree", "Breadth-First Search", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Merge Sort", "Monotonic Stack", "Number Theory", "Ordered Set", "Queue", "Randomized", "Recursion", "Reservoir Sampling", "Simulation", "Sorting", "Stack", "String", "Tree", "Two Pointers"],
    "Math": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Interactive", "Linked List", "Matrix", "Memoization", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Probability and Statistics", "Queue", "Quickselect", "Randomized", "Recursion", "Rejection Sampling", "Reservoir Sampling", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Topological Sort", "Tree", "Two Pointers", "Union Find"],
    "Matrix": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Counting", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Interactive", "Linked List", "Math", "Memoization", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Quickselect", "Segment Tree", "Shortest Path", "Simulation", "Sorting", "Stack", "String", "Strongly Connected Component", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Memoization": ["Array", "Backtracking", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Divide and Conquer", "Dynamic Programming", "Game Theory", "Graph", "Greedy", "Hash Table", "Math", "Matrix", "Ordered Set", "Prefix Sum", "Recursion", "Sorting", "Stack", "String", "Topological Sort", "Tree", "Trie", "Union Find"],
    "Merge Sort": ["Array", "Binary Indexed Tree", "Binary Search", "Bucket Sort", "Counting Sort", "Divide and Conquer", "Heap (Priority Queue)", "Linked List", "Ordered Set", "Radix Sort", "Segment Tree", "Sorting", "Two Pointers"],
    "Minimum Spanning Tree": ["Array", "Graph", "Heap (Priority Queue)", "Sorting", "Strongly Connected Component", "Union Find"],
    "Monotonic Queue": ["Array", "Binary Indexed Tree", "Binary Search", "Divide and Conquer", "Dynamic Programming", "Greedy", "Heap (Priority Queue)", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Segment Tree", "Sliding Window", "Sorting", "Stack"],
    "Monotonic Stack": ["Array", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Breadth-First Search", "Data Stream", "Design", "Divide and Conquer", "Dynamic Programming", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Linked List", "Math", "Matrix", "Monotonic Queue", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Recursion", "Segment Tree", "Shortest Path", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Number Theory": ["Array", "Backtracking", "Binary Search", "Bit Manipulation", "Bitmask", "Combinatorics", "Counting", "Depth-First Search", "Dynamic Programming", "Enumeration", "Geometry", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Linked List", "Math", "Matrix", "Monotonic Stack", "Prefix Sum", "Recursion", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Union Find"],
    "Ordered Set": ["Array", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Bucket Sort", "Data Stream", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Geometry", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Line Sweep", "Linked List", "Math", "Matrix", "Memoization", "Merge Sort", "Monotonic Queue", "Monotonic Stack", "Prefix Sum", "Queue", "Randomized", "Reservoir Sampling", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Prefix Sum": ["Array", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Memoization", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Queue", "Quickselect", "Randomized", "Reservoir Sampling", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Tree", "Two Pointers", "Union Find"],
    "Probability and Statistics": ["Array", "Backtracking", "Brainteaser", "Combinatorics", "Dynamic Programming", "Math", "Randomized", "Rejection Sampling", "Sliding Window"],
    "Queue": ["Array", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Greedy", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Monotonic Queue", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Recursion", "Segment Tree", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "Tree"],
    "Quickselect": ["Array", "Bit Manipulation", "Bucket Sort", "Counting", "Divide and Conquer", "Geometry", "Greedy", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Prefix Sum", "Radix Sort", "Sorting", "String"],
    "Radix Sort": ["Array", "Bucket Sort", "Counting Sort", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort", "Quickselect", "Sorting", "String"],
    "Randomized": ["Array", "Binary Search", "Design", "Geometry", "Hash Table", "Linked List", "Math", "Ordered Set", "Prefix Sum", "Probability and Statistics", "Rejection Sampling", "Reservoir Sampling", "Sorting"],
    "Recursion": ["Array", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Dynamic Programming", "Enumeration", "Game Theory", "Greedy", "Hash Table", "Linked List", "Math", "Memoization", "Monotonic Stack", "Number Theory", "Queue", "Simulation", "Stack", "String", "Tree", "Two Pointers"],
    "Rejection Sampling": ["Geometry", "Math", "Probability and Statistics", "Randomized"],
    "Reservoir Sampling": ["Array", "Binary Search", "Hash Table", "Linked List", "Math", "Ordered Set", "Prefix Sum", "Randomized"],
    "Rolling Hash": ["Array", "Binary Search", "Bit Manipulation", "Counting", "Dynamic Programming", "Enumeration", "Greedy", "Hash Function", "Hash Table", "Segment Tree", "Sliding Window", "String", "String Matching", "Suffix Array", "Trie", "Two Pointers"],
    "Segment Tree": ["Array", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Geometry", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Line Sweep", "Math", "Matrix", "Merge Sort", "Monotonic Queue", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Queue", "Rolling Hash", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Tree", "Trie", "Union Find"],
    "Shortest Path": ["Array", "Binary Search", "Bit Manipulation", "Breadth-First Search", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Graph", "Heap (Priority Queue)", "Interactive", "Math", "Matrix", "Monotonic Stack", "Number Theory", "Stack", "String", "Topological Sort", "Trie", "Union Find"],
    "Simulation": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Brainteaser", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Doubly-Linked List", "Dynamic Programming", "Game Theory", "Greedy", "Hash Table", "Heap (Priority Queue)", "Interactive", "Linked List", "Math", "Matrix", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Recursion", "Segment Tree", "Sorting", "Stack", "String", "Two Pointers"],
    "Sliding Window": ["Array", "Binary Indexed Tree", "Binary Search", "Bit Manipulation", "Bucket Sort", "Counting", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Geometry", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Math", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Probability and Statistics", "Queue", "Rolling Hash", "Segment Tree", "Sorting", "Stack", "String", "String Matching", "Suffix Array", "Trie", "Two Pointers"],
    "Sorting": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Bucket Sort", "Combinatorics", "Counting", "Counting Sort", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Geometry", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Line Sweep", "Linked List", "Math", "Matrix", "Memoization", "Merge Sort", "Minimum Spanning Tree", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Radix Sort", "Randomized", "Segment Tree", "Simulation", "Sliding Window", "Stack", "String", "Strongly Connected Component", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "Stack": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Breadth-First Search", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Graph", "Greedy", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Matrix", "Memoization", "Monotonic Queue", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Recursion", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "String", "Tree", "Two Pointers", "Union Find"],
    "String": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Bucket Sort", "Combinatorics", "Counting", "Counting Sort", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Iterator", "Linked List", "Math", "Matrix", "Memoization", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Quickselect", "Radix Sort", "Recursion", "Rolling Hash", "Segment Tree", "Shortest Path", "Simulation", "Sliding Window", "Sorting", "Stack", "String Matching", "Suffix Array", "Topological Sort", "Tree", "Trie", "Two Pointers", "Union Find"],
    "String Matching": ["Array", "Binary Search", "Binary Tree", "Depth-First Search", "Dynamic Programming", "Greedy", "Hash Function", "Hash Table", "Math", "Rolling Hash", "Segment Tree", "Sliding Window", "String", "Suffix Array", "Tree", "Trie", "Two Pointers"],
    "Strongly Connected Component": ["Array", "Breadth-First Search", "Depth-First Search", "Graph", "Matrix", "Minimum Spanning Tree", "Sorting", "Tree", "Union Find"],
    "Suffix Array": ["Array", "Binary Search", "Dynamic Programming", "Hash Function", "Rolling Hash", "Sliding Window", "String", "String Matching", "Trie"],
    "Topological Sort": ["Array", "Bit Manipulation", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Hash Table", "Heap (Priority Queue)", "Math", "Matrix", "Memoization", "Shortest Path", "Sorting", "String", "Tree", "Union Find"],
    "Tree": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Breadth-First Search", "Combinatorics", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Doubly-Linked List", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Iterator", "Linked List", "Math", "Matrix", "Memoization", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Queue", "Recursion", "Segment Tree", "Sorting", "Stack", "String", "String Matching", "Strongly Connected Component", "Topological Sort", "Trie", "Two Pointers", "Union Find"],
    "Trie": ["Array", "Backtracking", "Binary Search", "Bit Manipulation", "Bucket Sort", "Counting", "Data Stream", "Depth-First Search", "Design", "Dynamic Programming", "Enumeration", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Matrix", "Memoization", "Rolling Hash", "Segment Tree", "Shortest Path", "Sliding Window", "Sorting", "String", "String Matching", "Suffix Array", "Tree", "Two Pointers"],
    "Two Pointers": ["Array", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Bitmask", "Brainteaser", "Breadth-First Search", "Counting", "Data Stream", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Enumeration", "Game Theory", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Iterator", "Line Sweep", "Linked List", "Math", "Matrix", "Merge Sort", "Monotonic Stack", "Ordered Set", "Prefix Sum", "Recursion", "Rolling Hash", "Simulation", "Sliding Window", "Sorting", "Stack", "String", "String Matching", "Tree", "Trie", "Union Find"],
    "Union Find": ["Array", "Backtracking", "Binary Indexed Tree", "Binary Search", "Binary Search Tree", "Binary Tree", "Bit Manipulation", "Breadth-First Search", "Combinatorics", "Counting", "Depth-First Search", "Design", "Divide and Conquer", "Dynamic Programming", "Geometry", "Graph", "Greedy", "Hash Function", "Hash Table", "Heap (Priority Queue)", "Interactive", "Math", "Matrix", "Memoization", "Minimum Spanning Tree", "Monotonic Stack", "Number Theory", "Ordered Set", "Prefix Sum", "Segment Tree", "Shortest Path", "Sorting", "Stack", "String", "Strongly Connected Component", "Topological Sort", "Tree", "Two Pointers"],
}


def show_graph_visualizer(graph, tag_map, df=None):
    st.subheader("🕸️ Interactive Tag Graph Visualizer")

    # 1. Topic selection and session state sync
    selected_tag = st.selectbox(
        "Select a topic/tag to explore:", sorted(tag_map.keys()),
        key="graph_tag_select"
    )

    # Set session state for home tab
    if selected_tag:
        st.session_state["selected_tag"] = selected_tag

    # 2. Build the graph with color highlights
    net = Network(height="600px", width="100%", directed=True, notebook=False)
    net.barnes_hut()

    # Find neighbors for highlighting
    neighbors = set()
    for related in RELATED_TOPICS.get(selected_tag, []):
        if related in tag_map:
            neighbors.add(related)
    for tag, related_list in RELATED_TOPICS.items():
        if selected_tag == tag:
            neighbors.update([r for r in related_list if r in tag_map])
        if selected_tag in related_list and tag in tag_map:
            neighbors.add(tag)

    # Add nodes with color coding
    for tag in tag_map:
        if tag == selected_tag:
            color = "#FF9800"  # Orange for selected
        elif tag in neighbors:
            color = "#4CAF50"  # Green for neighbors
        else:
            color = "#2196F3"  # Blue for others
        net.add_node(tag, label=tag, color=color)

    # Add edges, highlight those connected to selected node
    for tag, related_list in RELATED_TOPICS.items():
        if tag in tag_map:
            for related in related_list:
                if related in tag_map:
                    if tag == selected_tag or related == selected_tag:
                        edge_color = "#FF1744"  # Red for edges connected to selected
                        width = 4
                    elif tag in neighbors or related in neighbors:
                        edge_color = "#4CAF50"  # Green for neighbor edges
                        width = 2
                    else:
                        edge_color = "#BDBDBD"  # Gray for others
                        width = 1
                    net.add_edge(tag, related, color=edge_color, width=width)

    # 3. Save and display the graph
    fd, temp_path = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    net.save_graph(temp_path)
    with open(temp_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=650, scrolling=True)
    os.unlink(temp_path)

    # 4. Show questions for selected tag
    if selected_tag:
        st.markdown(f"### Questions for `{selected_tag}`")
        questions = tag_map[selected_tag]
        difficulties = sorted(set(q[2] for q in questions))
        selected_diff = st.selectbox("Filter by difficulty:", ["All"] + difficulties, key="graph_diff")
        for question, slug, difficulty in questions:
            if selected_diff == "All" or difficulty == selected_diff:
                url = f"https://leetcode.com/problems/{slug}"
                st.markdown(f"- [{question}]({url}) — *{difficulty}*")

def show_questions_by_tag_and_difficulty(tag_map):
    st.subheader("Explore Questions by Tag and Difficulty")
    # Use session state for default tag
    default_tag = st.session_state.get("selected_tag", None)
    tag = st.selectbox("Select a topic/tag:", sorted(tag_map.keys()), index=sorted(tag_map.keys()).index(default_tag) if default_tag in tag_map else 0, key="home_tag_select")
    if tag:
        st.session_state["selected_tag"] = tag  # keep in sync
        questions = tag_map[tag]
        difficulties = sorted(set(q[2] for q in questions))
        selected_diff = st.selectbox("Select difficulty:", ["All"] + difficulties, key="home_diff_select")
        st.markdown(f"### Questions for: `{tag}` ({selected_diff})")
        for question, slug, difficulty in questions:
            if selected_diff == "All" or difficulty == selected_diff:
                url = f"https://leetcode.com/problems/{slug}"
                st.markdown(f"- [{question}]({url}) — *{difficulty}*")

# def show_questions_by_tag(tag_map):
#     st.subheader("Explore Questions by Tag")
#     tag = st.selectbox("Select a topic/tag:", sorted(tag_map.keys()))
#     if tag:
#         st.markdown(f"### Questions for: `{tag}`")
#         for question, slug, difficulty in tag_map[tag]:
#             url = f"https://leetcode.com/problems/{slug}"
#             st.markdown(f"- [{question}]({url}) — *{difficulty}*")

# def show_questions_by_difficulty(question_list):
#     st.subheader("Filter Questions by Difficulty")
#     difficulties = sorted(set(q[2] for q in question_list))
#     selected_diff = st.selectbox("Select difficulty:", ["All"] + difficulties)
#     st.markdown(f"### Questions ({selected_diff})")
#     for question, slug, difficulty in question_list:
#         if selected_diff == "All" or difficulty == selected_diff:
#             url = f"https://leetcode.com/problems/{slug}"
#             st.markdown(f"- [{question}]({url}) — *{difficulty}*")

def show_graph_tools(graph, selected_node, topological_sort, bfs, shortest_path):
    st.subheader("Graph Tools")
    st.markdown(f"### Topological Sort (all tags and questions)")
    st.write(topological_sort(graph))

    if selected_node:
        st.markdown(f"### BFS from `{selected_node}`")
        st.write(bfs(graph, selected_node))

        st.markdown(f"### Shortest Paths from `{selected_node}`")
        st.write(shortest_path(graph, selected_node))