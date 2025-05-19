from pyvis.network import Network
from graph_models import topological_sort, bfs, shortest_path
import streamlit as st
import tempfile
import os
import time
import streamlit.components.v1 as components

RELATED_TOPICS = {
    "Array": ['Backtracking', 'Binary Indexed Tree', 'Binary Search', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Bucket Sort', 'Combinatorics', 'Counting', 'Counting Sort', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Doubly-Linked List', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Greedy', 'Hash Function', 'Hash Table', 'Heap (Priority Queue)', 'Interactive', 'Iterator', 'Line Sweep', 'Linked List', 'Math', 'Matrix', 'Memoization', 'Merge Sort', 'Minimum Spanning Tree', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Probability and Statistics', 'Queue', 'Quickselect', 'Radix Sort', 'Randomized', 'Recursion', 'Reservoir Sampling', 'Rolling Hash', 'Segment Tree', 'Shortest Path', 'Simulation', 'Sliding Window', 'Sorting', 'Stack', 'String', 'String Matching', 'Strongly Connected Component', 'Suffix Array', 'Topological Sort', 'Tree', 'Trie', 'Two Pointers', 'Union Find'],  
    "Hash Table": ['Backtracking', 'Binary Indexed Tree', 'Binary Search', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Breadth-First Search', 'Bucket Sort', 'Combinatorics', 'Counting', 'Counting Sort', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Doubly-Linked List', 'Dynamic Programming', 'Enumeration', 'Geometry', 'Graph', 'Greedy', 'Hash Function', 'Heap (Priority Queue)', 'Linked List', 'Math', 'Memoization', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Queue', 'Quickselect', 'Randomized', 'Recursion', 'Reservoir Sampling', 'Rolling Hash', 'Segment Tree', 'Simulation', 'Sliding Window', 'Sorting', 'Stack', 'String Matching', 'Topological Sort', 'Tree', 'Trie', 'Two Pointers', 'Union Find'],
    "Recursion": ['Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Greedy', 'Linked List', 'Math', 'Memoization', 'Monotonic Stack', 'Number Theory', 'Queue', 'Simulation', 'Stack', 'Tree'],
    "String": ['Backtracking', 'Binary Indexed Tree', 'Binary Search', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Bucket Sort', 'Combinatorics', 'Counting', 'Counting Sort', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Doubly-Linked List', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Graph', 'Greedy', 'Hash Function', 'Hash Table', 'Heap (Priority Queue)', 'Interactive', 'Iterator', 'Linked List', 'Math', 'Matrix', 'Memoization', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Queue', 'Quickselect', 'Radix Sort', 'Recursion', 'Rolling Hash', 'Segment Tree', 'Shortest Path', 'Simulation', 'Sliding Window', 'Sorting', 'Stack', 'String Matching', 'Suffix Array', 'Topological Sort', 'Tree', 'Trie', 'Two Pointers', 'Union Find'],
    "Sliding Window": ['Binary Indexed Tree', 'Binary Search', 'Bit Manipulation', 'Bucket Sort', 'Counting', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Geometry', 'Greedy', 'Hash Function', 'Heap (Priority Queue)', 'Math', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Probability and Statistics', 'Queue', 'Rolling Hash', 'Segment Tree', 'Stack', 'String Matching', 'Suffix Array', 'Trie'],
    "Binary Search": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Geometry', 'Graph', 'Greedy', 'Hash Function', 'Heap (Priority Queue)', 'Interactive', 'Line Sweep', 'Math', 'Memoization', 'Merge Sort', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Queue', 'Randomized', 'Reservoir Sampling', 'Rolling Hash', 'Segment Tree', 'Shortest Path', 'Simulation', 'Stack', 'String Matching', 'Suffix Array', 'Tree', 'Trie', 'Union Find'],
    "Dynamic Programming": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Hash Function', 'Heap (Priority Queue)', 'Math', 'Memoization', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Probability and Statistics', 'Queue', 'Rolling Hash', 'Segment Tree', 'Shortest Path', 'Simulation', 'Stack', 'String Matching', 'Suffix Array', 'Topological Sort', 'Tree', 'Trie', 'Union Find'],
    "Two Pointers": ['Binary Indexed Tree', 'Binary Search', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Counting', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Graph', 'Greedy', 'Hash Function', 'Heap (Priority Queue)', 'Interactive', 'Iterator', 'Line Sweep', 'Linked List', 'Math', 'Merge Sort', 'Monotonic Stack', 'Ordered Set', 'Prefix Sum', 'Recursion', 'Rolling Hash', 'Simulation', 'Sliding Window', 'Stack', 'String Matching', 'Tree', 'Trie', 'Union Find'],
    "Greedy": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Brainteaser', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Counting Sort', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Graph', 'Hash Function', 'Heap (Priority Queue)', 'Math', 'Memoization', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Queue', 'Quickselect', 'Rolling Hash', 'Segment Tree', 'Simulation', 'Stack', 'String Matching', 'Tree', 'Trie', 'Union Find'],
    "Sorting": ['Backtracking', 'Binary Indexed Tree', 'Binary Search', 'Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Bucket Sort', 'Combinatorics', 'Counting', 'Counting Sort', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Greedy', 'Heap (Priority Queue)', 'Line Sweep', 'Linked List', 'Math', 'Memoization', 'Merge Sort', 'Minimum Spanning Tree', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Queue', 'Quickselect', 'Radix Sort', 'Randomized', 'Segment Tree', 'Simulation', 'Sliding Window', 'Stack', 'Strongly Connected Component', 'Topological Sort', 'Tree', 'Trie', 'Two Pointers', 'Union Find'],
    "Backtracking": ['Binary Search Tree', 'Binary Tree', 'Bit Manipulation', 'Bitmask', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Design', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Greedy', 'Interactive', 'Iterator', 'Math', 'Memoization', 'Number Theory', 'Probability and Statistics', 'Simulation', 'Stack', 'Tree', 'Trie', 'Union Find'],
    "Bit Manipulation": ['Binary Tree', 'Bitmask', 'Brainteaser', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Divide and Conquer', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Hash Function', 'Heap (Priority Queue)', 'Interactive', 'Math', 'Memoization', 'Number Theory', 'Ordered Set', 'Queue', 'Quickselect', 'Rolling Hash', 'Segment Tree', 'Shortest Path', 'Simulation', 'Topological Sort', 'Tree', 'Trie', 'Union Find'],
    "Matrix": ['Backtracking', 'Binary Indexed Tree', 'Binary Search', 'Bit Manipulation', 'Bitmask', 'Breadth-First Search', 'Counting', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Geometry', 'Graph', 'Greedy', 'Hash Table', 'Heap (Priority Queue)', 'Interactive', 'Linked List', 'Math', 'Memoization', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Prefix Sum', 'Quickselect', 'Segment Tree', 'Shortest Path', 'Simulation', 'Sorting', 'Stack', 'Strongly Connected Component', 'Topological Sort', 'Tree', 'Trie', 'Two Pointers', 'Union Find'],
    "Tree": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Bitmask', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Doubly-Linked List', 'Enumeration', 'Game Theory', 'Graph', 'Hash Function', 'Heap (Priority Queue)', 'Iterator', 'Linked List', 'Math', 'Memoization', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Queue', 'Segment Tree', 'Stack', 'String Matching', 'Strongly Connected Component', 'Topological Sort', 'Trie', 'Union Find'],
    "Union Find": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Geometry', 'Hash Function', 'Heap (Priority Queue)', 'Interactive', 'Math', 'Memoization', 'Minimum Spanning Tree', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Segment Tree', 'Shortest Path', 'Stack', 'Strongly Connected Component'],
    "Graph": ['Biconnected Component', 'Binary Tree', 'Bitmask', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Design', 'Enumeration', 'Eulerian Circuit', 'Game Theory', 'Geometry', 'Heap (Priority Queue)', 'Interactive', 'Math', 'Memoization', 'Minimum Spanning Tree', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Shortest Path', 'Stack', 'Strongly Connected Component', 'Topological Sort', 'Trie', 'Union Find'],
    "Design": ['Binary Indexed Tree', 'Binary Search Tree', 'Binary Tree', 'Breadth-First Search', 'Counting', 'Data Stream', 'Depth-First Search', 'Doubly-Linked List', 'Hash Function', 'Heap (Priority Queue)', 'Iterator', 'Linked List', 'Math', 'Monotonic Stack', 'Ordered Set', 'Queue', 'Randomized', 'Shortest Path', 'Simulation', 'Stack', 'Trie'],
    "Topological Sort": ['Breadth-First Search', 'Combinatorics', 'Counting', 'Depth-First Search', 'Design', 'Enumeration', 'Game Theory', 'Heap (Priority Queue)', 'Math', 'Memoization', 'Shortest Path', 'Union Find'],
    "Prefix Sum": ['Binary Indexed Tree', 'Binary Search', 'Bit Manipulation', 'Brainteaser', 'Breadth-First Search', 'Combinatorics', 'Counting', 'Data Stream', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Dynamic Programming', 'Enumeration', 'Game Theory', 'Graph', 'Greedy', 'Heap (Priority Queue)', 'Math', 'Memoization', 'Monotonic Queue', 'Monotonic Stack', 'Number Theory', 'Ordered Set', 'Queue', 'Quickselect', 'Randomized', 'Reservoir Sampling', 'Segment Tree', 'Simulation', 'Stack', 'Tree', 'Union Find'],
    "Segment Tree": ['Binary Indexed Tree', 'Depth-First Search', 'Design', 'Divide and Conquer', 'Enumeration', 'Geometry', 'Hash Function', 'Heap (Priority Queue)', 'Line Sweep', 'Math', 'Merge Sort', 'Monotonic Queue', 'Monotonic Stack', 'Ordered Set', 'Queue', 'Rolling Hash', 'Simulation', 'Stack', 'String Matching', 'Trie'],
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