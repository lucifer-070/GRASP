import streamlit as st
from collections import defaultdict
from graph_models import Graph, HashMap, topological_sort, bfs, shortest_path
from data_loader import load_data, build_tag_cooccurrence, get_top_k_tags
from ui_sections import show_questions_by_tag_and_difficulty, show_graph_tools, show_graph_visualizer

def build_graph_and_tag_map(df):
    graph = Graph()
    tag_map = defaultdict(list)
    for _, row in df.iterrows():
        question = row['question']
        slug = row['Slug']
        difficulty = row['Difficulty']
        tags = row['dependencies']
        graph.add_node(question)
        for tag in tags:
            graph.add_node(tag)
            graph.add_edge(tag, question)
            graph.add_edge(question, tag)
            tag_map[tag].append((question, slug, difficulty))
    return graph, tag_map

def recommend_tags(selected_tags, cooccur, top_n=5):
    scores = defaultdict(int)
    for tag in selected_tags:
        for related, count in cooccur.get(tag, {}).items():
            if related not in selected_tags:
                scores[related] += count
    recommended = sorted(scores.items(), key=lambda x: -x[1])[:top_n]
    return [tag for tag, _ in recommended]

def main():
    st.set_page_config(page_title="GRASP: DSA Roadmap", layout="wide")
    df = load_data()
    if df.empty:
        st.error("Failed to load or parse data.")
        return

    graph, tag_map = build_graph_and_tag_map(df)
    cooccur = build_tag_cooccurrence(df)

    tab1, tab2 = st.tabs(["🏠 Home", "🕸️ Graph Visualizer"])
    with tab1:
        st.markdown(
            "<div class='centered-content'>"
            "<h1>📘 GRASP: Graph-Based Roadmap for Algorithmic Study and Preparation</h1>"
            "<p>Welcome! Use the filters below to explore LeetCode DSA questions by tag and difficulty.<br>"
            "Use the sidebar for learning order and graph-based exploration.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("### 🌟 Top-K Most Frequent Tags")
        top_k = st.slider("Select K:", min_value=3, max_value=20, value=10)
        top_tags = get_top_k_tags(df, k=top_k)
        for tag, count in top_tags:
            st.write(f"**{tag}**: {count} questions")
        show_questions_by_tag_and_difficulty(tag_map)

    with tab2:
        show_graph_visualizer(graph, tag_map, df)

    # Sidebar for graph tools and tag recommendation
    with st.sidebar:
        with st.expander("🗺️ Learning Order & Graph Tools", expanded=False):
            st.markdown("#### Topological Sort (Learning Order)")
            topo_order = topological_sort(graph)
            st.write(topo_order)
            st.markdown("---")
            selected_node = st.selectbox(
                "Analyze a tag or question:", sorted(graph.nodes.keys()), key="sidebar_select"
            )
            st.markdown("**BFS (Closest Related Topics/Questions):**")
            st.write(bfs(graph, selected_node))
            st.markdown("**Shortest Path (Distance from selected node):**")
            st.write(shortest_path(graph, selected_node))

        with st.expander("✨ Tag Recommendation", expanded=True):
            all_tags = sorted(tag_map.keys())
            solved_tags = st.multiselect("Select tags you know/solved:", all_tags, key="solved_tags")
            if solved_tags:
                recommended = recommend_tags(solved_tags, cooccur)
                st.markdown("**Recommended tags to learn next (based on co-occurrence):**")
                for tag in recommended:
                    st.write(f"- {tag}")

if __name__ == "__main__":
    main()