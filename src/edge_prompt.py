import networkx as nx
from pyvis.network import Network

# Create an empty graph
G = nx.Graph()

# Add nodes for the two papers
G.add_node("Paper A")
G.add_node("Paper B")

# Define the key concepts shared between the papers
concepts = [
    "Transformer Model",
    "English Constituency Parsing",
    "Wall Street Journal (WSJ) Dataset",
    "Recurrent Neural Networks (RNN)",
    "Semi-Supervised Learning",
    "Discriminative Training",
    "Performance Evaluation",
    "Sequence Modeling",
]

# Define the presence of concepts in each paper
paper_a_concepts = [
    "Transformer Model",
    "English Constituency Parsing",
    "Wall Street Journal (WSJ) Dataset",
    "Recurrent Neural Networks (RNN)",
    "Semi-Supervised Learning",
    "Discriminative Training",
    "Performance Evaluation",
]

paper_b_concepts = [
    "Transformer Model",
    "Wall Street Journal (WSJ) Dataset",
    "Recurrent Neural Networks (RNN)",
    "Performance Evaluation",
    "Sequence Modeling",
]

# Create edges between the papers based on shared concepts
for concept in concepts:
    if concept in paper_a_concepts and concept in paper_b_concepts:
        # Both papers share this concept, so add an edge with a weight
        G.add_edge("Paper A", "Paper B", weight=1.0)  # You can adjust the weight as needed

# Print the edges and their weights
for edge in G.edges(data=True):
    print(edge)



nt = Network(500, 500, notebook=True)
nt.from_nx(G)
nt.show('test.html')