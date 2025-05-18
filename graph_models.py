class Node:
    def __init__(self, question):
        self.question = question
        self.dependencies = []

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, question):
        if question not in self.nodes:
            self.nodes[question] = Node(question)

    def add_edge(self, prerequisite, dependent):
        self.add_node(prerequisite)
        self.add_node(dependent)
        self.nodes[prerequisite].dependencies.append(dependent)

class HashMap:
    def __init__(self):
        self.map = {}

    def insert(self, question, status):
        self.map[question] = status

    def get(self, question):
        return self.map.get(question, None)

    def delete(self, question):
        if question in self.map:
            del self.map[question]

def topological_sort(graph):
    def dfs(node, visited, stack):
        visited[node] = True
        for neighbor in graph.nodes[node].dependencies:
            if not visited.get(neighbor, False):
                dfs(neighbor, visited, stack)
        stack.insert(0, node)
    
    visited = {}
    stack = []
    for node in graph.nodes:
        if not visited.get(node, False):
            dfs(node, visited, stack)
    return stack

def bfs(graph, start_node):
    visited = {start_node: True}
    queue = [start_node]
    result = [start_node]

    while queue:
        node = queue.pop(0)
        for neighbor in graph.nodes[node].dependencies:
            if neighbor not in visited:
                visited[neighbor] = True
                queue.append(neighbor)
                result.append(neighbor)
    return result

def shortest_path(graph, start_node):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    queue = [start_node]

    while queue:
        curr_node = queue.pop(0)
        for neighbor in graph.nodes[curr_node].dependencies:
            if distances[neighbor] > distances[curr_node] + 1:
                distances[neighbor] = distances[curr_node] + 1
                queue.append(neighbor)
    return distances