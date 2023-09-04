from matplotlib import pyplot as plt
import requests
import networkx as nx


# Set your Semantic Scholar API key
api_key = "x-api-key"

# Search for papers related to data science
query = "data science"
response = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/autocomplete?query={query}&citations=true&apiKey={api_key}")
data = response.json()

input(data)

# Create a NetworkX graph
G = nx.Graph()

# Add papers as nodes and citations as edges
for paper in data['matches']:
    paper_id = paper['id']
    G.add_node(paper_id, title=paper['title'])
    for citation_id in paper.get('citations', []):
        input(citation_id)
        G.add_edge(paper_id, citation_id)


# Visualize the graph using NetworkX's built-in drawing
nx.draw(G, with_labels=True)

plt.show()
