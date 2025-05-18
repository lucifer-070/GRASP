from pyvis.network import Network
from graph_models import topological_sort, bfs, shortest_path
import streamlit as st
import tempfile
import os
import time
import streamlit.components.v1 as components

RELATED_TOPICS = {
    "Array": ["Sorting", "Two Pointers", "Sliding Window", "Binary Search", "Matrix", "Hash Table", "Greedy"],
    "Sorting": ["Array", "Heap", "QuickSort", "MergeSort", "Counting Sort"],
    "Two Pointers": ["Array", "Sliding Window", "String"],
    "Sliding Window": ["Array", "Two Pointers", "String"],
    "Binary Search": ["Array", "Sorting", "Tree"],
    "Matrix": ["Array", "Dynamic Programming"],
    "Hash Table": ["Array", "String", "Counting", "Design"],
    "Greedy": ["Array", "Sorting", "Dynamic Programming"],
    "Heap": ["Priority Queue", "Sorting", "Array"],
    "Priority Queue": ["Heap", "Graph"],
    "String": ["Hash Table", "Sliding Window", "Two Pointers", "Trie"],
    "Trie": ["String", "Hash Table"],
    "Stack": ["Array", "String", "Monotonic Stack"],
    "Monotonic Stack": ["Stack", "Array"],
    "Queue": ["Array", "Breadth-First Search"],
    "Graph": ["Breadth-First Search", "Depth-First Search", "Topological Sort", "Union Find", "Tree"],
    "Breadth-First Search": ["Graph", "Tree", "Queue"],
    "Depth-First Search": ["Graph", "Tree", "Stack"],
    "Topological Sort": ["Graph", "Breadth-First Search", "Depth-First Search"],
    "Union Find": ["Graph"],
    "Tree": ["Binary Tree", "Binary Search Tree", "Graph", "Depth-First Search", "Breadth-First Search"],
    "Binary Tree": ["Tree", "Binary Search Tree"],
    "Binary Search Tree": ["Tree", "Binary Tree"],
    "Dynamic Programming": ["Array", "String", "Greedy", "Bit Manipulation"],
    "Bit Manipulation": ["Array", "Dynamic Programming"],
    "Backtracking": ["Array", "String", "Recursion"],
    "Recursion": ["Backtracking", "Tree"],
    "Design": ["Hash Table", "Array"],
    "Counting": ["Array", "Hash Table"],
    "Math": ["Array", "Bit Manipulation"],
    "Simulation": ["Array", "Matrix"],
    "Memoization": ["Dynamic Programming", "Recursion"],
    "Divide and Conquer": ["Array", "Sorting", "Tree"],
    "Segment Tree": ["Array", "Tree"],
    "Binary Indexed Tree": ["Array", "Tree"],
    "Ordered Set": ["Array", "Tree"],
    "Enumeration": ["Array", "Math"],
    "Game Theory": ["Math"],
    "Geometry": ["Array", "Math"],
    "Prefix Sum": ["Array", "Dynamic Programming"],
    "Suffix Array": ["String"],
    "Bucket Sort": ["Sorting", "Array"],
    "Randomized": ["Array", "Math"],
    "Bitmask": ["Dynamic Programming", "Bit Manipulation"],
    "Memoization": ["Dynamic Programming", "Recursion"],
    # Add more as needed for your dataset
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